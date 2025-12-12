"""Status bar helpers for the Textual TUI."""

from __future__ import annotations

from typing import Any

from ..utils.colors import EARTH_TONES


def update_status_bar(app: Any) -> None:
    """Render connection, project, and user info in the status bar."""
    status_bar = getattr(app, "status_bar", None)
    if not status_bar:
        return
    try:
        pulses = ["·", "•", "●", "•"]
        idx = app._pulse_step % len(pulses)  # type: ignore[attr-defined]
    except Exception:
        pulses = ["●"]
        idx = 0
    if getattr(app, "_connected", False):
        dot = pulses[idx]
        dot_markup = (
            f"[{EARTH_TONES['success']}]{dot}[/{EARTH_TONES['success']}]"
        )
    else:
        dot_markup = f"[{EARTH_TONES['error']}]●[/{EARTH_TONES['error']}]"
    err = f"errors: {'1' if getattr(app, '_last_error', None) else '0'}"
    if getattr(app, "_project_name", None) and str(app._project_name).strip():  # type: ignore[attr-defined]
        project_label = str(app._project_name).strip()  # type: ignore[attr-defined]
    elif getattr(app, "initial_project_id", None):
        project_label = app.initial_project_id  # type: ignore[attr-defined]
    else:
        project_label = "N/A"
    user_label = (getattr(app, "_user_display", None) or "N/A")  # type: ignore[attr-defined]
    refresh_interval = getattr(app, "_current_refresh_interval", None) or getattr(app, "refresh_interval_secs", None)
    refresh_latency = getattr(app, "_last_refresh_latency_ms", None)
    refresh_at = getattr(app, "_last_refresh_at", None)
    refresh_parts = []
    if refresh_interval:
        refresh_parts.append(f"{refresh_interval}s")
    if refresh_latency is not None:
        refresh_parts.append(f"{int(refresh_latency)}ms")
    if refresh_at:
        refresh_parts.append(f"{refresh_at}")
    refresh_label = " / ".join(refresh_parts) if refresh_parts else "n/a"
    status = (
        f"[dim]{dot_markup} [project: {project_label}] "
        f"[user: {user_label}] [{err}] [refresh: {refresh_label}][/dim]"
    )
    status_bar.update(status)


def tick_status_pulse(app: Any) -> None:
    """Advance pulse animation state and refresh status bar."""
    try:
        if getattr(app, "_connected", False):
            app._pulse_step = (getattr(app, "_pulse_step", 0) + 1) % 1024  # type: ignore[attr-defined]
        update_status_bar(app)
    except Exception:
        pass


def refresh_context_labels(app: Any) -> None:
    """Refresh user and project labels, updating the status bar when done."""
    try:
        if (
            not getattr(app, "_user_display", None)
            and app.auth_manager.is_authenticated()  # type: ignore[attr-defined]
        ):
            data = app._run_cli_json(  # type: ignore[attr-defined]
                ["account", "info", "--format", "json"], timeout=10
            ) or {}
            if isinstance(data, dict):
                app._user_display = (
                    str(
                        data.get("display_name")
                        or data.get("name")
                        or data.get("email")
                        or data.get("user_id")
                        or ""
                    ).strip()
                    or None
                )  # type: ignore[attr-defined]
    except Exception:
        pass
    try:
        if getattr(app, "initial_project_id", None):
            pdata = app._run_cli_json(  # type: ignore[attr-defined]
                ["projects", "info", app.initial_project_id, "--format", "json"],
                timeout=10,
            ) or {}
            if isinstance(pdata, dict):
                name_val = str(pdata.get("name") or "").strip()
                app._project_name = name_val or None  # type: ignore[attr-defined]
    except Exception:
        pass
    finally:
        update_status_bar(app)


