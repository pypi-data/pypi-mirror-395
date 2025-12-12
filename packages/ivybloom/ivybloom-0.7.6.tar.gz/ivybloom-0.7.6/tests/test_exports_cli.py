from click.testing import CliRunner
from ivybloom_cli.main import cli


def test_exports_create(monkeypatch):
    # Bypass test gate
    from ivybloom_cli.utils import test_gate as _tg

    class DummyGate(_tg.TestGate):
        __test__ = False
        def __init__(self, *a, **k):
            pass
        def run_sync(self):
            return {"ok": True, "output": "", "summary_line": "ok", "warnings": 0}

    monkeypatch.setattr(_tg, "TestGate", DummyGate)

    # Mock API client methods
    from ivybloom_cli.client import api_client as client_mod

    def dummy_create_export(self, spec, idempotency_key=None):
        return {"export_id": "exp_123", "status": "queued", "accepted_items": spec.get("include", [])}

    monkeypatch.setattr(client_mod.IvyBloomAPIClient, "create_export", dummy_create_export, raising=True)

    runner = CliRunner()
    result = runner.invoke(cli, [
        "exports", "create",
        "--type", "project_summary",
        "--scope", '{"project_id":"proj_1"}',
        "--include", "jobs_table,metrics_overview",
        "--format", "zip",
        "--idempotency-key", "k-1",
    ])
    assert result.exit_code == 0
    assert "exp_123" in result.stdout


