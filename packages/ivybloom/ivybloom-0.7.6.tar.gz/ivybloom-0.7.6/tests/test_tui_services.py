"""Unit tests for lightweight TUI services."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from ivybloom_cli.tui.artifacts_service import ArtifactsService
from ivybloom_cli.tui.jobs_service import JobsService
from ivybloom_cli.tui.projects_service import ProjectsService


class DummyRunner:
    """Minimal runner that returns canned responses."""

    def __init__(self, json_map: Optional[Dict[Any, Any]] = None) -> None:
        self.json_map = json_map or {}

    def run_cli_json(
        self, args: List[str], timeout: int = 30, env_overrides: Optional[Dict[str, str]] = None
    ) -> Any:
        return self.json_map.get(tuple(args))


class DummyResponse:
    """Simple response stand-in."""

    def __init__(self, content: bytes) -> None:
        self.content = content

    def raise_for_status(self) -> None:
        return None


class DummySession:
    """Mock requests-like session."""

    def __init__(self) -> None:
        self.calls: List[tuple[str, int]] = []

    def get(self, url: str, timeout: int) -> DummyResponse:
        self.calls.append((url, timeout))
        return DummyResponse(b"content")


def test_jobs_service_format_row_progress() -> None:
    job = {
        "job_id": "abcdefghijk",
        "tool_name": "esmfold",
        "status": "running",
        "progress_percent": 50,
        "completed_at": "2024-02-01T00:00:00Z",
    }
    cells = JobsService.format_row(job)
    assert cells[0] == "abcdefgh"
    assert "50%" in cells[2]


def test_jobs_service_list_jobs_handles_non_list() -> None:
    runner = DummyRunner(json_map={("jobs", "list", "--format", "json", "--limit", "10", "--offset", "0"): {}})
    service = JobsService(runner)
    assert service.list_jobs(project_id=None, limit=10, offset=0) == []


def test_projects_service_get_project_invalid_returns_empty() -> None:
    runner = DummyRunner()
    service = ProjectsService(runner)
    assert service.get_project("") == {}


def test_artifacts_service_choose_and_fetch() -> None:
    job_id = "job-1"
    artifact_list = {
        "artifacts": [
            {"artifact_type": "csv", "filename": "table.csv", "url": "http://example/csv"},
            {"artifact_type": "json", "filename": "data.json", "presigned_url": "http://example/json"},
            {"artifact_type": "png", "filename": "image.png", "url": "http://example/img.png"},
        ]
    }
    runner = DummyRunner(
        json_map={
            ("jobs", "download", job_id, "--list-only", "--format", "json"): artifact_list,
        }
    )
    service = ArtifactsService(runner)
    session = DummySession()
    service._http = session  # type: ignore[attr-defined]
    chosen_json = service.choose_artifact(job_id, selector=None)
    assert chosen_json and chosen_json.get("artifact_type") == "json"
    chosen_png = service.choose_artifact_by_ext(job_id, [".png"])
    assert chosen_png and chosen_png.get("filename") == "image.png"
    content = service.fetch_bytes("http://example/json", timeout=5)
    assert content == b"content"
    assert session.calls == [("http://example/json", 5)]


def test_artifacts_service_table_renders_rows() -> None:
    job_id = "job-2"
    artifact_list = {
        "artifacts": [
            {"artifact_type": "csv", "filename": "table.csv", "url": "http://example/csv"},
            {"artifact_type": "zip", "filename": "archive.zip", "url": "http://example/zip"},
        ]
    }
    runner = DummyRunner(
        json_map={
            ("jobs", "download", job_id, "--list-only", "--format", "json"): artifact_list,
        }
    )
    service = ArtifactsService(runner)
    table = service.list_artifacts_table(job_id)
    assert len(table.rows) == 2
    assert table.columns[0].header == "Type"



