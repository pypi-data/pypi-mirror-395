"""
Workflow-related API helpers.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .base import JSONDict


class WorkflowsClientMixin:
    """Mixin providing workflow endpoints."""

    def list_workflows(self, **filters: Any) -> List[Dict[str, Any]]:
        """List workflows with optional filters."""
        params: Dict[str, Any] = {}
        if filters.get("project_id"):
            params["project_id"] = filters["project_id"]
        if filters.get("status"):
            params["status"] = filters["status"]
        if filters.get("limit"):
            params["limit"] = filters["limit"]
        if filters.get("offset"):
            params["offset"] = filters["offset"]
        if filters.get("sort_by"):
            params["sort_by"] = filters["sort_by"]
        if filters.get("sort_order"):
            params["sort_order"] = filters["sort_order"]
        data = self.get("/api/cli/workflows", params=params)
        return data if isinstance(data, list) else []

    def get_workflow(self, workflow_id: str) -> JSONDict:
        """Get workflow details."""
        return self.get(f"/api/cli/workflows/{workflow_id}")

    def create_workflow(self, workflow_data: Dict[str, Any]) -> JSONDict:
        """Create a new workflow."""
        return self.post("/api/cli/workflows", json_data=workflow_data)

    def execute_workflow(
        self,
        workflow_id: str,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> JSONDict:
        """Execute a workflow."""
        payload = {"parameters": parameters or {}}
        return self.post(f"/api/cli/workflows/{workflow_id}/execute", json_data=payload)

