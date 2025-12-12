"""
Reports/export preview API helpers.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional

import httpx

from .base import JSONDict


class ReportsClientMixin:
    """Mixin providing report endpoints."""

    def reports_post(
        self,
        action: str,
        *,
        job_id: str,
        template: Optional[str] = None,
        export_type: Optional[str] = None,
        format: Optional[str] = None,
        extra_params: Optional[Dict[str, Any]] = None,
        idempotency_key: Optional[str] = None,
    ) -> JSONDict:
        """POST /api/cli/reports to trigger async readiness/self-heal flows."""
        self._ensure_authenticated()

        params: Dict[str, Any] = {"action": action, "jobId": job_id}
        if template:
            params["template"] = template
        if export_type:
            params["type"] = export_type
        if format:
            params["format"] = format
        if extra_params:
            params.update(extra_params)
        if idempotency_key:
            params.setdefault("idempotency_key", idempotency_key)
            params.setdefault("idempotencyKey", idempotency_key)

        path = "/api/cli/reports"
        request_headers: Optional[Dict[str, str]] = None
        if idempotency_key:
            request_headers = {
                "Idempotency-Key": idempotency_key,
                "x-idempotency-key": idempotency_key,
            }
        response = self._make_request("POST", path, params=params, headers=request_headers)
        self._raise_for_status(
            response,
            access_denied_message="Access denied. You don't have permission for this resource.",
            error_prefix="API error",
        )
        try:
            return response.json()
        except json.JSONDecodeError:
            return {"status_code": response.status_code}

    def reports_get(
        self,
        action: str,
        *,
        job_id: str,
        template: Optional[str] = None,
        export_type: Optional[str] = None,
        format: Optional[str] = None,
        follow_redirects: bool = True,
        extra_params: Optional[Dict[str, Any]] = None,
    ) -> JSONDict:
        """GET /api/cli/reports to fetch preview/generate content or export redirect."""
        self._ensure_authenticated()

        params: Dict[str, Any] = {"action": action, "jobId": job_id}
        if template:
            params["template"] = template
        if export_type:
            params["type"] = export_type
        if format:
            params["format"] = format
        if extra_params:
            params.update(extra_params)

        path = "/api/cli/reports"
        if follow_redirects:
            response = self._make_request("GET", path, params=params)
            self._raise_for_status(
                response,
                access_denied_message="Access denied. You don't have permission for this resource.",
                error_prefix="API error",
            )
            try:
                return response.json()
            except json.JSONDecodeError:
                return {"data": response.text, "status_code": response.status_code}

        try:
            temp_client = httpx.Client(
                base_url=self.base_url,
                timeout=self.timeout,
                headers=self._get_default_headers(),
                follow_redirects=False,
            )
            response = temp_client.request("GET", path, params=params)
        finally:
            try:
                temp_client.close()
            except Exception:
                pass

        if response.status_code in (301, 302, 303, 307, 308):
            return {
                "status_code": response.status_code,
                "redirect_to": response.headers.get("location", ""),
            }
        self._raise_for_status(
            response,
            access_denied_message="Access denied. You don't have permission for this resource.",
            error_prefix="API error",
        )
        try:
            return response.json()
        except json.JSONDecodeError:
            return {"data": response.text, "status_code": response.status_code}

