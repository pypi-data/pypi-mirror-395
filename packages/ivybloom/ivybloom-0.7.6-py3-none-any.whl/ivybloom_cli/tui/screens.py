"""Modal screens and pickers used throughout the Textual TUI."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

try:
    from textual.app import ComposeResult
except Exception:  # pragma: no cover
    # Minimal fallback type when ComposeResult is unavailable
    ComposeResult = object  # type: ignore

# Robust ModalScreen compatibility across Textual versions
try:
    from textual.screen import ModalScreen  # Preferred in newer Textual
except Exception:  # pragma: no cover - compatibility for older / different layouts
    try:
        # Some versions expose Screen under textual.screen
        from textual.screen import Screen as ModalScreen  # type: ignore
    except Exception:
        try:
            # Older versions expose Screen under textual.app
            from textual.app import Screen as ModalScreen  # type: ignore
        except Exception:
            # Last resort: define a no-op base class so imports succeed
            class ModalScreen(object):  # type: ignore
                pass
from textual.widgets import Static, Input, ListView, ListItem, LoadingIndicator, Button
from textual.containers import Vertical, Horizontal
from .search import rank_commands
from .debug_logger import DebugLogger


class CommandPalette(ModalScreen[Optional[str]]):
    """Lightweight command palette for fuzzy searching available actions."""

    def __init__(self, commands: List[tuple[str, str, str]], logger: DebugLogger | None = None):
        super().__init__()
        self._all_commands = commands
        self._filtered = commands
        self.query_input: Input | None = None
        self.list_view: ListView | None = None
        self._row_map: List[int] = []
        self._logger = logger or DebugLogger(False)

    def compose(self) -> ComposeResult:
        with Vertical():
            self.query_input = Input(placeholder="Type to filter commands… (Esc to close)")
            yield self.query_input
        self.list_view = ListView()
        yield self.list_view

    def on_mount(self) -> None:
        self._logger.debug("CommandPalette.on_mount: refreshing list and focusing input")
        self._refresh_list()
        if self.query_input:
            self.query_input.focus()
        # Ensure the first item is highlighted for immediate arrow/enter usage
        if self.list_view and len(self.list_view.children) > 0:
            try:
                self.list_view.index = 0  # type: ignore[attr-defined]
            except Exception:
                pass

    def _refresh_list(self) -> None:
        if not self.list_view:
            return
        self.list_view.clear()
        self._row_map = []
        key_hints = {
            "refresh": "Shortcut: r",
            "open_external": "Shortcut: o",
            "toggle_help": "Shortcut: ?",
            "focus_filter": "Shortcut: f",
            "jobs_load_more": "",
        }
        # Group by section prefix before ':'
        grouped: Dict[str, List[tuple[str, str, str]]] = {}
        for item in self._filtered:
            _, name, _ = item
            section = name.split(":", 1)[0].strip() if ":" in name else "General"
            grouped.setdefault(section, []).append(item)

        for section in sorted(grouped.keys()):
            # Non-selectable header row
            self.list_view.append(ListItem(Static(f"[b]{section}[/b]")))
            for item in grouped[section]:
                cmd_id, name, desc = item
                hint = key_hints.get(cmd_id, "")
                suffix = f"\n[dim]{desc}[/dim]" if desc else ""
                if hint:
                    suffix += f"\n[dim]{hint}[/dim]"
                self.list_view.append(ListItem(Static(f"{name}{suffix}")))
                # Map this visual row to index in filtered list
                self._row_map.append(self._filtered.index(item))
        # Keep cursor at top after refresh so Enter selects the first item
        try:
            if len(self._filtered) > 0 and self.list_view:
                self.list_view.index = 0  # type: ignore[attr-defined]
        except Exception:
            pass

    def on_input_changed(self, event: Input.Changed) -> None:  # type: ignore[override]
        if event.input is not self.query_input:
            return
        q = (event.value or "").strip().lower()
        self._logger.debug(f"CommandPalette.on_input_changed: query='{q}'")
        self._filtered = rank_commands(self._all_commands, q, limit=200)
        self._refresh_list()

    def on_list_view_selected(self, event: ListView.Selected) -> None:  # type: ignore[override]
        if self._logger:
            try:
                self._logger.debug(f"CommandPalette.on_list_view_selected: index={event.index}")
            except Exception:
                pass
        idx = event.index
        # First rows of each section are headers. Only rows with mapping are selectable.
        if 0 <= idx - 0 < len(self._row_map) and 0 <= idx < len(self._row_map):
            filtered_idx = self._row_map[idx]
            if 0 <= filtered_idx < len(self._filtered):
                self.dismiss(self._filtered[filtered_idx][0])
                return
        self.dismiss(None)

    def on_key(self, event) -> None:  # type: ignore[override]
        # Esc closes the palette
        if event.key == "escape":
            if self._logger:
                try:
                    self._logger.debug("CommandPalette.on_key: escape -> dismiss")
                except Exception:
                    pass
            self.dismiss(None)
            return
        # Arrow keys navigate the list even when focus is in the query input
        if event.key in ("down", "up") and self.list_view:
            try:
                self.list_view.focus()
                if event.key == "down":
                    self.list_view.action_cursor_down()  # type: ignore[attr-defined]
                else:
                    self.list_view.action_cursor_up()  # type: ignore[attr-defined]
                event.stop()
            except Exception:
                pass
            return
        # Enter selects the current item
        if event.key == "enter":
            try:
                if self.list_view and len(self._row_map) > 0:
                    # If focus is on list, trigger selection; otherwise, pick current index (default 0)
                    if self.list_view.has_focus:
                        self.list_view.action_select_cursor()  # type: ignore[attr-defined]
                    else:
                        idx = getattr(self.list_view, "index", 0)  # type: ignore[attr-defined]
                        idx = 0 if idx is None else idx
                        if 0 <= idx < len(self._row_map):
                            filtered_idx = self._row_map[idx]
                            if 0 <= filtered_idx < len(self._filtered):
                                self.dismiss(self._filtered[filtered_idx][0])
                                return
                        self.dismiss(None)
                    event.stop()
            except Exception:
                pass


class PromptScreen(ModalScreen[Optional[str]]):
    """Simple prompt dialog with a single input and placeholder."""

    def __init__(self, prompt: str, placeholder: str = ""):
        super().__init__()
        self._prompt = prompt
        self._placeholder = placeholder
        self.input: Input | None = None

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static(self._prompt)
            self.input = Input(placeholder=self._placeholder or "Press Enter to submit; Esc to cancel")
            yield self.input

    def on_mount(self) -> None:
        if self.input:
            self.input.focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:  # type: ignore[override]
        if event.input is self.input:
            self.dismiss(event.value)

    def on_key(self, event) -> None:  # type: ignore[override]
        if event.key == "escape":
            self.dismiss(None)


class FiltersScreen(ModalScreen[Optional[Dict[str, str]]]):
    """Collect ad-hoc filters for jobs list via a modal form."""

    def __init__(self) -> None:
        super().__init__()
        self.inputs: Dict[str, Input] = {}

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("Jobs Filters (leave blank to skip)")
            for label, key in [
                ("Status", "status"),
                ("Tool", "tool"),
                ("Project ID", "project-id"),
                ("Created After (ISO)", "created-after"),
                ("Created Before (ISO)", "created-before"),
                ("Sort By (created_at|status|job_type)", "sort-by"),
                ("Sort Order (asc|desc)", "sort-order"),
            ]:
                yield Static(label)
                inp = Input()
                self.inputs[key] = inp
                yield inp
            yield Static("Limit (default 50)")
            limit_inp = Input()
            self.inputs["limit"] = limit_inp
            yield limit_inp
            yield Static("Offset (default 0)")
            offset_inp = Input()
            self.inputs["offset"] = offset_inp
            yield offset_inp
            yield Static("Press Enter to apply; Esc to cancel", classes="muted")

    def on_mount(self) -> None:
        # Focus first field
        if self.inputs:
            first = next(iter(self.inputs.values()))
            first.focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:  # type: ignore[override]
        # When any input submits, collect all values and dismiss
        values: Dict[str, str] = {}
        for k, inp in self.inputs.items():
            val = (inp.value or "").strip()
            if val:
                values[k] = val
        self.dismiss(values or None)

    def on_key(self, event) -> None:  # type: ignore[override]
        if event.key == "escape":
            self.dismiss(None)


class SplashScreen(ModalScreen[None]):
    """Minimal splash/loading screen shown at startup."""

    def __init__(self, title: str = "IvyBloom", subtitle: str = "Loading…"):
        super().__init__()
        self._title = title
        self._subtitle = subtitle

    def compose(self) -> ComposeResult:
        from rich.table import Table  # optional import for consistency with app styles
        from ..utils.colors import EARTH_TONES
        ascii_logo = "\n".join([
            "  ____      __     ____  _                          ",
            " |_  /___  / /__  / __ )(_)___  ____  ____ _      __",
            "  / // _ \\ / _ \\ __  / / __ \\_/ __ \\ __ \\ | /| / /",
            " /___/\\___/_/\\___/_/ /_/_/_/ /_(_) /_/ / /_/ / |/ |/ / ",
            "                                 /____/\\____/|__/|__/  ",
        ])
        with Vertical(classes="splash"):
            yield Static(f"[b]{self._title}[/b]", classes="panel-title")
            yield Static(ascii_logo, classes="welcome-art")
            yield LoadingIndicator(classes="welcome-loading")
            yield Static(self._subtitle, classes="muted")


class ConfigEditorScreen(ModalScreen[Optional[Dict[str, Any]]]):
    """Simple key-value editor for core config fields.

    Returns a dict of updated keys on submit, or None on cancel.
    """
    def __init__(self, *, initial: Optional[Dict[str, Any]] = None, config_path: Optional[str] = None) -> None:
        super().__init__()
        self._initial = dict(initial or {})
        self._inputs: Dict[str, Input] = {}
        self._status: Static | None = None
        self._config_path: str = str(config_path or "")

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("[b]Edit Configuration[/b]")
            if self._config_path:
                yield Static(f"Config file: [dim]{self._config_path}[/dim]")
            fields: List[tuple[str, str]] = [
                ("API URL", "api_url"),
                ("Frontend URL", "frontend_url"),
                ("Timeout (secs)", "timeout"),
                ("Retries", "retries"),
                ("Output Format (json|yaml|table|csv)", "output_format"),
                ("Theme (light|dark)", "theme"),
                ("Debug (true|false)", "debug"),
                ("Disable Keyring (true|false)", "disable_keyring"),
                ("TUI Refresh Interval (secs)", "tui_refresh_interval_secs"),
            ]
            for label, key in fields:
                yield Static(label)
                val = self._coerce_to_str(self._initial.get(key))
                inp = Input(placeholder=val or "")
                if val:
                    try:
                        inp.value = val
                    except Exception:
                        pass
                self._inputs[key] = inp
                yield inp
            self._status = Static("Press Save to apply changes, or Reset to restore defaults.", classes="muted")
            yield self._status
            with Horizontal():
                yield Button("Save", id="save")
                yield Button("Reset to Defaults", id="reset")
                yield Button("Cancel", id="cancel")

    def on_mount(self) -> None:
        # Focus first input
        if self._inputs:
            first = next(iter(self._inputs.values()))
            first.focus()

    def _coerce_to_str(self, v: Any) -> str:
        if v is None:
            return ""
        if isinstance(v, bool):
            return "true" if v else "false"
        return str(v)

    def on_input_submitted(self, event: Input.Submitted) -> None:  # type: ignore[override]
        # Move focus to next input on Enter
        keys = list(self._inputs.keys())
        for idx, (key, inp) in enumerate(self._inputs.items()):
            if event.input is inp:
                # Focus next input field if present
                if idx + 1 < len(keys):
                    nxt = self._inputs[keys[idx + 1]]
                    try:
                        nxt.focus()
                    except Exception:
                        pass
                return

    def on_button_pressed(self, event) -> None:  # type: ignore[override]
        try:
            bid = getattr(event.button, "id", "")
        except Exception:
            bid = ""
        if bid == "cancel":
            self.dismiss(None)
            return
        if bid == "reset":
            self.dismiss({"__reset__": True})
            return
        if bid == "save":
            changes, error = self._collect_and_validate_changes()
            if error:
                try:
                    if self._status:
                        self._status.update(f"[red]{error}[/red]")
                except Exception:
                    pass
                return
            self.dismiss(changes)

    def _collect_and_validate_changes(self) -> tuple[Dict[str, Any], Optional[str]]:
        changes: Dict[str, Any] = {}
        # Validators and coercers
        def as_bool(s: str) -> Optional[bool]:
            v = s.strip().lower()
            if v in {"true","1","yes","y"}: return True
            if v in {"false","0","no","n"}: return False
            return None
        def as_int(s: str) -> Optional[int]:
            try:
                return int(s.strip())
            except Exception:
                return None
        def is_url(s: str) -> bool:
            return s.startswith("http://") or s.startswith("https://")

        for key, inp in self._inputs.items():
            raw = (inp.value or "").strip()
            current = self._initial.get(key)
            if raw == self._coerce_to_str(current):
                continue
            if key in {"api_url","frontend_url"}:
                if raw and not is_url(raw):
                    return {}, f"{key} must start with http:// or https://"
                changes[key] = raw
            elif key in {"output_format"}:
                allowed = {"json","yaml","table","csv"}
                if raw and raw not in allowed:
                    return {}, f"output_format must be one of {', '.join(sorted(allowed))}"
                changes[key] = raw or "json"
            elif key in {"theme"}:
                allowed = {"light","dark"}
                if raw and raw not in allowed:
                    return {}, "theme must be 'light' or 'dark'"
                changes[key] = raw or "light"
            elif key in {"timeout","retries","tui_refresh_interval_secs"}:
                iv = as_int(raw)
                if iv is None or iv < 0:
                    return {}, f"{key} must be a non-negative integer"
                changes[key] = iv
            elif key in {"debug","disable_keyring"}:
                bv = as_bool(raw)
                if bv is None:
                    return {}, f"{key} must be true/false"
                changes[key] = bv
            else:
                changes[key] = raw
        return changes, None

    def on_key(self, event) -> None:  # type: ignore[override]
        if event.key == "escape":
            self.dismiss(None)


def _resolve_selected_index(event, list_view) -> int:
    """Best-effort to resolve selected index across Textual versions.

    Tries event.index, then list_view.index, then falls back to 0.
    """
    try:
        idx = getattr(event, "index")
        if isinstance(idx, int):
            return idx
    except Exception:
        pass
    try:
        if list_view is not None:
            idx = getattr(list_view, "index", None)
            if isinstance(idx, int):
                return idx
    except Exception:
        pass
    try:
        # As a last resort, try to locate the event.item within list_view children
        item = getattr(event, "item", None)
        if item is not None and list_view is not None:
            try:
                children = list_view.children
                for i, child in enumerate(children):
                    if child is item:
                        return i
            except Exception:
                pass
    except Exception:
        pass
    return 0


class ProjectPicker(ModalScreen[Optional[str]]):
    """Modal project picker used on boot and when switching projects."""
    CSS = """
    ProjectPicker {
        background: #E6D5C7;
        border: solid #4A5D4C;
        padding: 1;
    }
    
    ListView {
        background: #E6D5C7;
        color: #4A5D4C;
        border: solid #739177;
    }
    
    ListItem {
        background: #E6D5C7;
        color: #4A5D4C;
        padding: 0 1;
    }
    
    ListItem:focus {
        background: #739177;
        color: #E6D5C7;
    }
    """
    
    def __init__(self, projects: List[Dict[str, Any]]):
        super().__init__()
        self._projects = projects
        self._list: ListView | None = None

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("[b]Select a Project[/b] (Enter to confirm, Esc to cancel)")
            # Create list items directly in compose to avoid append issues
            list_items = []
            for p in self._projects:
                pid = str(p.get('project_id') or p.get('id') or '')
                name = str(p.get('name') or pid or 'Unnamed')
                list_items.append(ListItem(Static(f"[b]{name}[/b]  [dim]{pid}[/dim]")))
            
            self._list = ListView(*list_items)
            yield self._list

    def on_mount(self) -> None:
        if self._list:
            self._list.index = 0

    def on_list_view_selected(self, event: ListView.Selected) -> None:  # type: ignore[override]
        index = _resolve_selected_index(event, self._list)
        if 0 <= index < len(self._projects):
            pid = str(self._projects[index].get('project_id') or self._projects[index].get('id') or '')
            self.dismiss(pid or None)
        else:
            self.dismiss(None)

    def on_key(self, event) -> None:  # type: ignore[override]
        if event.key == "escape":
            self.dismiss(None)


class HistorySelectScreen(ModalScreen[Optional[int]]):
    """Select a recent custom run command from history."""
    def __init__(self, entries: List[Dict[str, Any]]):
        super().__init__()
        self._entries = entries
        self._list: ListView | None = None

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("Select a history entry (Enter to run, Esc to cancel)")
            self._list = ListView()
            for i, e in enumerate(self._entries):
                ts = str(e.get("timestamp", ""))
                args = str(e.get("args", ""))
                label = f"[b]{i}.[/b] [dim]{ts}[/dim]\n{args}"
                self._list.append(ListItem(Static(label)))
            yield self._list

    def on_mount(self) -> None:
        if self._list:
            self._list.index = 0

    def on_list_view_selected(self, event: ListView.Selected) -> None:  # type: ignore[override]
        index = _resolve_selected_index(event, self._list)
        if 0 <= index < len(self._entries):
            self.dismiss(index)
        else:
            self.dismiss(None)

    def on_key(self, event) -> None:  # type: ignore[override]
        if event.key == "escape":
            self.dismiss(None)

