from __future__ import annotations

from typing import Any, Dict

from ..http import HttpClient


class ScoresEndpoint:
    def __init__(self, http: HttpClient):
        self._http = http

    def get_by_event(self, event_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"/events/{event_id}/score")
