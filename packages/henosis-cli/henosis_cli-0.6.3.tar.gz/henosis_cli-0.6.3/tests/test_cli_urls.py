import pytest


def make_cli(server_base: str):
    # Import lazily to avoid heavy module init when running other tests
    import importlib
    cli_mod = importlib.import_module("cli")
    # Construct with minimal args; avoid network by not calling run()
    return cli_mod.ChatCLI(
        server=server_base,
        model=None,
        system_prompt=None,
        timeout=5.0,
        map_prefix=False,
        log_enabled=False,
        save_to_threads=False,
        server_usage_commit=False,
        verbose=False,
    )


@pytest.mark.parametrize(
    "base,expected_suffix",
    [
        ("http://127.0.0.1:8000", "/api/chat/stream"),
        ("http://127.0.0.1:8000/", "/api/chat/stream"),
        ("https://henosis.us/api_v2", "/api_v2/api/chat/stream"),
        ("https://henosis.us/api_v2/", "/api_v2/api/chat/stream"),
        ("https://example.com/api", "/api/chat/stream"),  # already ends with /api -> no extra /api
        ("https://example.com/api/", "/api/chat/stream"),
    ],
)
def test_stream_url_prefix_handling(base, expected_suffix):
    cli = make_cli(base)
    assert cli.stream_url.endswith(expected_suffix)
