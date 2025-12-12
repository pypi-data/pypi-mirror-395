"""Additional tests for TUI command wrappers."""

from __future__ import annotations

from typing import Any, Dict, Optional

from ivybloom_cli.tui.commands import (
    account_cmds,
    auth_cmds,
    batch_cmds,
    config_cmds,
    data_cmds,
    jobs_cmds,
    tools_cmds,
)
from ivybloom_cli.tui.commands import artifacts_cmds


class DummyRunner:
    def __init__(self) -> None:
        self.calls: list[list[str]] = []

    def run_cli_text(
        self,
        args: list[str],
        timeout: int = 60,
        input_text: Optional[str] = None,
        env_overrides: Optional[Dict[str, str]] = None,
    ) -> str:
        self.calls.append(args)
        if args[:2] == ["auth", "logout"]:
            return "logged out"
        return "ok"

    def run_cli_json(
        self,
        args: list[str],
        timeout: int = 30,
        env_overrides: Optional[Dict[str, str]] = None,
    ) -> Any:
        self.calls.append(args)
        return {"artifacts": []}

    def run_cli_stream(self, args, env_overrides=None):
        self.calls.append(args)
        yield "line"


def test_account_usage_builds_args() -> None:
    runner = DummyRunner()
    account_cmds.usage(runner, tool="esmfold", period="day")
    assert ["account", "usage", "--format", "table", "--tool", "esmfold", "--period", "day"] in runner.calls


def test_auth_link_no_wait() -> None:
    runner = DummyRunner()
    auth_cmds.link(runner, wait=False)
    assert ["auth", "link", "--no-wait"] in runner.calls


def test_batch_cancel_and_results() -> None:
    runner = DummyRunner()
    batch_cmds.cancel(runner, ids="a,b")
    batch_cmds.results(runner, ids="a", fmt="json", output_dir=None)
    assert any("batch" in call for call in runner.calls)


def test_config_export_and_import() -> None:
    runner = DummyRunner()
    config_cmds.export(runner, fmt="yaml", output="out.yml")
    config_cmds.import_file(runner, file_path="in.yml", merge=True)
    assert ["config", "export", "--format", "yaml", "--output", "out.yml"] in runner.calls
    assert ["config", "import", "in.yml", "--merge"] in runner.calls


def test_data_upload_and_sync() -> None:
    runner = DummyRunner()
    data_cmds.upload(runner, file_path="file.txt", project_id="p1")
    data_cmds.sync(runner, local_dir="/tmp", project_id=None)
    assert ["data", "upload", "file.txt", "--project-id", "p1"] in runner.calls
    assert ["data", "sync", "/tmp"] in runner.calls


def test_jobs_status_follow_streams_lines() -> None:
    runner = DummyRunner()
    lines: list[str] = []
    jobs_cmds.status(runner, "job1", extra_flags="--follow", on_line=lambda s: lines.append(s))
    assert lines == ["line"]


def test_tools_list_verbose_with_schemas() -> None:
    runner = DummyRunner()
    tools_cmds.list_tools(runner, fmt="json", verbose=True, schemas=True)
    assert ["tools", "list", "--format", "json", "--verbose", "--format-json-with-schemas"] in runner.calls


def test_artifacts_best_url_no_job_returns_none() -> None:
    runner = DummyRunner()
    assert artifacts_cmds.best_artifact_url(runner, "") is None


def test_jobs_cmds_guard_empty_job_id() -> None:
    runner = DummyRunner()
    assert jobs_cmds.results(runner, "") == ""
    assert jobs_cmds.cancel(runner, "") == ""
    assert jobs_cmds.status(runner, "", extra_flags=None) == ""


