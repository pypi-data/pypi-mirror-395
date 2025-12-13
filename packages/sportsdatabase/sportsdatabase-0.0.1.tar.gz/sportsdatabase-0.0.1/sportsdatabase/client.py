from __future__ import annotations

from .config import ClientConfig
from .http import HttpClient
from .endpoints.events import EventsEndpoint
from .endpoints.leagues import LeaguesEndpoint
from .endpoints.teams import TeamsEndpoint
from .endpoints.schedules import SchedulesEndpoint
from .endpoints.scores import ScoresEndpoint


class SportsDatabaseClient:
    def __init__(self, *, api_key: str, base_url: str | None = None, timeout: float | None = None, max_retries: int | None = None, user_agent_suffix: str = ""):
        config = ClientConfig(
            api_key=api_key,
            base_url=base_url or ClientConfig.base_url,
            timeout=timeout or ClientConfig.timeout,
            max_retries=max_retries or ClientConfig.max_retries,
            user_agent_suffix=user_agent_suffix,
        )
        self._http = HttpClient(config)
        self.events = EventsEndpoint(self._http)
        self.leagues = LeaguesEndpoint(self._http)
        self.teams = TeamsEndpoint(self._http)
        self.schedules = SchedulesEndpoint(self._http)
        self.scores = ScoresEndpoint(self._http)

    def close(self) -> None:
        self._http.close()
