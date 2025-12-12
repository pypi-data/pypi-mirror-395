"""
Data-file-related API helpers.
"""

from __future__ import annotations

from typing import Any, Dict, List

from .base import JSONDict


class DataFilesClientMixin:
    """Mixin providing data file endpoints."""

    def list_data_files(self, **filters: Any) -> List[Dict[str, Any]]:
        """List data files with optional filters."""
        params: Dict[str, Any] = {}
        if filters.get("project_id"):
            params["project_id"] = filters["project_id"]
        if filters.get("file_type"):
            params["file_type"] = filters["file_type"]
        if filters.get("tags"):
            params["tags"] = filters["tags"]
        if filters.get("limit"):
            params["limit"] = filters["limit"]
        if filters.get("offset"):
            params["offset"] = filters["offset"]
        if filters.get("sort_by"):
            params["sort_by"] = filters["sort_by"]
        if filters.get("sort_order"):
            params["sort_order"] = filters["sort_order"]
        data = self.get("/api/cli/data", params=params)
        return data if isinstance(data, list) else []

    def upload_data_file(self, file_data: Dict[str, Any]) -> JSONDict:
        """Upload a data file."""
        return self.post("/api/cli/data/upload", json_data=file_data)

    def get_data_file(self, file_id: str) -> JSONDict:
        """Get data file details."""
        return self.get(f"/api/cli/data/{file_id}")

    def delete_data_file(self, file_id: str) -> JSONDict:
        """Delete a data file."""
        return self.delete(f"/api/cli/data/{file_id}")

