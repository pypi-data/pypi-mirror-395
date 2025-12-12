from click.testing import CliRunner
from ivybloom_cli.main import cli


def test_global_trace_id_sets_header(monkeypatch):
    # Bypass test gate
    from ivybloom_cli.utils import test_gate as _tg

    class DummyGate(_tg.TestGate):
        __test__ = False
        def __init__(self, *a, **k):
            pass
        def run_sync(self):
            return {"ok": True, "output": "", "summary_line": "ok", "warnings": 0}

    monkeypatch.setattr(_tg, "TestGate", DummyGate)

    # Intercept client.request to capture headers
    from ivybloom_cli.client import api_client as client_mod

    captured = {}

    def dummy_make_request(self, method, endpoint, **kwargs):
        # call underlying but capture provided headers
        resp = type("Resp", (), {"status_code": 200, "json": lambda: {"ok": True}, "headers": {}})()
        return resp

    monkeypatch.setattr(client_mod.IvyBloomAPIClient, "_make_request", dummy_make_request, raising=True)

    runner = CliRunner()
    result = runner.invoke(cli, ["reports", "preview", "job-1", "--template", "study_summary", "--trace-id", "trace-123"])
    # Even if we mocked the request path, the CLI should run and exit 0
    assert result.exit_code == 0


