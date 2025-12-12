from click.testing import CliRunner
from ivybloom_cli.main import cli


def test_reports_generate_redirect_capture(monkeypatch):
    # Monkeypatch TestGate to bypass real test run during CLI invocation
    from ivybloom_cli import utils as _utils
    from ivybloom_cli.utils import test_gate as _tg

    class DummyGate(_tg.TestGate):
        __test__ = False
        def __init__(self, *a, **k):
            pass
        def run_sync(self):
            return {"ok": True, "output": "", "summary_line": "ok", "warnings": 0}

    monkeypatch.setattr(_tg, "TestGate", DummyGate)

    # Monkeypatch API client method used by reports command
    from ivybloom_cli.client import api_client as client_mod

    def dummy_reports_get(self, action, *, job_id, template=None, export_type=None, format=None, follow_redirects=True, extra_params=None):
        return {"status_code": 302, "redirect_to": "https://download.test/file.pdf"}

    monkeypatch.setattr(client_mod.IvyBloomAPIClient, "reports_get", dummy_reports_get, raising=True)

    # Also patch post to avoid network
    def dummy_reports_post(self, *a, **k):
        return {"status": "accepted"}

    monkeypatch.setattr(client_mod.IvyBloomAPIClient, "reports_post", dummy_reports_post, raising=True)

    runner = CliRunner()
    result = runner.invoke(cli, ["reports", "generate", "job-1", "--template", "t1", "--format", "pdf", "--no-follow-redirect"])
    assert result.exit_code == 0
    assert "redirect_to" in result.stdout


