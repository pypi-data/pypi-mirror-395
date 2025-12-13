from __future__ import annotations

import httpx
import pytest

from sportsdatabase.config import ClientConfig
from sportsdatabase.errors import RateLimitError
from sportsdatabase.http import HttpClient


class StubHttpxClient:
    def __init__(self, responses: list[httpx.Response]):
        self._responses = iter(responses)

    def request(self, *args, **kwargs):
        try:
            return next(self._responses)
        except StopIteration:
            raise AssertionError("No more responses configured")

    def close(self):
        pass


def _make_response(status: int, json_data: dict, headers: dict[str, str] | None = None) -> httpx.Response:
    request = httpx.Request("GET", "https://api.test/events")
    return httpx.Response(status_code=status, json=json_data, headers=headers, request=request)


def _build_client() -> HttpClient:
    config = ClientConfig(api_key="test", base_url="https://api.test")
    client = HttpClient(config)
    client._client.close()  # type: ignore[attr-defined]
    return client


def test_http_client_enriches_rate_limit_metadata():
    response_headers = {
        "x-ratelimit-limit": "100",
        "x-ratelimit-remaining": "95",
        "x-ratelimit-reset": "12",
        "x-request-id": "req_123",
    }
    response = _make_response(200, {"data": [], "meta": {}}, response_headers)

    client = _build_client()
    client._client = StubHttpxClient([response])  # type: ignore[attr-defined]

    payload = client.request("GET", "/events")

    assert payload["meta"]["rateLimit"] == {
        "limit": "100",
        "remaining": "95",
        "reset": "12",
    }
    assert payload["meta"]["requestId"] == "req_123"


def test_http_client_raises_rate_limit_error_after_retries(monkeypatch):
    response_headers = {"x-ratelimit-reset": "42"}
    rate_limited = _make_response(429, {"error": {"message": "Too many"}}, response_headers)

    client = _build_client()
    # Provide responses for initial try plus two retries (max_retries=2)
    client._client = StubHttpxClient([rate_limited, rate_limited, rate_limited])  # type: ignore[attr-defined]

    monkeypatch.setattr("sportsdatabase.http.time.sleep", lambda *_args, **_kwargs: None)

    with pytest.raises(RateLimitError) as excinfo:
        client.request("GET", "/events")

    assert excinfo.value.reset_at == 42.0
