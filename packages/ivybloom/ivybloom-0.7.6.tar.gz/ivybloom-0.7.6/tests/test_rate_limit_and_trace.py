import types
import httpx
import json
import time
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
        self._store = {"timeout": 5, "rate_limit_retries": 2, "rate_limit_backoff_base": 0.01, "debug": False}
    def get_frontend_url(self):
        return "https://frontend.test"
    def get(self, key, default=None):
        return self._store.get(key, default)
    def get_or_create_client_id(self):
        return "client-123"


class DummyResponse:
    def __init__(self, status_code=200, json_data=None, text="", headers=None):
        self.status_code = status_code
        self._json = json_data
        self.text = text
        self.headers = headers or {}
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
        self.calls = []
        self._queue = []
        self.last_headers = None
    def queue(self, response: DummyResponse):
        self._queue.append(response)
    def request(self, method, path, **kwargs):
        # capture headers to inspect trace id
        self.last_headers = dict(kwargs.get("headers") or {})
        self.calls.append((method, path))
        if self._queue:
            return self._queue.pop(0)
        return DummyResponse(200, {"ok": True})
    def close(self):
        pass


def test_rate_limit_backoff_and_trace_header(monkeypatch):
    # Install dummy client
    temp_client = DummyClient("https://frontend.test", 5, {"h": "v"})
    monkeypatch.setattr(httpx, "Client", lambda **kwargs: temp_client)

    cfg = DummyConfig()
    auth = DummyAuth()
    client = IvyBloomAPIClient(cfg, auth)

    # Queue: 429 with Retry-After 0.01, then success
    temp_client.queue(DummyResponse(429, None, "", headers={"Retry-After": "0.01"}))
    temp_client.queue(DummyResponse(200, {"ok": True}))

    t0 = time.time()
    resp = client.get("/api/ping")
    dt = time.time() - t0
    # should be >= retry-after, but allow small timing variance
    assert dt >= 0.008
    assert isinstance(resp, dict) and resp.get("ok") is True
    # Verify x-trace-id is attached on each request
    assert "x-trace-id" in temp_client.last_headers


