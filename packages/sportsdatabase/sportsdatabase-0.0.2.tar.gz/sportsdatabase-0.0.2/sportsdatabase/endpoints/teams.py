from __future__ import annotations

from typing import Any, Dict

from ..http import HttpClient


class TeamsEndpoint:
    def __init__(self, http: HttpClient):
        self._http = http

    def list(
        self,
        *,
        league_id: str,
        season: str | None = None,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> Dict[str, Any]:
        params = _clean({"season": season, "cursor": cursor, "limit": limit})
        return self._http.request("GET", f"/leagues/{league_id}/teams", params=params)

    def get_by_id(self, team_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"/teams/{team_id}")


def _clean(params: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in params.items() if v is not None}
