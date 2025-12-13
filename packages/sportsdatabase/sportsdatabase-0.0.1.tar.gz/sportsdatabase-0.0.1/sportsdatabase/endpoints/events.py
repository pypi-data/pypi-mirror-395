from __future__ import annotations

from typing import Any, Dict, Optional

from ..http import HttpClient


class EventsEndpoint:
    def __init__(self, http: HttpClient):
        self._http = http

    def list(self, *, sport: str | None = None, league: str | None = None, date: str | None = None, status: str | None = None, cursor: str | None = None, limit: int | None = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "sport": sport,
            "league": league,
            "date": date,
            "status": status,
            "cursor": cursor,
            "limit": limit,
        }
        return self._http.request("GET", "/events", params=_clean(params))

    def get_by_id(self, event_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"/events/{event_id}")

    def get_by_date(self, *, date: str, sport: Optional[str] = None, league: Optional[str] = None) -> Dict[str, Any]:
        params = _clean({"sport": sport, "league": league})
        return self._http.request("GET", f"/events/date/{date}", params=params)


def _clean(params: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in params.items() if v is not None}
