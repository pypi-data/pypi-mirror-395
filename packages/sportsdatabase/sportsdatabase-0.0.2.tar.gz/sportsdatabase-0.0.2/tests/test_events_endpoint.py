from sportsdatabase.endpoints.events import EventsEndpoint


class DummyHttp:
    def __init__(self):
        self.calls = []

    def request(self, method, path, **kwargs):
        self.calls.append((method, path, kwargs))
        return {"data": [], "meta": {}}


def test_events_list_filters_none_parameters():
    http = DummyHttp()
    endpoint = EventsEndpoint(http)

    endpoint.list(sport="soccer", league=None, limit=50)

    method, path, kwargs = http.calls[0]
    assert method == "GET"
    assert path == "/events"
    assert kwargs["params"] == {"sport": "soccer", "limit": 50}


def test_events_get_by_date_passes_partial_params():
    http = DummyHttp()
    endpoint = EventsEndpoint(http)

    endpoint.get_by_date(date="2025-01-01", sport="soccer")

    _, path, kwargs = http.calls[0]
    assert path == "/events/date/2025-01-01"
    assert kwargs["params"] == {"sport": "soccer"}
