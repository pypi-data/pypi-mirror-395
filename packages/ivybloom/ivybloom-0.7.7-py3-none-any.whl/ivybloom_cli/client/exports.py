"""
Export orchestrator API helpers.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional

from .base import JSONDict


class ExportsClientMixin:
    """Mixin providing export endpoints."""

    def create_export(self, spec: Dict[str, Any], *, idempotency_key: Optional[str] = None) -> JSONDict:
        """Create an export orchestration."""
        self._ensure_authenticated()
        headers: Optional[Dict[str, str]] = None
        body = dict(spec)
        if idempotency_key:
            headers = {
                "Idempotency-Key": idempotency_key,
                "x-idempotency-key": idempotency_key,
            }
            body.setdefault("idempotency_key", idempotency_key)
        response = self._make_request("POST", "/api/cli/exports", json=body, headers=headers)
        self._raise_for_status(
            response,
            access_denied_message="Access denied. You don't have permission for this resource.",
            error_prefix="API error",
        )
        try:
            return response.json()
        except json.JSONDecodeError:
            return {"status_code": response.status_code}

    def get_export_status(self, export_id: str) -> JSONDict:
        """Get export status."""
        self._ensure_authenticated()
        response = self._make_request("GET", f"/api/cli/exports/{export_id}")
        self._raise_for_status(
            response,
            access_denied_message="Access denied. You don't have permission for this resource.",
            error_prefix="API error",
        )
        try:
            return response.json()
        except json.JSONDecodeError:
            return {"status_code": response.status_code, "data": response.text}

    def get_export_results(self, export_id: str) -> JSONDict:
        """Get export results."""
        self._ensure_authenticated()
        response = self._make_request("GET", f"/api/cli/exports/{export_id}/results")
        self._raise_for_status(
            response,
            access_denied_message="Access denied. You don't have permission for this resource.",
            error_prefix="API error",
        )
        try:
            return response.json()
        except json.JSONDecodeError:
            return {"status_code": response.status_code, "data": response.text}

    def list_export_catalog(self) -> JSONDict:
        """List export catalog."""
        self._ensure_authenticated()
        response = self._make_request("GET", "/api/cli/exports/catalog")
        self._raise_for_status(
            response,
            access_denied_message="Access denied. You don't have permission for this resource.",
            error_prefix="API error",
        )
        try:
            return response.json()
        except json.JSONDecodeError:
            return {"status_code": response.status_code, "data": response.text}

