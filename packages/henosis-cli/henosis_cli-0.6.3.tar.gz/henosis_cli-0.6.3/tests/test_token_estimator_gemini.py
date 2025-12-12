import os
import math
import pytest

try:
    from google import genai as _genai
    HAS_GENAI = True
except Exception:
    HAS_GENAI = False

from cli import ChatCLI


pytestmark = pytest.mark.skipif(
    not HAS_GENAI or not (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")),
    reason="Gemini SDK or API key not available; set GEMINI_API_KEY or GOOGLE_API_KEY to run token estimator tests.",
)


def _count_tokens_with_gemini(contents: list[dict], model: str = "gemini-2.5-pro") -> int:
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    client = _genai.Client(api_key=api_key)
    res = client.models.count_tokens(model=model, contents=contents)
    return int(getattr(res, "total_tokens", 0) or 0)


def _to_gemini_contents(messages: list[dict]) -> list[dict]:
    """Convert ChatCLI-style messages into Gemini SDK contents for counting."""
    contents: list[dict] = []
    for m in messages:
        role = m.get("role", "user")
        text = m.get("content", "") or ""
        contents.append({"role": role, "parts": [{"text": text}]})
    return contents


def _fallback_estimate_tokens(messages: list[dict]) -> int:
    total_chars = 0
    for m in messages:
        total_chars += len(m.get("content", "") or "")
    return max(1, int(round(total_chars / 4.0)))


def test_fallback_estimate_within_reason_of_gemini():
    cli = ChatCLI(
        server=os.getenv("HENOSIS_SERVER", "https://henosis.us/api_v2"),
        model=None,
        system_prompt="You are helpful.",
        timeout=5.0,
        map_prefix=False,
        log_enabled=False,
        save_to_threads=False,
        server_usage_commit=False,
        verbose=False,
    )
    user_input = (
        "Summarize this input in 3 bullet points and include a final one-line takeaway.\n" * 5
    )
    msgs = cli._build_messages(user_input)
    contents = _to_gemini_contents(msgs)
    gem_tokens = _count_tokens_with_gemini(contents)
    fb_tokens = _fallback_estimate_tokens(msgs)
    # Accept fairly generous tolerance because char/token varies by language and content
    # Require within +/- 35% relative difference
    rel = abs(gem_tokens - fb_tokens) / max(1, gem_tokens)
    assert rel <= 0.35, f"fallback estimate off by {rel*100:.1f}% (gemini={gem_tokens}, fallback={fb_tokens})"


def test_code_map_injection_only_first_turn_changes_token_count():
    cli = ChatCLI(
        server=os.getenv("HENOSIS_SERVER", "https://henosis.us/api_v2"),
        model=None,
        system_prompt=None,
        timeout=5.0,
        map_prefix=True,
        log_enabled=False,
        save_to_threads=False,
        server_usage_commit=False,
        verbose=False,
    )
    # Inject a known map payload
    cli._codebase_map_raw = ("# MAP\n" + ("A" * 1500) + "\n- file: x.py\n- dir: y\n")
    cli._did_inject_codebase_map = False

    # First turn: map should be prefixed
    msgs1 = cli._build_messages("First question?")
    contents1 = _to_gemini_contents(msgs1)
    t1 = _count_tokens_with_gemini(contents1)

    # Second turn: map should NOT be injected again
    msgs2 = cli._build_messages("Second question?")
    contents2 = _to_gemini_contents(msgs2)
    t2 = _count_tokens_with_gemini(contents2)

    # Pure map token count (approx) for reference
    map_contents = _to_gemini_contents([{ "role": "user", "content": cli._codebase_map_raw }])
    map_tokens = _count_tokens_with_gemini(map_contents)

    # First turn should be significantly larger than second due to prefixed map
    assert t1 > t2, f"Expected first-turn tokens > second-turn tokens (got {t1} <= {t2})"
    # Difference should be within reasonable range of the map size (allowing for prompt framing)
    diff = t1 - t2
    # Accept +/- 30% tolerance vs pure map size
    rel = abs(diff - map_tokens) / max(1, map_tokens)
    assert rel <= 0.30, f"Map injection delta off by {rel*100:.1f}% (delta={diff}, map={map_tokens})"
