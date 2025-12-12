from __future__ import annotations

from ivybloom_cli.tui.status import update_status_bar


class _DummyBar:
    def __init__(self) -> None:
        self.text: str = ""

    def update(self, text: str) -> None:
        self.text = text


class _DummyApp:
    def __init__(self) -> None:
        self.status_bar = _DummyBar()
        self._connected = True
        self._pulse_step = 2
        self._last_error = "boom"
        self._project_name = "proj-1"
        self._user_display = "user@example.com"
        self._current_refresh_interval = 12
        self._last_refresh_latency_ms = 123
        self._last_refresh_at = "12:00:00"


def test_status_bar_includes_refresh_and_error_info() -> None:
    app = _DummyApp()
    update_status_bar(app)
    text = app.status_bar.text
    assert "refresh: 12s / 123ms / 12:00:00" in text
    assert "errors: 1" in text
    assert "proj-1" in text

