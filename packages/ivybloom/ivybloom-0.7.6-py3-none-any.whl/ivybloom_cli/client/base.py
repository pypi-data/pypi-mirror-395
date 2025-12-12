"""
Core HTTP client utilities for IvyBloom CLI.
"""

from __future__ import annotations

import json
import sys
import time
import uuid
from typing import Any, Dict, List, Optional, Union

import httpx

from ..utils.auth import AuthManager
from ..utils.config import Config

JSONDict = Dict[str, Any]
JSONData = Union[JSONDict, List[Any]]


class APIClientError(Exception):
    """Raised when an API request fails."""


class BaseAPIClient:
    """Shared IvyBloom API HTTP client with auth, tracing, and retries."""

    def __init__(self, config: Config, auth_manager: AuthManager) -> None:
        """Initialize the HTTP client."""
        self.config = config
        self.auth_manager = auth_manager
        self.base_url = config.get_frontend_url()
        self.timeout = config.get("timeout", 30)
        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            headers=self._get_default_headers(),
            follow_redirects=True,
            cookies={},
        )

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self.client.close()

    def __enter__(self) -> "BaseAPIClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def _ensure_authenticated(self) -> None:
        """Ensure user is authenticated before making requests."""
        if not self.auth_manager.is_authenticated():
            raise APIClientError(
                "Authentication required. Please run 'ivybloom auth login' "
                "(browser/device/link) or provide an API key."
            )

    def _get_default_headers(self, *, prefer_jwt: bool = False) -> Dict[str, str]:
        """Build default headers including authentication."""
        headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "User-Agent": "ivybloom-cli/0.7.6",
            "Accept": "application/json",
        }
        headers.update(self.auth_manager.get_auth_headers(prefer_jwt=prefer_jwt))

        try:
            headers["x-ivybloom-client"] = self.config.get_or_create_client_id()
        except Exception:
            # Best-effort client id; do not block requests on failure.
            pass

        return headers

    def _refresh_headers(self, *, prefer_jwt: bool = False) -> None:
        """Refresh authentication headers on the existing client."""
        self.client.headers.update(self._get_default_headers(prefer_jwt=prefer_jwt))

    def _make_request(self, method: str, endpoint: str, **kwargs: Any) -> httpx.Response:
        """Make an HTTP request with trace id and 429 backoff handling."""
        path = endpoint if endpoint.startswith("/") else f"/{endpoint}"
        self._refresh_headers()

        configured_trace_id = self.config.get("trace_id")
        trace_id = str(configured_trace_id) if configured_trace_id else str(uuid.uuid4())
        headers_override = kwargs.pop("headers", None) or {}
        headers_override.setdefault("x-trace-id", trace_id)

        max_rl_retries = int(self.config.get("rate_limit_retries", 2) or 0)
        backoff_base = float(self.config.get("rate_limit_backoff_base", 1.0) or 1.0)

        attempt = 0
        start_time = time.time()
        while True:
            if self.config.get("debug"):
                print(
                    f"{method} {endpoint} [trace_id={trace_id}] -> (sending request)",
                    file=sys.stderr,
                )

            try:
                response = self.client.request(method, path, headers=headers_override, **kwargs)
            except httpx.TimeoutException as exc:
                raise APIClientError("Request timed out. Check your network and try again.") from exc
            except httpx.ConnectError as exc:
                raise APIClientError(
                    "Could not connect to API server. Verify IVY_ORCHESTRATOR_URL and your network."
                ) from exc
            except Exception as exc:  # pragma: no cover - defensive
                raise APIClientError(f"Request failed: {exc}") from exc

            if response.status_code != 429:
                if self.config.get("debug"):
                    duration_ms = int((time.time() - start_time) * 1000)
                    print(
                        f"{method} {endpoint} [trace_id={trace_id}] -> "
                        f"{response.status_code} ({duration_ms} ms)",
                        file=sys.stderr,
                    )
                return response

            if attempt >= max_rl_retries:
                if self.config.get("debug"):
                    print(
                        f"{method} {endpoint} [trace_id={trace_id}] -> 429 "
                        f"(giving up after {attempt} retries)",
                        file=sys.stderr,
                    )
                return response

            retry_after_header = response.headers.get("Retry-After") or response.headers.get(
                "retry-after"
            )
            try:
                sleep_seconds = (
                    float(retry_after_header)
                    if retry_after_header
                    else backoff_base * (2**attempt)
                )
            except Exception:
                sleep_seconds = backoff_base * (2**attempt)
            sleep_seconds = max(0.1, min(sleep_seconds, 10.0))
            if self.config.get("debug"):
                print(
                    f"{method} {endpoint} [trace_id={trace_id}] -> 429 "
                    f"(retrying in {sleep_seconds:.2f}s)",
                    file=sys.stderr,
                )
            time.sleep(sleep_seconds)
            attempt += 1

    def _parse_json_response(self, response: httpx.Response) -> JSONData:
        """Parse JSON body or return textual content."""
        try:
            return response.json()
        except json.JSONDecodeError:
            return {"data": response.text}

    def _raise_for_status(
        self,
        response: httpx.Response,
        *,
        access_denied_message: str,
        not_found_message: Optional[str] = None,
        error_prefix: str = "❌ API error",
    ) -> None:
        """Raise APIClientError for non-success statuses."""
        if response.status_code == 403:
            raise APIClientError(access_denied_message)
        if response.status_code == 404 and not_found_message:
            raise APIClientError(not_found_message)
        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get(
                    "detail",
                    error_data.get("message", f"HTTP {response.status_code}"),
                )
            except Exception:
                error_msg = f"HTTP {response.status_code}"
            raise APIClientError(f"{error_prefix}: {error_msg}")

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> JSONData:
        """Make GET request with automatic token refresh."""
        self._ensure_authenticated()
        response = self._make_request("GET", endpoint, params=params)

        if response.status_code == 401:
            detail = None
            try:
                detail = response.json().get("code")
            except Exception:
                detail = None

            if detail == "CLI_CLIENT_UNLINKED":
                raise APIClientError(
                    "❌ CLI not linked to your account. Run 'ivybloom auth link' to link this CLI installation."
                )

            print("Access token may be expired, attempting refresh...", file=sys.stderr)
            self._refresh_headers()
            retry_response = self._make_request("GET", endpoint, params=params)
            if retry_response.status_code == 401:
                self._refresh_headers(prefer_jwt=True)
                retry_jwt_response = self._make_request("GET", endpoint, params=params)
                if retry_jwt_response.status_code == 401:
                    raise APIClientError(
                        "❌ Authentication failed. Please run 'ivybloom auth login' or check your API key."
                    )
                response = retry_jwt_response
            else:
                response = retry_response

        self._raise_for_status(
            response,
            access_denied_message="❌ Access denied. You don't have permission for this resource.",
            not_found_message="❌ Resource not found.",
        )
        return self._parse_json_response(response)

    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> JSONData:
        """Make POST request with automatic token refresh."""
        self._ensure_authenticated()
        kwargs: Dict[str, Any] = {}
        if data is not None:
            kwargs["data"] = data
        if json_data is not None:
            kwargs["json"] = json_data

        response = self._make_request("POST", endpoint, **kwargs)

        if response.status_code == 401:
            detail = None
            try:
                detail = response.json().get("code")
            except Exception:
                detail = None

            if detail == "CLI_CLIENT_UNLINKED":
                raise APIClientError(
                    "Authentication required. Run 'ivybloom auth link' to link this CLI and retry."
                )

            print("Access token may be expired, attempting refresh...", file=sys.stderr)
            self._refresh_headers(prefer_jwt=True)
            retry_jwt_first = self._make_request("POST", endpoint, **kwargs)
            if retry_jwt_first.status_code == 401:
                self._refresh_headers(prefer_jwt=False)
                retry_default = self._make_request("POST", endpoint, **kwargs)
                if retry_default.status_code == 401:
                    raise APIClientError(
                        "Authentication failed. Please check your API key or login status."
                    )
                response = retry_default
            else:
                response = retry_jwt_first

        self._raise_for_status(
            response,
            access_denied_message="Access denied. You don't have permission for this resource.",
            error_prefix="API error",
        )
        return self._parse_json_response(response)

    def delete(self, endpoint: str) -> JSONData:
        """Make DELETE request."""
        self._ensure_authenticated()
        response = self._make_request("DELETE", endpoint)

        if response.status_code == 401:
            detail = None
            try:
                detail = response.json().get("code")
            except Exception:
                detail = None
            if detail == "CLI_CLIENT_UNLINKED":
                raise APIClientError(
                    "Authentication required. Run 'ivybloom auth link' to link this CLI and retry."
                )
            self._refresh_headers(prefer_jwt=True)
            retry_jwt_response = self._make_request("DELETE", endpoint)
            if retry_jwt_response.status_code == 401:
                raise APIClientError(
                    "Authentication failed. Please check your API key or login status."
                )
            response = retry_jwt_response

        self._raise_for_status(
            response,
            access_denied_message="Access denied. You don't have permission for this resource.",
            not_found_message="Resource not found.",
            error_prefix="API error",
        )

        if response.status_code == 204:
            return {"success": True}

        try:
            return response.json()
        except json.JSONDecodeError:
            return {"success": True}

