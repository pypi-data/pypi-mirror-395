"""Jobs command wrappers for the TUI."""

from __future__ import annotations

from typing import Callable, Optional

from ..cli_runner import CLIRunner


def results(runner: CLIRunner, job_id: str) -> str:
    """Return job results JSON."""
    jid = _normalized_job_id(job_id)
    if not jid:
        return ""
    return runner.run_cli_text(["jobs", "results", jid, "--format", "json"]) or ""


def download_list_only(runner: CLIRunner, job_id: str, fmt: str = "table") -> str:
    """List downloadable artifacts for a job."""
    jid = _normalized_job_id(job_id)
    if not jid:
        return ""
    return runner.run_cli_text(["jobs", "download", jid, "--list-only", "--format", fmt or "table"]) or ""


def cancel(runner: CLIRunner, job_id: str) -> str:
    """Cancel a job; auto-confirms."""
    jid = _normalized_job_id(job_id)
    if not jid:
        return ""
    return runner.run_cli_text(["jobs", "cancel", jid], input_text="y\n") or ""


def status(runner: CLIRunner, job_id: str, extra_flags: Optional[str], on_line: Optional[Callable[[str], None]] = None) -> Optional[str]:
    import shlex
    jid = _normalized_job_id(job_id)
    if not jid:
        return ""
    args = ["jobs", "status", jid, "--format", "table"]
    if extra_flags:
        args += shlex.split(extra_flags)
    follow = any(flag in args for flag in ["--follow", "-f"]) 
    if follow and on_line is not None:
        for line in runner.run_cli_stream(args):
            on_line(line)
        return None
    return runner.run_cli_text(args, timeout=600) or ""


def _normalized_job_id(job_id: str) -> str:
    """Normalize job id input for CLI commands."""
    return (job_id or "").strip()


