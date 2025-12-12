import os


def test_tonext_settings_defaults():
    # Ensure import picks up .env but we do not rely on env overrides here
    from app.settings import settings

    assert hasattr(settings, "ANTHROPIC_ENABLE_TONEXT_TOOL")
    assert settings.ANTHROPIC_TONEXT_TOOL_NAME in ("context", "to_next")
    assert hasattr(settings, "ANTHROPIC_TONEXT_ATTACH_BETA")
    assert isinstance(settings.ANTHROPIC_TONEXT_ATTACH_BETA, bool)
    assert hasattr(settings, "ANTHROPIC_TONEXT_BETA_HEADER")
    assert isinstance(settings.ANTHROPIC_TONEXT_BETA_HEADER, str)
    assert hasattr(settings, "ANTHROPIC_TONEXT_ENABLE_MEMORY_TOOL")
    assert hasattr(settings, "ANTHROPIC_TONEXT_MEMORY_DIR")
