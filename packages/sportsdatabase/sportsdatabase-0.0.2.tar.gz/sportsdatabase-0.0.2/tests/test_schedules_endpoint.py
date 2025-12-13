from sportsdatabase.endpoints.schedules import SchedulesEndpoint


class DummyHttp:
    def __init__(self):
        self.calls = []

    def request(self, method, path, **kwargs):
        self.calls.append((method, path, kwargs))
        return {"data": [], "meta": {}}


def test_team_next_includes_team_id_and_optional_limit():
    http = DummyHttp()
    endpoint = SchedulesEndpoint(http)

    endpoint.team_next("team_1", limit=5)

    method, path, kwargs = http.calls[0]
    assert path == "/schedule/team/next"
    assert kwargs["params"] == {"teamId": "team_1", "limit": 5}


def test_league_season_passes_required_params():
    http = DummyHttp()
    endpoint = SchedulesEndpoint(http)

    endpoint.league_season("league_1", "2025")

    _, path, kwargs = http.calls[0]
    assert path == "/schedule/by-season"
    assert kwargs["params"] == {"leagueId": "league_1", "season": "2025"}
