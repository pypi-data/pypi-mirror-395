"""
CLI configuration API helpers.
"""

from __future__ import annotations

from typing import Any, Dict

from .base import JSONDict


class ConfigClientMixin:
    """Mixin providing configuration endpoints."""

    def get_config_settings(self) -> JSONDict:
        """Get CLI configuration settings from backend."""
        return self.get("/api/cli/config")

    def update_config_settings(self, settings: Dict[str, Any]) -> JSONDict:
        """Update CLI configuration settings."""
        return self.post("/api/cli/config", json_data=settings)

