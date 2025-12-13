from sportsdatabase.client import SportsDatabaseClient
from sportsdatabase.endpoints.events import EventsEndpoint


class DummyHttp:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def request(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        return self.response


def test_events_list_makes_request():
    client = SportsDatabaseClient(api_key="test")
    dummy = DummyHttp({"data": []})
    client.events = EventsEndpoint(dummy)  # type: ignore[arg-type]

    result = client.events.list(sport="soccer")

    assert result == {"data": []}
    assert dummy.calls
