"""Project listing helpers for the Textual TUI."""

from __future__ import annotations

from typing import Any, Dict, List

from .cli_runner import CLIRunner


class ProjectsService:
    """Service for listing and fetching projects via CLI subprocess."""

    def __init__(self, runner: CLIRunner) -> None:
        """Initialize the service with the CLI runner."""
        self.runner = runner

    def list_projects(self) -> List[Dict[str, Any]]:
        """Return all projects available to the current user."""
        projects = self.runner.run_cli_json(
            ["projects", "list", "--format", "json"]
        ) or []
        if not isinstance(projects, list):
            return []
        return projects

    def get_project(self, project_id: str) -> Dict[str, Any]:
        """Fetch a single project's details by id via CLI JSON.

        Args:
            project_id: The project identifier to query.

        Returns:
            Project details dict or an empty dict on error.
        """
        if not project_id:
            return {}
        try:
            data = self.runner.run_cli_json(
                ["projects", "info", project_id, "--format", "json"]
            ) or {}
            if isinstance(data, dict):
                return data
            return {}
        except Exception:
            return {}


