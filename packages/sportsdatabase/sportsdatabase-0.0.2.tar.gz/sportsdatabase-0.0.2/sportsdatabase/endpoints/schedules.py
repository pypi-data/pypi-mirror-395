from __future__ import annotations

from typing import Any, Dict

from ..http import HttpClient


class SchedulesEndpoint:
    def __init__(self, http: HttpClient):
        self._http = http

    def team_next(self, team_id: str, *, limit: int | None = None) -> Dict[str, Any]:
        return self._http.request("GET", "/schedule/team/next", params=_clean({"teamId": team_id, "limit": limit}))

    def team_previous(self, team_id: str, *, limit: int | None = None) -> Dict[str, Any]:
        return self._http.request("GET", "/schedule/team/previous", params=_clean({"teamId": team_id, "limit": limit}))

    def league_next(self, league_id: str, *, season: str | None = None, limit: int | None = None) -> Dict[str, Any]:
        return self._http.request(
            "GET", "/schedule/league/next", params=_clean({"leagueId": league_id, "season": season, "limit": limit})
        )

    def league_previous(self, league_id: str, *, season: str | None = None, limit: int | None = None) -> Dict[str, Any]:
        return self._http.request(
            "GET",
            "/schedule/league/previous",
            params=_clean({"leagueId": league_id, "season": season, "limit": limit}),
        )

    def league_season(self, league_id: str, season: str) -> Dict[str, Any]:
        return self._http.request("GET", "/schedule/by-season", params={"leagueId": league_id, "season": season})

    def by_day(self, date: str, *, sport_id: str | None = None, league_id: str | None = None) -> Dict[str, Any]:
        return self._http.request(
            "GET", "/schedule/by-day", params=_clean({"date": date, "sportId": sport_id, "leagueId": league_id})
        )


def _clean(params: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in params.items() if v is not None}
