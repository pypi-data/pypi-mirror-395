from __future__ import annotations

import pytest

from ivybloom_cli.tui.app import IvyBloomTUI
from ivybloom_cli.utils.auth import AuthManager
from ivybloom_cli.utils.config import Config


def _make_app(monkeypatch: pytest.MonkeyPatch) -> IvyBloomTUI:
    config = Config()
    auth = AuthManager(config)
    app = IvyBloomTUI(config, auth, show_header=False, show_footer=False)
    # Avoid UI side effects during isolated unit tests
    monkeypatch.setattr(app, "_update_status_bar", lambda: None)
    monkeypatch.setattr(app, "_debug", lambda *args, **kwargs: None)
    return app


def test_probe_connectivity_success(monkeypatch: pytest.MonkeyPatch) -> None:
    app = _make_app(monkeypatch)
    monkeypatch.setattr(app, "_run_cli_text", lambda args, timeout=5, input_text=None: "ok")
    app._connected = False
    app._probe_connectivity()
    assert app._connected is True


def test_probe_connectivity_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    app = _make_app(monkeypatch)

    def _raise(*args, **kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr(app, "_run_cli_text", _raise)
    app._connected = True
    app._probe_connectivity()
    assert app._connected is False


def test_start_boot_sequence_runs_healthcheck_and_schedules_continue(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = _make_app(monkeypatch)
    called: dict[str, object] = {"probe": 0, "continued": 0}

    def _probe():
        called["probe"] = called["probe"] + 1

    def _continue():
        called["continued"] = called["continued"] + 1

    def _set_timer(delay: float, fn):
        called["delay"] = delay
        called["fn"] = fn
        return "timer"

    monkeypatch.setattr(app, "_probe_connectivity", _probe)
    monkeypatch.setattr(app, "_continue_boot_sequence", _continue)
    monkeypatch.setattr(app, "set_timer", _set_timer)

    app._start_boot_sequence()

    assert called["probe"] == 1
    assert called.get("delay") == 0.2
    assert callable(called.get("fn"))

    # Invoke the scheduled callback to ensure continuation is wired
    fn = called.get("fn")
    assert fn is not None
    fn()  # type: ignore[operator]
    assert called["continued"] == 1

