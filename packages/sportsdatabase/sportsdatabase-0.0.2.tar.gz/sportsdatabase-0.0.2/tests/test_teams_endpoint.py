import pytest

from sportsdatabase.endpoints.teams import TeamsEndpoint


class DummyHttp:
    def __init__(self):
        self.calls = []

    def request(self, method, path, **kwargs):
        self.calls.append((method, path, kwargs))
        return {"data": [], "meta": {}}


def test_teams_list_requires_league_id():
    http = DummyHttp()
    endpoint = TeamsEndpoint(http)

    endpoint.list(league_id="league_1", season="2024", limit=10)

    method, path, kwargs = http.calls[0]
    assert method == "GET"
    assert path == "/leagues/league_1/teams"
    assert kwargs["params"] == {"season": "2024", "limit": 10}


def test_teams_get_by_id_hits_team_endpoint():
    http = DummyHttp()
    endpoint = TeamsEndpoint(http)

    endpoint.get_by_id("team_1")

    assert http.calls[0][1] == "/teams/team_1"
