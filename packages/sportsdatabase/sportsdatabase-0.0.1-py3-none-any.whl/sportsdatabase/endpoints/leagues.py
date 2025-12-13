from __future__ import annotations

from typing import Any, Dict

from ..http import HttpClient


class LeaguesEndpoint:
    def __init__(self, http: HttpClient):
        self._http = http

    def list(
        self,
        *,
        sport_id: str | None = None,
        sport_slug: str | None = None,
        status: str | None = None,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> Dict[str, Any]:
        params = _clean(
            {
                "sportId": sport_id,
                "sportSlug": sport_slug,
                "status": status,
                "cursor": cursor,
                "limit": limit,
            }
        )
        return self._http.request("GET", "/leagues", params=params)

    def get_by_id(self, league_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"/leagues/{league_id}")


def _clean(params: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in params.items() if v is not None}
