"""
Job-related API helpers.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .base import JSONDict


class JobsClientMixin:
    """Mixin providing job endpoints."""

    def create_job(self, job_request: Dict[str, Any]) -> JSONDict:
        """Create a new job."""
        payload = {
            "tool_name": job_request.get("tool_name"),
            "parameters": job_request.get("parameters", {}),
            "project_id": job_request.get("project_id"),
            "job_title": job_request.get("job_title"),
            "wait_for_completion": job_request.get("wait_for_completion", False),
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        return self.post("/api/cli/jobs", json_data=payload)

    def get_job_status(
        self,
        job_id: str,
        include_logs: bool = False,
        logs_tail: Optional[int] = None,
    ) -> JSONDict:
        """Get job status."""
        params: Optional[Dict[str, Any]] = None
        if include_logs:
            params = {"include_logs": True}
            if isinstance(logs_tail, int) and logs_tail > 0:
                params["logs_tail"] = logs_tail
        response = self.get(f"/api/cli/jobs/{job_id}", params=params)
        if response and "id" in response:
            response["job_id"] = response["id"]
        if response and "job_type" in response:
            response["tool_name"] = response["job_type"]
        if response and "progress_percent" in response:
            response["progress_percentage"] = response["progress_percent"]
        return response

    def get_job_results(self, job_id: str, format: str = "json") -> JSONDict:
        """Get job results."""
        params = {"format": format}
        response = self.get(f"/api/cli/jobs/{job_id}/results", params=params)
        if response and "id" in response:
            response["job_id"] = response["id"]
        if response and "job_type" in response:
            response["tool_name"] = response["job_type"]
        return response

    def cancel_job(self, job_id: str) -> JSONDict:
        """Cancel a job."""
        return self.delete(f"/api/cli/jobs/{job_id}")

    def get_job_download_urls(self, job_id: str, artifact_type: Optional[str] = None) -> JSONDict:
        """Get presigned download URLs for job artifacts."""
        params: Dict[str, Any] = {"job_id": job_id}
        if artifact_type:
            params["artifact_type"] = artifact_type
        return self.get("/api/cli/download", params=params)

    def list_jobs(self, **filters: Any) -> List[Dict[str, Any]]:
        """List jobs with optional filters."""
        params: Dict[str, Any] = {}
        if filters.get("project_id"):
            params["project_id"] = filters["project_id"]
        if filters.get("status"):
            params["status"] = filters["status"]
        if filters.get("tool_name"):
            params["job_type"] = filters["tool_name"]
        if filters.get("created_after"):
            params["created_after"] = filters["created_after"]
        if filters.get("created_before"):
            params["created_before"] = filters["created_before"]
        if filters.get("limit"):
            params["limit"] = filters["limit"]
        if filters.get("offset"):
            params["offset"] = filters["offset"]
        data = self.get("/api/cli/jobs", params=params)
        return data if isinstance(data, list) else []

