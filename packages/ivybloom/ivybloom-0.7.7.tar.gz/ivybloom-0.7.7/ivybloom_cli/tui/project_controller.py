"""Project selection flow helper for the TUI."""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional


class ProjectSelectionController:
    """Encapsulates project selection flow and timer management.

    Responsibilities:
    - Track whether a picker is open
    - Manage timers scheduled for pick prompts (boot, first-boot, retry)
    - Provide hooks for showing the picker and reacting to selection
    """

    def __init__(
        self,
        list_projects: Callable[[], List[Dict[str, Any]]],
        open_picker: Callable[
            [List[Dict[str, Any]], Callable[[Optional[str]], None]], None
        ],
    ) -> None:
        """Create controller with project list and picker callbacks."""
        self.list_projects = list_projects
        self.open_picker = open_picker
        self.current_project_id: Optional[str] = None
        self.picker_open: bool = False
        self.boot_timer = None
        self.first_boot_timer = None
        self.retry_timer = None
        self.first_boot: bool = True

    def schedule_boot_prompt(
        self, set_timer: Callable[[float, Callable[[], None]], Any], delay: float = 2.0
    ) -> None:
        """Schedule a picker prompt after boot with a delay."""
        try:
            self.boot_timer = set_timer(delay, self.ensure_pick)
        except Exception:
            pass

    def schedule_first_boot_prompt(
        self, set_timer: Callable[[float, Callable[[], None]], Any], delay: float = 0.5
    ) -> None:
        """Schedule a picker prompt for first boot."""
        try:
            self.first_boot_timer = set_timer(delay, self.ensure_pick)
        except Exception:
            pass

    def cancel_all_timers(self) -> None:
        """Stop and clear all scheduled timers."""
        for timer_name in ("boot_timer", "first_boot_timer", "retry_timer"):
            try:
                timer = getattr(self, timer_name)
                if timer:
                    timer.stop()  # type: ignore[attr-defined]
                    setattr(self, timer_name, None)
            except Exception:
                setattr(self, timer_name, None)

    def ensure_pick(self) -> None:
        """Open the project picker if projects exist and picker not already open."""
        if self.picker_open:
            return
        try:
            projects = self.list_projects()
        except Exception:
            projects = []
        if not projects:
            return
        self.picker_open = True
        self.open_picker(projects, self.on_picked)

    def on_picked(self, project_id: Optional[str]) -> None:
        """Handle project selection callback."""
        self.picker_open = False
        if not project_id:
            return
        self.current_project_id = project_id
        self.cancel_all_timers()
        self.first_boot = False


