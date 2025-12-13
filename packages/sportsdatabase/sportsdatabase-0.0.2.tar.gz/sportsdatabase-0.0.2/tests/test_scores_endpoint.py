from sportsdatabase.endpoints.scores import ScoresEndpoint


class DummyHttp:
    def __init__(self):
        self.calls = []

    def request(self, method, path, **kwargs):
        self.calls.append((method, path, kwargs))
        return {"data": {"eventId": "evt_1"}}


def test_scores_get_by_event_hits_correct_path():
    http = DummyHttp()
    endpoint = ScoresEndpoint(http)

    result = endpoint.get_by_event("evt_1")

    assert result["data"]["eventId"] == "evt_1"
    assert http.calls[0][1] == "/events/evt_1/score"
