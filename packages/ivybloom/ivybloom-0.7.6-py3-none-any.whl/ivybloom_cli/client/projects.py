"""
Project-related API helpers.
"""

from __future__ import annotations

from typing import Any, Dict, List

from .base import APIClientError, JSONDict


class ProjectsClientMixin:
    """Mixin providing project endpoints."""

    def list_projects(self) -> List[Dict[str, Any]]:
        """List user's projects with response normalization."""
        data = self.get("/api/cli/projects")
        if isinstance(data, list):
            raw_items = data
        elif isinstance(data, dict):
            if isinstance(data.get("projects"), list):
                raw_items = data["projects"]
            elif isinstance(data.get("data"), list):
                raw_items = data["data"]
            else:
                raise APIClientError(
                    "Unexpected response while listing projects (expected a list of projects)."
                )
        else:
            raise APIClientError(
                "Unexpected response while listing projects (expected a list of projects)."
            )

        items: List[JSONDict] = []
        for item in raw_items:
            if not isinstance(item, dict):
                continue
            normalized = dict(item)
            if "id" not in normalized and "project_id" in normalized:
                normalized["id"] = normalized["project_id"]
            items.append(normalized)
        return items

    def get_project(self, project_id: str) -> JSONDict:
        """Get project details."""
        return self.get(f"/api/cli/projects/{project_id}")

    def list_project_jobs(self, project_id: str) -> List[Dict[str, Any]]:
        """List jobs for a specific project."""
        data = self.get(f"/api/cli/projects/{project_id}/jobs")
        return data if isinstance(data, list) else []

