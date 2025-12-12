import types
import httpx
import json
from ivybloom_cli.client.api_client import IvyBloomAPIClient
from ivybloom_cli.utils.config import Config
from ivybloom_cli.utils.auth import AuthManager


class DummyAuth(AuthManager):
    def __init__(self):
        pass

    def is_authenticated(self) -> bool:
        return True

    def get_auth_headers(self, prefer_jwt: bool = False):
        return {"Authorization": "Bearer test"}


class DummyConfig(Config):
    def __init__(self):
        self._store = {"timeout": 5}

    def get_frontend_url(self):
        return "https://frontend.test"

    def get(self, key, default=None):
        return self._store.get(key, default)

    def get_or_create_client_id(self):
        return "client-123"


class DummyResponse:
    def __init__(self, status_code=200, json_data=None, text=""):
        self.status_code = status_code
        self._json = json_data
        self.text = text
        self.headers = {}

    def json(self):
        if self._json is None:
            raise json.JSONDecodeError("no json", "", 0)
        return self._json


class DummyClient:
    def __init__(self, base_url, timeout, headers, follow_redirects=False, cookies=None):
        self.base_url = base_url
        self.timeout = timeout
        self.headers = dict(headers)
        self.follow_redirects = follow_redirects
        self.cookies = cookies or {}
        self._next = []

    def queue(self, response: DummyResponse):
        self._next.append(response)

    def request(self, method, path, **kwargs):
        # capture headers if provided
        headers = kwargs.get("headers")
        if headers:
            # update last headers used for assertion
            self.last_headers = dict(headers)
        # support redirect capture path
        if self._next:
            return self._next.pop(0)
        return DummyResponse(200, {"ok": True})

    def close(self):
        pass


def test_reports_post_includes_idempotency_headers(monkeypatch):
    dummy_http = types.SimpleNamespace()

    temp_client = DummyClient("https://frontend.test", 5, {"h": "v"})
    dummy_http.Client = lambda **kwargs: temp_client

    monkeypatch.setattr(httpx, "Client", dummy_http.Client)

    cfg = DummyConfig()
    auth = DummyAuth()
    client = IvyBloomAPIClient(cfg, auth)

    temp_client.queue(DummyResponse(202, {"status": "accepted"}))
    out = client.reports_post("generate", job_id="job-1", template="t1", format="pdf", idempotency_key="k1")
    assert out.get("status") == "accepted"
    # ensure header variants are present when provided
    assert temp_client.last_headers.get("Idempotency-Key") == "k1"
    assert temp_client.last_headers.get("x-idempotency-key") == "k1"


def test_reports_get_redirect_capture(monkeypatch):
    # Simulate a 302 redirect when follow_redirects=False
    temp_client = DummyClient("https://frontend.test", 5, {"h": "v"}, follow_redirects=False)

    def mkclient(**kwargs):
        # return a fresh dummy client each call for isolation
        return temp_client

    monkeypatch.setattr(httpx, "Client", mkclient)

    cfg = DummyConfig()
    auth = DummyAuth()
    client = IvyBloomAPIClient(cfg, auth)

    resp = DummyResponse(302, None, "")
    resp.headers["location"] = "https://download.test/file.pdf"
    temp_client.queue(resp)

    out = client.reports_get("generate", job_id="job-1", template="t1", format="pdf", follow_redirects=False)
    assert out.get("status_code") == 302
    assert out.get("redirect_to") == "https://download.test/file.pdf"


