"""
henosis_cli_tools
-----------------
Reusable, policy-aware local machine tools extracted from the server.

Exports:
- FileToolPolicy: sandbox/scope configuration
- resolve_path: path resolution and sandbox enforcement
- read_text_auto: BOM/encoding-aware text reader
- read_file, write_file, append_file, list_dir
- run_command: safe command execution with allowlist and timeout
- apply_patch: simplified multi-file patch applier

These functions are framework-agnostic and can be used by both the
FastAPI server and the standalone CLI.

Also exports:
- SettingsUI: dependency-free interactive settings UI used by henosis-cli.
"""

from .tool_impl import (
    FileToolPolicy,
    resolve_path,
    read_text_auto,
    read_file,
    write_file,
    append_file,
    list_dir,
    run_command,
    apply_patch,
    string_replace,
)
from .settings_ui import SettingsUI

__all__ = [
    "FileToolPolicy",
    "resolve_path",
    "read_text_auto",
    "read_file",
    "write_file",
    "append_file",
    "list_dir",
    "run_command",
    "apply_patch",
    "string_replace",
    "SettingsUI",
]
