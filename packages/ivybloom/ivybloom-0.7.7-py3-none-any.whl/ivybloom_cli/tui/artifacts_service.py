"""Artifact listing and preview utilities for the Textual TUI."""

from __future__ import annotations

import csv
import io
import json
from typing import Any, Dict, List, Optional

import requests
from rich.table import Table

from ..utils.colors import EARTH_TONES
from .artifact_preview import ArtifactPreviewRegistry, register_default_previewers
from .cli_runner import CLIRunner
from .debug_logger import DebugLogger


class ArtifactsService:
    """Service for listing and previewing artifacts via CLI subprocess + HTTP fetch."""

    def __init__(
        self, runner: CLIRunner, logger: DebugLogger | None = None
    ) -> None:
        """Initialize the service with runner and preview registry."""
        self.runner = runner
        self._logger = logger or DebugLogger(False, prefix="ART")
        self._registry = register_default_previewers(ArtifactPreviewRegistry())
        self._http = requests.Session()

    def list_artifacts_table(self, job_id: str) -> Table:
        """Render artifacts for a job as a rich Table."""
        self._logger.debug(f"list_artifacts_table: job_id={job_id}")
        arts = self.list_artifacts(job_id)
        table = Table(
            title="Artifacts",
            show_header=True,
            header_style=f"bold {EARTH_TONES['sage_dark']}",
        )
        table.add_column("Type", style="green")
        table.add_column("Filename", style="blue")
        table.add_column("Size", style="yellow")
        table.add_column("URL", style="dim")
        for art in arts:
            atype = str(art.get("artifact_type") or art.get("type") or "")
            fname = str(art.get("filename") or "")
            size = str(art.get("file_size") or "")
            url = str(art.get("presigned_url") or art.get("url") or "")
            if url and len(url) > 64:
                url = url[:61] + "..."
            table.add_row(atype, fname, size, url)
        return table

    def choose_artifact(
        self, job_id: str, selector: Optional[str]
    ) -> Optional[Dict[str, Any]]:
        """Choose an artifact by fuzzy selector with JSON/CSV priority."""
        self._logger.debug(f"choose_artifact: job_id={job_id} selector={selector}")
        arts = self.list_artifacts(job_id)
        chosen = None
        selection = (selector or "").strip().lower()

        def is_match(artifact: Dict[str, Any]) -> bool:
            if not selection:
                return True
            artifact_type = str(
                artifact.get("artifact_type") or artifact.get("type") or ""
            ).lower()
            filename = str(artifact.get("filename") or "").lower()
            return selection in artifact_type or selection in filename

        for priority_type in ("json", "csv"):
            for artifact in arts:
                artifact_type = str(
                    artifact.get("artifact_type") or artifact.get("type") or ""
                ).lower()
                if artifact_type == priority_type and is_match(artifact):
                    chosen = artifact
                    break
            if chosen:
                break

        if not chosen:
            for artifact in arts:
                if is_match(artifact):
                    chosen = artifact
                    break
        return chosen

    def choose_artifact_by_ext(
        self, job_id: str, exts: List[str]
    ) -> Optional[Dict[str, Any]]:
        """Choose first artifact whose filename ends with any of the given extensions."""
        self._logger.debug(f"choose_artifact_by_ext: job_id={job_id} exts={exts}")
        arts = self.list_artifacts(job_id)
        lower_exts = [ext.lower() for ext in exts]
        for artifact in arts:
            filename = str(artifact.get("filename") or "").lower()
            for ext in lower_exts:
                if filename.endswith(ext):
                    return artifact
        return None

    def fetch_bytes(self, url: str, timeout: int = 15) -> bytes:
        """Fetch raw bytes from a presigned URL."""
        self._logger.debug(f"fetch_bytes: GET {url} timeout={timeout}")
        try:
            response = self._http.get(url, timeout=timeout)
            response.raise_for_status()
            return response.content
        except requests.HTTPError as http_err:  # pragma: no cover - network dependent
            status = getattr(http_err.response, "status_code", "unknown")
            raise RuntimeError(f"HTTP {status} fetching artifact: {http_err}") from http_err
        except Exception as err:  # pragma: no cover - network dependent
            raise RuntimeError(f"Failed to fetch artifact: {err}") from err

    def preview_generic(
        self, content: bytes, filename: str, content_type: str | None = None
    ) -> str | Table:
        """Return best-effort preview for arbitrary artifact bytes."""
        try:
            result = self._registry.preview(content, filename, content_type)
            if result is not None:
                return result  # type: ignore[return-value]
        except Exception:
            pass

        try:
            if filename.lower().endswith(".json"):
                return self.preview_json(content, filename)
            if filename.lower().endswith(".csv"):
                return self.preview_csv(content, filename)
        except Exception:
            pass

        try:
            text = content.decode("utf-8", errors="ignore")
            if len(text) > 4000:
                text = text[:4000] + "\n[dim](truncated)[/dim]"
            return text
        except Exception:
            return "Unsupported preview format. Use 'Open' or 'Download'."

    def preview_json(self, content: bytes, filename: str) -> str | Table:
        """Preview JSON as structured table or formatted text."""
        max_json_bytes = 2_000_000
        text = content.decode("utf-8", errors="ignore")
        if len(text) > max_json_bytes:
            preview = text[:max_json_bytes]
            if not preview.rstrip().endswith(("}", "]", '"')):
                preview = preview.rsplit("\n", 1)[0] if "\n" in preview else preview
            return preview + "\n[dim](truncated JSON preview)[/dim]"
        try:
            data_obj = json.loads(text or "")
        except Exception:
            suffix = "\n[dim](truncated)[/dim]" if len(text) > max_json_bytes else ""
            return text[:max_json_bytes] + suffix

        if isinstance(data_obj, list) and data_obj and isinstance(data_obj[0], dict):
            cols = list(data_obj[0].keys())[:20]
            table = Table(title=f"JSON Preview: {filename}")
            for col in cols:
                table.add_column(str(col))
            for row in data_obj[:100]:
                table.add_row(*[str(row.get(col, ""))[:120] for col in cols])
            return table
        return json.dumps(data_obj, indent=2)

    def preview_csv(self, content: bytes, filename: str) -> str | Table:
        """Preview CSV content with a small table or truncated text."""
        max_csv_bytes = 500 * 1024
        text = content.decode("utf-8", errors="ignore")
        if len(content) > max_csv_bytes:
            preview = "\n".join(text.splitlines()[:15])
            return preview + "\n[dim](truncated) Use Open/Download[/dim]"
        sample = text[:4096]
        try:
            dialect = csv.Sniffer().sniff(sample)
        except Exception:
            dialect = csv.excel
        reader = csv.reader(io.StringIO(text), dialect)
        rows = list(reader)
        if not rows:
            return "Empty CSV"
        table = Table(title=f"CSV Preview: {filename}")
        header = rows[0]
        for heading in header[:20]:
            table.add_column(str(heading))
        for row in rows[1:101]:
            table.add_row(*[str(value)[:120] for value in row[:20]])
        return table

    def visualize_json_fast(
        self, content: bytes, width: int = 80, height: int = 20
    ) -> str:
        """Produce a compact JSON visualization with minimap."""
        try:
            text = content.decode("utf-8", errors="ignore")
            mini = braille_minimap(text, max(20, width // 2), max(3, height // 6))
            preview = text[: min(len(text), width * height * 2)]
            more = (
                "\n[dim](truncated) Use Open/Download for full)[/dim]"
                if len(text) > len(preview)
                else ""
            )
            return f"[b]JSON Preview[/b]\n\n{mini}\n\n```json\n{preview}\n```{more}"
        except Exception:
            return "Invalid or unsupported JSON"

    def visualize_txt_fast(
        self, content: bytes, filename: str, width: int = 80, height: int = 20
    ) -> str:
        """Produce a compact text visualization with minimap."""
        try:
            text = content.decode("utf-8", errors="ignore")
            mini = braille_minimap(text, max(20, width // 2), max(3, height // 6))
            preview = text[: min(len(text), width * height * 2)]
            more = "\n[dim](truncated)[/dim]" if len(text) > len(preview) else ""
            return f"[b]{filename}[/b]\n\n{mini}\n\n{preview}{more}"
        except Exception:
            return filename

    def visualize_csv_fast(
        self, content: bytes, filename: str, width: int = 80, height: int = 20
    ) -> str | Table:
        """Render a width-aware CSV preview using fixed-width layout."""
        try:
            text = content.decode("utf-8", errors="ignore")
            rows = list(csv.reader(io.StringIO(text)))
            if not rows:
                return "Empty CSV"
            header = rows[0]
            data = rows[1 : min(len(rows), 1 + max(10, height))]
            max_width = max(40, width * 2)

            min_col_width = 6
            col_count = min(len(header), 12)
            col_widths = [min_col_width] * col_count
            for index in range(col_count):
                desired = len(str(header[index]))
                for row in data:
                    if index < len(row):
                        desired = max(desired, len(str(row[index])))
                col_widths[index] = min(max(8, desired), max_width // col_count)

            total_width = sum(col_widths) + (col_count - 1) * 3
            if total_width > max_width:
                scale = max_width / total_width
                col_widths = [max(8, int(width * scale)) for width in col_widths]

            def _fmt_row(items: List[Any]) -> str:
                cells: List[str] = []
                for idx in range(col_count):
                    val = str(items[idx]) if idx < len(items) else ""
                    width = col_widths[idx]
                    val = (
                        val[: width - 1] + "…"
                        if len(val) > width
                        else val.ljust(width)
                    )
                    cells.append(val)
                return " | ".join(cells)

            head = _fmt_row(header)
            separator = "-+-".join(["-" * width for width in col_widths])
            body = "\n".join(_fmt_row(row) for row in data)
            more = "\n[dim](truncated)[/dim]" if len(rows) > len(data) + 1 else ""
            return f"[b]{filename}[/b]\n\n{head}\n{separator}\n{body}{more}"
        except Exception:
            return f"Unsupported CSV: {filename}"

    def list_artifacts(self, job_id: str) -> List[Dict[str, Any]]:
        """Return artifacts list with presigned URLs when available."""
        return self._list_artifacts(job_id)

    def _list_artifacts(self, job_id: str) -> List[Dict[str, Any]]:
        """Return the artifacts list for a job; empty list on error."""
        payload = self.runner.run_cli_json(
            ["jobs", "download", job_id, "--list-only", "--format", "json"]
        ) or {}
        if isinstance(payload, dict):
            artifacts = payload.get("artifacts")
            if isinstance(artifacts, list):
                return [art for art in artifacts if isinstance(art, dict)]
        return []


