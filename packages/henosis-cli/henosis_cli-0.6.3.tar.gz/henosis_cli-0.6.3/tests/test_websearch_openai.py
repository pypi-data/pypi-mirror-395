import sys
from pathlib import Path
import json
from typing import Any, Dict, List, Optional

import pytest
from starlette.testclient import TestClient

# Ensure repository root is on sys.path so `import app` works regardless of how pytest is invoked
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from app.main import app
from app.settings import settings


class FakeEvent:
    def __init__(self, typ: str, delta: Optional[str] = None, error: Optional[Dict[str, Any]] = None):
        self.type = typ
        self.delta = delta
        self.error = error


class FakeUsage:
    def __init__(self, input_tokens: int, output_tokens: int, cached_tokens: int = 0):
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.total_tokens = input_tokens + output_tokens
        # OpenAI Responses API exposes input_tokens_details.cached_tokens; emulate attribute access
        class _InputTokensDetails:
            def __init__(self, cached_tokens: int) -> None:
                self.cached_tokens = cached_tokens

        self.input_tokens_details = _InputTokensDetails(cached_tokens)


class FakeWebSearchCall:
    def __init__(self, action: Dict[str, Any]):
        self.type = "web_search_call"
        self.id = "ws_test_1"
        self.status = "completed"
        self.action = action


class FakeFinal:
    def __init__(self, text: str, usage: FakeUsage, output_items: List[Any]):
        self.output_text = text
        self.usage = usage
        self.output = output_items
        self.id = "resp_test_123"


class FakeResponsesStream:
    """Context manager that records request kwargs and yields a simple delta stream."""

    def __init__(self, recorded: List[Dict[str, Any]], kwargs: Dict[str, Any], include_sources: bool):
        self._recorded = recorded
        self._kwargs = kwargs
        self._include_sources = include_sources
        self._final: Optional[FakeFinal] = None
        # Persist the call
        self._recorded.append(dict(kwargs))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def __iter__(self):
        # Yield a single text delta
        yield FakeEvent("response.output_text.delta", delta="hello world")

    # The router calls get_final_response() after the stream
    def get_final_response(self) -> FakeFinal:
        if self._final is None:
            usage = FakeUsage(input_tokens=42, output_tokens=17, cached_tokens=0)
            # Provide a minimal web_search_call output item to simulate tool usage
            sources = []
            if self._include_sources:
                sources = [
                    {"title": "Example", "url": "https://example.com"},
                    {"title": "OpenAI", "url": "https://openai.com"},
                ]
            action = {
                "type": "search",
                "query": "positive news today",
            }
            if sources:
                action["sources"] = sources
            output_items = [FakeWebSearchCall(action=action)]
            self._final = FakeFinal("hello world", usage=usage, output_items=output_items)
        return self._final


class FakeResponses:
    def __init__(self, recorded: List[Dict[str, Any]]):
        self._recorded = recorded

    def stream(self, **kwargs):  # matches client.responses.stream(**request_kwargs)
        include = kwargs.get("include") or []
        include_sources = isinstance(include, list) and ("web_search_call.action.sources" in include)
        return FakeResponsesStream(self._recorded, kwargs, include_sources)


class FakeOpenAI:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self._recorded: List[Dict[str, Any]] = []
        self.responses = FakeResponses(self._recorded)

    # Helper for tests
    @property
    def recorded_calls(self) -> List[Dict[str, Any]]:
        return self._recorded


@pytest.fixture(autouse=True)
def _env_keys(monkeypatch):
    # Ensure provider gates pass
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "sk-test")
    # Enable v0 routes for test client
    monkeypatch.setattr(settings, "DISABLE_V0_ROUTES", False)
    yield


def _post_stream(client: TestClient, payload: Dict[str, Any]) -> List[str]:
    """Helper to collect SSE events from /v0/chat/stream into a list of event names."""
    r = client.post("/v0/chat/stream", json=payload)
    assert r.status_code == 200
    events: List[str] = []
    for line in r.iter_lines():
        s = line.decode("utf-8") if isinstance(line, (bytes, bytearray)) else str(line)
        if s.startswith("event:"):
            events.append(s[len("event:") :].strip())
    return events


def _collect_completed_payload(client: TestClient, payload: Dict[str, Any]) -> Dict[str, Any]:
    r = client.post("/v0/chat/stream", json=payload)
    assert r.status_code == 200
    current_event: Optional[str] = None
    completed: Optional[Dict[str, Any]] = None
    for line in r.iter_lines():
        s = line.decode("utf-8") if isinstance(line, (bytes, bytearray)) else str(line)
        if s.startswith("event:"):
            current_event = s[len("event:") :].strip()
        elif s.startswith("data:"):
            try:
                obj = json.loads(s[len("data:") :].strip())
            except Exception:
                obj = None
            if current_event == "message.completed" and isinstance(obj, dict):
                completed = obj
    assert completed is not None, "Did not receive message.completed payload"
    return completed  # type: ignore


def test_openai_websearch_includes_tool_and_filters_and_location(monkeypatch):
    # Patch OpenAI class used in router to our fake
    recorded_holder: Dict[str, Any] = {}

    def _factory(api_key: Optional[str] = None):
        inst = FakeOpenAI(api_key)
        recorded_holder["inst"] = inst
        return inst

    import app.routers.chat as chat_router

    # Ensure legacy v0 route is mounted for tests regardless of settings at import time
    try:
        app.include_router(chat_router.router, prefix="/v0")
    except Exception:
        pass

    monkeypatch.setattr(chat_router, "OpenAI", _factory)  # type: ignore

    client = TestClient(app)

    payload = {
        "model": "gpt-5",
        "messages": [
            {"role": "user", "content": "What was a positive news story from today?"}
        ],
        # Tools can be off; web search is independent for OpenAI path
        "enable_tools": False,
        "enable_web_search": True,
        # messy domains to test cleaning and de-duplication
        "web_search_allowed_domains": [
            "https://OpenAI.com/",
            "pubmed.ncbi.nlm.nih.gov",
            "openai.com",
        ],
        "web_search_include_sources": True,
        "web_search_user_location": {
            "type": "approximate",
            "country": "US",
            "city": "Seattle",
            "region": "Washington",
        },
    }

    events = _post_stream(client, payload)
    # Ensure basic SSE lifecycle occurred
    assert "session.started" in events
    assert "message.completed" in events

    # Validate captured OpenAI request payload
    fake: FakeOpenAI = recorded_holder["inst"]
    assert fake.recorded_calls, "OpenAI.responses.stream was not called"
    call = fake.recorded_calls[0]
    # tools should contain web_search tool with cleaned filters and user_location
    tools = call.get("tools") or []
    assert any(isinstance(t, dict) and t.get("type") == "web_search" for t in tools), "web_search tool missing"
    web_tool = next(t for t in tools if t.get("type") == "web_search")
    # Filters: allowed_domains should be lowercased, schemes/slashes stripped, de-duped
    filters = web_tool.get("filters") or {}
    allowed = filters.get("allowed_domains") or []
    assert "openai.com" in allowed
    assert "pubmed.ncbi.nlm.nih.gov" in allowed
    # No scheme/trailing slashes
    assert all(not d.startswith("http") for d in allowed)
    # User location should pass through as-is
    ul = web_tool.get("user_location") or {}
    assert ul.get("type") == "approximate"
    assert ul.get("country") == "US"
    assert ul.get("city") == "Seattle"
    assert ul.get("region") == "Washington"
    # include should request sources when asked
    include = call.get("include") or []
    assert "web_search_call.action.sources" in include
    # Validate SSE final payload includes web_search list with sources
    completed_payload = _collect_completed_payload(client, payload)
    assert isinstance(completed_payload.get("web_search"), list)
    ws = completed_payload["web_search"]
    assert ws and isinstance(ws[0], dict)
    action = ws[0].get("action") or {}
    assert action.get("type") == "search"
    assert action.get("query")
    # Since include_sources=True, we expect sources present
    sources = action.get("sources")
    assert isinstance(sources, list) and len(sources) >= 2


def test_openai_websearch_disabled_omits_tool(monkeypatch):
    # Patch OpenAI again
    calls: Dict[str, Any] = {}

    def _factory(api_key: Optional[str] = None):
        inst = FakeOpenAI(api_key)
        calls["inst"] = inst
        return inst

    import app.routers.chat as chat_router

    # Ensure legacy v0 route is mounted for tests
    try:
        app.include_router(chat_router.router, prefix="/v0")
    except Exception:
        pass

    monkeypatch.setattr(chat_router, "OpenAI", _factory)  # type: ignore

    client = TestClient(app)

    payload = {
        "model": "gpt-5",
        "messages": [{"role": "user", "content": "Hello"}],
        "enable_web_search": False,
    }

    events = _post_stream(client, payload)
    assert "session.started" in events
    assert "message.completed" in events

    fake: FakeOpenAI = calls["inst"]
    assert fake.recorded_calls
    call = fake.recorded_calls[0]
    tools = call.get("tools") or []
    # Should not contain web_search when disabled
    assert not any(t.get("type") == "web_search" for t in tools)
