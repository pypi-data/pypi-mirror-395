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
        headers = kwargs.get("headers")
        if headers:
            self.last_headers = dict(headers)
        if self._next:
            return self._next.pop(0)
        return DummyResponse(200, {"ok": True})

    def close(self):
        pass


def test_create_export_sends_idempotency(monkeypatch):
    temp_client = DummyClient("https://frontend.test", 5, {"h": "v"})
    monkeypatch.setattr(httpx, "Client", lambda **kwargs: temp_client)

    cfg = DummyConfig()
    auth = DummyAuth()
    client = IvyBloomAPIClient(cfg, auth)

    temp_client.queue(DummyResponse(202, {"export_id": "exp_1", "status": "queued"}))
    out = client.create_export({"export_type": "project_summary"}, idempotency_key="key-1")
    assert out["export_id"] == "exp_1"
    assert temp_client.last_headers.get("Idempotency-Key") == "key-1"
    assert temp_client.last_headers.get("x-idempotency-key") == "key-1"


def test_export_status_and_results(monkeypatch):
    temp_client = DummyClient("https://frontend.test", 5, {"h": "v"})
    monkeypatch.setattr(httpx, "Client", lambda **kwargs: temp_client)

    cfg = DummyConfig()
    auth = DummyAuth()
    client = IvyBloomAPIClient(cfg, auth)

    temp_client.queue(DummyResponse(200, {"export_id": "exp_1", "status": "processing"}))
    status = client.get_export_status("exp_1")
    assert status["status"] == "processing"

    temp_client.queue(DummyResponse(200, {"export_id": "exp_1", "status": "completed", "result_urls": []}))
    results = client.get_export_results("exp_1")
    assert results["status"] == "completed"


