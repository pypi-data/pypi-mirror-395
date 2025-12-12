import os

from fastapi.testclient import TestClient

import kl_exec_gateway.server as server


class DummyModelClient:
    """
    Dummy replacement for OpenAIChatClient in server context.
    """

    def __init__(self, model: str = "gpt-4.1-mini", api_key: str | None = None) -> None:
        self.model = model
        self.api_key = api_key

    def complete(self, messages):
        return "ok"


def _reset_server_state() -> None:
    server._api_key = None
    server._kernel = None
    server._event_store = None
    server._session = None


def test_status_not_configured(monkeypatch) -> None:
    _reset_server_state()
    os.environ.pop("OPENAI_API_KEY", None)

    client = TestClient(server.app)

    resp = client.get("/api/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["configured"] is False


def test_chat_flow_with_dummy_model(monkeypatch) -> None:
    _reset_server_state()
    os.environ["OPENAI_API_KEY"] = "dummy-key"

    # Replace OpenAIChatClient in server module with dummy
    monkeypatch.setattr(server, "OpenAIChatClient", DummyModelClient)

    client = TestClient(server.app)

    resp = client.post("/api/chat", json={"message": "hello"})
    assert resp.status_code == 200

    data = resp.json()
    assert data["reply"] == "ok"

    trace = data["trace"]
    assert trace["policy"]["allowed"] is True
    # Check basic trace structure
    assert "trace_id" in trace
    assert "user_message" in trace
    assert "effective_chat_response" in trace
