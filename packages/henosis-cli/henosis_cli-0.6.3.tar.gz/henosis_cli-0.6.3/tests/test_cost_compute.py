import os
import math
import pytest

from cli import ChatCLI


def make_cli(model: str | None = None) -> ChatCLI:
    # Minimal CLI with no network calls exercised in these tests
    return ChatCLI(
        server=os.getenv("HENOSIS_SERVER", "https://henosis.us/api_v2"),
        model=model,
        system_prompt=None,
        timeout=5.0,
        map_prefix=False,
        log_enabled=False,
        save_to_threads=False,
        server_usage_commit=False,
        verbose=False,
    )


def approx(a: float, b: float, rel: float = 1e-9, abs_tol: float = 1e-9) -> bool:
    return math.isclose(float(a), float(b), rel_tol=rel, abs_tol=abs_tol)


def test_openai_prompt_cache_cost_split():
    cli = make_cli()
    model = "gpt-5"
    usage = {
        "prompt_tokens": 1000,
        "completion_tokens": 500,
        "input_tokens_details": {"cached_tokens": 600},
    }
    # Pricing table in cli.py: gpt-5 input=$1.75/m, output=$14/m
    in_rate = 1.75
    out_rate = 14.0
    non_cached = 400
    cached = 600
    expected = (non_cached / 1_000_000) * in_rate
    expected += (cached / 1_000_000) * (in_rate * 0.10)
    expected += (500 / 1_000_000) * out_rate
    got = cli.compute_cost_usd(model, usage)
    assert approx(got, expected, rel=1e-12, abs_tol=1e-12)


def test_anthropic_image_tokens_count_as_input():
    cli = make_cli()
    model = "claude-sonnet-4-20250514"
    usage = {
        "prompt_tokens": 1000,
        "completion_tokens": 400,
        "image_tokens": 200,
    }
    # Pricing table in cli.py: input=$4.20/m, output=$21/m
    in_rate = 4.20
    out_rate = 21.0
    # image tokens added to prompt side
    expected = ((1000 + 200) / 1_000_000) * in_rate + (400 / 1_000_000) * out_rate
    got = cli.compute_cost_usd(model, usage)
    assert approx(got, expected, rel=1e-12, abs_tol=1e-12)


def test_reasoning_gap_billed_as_output_when_total_exceeds_sum():
    cli = make_cli()
    model = "gpt-5"
    usage = {
        "prompt_tokens": 1000,
        "completion_tokens": 400,
        "total_tokens": 1700,  # gap of 300 (think/reasoning, etc.)
    }
    in_rate = 1.75
    out_rate = 14.0
    gap = 1700 - (1000 + 400)
    expected = (1000 / 1_000_000) * in_rate + ((400 + gap) / 1_000_000) * out_rate
    got = cli.compute_cost_usd(model, usage)
    assert approx(got, expected, rel=1e-12, abs_tol=1e-12)


def test_deepseek_cache_pricing_path():
    cli = make_cli()
    model = "deepseek-chat"
    usage = {
        "prompt_cache_hit_tokens": 300,
        "prompt_cache_miss_tokens": 700,
        "completion_tokens": 200,
    }
    # deepseek-chat pricing (cli.py): input=$0.196/m, output=$0.392/m, cache_hit=$0.014/m
    in_rate = 0.196
    out_rate = 0.392
    cache_hit_rate = 0.014
    expected = (300 / 1_000_000) * cache_hit_rate
    expected += (700 / 1_000_000) * in_rate
    expected += (200 / 1_000_000) * out_rate
    got = cli.compute_cost_usd(model, usage)
    assert approx(got, expected, rel=1e-12, abs_tol=1e-12)


def test_openai_cached_tokens_do_not_exceed_prompt_tokens():
    """Guardrail: if server reports more cached tokens than prompt tokens, clamp to prompt size.
    This prevents negative non-cached math and over/under-billing.
    """
    cli = make_cli()
    model = "gpt-5"
    usage = {
        "prompt_tokens": 150,
        "completion_tokens": 50,
        "input_tokens_details": {"cached_tokens": 1000},  # nonsensical; will be clamped to 150
    }
    in_rate = 1.75
    out_rate = 14.0
    non_cached = 0
    cached = 150
    expected = (non_cached / 1_000_000) * in_rate
    expected += (cached / 1_000_000) * (in_rate * 0.10)
    expected += (50 / 1_000_000) * out_rate
    got = cli.compute_cost_usd(model, usage)
    assert approx(got, expected, rel=1e-12, abs_tol=1e-12)
