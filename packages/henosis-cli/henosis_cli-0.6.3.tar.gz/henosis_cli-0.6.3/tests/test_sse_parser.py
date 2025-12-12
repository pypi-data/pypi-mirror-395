import json
import asyncio


class FakeResp:
    def __init__(self, chunks):
        self._chunks = chunks

    async def aiter_text(self):
        for ch in self._chunks:
            yield ch


def test_parse_sse_lf_separators():
    from cli import parse_sse_lines

    async def _collect():
        # Two events split across chunks with LF separators
        chunks = [
            "event: session.started\n",
            "data: {\"session_id\":\"abc\"}\n\n",
            "event: message.delta\ndata: {\"text\": \"Hello\"}\n\n",
            "event: message.completed\n",
            "data: {\"usage\":{\"prompt_tokens\":1,\"completion_tokens\":1}}\n\n",
        ]
        seen = []
        async for ev, payload in parse_sse_lines(FakeResp(chunks)):
            seen.append((ev, json.loads(payload)))
        return seen

    seen = asyncio.run(_collect())
    assert seen[0][0] == "session.started"
    assert seen[0][1]["session_id"] == "abc"
    assert seen[1][0] == "message.delta"
    assert seen[1][1]["text"] == "Hello"
    assert seen[-1][0] == "message.completed"
    assert seen[-1][1]["usage"]["prompt_tokens"] == 1


def test_parse_sse_crlf_separators_and_multi_data_lines():
    from cli import parse_sse_lines

    async def _collect():
        # One event with two data lines and CRLF separators
        payload_part1 = "{\"a\":1}"
        payload_part2 = "{\"b\":2}"
        chunks = [
            "event: message\r\n",
            f"data: {payload_part1}\r\n",
            f"data: {payload_part2}\r\n\r\n",
        ]
        items = []
        async for ev, payload in parse_sse_lines(FakeResp(chunks)):
            items.append((ev, payload))
        return items, payload_part1, payload_part2

    items, part1, part2 = asyncio.run(_collect())
    # Default event name fallback is 'message' if omitted; here explicitly set to message
    assert items[0][0] == "message"
    # Data lines are joined with a newline between; verify content
    assert part1 in items[0][1] and part2 in items[0][1]
