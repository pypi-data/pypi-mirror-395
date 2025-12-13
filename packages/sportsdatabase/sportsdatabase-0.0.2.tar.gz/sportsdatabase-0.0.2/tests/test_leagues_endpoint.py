from sportsdatabase.endpoints.leagues import LeaguesEndpoint


class DummyHttp:
    def __init__(self):
        self.calls = []

    def request(self, method, path, **kwargs):
        self.calls.append((method, path, kwargs))
        return {"data": [], "meta": {}}


def test_leagues_list_filters_none_values():
    http = DummyHttp()
    endpoint = LeaguesEndpoint(http)

    endpoint.list(sport_slug="soccer", status=None, limit=25)

    method, path, kwargs = http.calls[0]
    assert method == "GET"
    assert path == "/leagues"
    assert kwargs["params"] == {"sportSlug": "soccer", "limit": 25}


def test_leagues_get_by_id_calls_detail_endpoint():
    http = DummyHttp()
    endpoint = LeaguesEndpoint(http)

    endpoint.get_by_id("league_1")

    assert http.calls[0][1] == "/leagues/league_1"
