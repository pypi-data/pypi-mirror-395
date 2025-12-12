"""Controllers for rendering detailed job panes and visualizations."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from .accelerated_text import braille_minimap, chunked_update
from .artifact_visualizer import visualize_json, visualize_txt
from .protein_visualizer import ProteinVisualizer
from .smiles_visualizer import render_smiles_unicode, summarize_smiles


class DetailsController:
    """Own rendering of details panes and optimized visualization paths."""

    def __init__(self, app: Any) -> None:
        self.app = app
        self._last_viz_kind: Optional[str] = None
        self._last_viz_payload: Optional[Dict[str, Any]] = None
        self._current_job_smiles: Optional[str] = None

    def render_all(self, job: Dict[str, Any]) -> None:
        """Render summary, manifest, placeholder, and artifacts for a job."""
        self.app._details_view.render_summary(job)
        self._render_manifest_fast(job)
        self.app._details_view.render_visualization_placeholder(job)
        self.app._details_view.render_artifacts(job)
        self._cache_job_smiles(job)
        self._render_inline_preview(job)
        self._activate_tab("summary")

    def try_render_protein(self, pdb_text: str, filename: str) -> None:
        """Render a protein structure, capturing legend and SMILES if available."""
        try:
            visualizer = ProteinVisualizer()
            width, height = self.app._compute_visualization_size()
            capabilities = getattr(self.app, "_accel_caps", {}) or {}
            use_fast = bool(capabilities.get("unicode_heavy", True))
            use_truecolor = bool(capabilities.get("truecolor", False))
            if use_fast:
                ascii_art = visualizer.render_pdb_fast_unicode(
                    pdb_text,
                    width=width,
                    height=height,
                    filename_hint=filename,
                    use_truecolor=use_truecolor,
                )
                if not ascii_art or ascii_art.startswith("Fast render failed"):
                    ascii_art = visualizer.render_pdb_as_text(
                        pdb_text, width=width, height=height, filename_hint=filename
                    )
            else:
                ascii_art = visualizer.render_pdb_as_text(
                    pdb_text, width=width, height=height, filename_hint=filename
                )
            try:
                smiles = getattr(self, "_current_job_smiles", None)
                if (
                    not smiles
                    and hasattr(self.app, "selected_job")
                    and isinstance(self.app.selected_job, dict)
                ):
                    smiles = self.app.selected_job.get("smiles") or self.app.selected_job.get(
                        "input_smiles"
                    )
                if smiles:
                    ascii_art = ascii_art + "\n\n" + summarize_smiles(str(smiles))
            except Exception:
                pass
            if self.app.details_visualization:
                legend = []
                try:
                    pairs = visualizer.chain_legend(pdb_text)
                    if pairs:
                        legend_lines = ["[dim]Chains:[/dim]"]
                        for cid, color in pairs[:10]:
                            legend_lines.append(f"[{color}]■[/] {cid}")
                        legend = ["", "\n".join(legend_lines)]
                except Exception:
                    pass
                self.app.details_visualization.update(
                    f"[green]Protein Structure (ASCII)[/green]\n\n{ascii_art}"
                    + ("\n\n" + legend[1] if legend else "")
                )
            self._last_viz_kind = "protein"
            self._last_viz_payload = {"pdb_text": pdb_text, "filename": filename}
        except Exception as error:
            if self.app.details_visualization:
                self.app.details_visualization.update(
                    f"[red]Visualization failed:[/red]\n{self.app._format_error(error)}"
                )

    def rerender_on_resize(self) -> None:
        """Re-render the last visualization on resize if applicable."""
        try:
            if self._last_viz_kind == "protein" and self._last_viz_payload:
                pdb_text = self._last_viz_payload.get("pdb_text", "")
                filename = self._last_viz_payload.get("filename", "protein.pdb")
                if pdb_text and self.app.details_visualization:
                    visualizer = ProteinVisualizer()
                    width, height = self.app._compute_visualization_size()
                    capabilities = getattr(self.app, "_accel_caps", {}) or {}
                    use_fast = bool(capabilities.get("unicode_heavy", True))
                    use_truecolor = bool(capabilities.get("truecolor", False))
                    if use_fast:
                        ascii_art = visualizer.render_pdb_fast_unicode(
                            pdb_text,
                            width=width,
                            height=height,
                            filename_hint=filename,
                            use_truecolor=use_truecolor,
                        )
                        if not ascii_art or ascii_art.startswith("Fast render failed"):
                            ascii_art = visualizer.render_pdb_as_text(
                                pdb_text,
                                width=width,
                                height=height,
                                filename_hint=filename,
                            )
                    else:
                        ascii_art = visualizer.render_pdb_as_text(
                            pdb_text, width=width, height=height, filename_hint=filename
                        )
                    self.app.details_visualization.update(
                        f"[green]Protein Structure (ASCII)[/green]\n\n{ascii_art}"
                    )
        except Exception:
            pass

    def _render_inline_preview(self, job: Dict[str, Any]) -> None:
        """Render a small deterministic preview in the right-column header."""
        panel = getattr(self.app.right_column, "preview", None) if getattr(self.app, "right_column", None) else None
        if panel is None:
            return
        job_id = str(job.get("job_id") or job.get("id") or "").strip()
        if not job_id:
            panel.update("")
            return
        artifact = self._choose_preview_artifact(job_id)
        if not artifact:
            self._render_smiles_preview(job, panel)
            return
        filename = str(artifact.get("filename") or "")
        url = str(artifact.get("presigned_url") or artifact.get("url") or "")
        if not url:
            panel.update(f"{filename or 'artifact'} (no URL)")
            self._notify_preview_error("Artifact missing URL for inline preview")
            return
        try:
            content = self.app._artifacts.fetch_bytes(url, timeout=6)
        except Exception as error:
            panel.update(f"{filename or 'artifact'}\n[red]Preview failed[/red]")
            self._notify_preview_error(f"Preview fetch failed: {error}")
            return
        capabilities = getattr(self.app, "_accel_caps", {}) or {}
        is_image = filename.lower().endswith((".png", ".jpg", ".jpeg", ".svg"))
        if is_image and (capabilities.get("kitty") or capabilities.get("wezterm")) and len(content) < 300_000:
            import base64

            b64 = base64.b64encode(content).decode("ascii")
            panel.update(f"[dim]{filename or 'image'} (inline)[/dim]")
            print(f"\033_Gf=100,t=f,a=T;{b64}\033\\", end="")
            return
        if filename.lower().endswith(".json"):
            snippet = content.decode("utf-8", errors="ignore")[:1000]
            suffix = "\n[dim](truncated)[/dim]" if len(content) > 1000 else ""
            panel.update(snippet + suffix)
            return
        panel.update(f"{filename or 'artifact'}")

    def _render_smiles_preview(self, job: Dict[str, Any], panel) -> None:
        """Render SMILES preview when no artifact is available."""
        try:
            smiles = job.get("smiles") or job.get("input_smiles")
            if smiles:
                mini = render_smiles_unicode(str(smiles), width=40, height=6)
                panel.update(mini)
                return
        except Exception:
            pass
        panel.update("[dim]No preview available[/dim]")

    def _choose_preview_artifact(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Pick the best artifact for inline preview deterministically."""
        image = self.app._artifacts.choose_artifact_by_ext(job_id, [".png", ".jpg", ".jpeg", ".svg"])
        if image:
            return image
        json_art = self.app._artifacts.choose_artifact_by_ext(job_id, [".json"])
        if json_art:
            return json_art
        return self.app._artifacts.choose_artifact(job_id, selector=None)

    def _cache_job_smiles(self, job: Dict[str, Any]) -> None:
        """Store SMILES for downstream navigation."""
        try:
            self._current_job_smiles = None
            smiles_arr = None
            if isinstance(job.get("smiles"), list):
                smiles_arr = job.get("smiles")
            elif isinstance(job.get("input_smiles"), list):
                smiles_arr = job.get("input_smiles")
            if smiles_arr and len(smiles_arr) > 0:
                self._current_job_smiles = smiles_arr[0]
            else:
                self._current_job_smiles = job.get("smiles") or job.get("input_smiles")
        except Exception:
            self._current_job_smiles = None

    def _activate_tab(self, tab_id: str) -> None:
        """Activate a tab by id when available."""
        try:
            tabbed_content = self.app.query_one("TabbedContent")
            if tabbed_content:
                tabbed_content.active = tab_id
        except Exception:
            pass

    def _notify_preview_error(self, message: str) -> None:
        """Send preview failure to the app notification bar when available."""
        try:
            notify = getattr(self.app, "_notify", None)
            if callable(notify):
                notify(message, level="error")
        except Exception:
            pass

    def _render_manifest_fast(self, job: Dict[str, Any]) -> None:
        """Fast manifest rendering using chunked update and minimap preview."""
        try:
            if not self.app.details_manifest:
                return
            lines: List[str] = []
            job_id = job.get("job_id") or job.get("id")
            lines.append(f"[b]Job ID:[/b] {job_id}")
            lines.append(f"[b]Tool:[/b] {job.get('tool_name') or job.get('job_type')}")
            lines.append(f"[b]Status:[/b] {job.get('status')}")
            title = job.get("job_title") or job.get("title")
            if title:
                lines.append(f"[b]Title:[/b] {title}")
            project = job.get("project_id")
            if project:
                lines.append(f"[b]Project:[/b] {project}")
            created = job.get("created_at")
            if created:
                lines.append(f"[b]Created:[/b] {created}")
            completed = job.get("completed_at")
            if completed:
                lines.append(f"[b]Completed:[/b] {completed}")
            progress = job.get("progress_percent") or job.get("progress_percentage")
            if progress is not None:
                lines.append(f"[b]Progress:[/b] {progress}%")
            lines.append("")
            lines.append("[b]Complete Job Data (preview):[/b]")
            import json as _json

            try:
                job_json = _json.dumps(job, indent=2)
            except Exception:
                job_json = str(job)
            try:
                width = 40
                height = 3
                mini = braille_minimap(job_json, width, height)
                lines.append("[dim]Minimap:[/dim]")
                lines.append(mini)
                lines.append("")
            except Exception:
                pass
            header = "\n".join(lines) + "\n"
            content = header + job_json
            chunked_update(
                self.app, self.app.details_manifest, content, chunk_bytes=15000
            )
        except Exception:
            try:
                self.app._details_view.render_manifest(job)
            except Exception:
                pass


