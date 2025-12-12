from click.testing import CliRunner
from ivybloom_cli.main import cli


def test_reports_export_post_then_get_flows(monkeypatch):
    # Bypass test gate
    from ivybloom_cli.utils import test_gate as _tg

    class DummyGate(_tg.TestGate):
        __test__ = False
        def __init__(self, *a, **k):
            pass
        def run_sync(self):
            return {"ok": True, "output": "", "summary_line": "ok", "warnings": 0}

    monkeypatch.setattr(_tg, "TestGate", DummyGate)

    # Mock API client
    from ivybloom_cli.client import api_client as client_mod

    def dummy_reports_post(self, action, *, job_id, template=None, export_type=None, format=None, extra_params=None, idempotency_key=None):
        assert action == "export"
        return {"status": "accepted"}

    def dummy_reports_get_no_follow(self, action, *, job_id, template=None, export_type=None, format=None, follow_redirects=True, extra_params=None):
        assert action == "export"
        if follow_redirects:
            return {"data": "followed"}
        return {"status_code": 302, "redirect_to": "https://download.test/bundle.zip"}

    monkeypatch.setattr(client_mod.IvyBloomAPIClient, "reports_post", dummy_reports_post, raising=True)
    monkeypatch.setattr(client_mod.IvyBloomAPIClient, "reports_get", dummy_reports_get_no_follow, raising=True)

    runner = CliRunner()
    # Case 1: POST then GET with follow redirects (default)
    result1 = runner.invoke(cli, ["reports", "export", "job-1", "--type", "package_zip", "--async"])
    assert result1.exit_code == 0
    assert "followed" in result1.stdout

    # Case 2: POST then GET without following redirects
    result2 = runner.invoke(cli, ["reports", "export", "job-1", "--type", "package_zip", "--async", "--no-follow-redirect"])
    assert result2.exit_code == 0
    assert "redirect_to" in result2.stdout


