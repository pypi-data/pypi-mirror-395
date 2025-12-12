import os
from pathlib import Path

from henosis_cli_tools import FileToolPolicy, string_replace


def test_string_replace_literal(tmp_path: Path):
    # Arrange: workspace with one file containing 3 matches
    ws = tmp_path / "workspace"
    ws.mkdir(parents=True, exist_ok=True)
    fp = ws / "demo.txt"
    fp.write_text("""
alpha
blue bird
sea is blue
another blue line
omega
""".strip(), encoding="utf-8")

    pol = FileToolPolicy(scope="workspace", workspace_base=ws)

    # Dry run first
    res_dry = string_replace(
        pattern="blue",
        replacement="green",
        policy=pol,
        cwd=".",
        file_globs=["**/*.txt"],
        expected_total_matches=3,
        dry_run=True,
    )
    assert res_dry["ok"], res_dry
    assert res_dry["data"]["summary"]["total_replacements"] == 3
    assert res_dry["data"]["dry_run"] is True

    # Apply
    res = string_replace(
        pattern="blue",
        replacement="green",
        policy=pol,
        cwd=".",
        file_globs=["**/*.txt"],
        expected_total_matches=3,
        dry_run=False,
    )
    assert res["ok"], res
    assert res["data"]["summary"]["total_replacements"] == 3
    text_after = fp.read_text(encoding="utf-8")
    assert "blue" not in text_after
    assert text_after.count("green") == 3


def test_string_replace_expected_mismatch(tmp_path: Path):
    ws = tmp_path / "ws"
    ws.mkdir(parents=True, exist_ok=True)
    (ws / "a.txt").write_text("blue\n", encoding="utf-8")
    pol = FileToolPolicy(scope="workspace", workspace_base=ws)
    res = string_replace(
        pattern="blue",
        replacement="green",
        policy=pol,
        cwd=".",
        file_globs=["**/*.txt"],
        expected_total_matches=2,  # wrong on purpose
        dry_run=True,
    )
    assert not res["ok"], res
    assert "expected_total_matches" in (res.get("error") or "")
