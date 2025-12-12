import json
from typing import Any, Dict

import pytest

from streamstraight_server.jwt_token import StreamstraightTokenError, fetch_client_token


class DummyResponse:
    def __init__(self, status_code: int, body: Dict[str, Any] | None = None):
        self.status_code = status_code
        self._body = body or {}

    @property
    def is_success(self) -> bool:  # type: ignore[override]
        return 200 <= self.status_code < 300

    def json(self) -> Dict[str, Any]:
        return self._body

    @property
    def text(self) -> str:  # type: ignore[override]
        return json.dumps(self._body)


class DummyClient:
    def __init__(self, response: DummyResponse):
        self._response = response
        self.post_args: Dict[str, Any] | None = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def post(self, url: str, headers, timeout: float):
        self.post_args = {"url": url, "headers": headers, "timeout": timeout}
        return self._response


@pytest.mark.asyncio
async def test_fetch_client_token_success(monkeypatch):
    response = DummyResponse(200, {"token": "abc123"})
    client = DummyClient(response)
    monkeypatch.setattr("httpx.AsyncClient", lambda: client)

    token = await fetch_client_token({"api_key": "key"})

    assert token == "abc123"
    assert client.post_args is not None
    assert client.post_args["headers"]["Authorization"] == "Bearer key"


@pytest.mark.asyncio
async def test_fetch_client_token_failure(monkeypatch):
    response = DummyResponse(500, {"error": "bad"})
    client = DummyClient(response)
    monkeypatch.setattr("httpx.AsyncClient", lambda: client)

    with pytest.raises(StreamstraightTokenError):
        await fetch_client_token({"api_key": "key"})


@pytest.mark.asyncio
async def test_fetch_client_token_requires_api_key():
    with pytest.raises(ValueError):
        await fetch_client_token({})
