from __future__ import annotations

import time
from typing import Any, Dict, Optional

import httpx

from .config import ClientConfig
from .errors import ApiError, NetworkError, RateLimitError


class HttpClient:
    def __init__(self, config: ClientConfig):
        self._config = config
        self._client = httpx.Client(
            base_url=config.base_url.rstrip("/"),
            headers={
                "User-Agent": self._build_user_agent(),
                "X-API-Key": config.api_key,
                "Accept": "application/json",
            },
            timeout=config.timeout,
        )

    def _build_user_agent(self) -> str:
        base = "SportsDatabasePythonSDK/0.0.1"
        return f"{base} {self._config.user_agent_suffix}".strip()

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Any = None,
    ) -> Dict[str, Any]:
        url = f"/{path.lstrip('/')}"
        retries = 0

        while True:
            try:
                response = self._client.request(method, url, params=params, json=json)
            except httpx.HTTPError as exc:
                if retries < self._config.max_retries:
                    retries += 1
                    time.sleep(0.3 * (2 ** (retries - 1)))
                    continue
                raise NetworkError("Network request failed") from exc

            if response.status_code == 429 and retries < self._config.max_retries:
                retries += 1
                time.sleep(0.5 * (2 ** (retries - 1)))
                continue

            if response.status_code >= 400:
                self._raise_for_status(response)

            payload_obj = response.json()
            if not isinstance(payload_obj, dict):
                raise ApiError("Unexpected response format", status=response.status_code)
            payload: Dict[str, Any] = payload_obj
            payload.setdefault("meta", {})
            payload["meta"]["rateLimit"] = {
                "limit": response.headers.get("x-ratelimit-limit"),
                "remaining": response.headers.get("x-ratelimit-remaining"),
                "reset": response.headers.get("x-ratelimit-reset"),
            }
            payload["meta"]["requestId"] = response.headers.get("x-request-id")
            return payload

    def close(self) -> None:
        self._client.close()

    def _raise_for_status(self, response: httpx.Response) -> None:
        data = None
        try:
            data = response.json()
        except ValueError:
            pass

        message = data.get("error", {}).get("message") if isinstance(data, dict) else None
        message = message or response.text or response.reason_phrase

        if response.status_code == 429:
            reset = response.headers.get("x-ratelimit-reset")
            raise RateLimitError(message, status=429, reset_at=float(reset) if reset else None, details=data or {})

        raise ApiError(message, status=response.status_code, code=(data or {}).get("error", {}).get("code"), details=data or {})
