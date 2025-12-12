# cli.py
# Enhanced CLI client: navigable menu, colorful output, emoji-rich tool rendering.
# - Optional arrow-key menu via prompt_toolkit (fallback to numeric menu)
# - Colorized UI via rich (fallback to plain text)
# - Friendly tool call/result summaries (🔍 read, 📝 write, 📎 append, 📂 list, ✏️ edit, 💻 run)
# - Preserves previous behavior and settings
# - Injects CODEBASE_MAP.md into the first user message (wrapped in <codebase_map>) without manual trimming.

import argparse
import asyncio
import json
import os
import sys
import socket
import shutil
from pathlib import Path
from typing import AsyncIterator, Dict, List, Optional, Tuple, Any, TYPE_CHECKING

import httpx
import time
import uuid
import random
from datetime import datetime, timezone
from typing import Callable
import getpass
from urllib.parse import urlparse, urlunparse
import subprocess
import shlex
import importlib
import importlib.util
import importlib.metadata
import re

# Optional websockets for Agent Mode (dev-only WS bridge)
try:
    import websockets  # type: ignore
    HAS_WS = True
except Exception:
    HAS_WS = False
    websockets = None  # type: ignore
if TYPE_CHECKING:
    from websockets.server import WebSocketServerProtocol  # type: ignore
else:
    from typing import Any as WebSocketServerProtocol  # type: ignore
# Local execution tools
try:
    from henosis_cli_tools import (
        FileToolPolicy as LocalFileToolPolicy,
        read_file as local_read_file,
        write_file as local_write_file,
        append_file as local_append_file,
        list_dir as local_list_dir,
        run_command as local_run_command,
        apply_patch as local_apply_patch,
        string_replace as local_string_replace,
    )
    HAS_LOCAL_TOOLS = True
except Exception:
    HAS_LOCAL_TOOLS = False
try:
    from henosis_cli_tools.settings_ui import SettingsUI  # no-deps settings UI
    HAS_SETTINGS_UI = True
except Exception:
    HAS_SETTINGS_UI = False

# Optional rich for colors and nice formatting
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt, Confirm
    from rich.text import Text
    HAS_RICH = True
except Exception:
    HAS_RICH = False
    Console = None
    Panel = None
    Table = None
    Prompt = None
    Confirm = None
    Text = None

"""
prompt_toolkit is optional (used for some menus when available). Input editing
for chat now uses a self-contained cross-platform engine that supports
Shift+Enter newlines on Windows and on modern POSIX terminals that advertise
extended keyboard protocols. It falls back to Ctrl+J for newline when
Shift+Enter cannot be distinguished.
"""
try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.completion import WordCompleter
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.selection import SelectionType
    from prompt_toolkit.application import Application
    from prompt_toolkit.application.current import get_app
    from prompt_toolkit.layout import Layout
    from prompt_toolkit.layout.containers import HSplit, Window
    from prompt_toolkit.layout.dimension import Dimension
    from prompt_toolkit.layout.controls import FormattedTextControl
    from prompt_toolkit.styles import Style
    HAS_PT = True
except Exception:
    HAS_PT = False
    PromptSession = None
    WordCompleter = None
    KeyBindings = None
    Application = None
    get_app = None
    Layout = None
    HSplit = None
    Window = None
    Dimension = None
    FormattedTextControl = None
    Style = None

# If optional deps are missing, print a friendly note but continue with fallbacks.
if not HAS_RICH or not HAS_PT:
    missing = []
    if not HAS_RICH:
        missing.append("rich")
    if not HAS_PT:
        missing.append("prompt_toolkit")
    if missing:
        msg = (
            "Note: optional packages missing: "
            + ", ".join(missing)
            + "\n- rich enables colorful output\n- prompt_toolkit enables arrow-key menus\n"
        )
        try:
            sys.stderr.write(msg)
        except Exception:
            pass

# New: low-level input engine (no third-party deps) for Shift+Enter newlines
try:
    from henosis_cli_tools.input_engine import make_engine
    HAS_INPUT_ENGINE = True
except Exception:
    HAS_INPUT_ENGINE = False
DEBUG_SSE = False  # set via --debug-sse
DEBUG_REQ = False  # set via --debug-req
# Max number of recent SSE event summaries to retain for diagnostics when a stream
# ends without a message.completed event. Overridable via env HENOSIS_CLI_SSE_TAIL.
try:
    SSE_TAIL_MAX = int(os.getenv("HENOSIS_CLI_SSE_TAIL", "40") or 40)
    if SSE_TAIL_MAX <= 0:
        SSE_TAIL_MAX = 40
except Exception:
    SSE_TAIL_MAX = 40


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="henosis-cli: Interactive CLI for Henosis Chat (henosis.us) multi-provider streaming backend"
    )
    p.add_argument(
        "-s",
        "--server",
        default=os.getenv("HENOSIS_SERVER", "https://henosis.us/api_v2"),
        help="Backend server base URL (default: env HENOSIS_SERVER or https://henosis.us/api_v2)",
    )
    # Quick dev toggle: use localhost/dev server base without typing --server
    p.add_argument("--dev", dest="use_dev", action="store_true", help="Use dev endpoint (env HENOSIS_DEV_SERVER or http://127.0.0.1:8000/api)")
    p.add_argument("-m", "--model", default=None, help="Model name (optional; server default if omitted)")
    p.add_argument("-S", "--system", default=None, help="Optional system prompt")
    p.add_argument("--timeout", type=float, default=None, help="HTTP timeout in seconds (default: None)")
    # Output verbosity
    p.add_argument("--verbose", action="store_true", help="Show extra status/debug output (dim logs)")
    # Debug toggles
    p.add_argument("--debug-sse", action="store_true", help="Verbose log of SSE events to console")
    p.add_argument("--debug-req", action="store_true", help="Log outgoing request payloads")
    # Raw log capture to file (CWD by default)
    p.add_argument("--raw-log", action="store_true", help="Write raw request/response logs to a file in the current working directory")
    p.add_argument("--raw-log-file", default=os.getenv("HENOSIS_RAW_LOG_PATH", None), help="Optional explicit path for the raw log file (default: CWD/henosis_raw-<ts>-<id>.log)")
    # Update checks
    p.add_argument("--no-update-check", action="store_true", help="Skip CLI and server version update checks")
    # Agent Mode (dev-only local WebSocket bridge)
    p.add_argument("--agent-mode", action="store_true", help="Enable local Agent Mode WS bridge (dev)")
    p.add_argument("--agent-host", default=os.getenv("HENOSIS_AGENT_HOST", "127.0.0.1"), help="Agent WS host (default: 127.0.0.1 or HENOSIS_AGENT_HOST)")
    p.add_argument("--agent-port", type=int, default=int(os.getenv("HENOSIS_AGENT_PORT", "8700")), help="Agent WS port (default: 8700 or HENOSIS_AGENT_PORT; use 0 for auto)")
    p.add_argument("--agent-allow-remote", action="store_true", help="Allow non-localhost WS connections (dev only; off by default)")
    # Agent scope per-terminal defaults
    p.add_argument(
        "--agent-scope",
        dest="agent_scope",
        default=os.getenv("HENOSIS_AGENT_SCOPE", None),
        help="Set Agent scope root (absolute path) for this terminal session. Defaults to the terminal's current working directory.",
    )
    # Workspace/terminal controls
    p.add_argument(
        "--workspace-dir",
        default=os.getenv("HENOSIS_WORKSPACE_DIR", None),
        help="Override workspace root directory (default: current working directory at CLI start)",
    )
    p.add_argument(
        "--terminal-id",
        default=os.getenv("HENOSIS_TERMINAL_ID", None),
        help="Optional terminal/session id used for server namespacing; does not affect local workspace root",
    )
    # Manual naming (optional). Everything else is auto-enabled by default.
    p.add_argument(
        "--title",
        default=None,
        help="Optional thread title. If omitted, CLI will name threads as '<YYYY-MM-DD HH:MM> - <project>'",
    )
    # Codebase map prefix toggle (controls <codebase_map> injection)
    p.add_argument(
        "--codebase-map-prefix",
        dest="map_prefix",
        action="store_true",
        help="Inject <codebase_map>...</codebase_map> before the first user message (overrides saved setting)",
    )
    p.add_argument(
        "--no-codebase-map-prefix",
        dest="map_prefix",
        action="store_false",
        help="Disable codebase map injection (overrides saved setting)",
    )
    p.set_defaults(map_prefix=None)
    # Onboarding helpers
    p.add_argument("--whoami", action="store_true", help="Print authentication status and exit")
    p.add_argument("--reset-config", action="store_true", help="Reset local CLI settings and re-run onboarding")
    return p

def mask_key(k: Optional[str], keep: int = 6) -> str:
    if not k:
        return "(none)"
    s = str(k).strip()
    if len(s) <= keep:
        return "*" * len(s)
    return s[:keep] + "*" * (len(s) - keep)

# Note: CLI does not read API keys; the server does. This helper remains here
# if you later choose to add a client-side /health check that prints masked keys.
# It does not change runtime behavior.

def join_url(base: str, path: str) -> str:
    base = base.rstrip("/")
    path = path.lstrip("/")
    return f"{base}/{path}"

def normalize_api_base(url: str) -> str:
    """Return the provided base URL as-is (minus a trailing slash).

    Important:
    - The CLI no longer appends '/api' automatically. Provide the full API base
      you want to use (for example, 'http://127.0.0.1:8000/api' in dev, or
      'https://henosis.us/api_v2' in production).
    - Query, fragment, and netloc are preserved; only a single trailing '/' is trimmed.
    """
    try:
        p = urlparse(url)
        # Trim a single trailing slash from the path (but keep root empty path)
        path = p.path or ""
        if path.endswith("/") and path != "/":
            path = path.rstrip("/")
        return urlunparse(p._replace(path=path))
    except Exception:
        # Fallback: simple right-strip of '/'
        return (url or "").rstrip("/")

def truncate_json(data: Any, max_chars: int = 500) -> str:
    try:
        s = json.dumps(data, ensure_ascii=False)
    except Exception:
        s = str(data)
    return (s[:max_chars] + "... (truncated)") if len(s) > max_chars else s

# --- debug flags controlled by CLI args (see amain) ---

async def parse_sse_lines(
    resp: httpx.Response,
    debug: Optional[Callable[[str], None]] = None,
) -> AsyncIterator[Tuple[str, str]]:
    """
    Robust SSE parser using aiter_lines(), compliant with the EventSource format.
    - Aggregates multiple data: lines per event block.
    - Handles LF and CRLF newlines naturally via httpx's line iterator.
    - Defaults to event name 'message' when 'event:' is omitted.
    - Flushes on blank line and at EOF.

    Also supports servers that place the logical event name inside the JSON payload
    (e.g., {"event":"message.delta"}) by mapping that onto the SSE event name when
    the SSE 'event:' field is missing.
    """
    event_name: Optional[str] = None
    data_lines: List[str] = []

    async for raw_line in resp.aiter_lines():
        if raw_line is None:
            # httpx may yield None for keep-alives
            continue
        line = raw_line.rstrip("\r\n")
        try:
            if debug is not None:
                # Show/log raw SSE line for deep debugging or raw file capture
                debug(f"sse.raw: {line!r}")
        except Exception:
            pass
        if line == "":
            # End of one SSE event block
            if data_lines:
                name = event_name or "message"
                payload = "\n".join(data_lines)
                # Best-effort: if name is the generic default and the JSON payload encodes an event/type,
                # prefer that so downstream handlers (message.delta, tool.*, etc.) keep working even
                # if a proxy stripped 'event:' headers.
                try:
                    j = json.loads(payload)
                    if isinstance(j, dict) and name in (None, "message"):
                        alt = j.get("event") or j.get("type") or j.get("evt")
                        if isinstance(alt, str) and alt.strip():
                            name = alt.strip()
                except Exception:
                    pass
                try:
                    if debug is not None:
                        debug(f"sse.emit: event={name} bytes={len(payload)}")
                except Exception:
                    pass
                yield name, payload
            # Reset for next block
            event_name = None
            data_lines = []
            continue
        if line.startswith(":"):
            # Comment/heartbeat line; ignore
            continue
        if line.startswith("event:"):
            event_name = line[len("event:") :].strip()
            continue
        if line.startswith("data:"):
            data_lines.append(line[len("data:") :].lstrip())
            continue
        # Ignore other fields (id:, retry:) for now

    # EOF: flush any pending block
    if data_lines:
        name = event_name or "message"
        payload = "\n".join(data_lines)
        try:
            j = json.loads(payload)
            if isinstance(j, dict) and name in (None, "message"):
                alt = j.get("event") or j.get("type") or j.get("evt")
                if isinstance(alt, str) and alt.strip():
                    name = alt.strip()
        except Exception:
            pass
        try:
            if debug is not None:
                debug(f"sse.emit(eof): event={name} bytes={len(payload)}")
        except Exception:
            pass
        yield name, payload

class UI:
    def __init__(self, verbose: bool = False) -> None:
        self.rich = HAS_RICH
        self.console = Console(force_terminal=True) if HAS_RICH else None
        # Verbosity: when False, suppress most 'dim' logs and developer chatter
        self.verbose = bool(verbose)
        # Lightweight debug sink for rendering issues
        try:
            self._debug_log_path = Path("cli_logs.txt").resolve()
        except Exception:
            self._debug_log_path = None
        # Theme colors
        self.theme = {
            "title": "bold white",
            # Primary accent -> orange
            "subtitle": "bold orange1",
            "label": "bold",
            "ok": "green",
            "err": "bold red",
            "warn": "yellow",
            # Use orange as primary accent for informational lines as well
            "info": "orange1",
            # Assistant stream color -> orange
            "assistant": "orange1",
            # Tool call accent -> orange
            "tool_call": "orange1",
            "tool_result": "green",
            "tool_result_err": "red",
            "dim": "grey62",
        }

    def debug_log(self, msg: str) -> None:
        """Append a timestamped line to cli_logs.txt for offline debugging.
        Never raises; disabled if filesystem unavailable.
        """
        try:
            ts = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            line = f"[{ts}] {msg}\n"
            if self._debug_log_path is not None:
                with open(self._debug_log_path, "a", encoding="utf-8") as f:
                    f.write(line)
        except Exception:
            pass

    def clear(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def header(self, title: str, subtitle: Optional[str] = None) -> None:
        if self.rich:
            text = Text(title, style=self.theme["title"])
            if subtitle:
                text.append(f"\n{subtitle}", style=self.theme["subtitle"])
            self.console.print(Panel(text, border_style=self.theme["subtitle"]))
        else:
            print("\n" + "=" * 80)
            print(title)
            if subtitle:
                print(subtitle)
            print("=" * 80)

    def header_inline(self, left: str, right: Optional[str] = None) -> None:
        """Render a single-line header with left text and optional right-aligned text.
        Uses a Panel when rich is available; falls back to ASCII alignment otherwise.
        """
        if self.rich and Panel and Table and Text:
            try:
                grid = Table.grid(expand=True)
                grid.add_column(justify="left")
                grid.add_column(justify="right")
                left_text = Text(str(left), style=self.theme["title"]) if left is not None else Text("")
                right_text = Text(str(right), style=self.theme["subtitle"]) if (right is not None and str(right).strip()) else Text("")
                grid.add_row(left_text, right_text)
                self.console.print(Panel(grid, border_style=self.theme["subtitle"]))
                return
            except Exception:
                pass
        # ASCII fallback
        try:
            width = shutil.get_terminal_size(fallback=(80, 20)).columns
        except Exception:
            width = 80
        if width < 20:
            width = 80
        left_str = str(left) if left is not None else ""
        right_str = str(right) if (right is not None and str(right).strip()) else ""
        # Compute available space for right segment
        avail = max(1, width - len(left_str))
        if right_str:
            # Trim right segment if it would exceed available space
            if len(right_str) > avail:
                right_str = right_str[:avail]
            line = left_str + right_str.rjust(avail)
        else:
            line = left_str
        print("\n" + ("=" * width))
        print(line)
        print("=" * width)

    def info(self, msg: str) -> None:
        if self.rich:
            self.console.print(f"[{self.theme['info']}]{msg}[/{self.theme['info']}]")
        else:
            print(msg)

    def warn(self, msg: str) -> None:
        if self.rich:
            self.console.print(f"[{self.theme['warn']}]! {msg}[/{self.theme['warn']}]")
        else:
            print(f"! {msg}")

    def error(self, msg: str) -> None:
        if self.rich:
            self.console.print(f"[{self.theme['err']}]✖ {msg}[/{self.theme['err']}]")
        else:
            print(f"ERROR: {msg}")

    def success(self, msg: str) -> None:
        if self.rich:
            self.console.print(f"[{self.theme['ok']}]✔ {msg}[/{self.theme['ok']}]")
        else:
            print(f"OK: {msg}")

    def print(self, msg: str = "", style: Optional[str] = None, end: str = "\n", force: bool = False) -> None:
        # Squelch most dim/debug output when not verbose, unless force=True
        if not self.verbose and not force:
            try:
                # If caller explicitly styles as 'dim', suppress
                if style == self.theme.get("dim"):
                    return
                # Suppress only when the ENTIRE line is dim-wrapped.
                # Do NOT suppress lines that include dim segments (e.g., context bars) mixed with normal text.
                if self.rich and isinstance(msg, str):
                    dim_tag = f"[{self.theme.get('dim')}]"
                    dim_close = f"[/{self.theme.get('dim')}]"
                    txt = msg.strip()
                    if txt.startswith(dim_tag) and txt.endswith(dim_close):
                        # Fully-dim line -> suppress when not verbose
                        return
            except Exception:
                pass
        # Best-effort: strip all simple [color]...[/color] tokens and apply the first seen as line style.
        # This avoids literal wrapper leakage when markup=False and multiple tags are present (e.g., [bold red] + [red]).
        try:
            # Strip our theme-based markup tokens even when Rich isn't available,
            # so wrappers never leak to plain terminals.
            if isinstance(msg, str) and style is None:
                first_style: Optional[str] = None
                earliest_idx: Optional[int] = None
                for _k, _color in (self.theme or {}).items():
                    if not isinstance(_color, str) or not _color:
                        continue
                    open_tag = f"[{_color}]"
                    close_tag = f"[/{_color}]"
                    # Track earliest occurrence to pick a reasonable dominant style for the line
                    try:
                        idx = msg.find(open_tag)
                        if idx != -1 and (earliest_idx is None or idx < earliest_idx):
                            earliest_idx = idx
                            first_style = _color
                    except Exception:
                        pass
                    # Remove all occurrences of these tokens regardless of order
                    if open_tag in msg:
                        msg = msg.replace(open_tag, "")
                    if close_tag in msg:
                        msg = msg.replace(close_tag, "")
                if first_style:
                    style = first_style
        except Exception:
            pass
        # Special fast-path for streaming assistant tokens on older rich versions that ignore end=""
        try:
            if end == "" and style and isinstance(style, str) and style == self.theme.get("assistant"):
                # Emit using ANSI 256-color orange and reset each chunk to avoid bleed
                s = str(msg)
                ORANGE_ANSI = "\x1b[38;5;214m"
                RESET = "\x1b[0m"
                try:
                    sys.stdout.write(ORANGE_ANSI + s + RESET)
                    sys.stdout.flush()
                    return
                except Exception:
                    # Last resort: plain write without color
                    try:
                        sys.stdout.write(s)
                        sys.stdout.flush()
                        return
                    except Exception:
                        pass
        except Exception:
            pass

        if self.rich:
            # Ensure immediate display during streaming by flushing each write.
            # IMPORTANT: disable Rich markup parsing so arbitrary model text like
            # "[tag]" or unmatched brackets doesn't raise MarkupError mid-stream.
            # We still apply the outer style via the style= param.
            try:
                self.console.print(
                    msg,
                    style=style,
                    end=end,
                    highlight=False,
                    soft_wrap=True,
                    markup=False,
                    flush=True,
                )
            except TypeError:
                # Older rich versions may not support some kwargs; degrade gracefully.
                try:
                    self.console.print(
                        msg,
                        style=style,
                        end=end,
                        highlight=False,
                        markup=False,
                    )
                    # Best-effort flush of the underlying file
                    try:
                        self.console.file.flush()
                    except Exception:
                        pass
                except Exception:
                    # Last-resort: print as Text to avoid markup parsing entirely
                    try:
                        from rich.text import Text as _Text
                        self.console.print(_Text(str(msg)), style=style, end=end)
                        try:
                            self.console.file.flush()
                        except Exception:
                            pass
                    except Exception:
                        # Give up on rich; fall back to plain print
                        print(str(msg), end=end, flush=True)
        else:
            print(msg, end=end, flush=True)

    # Raw stream writers used for high-fidelity token streaming without any wrapping/styling
    def write_raw(self, s: str) -> None:
        try:
            sys.stdout.write(str(s))
            sys.stdout.flush()
        except Exception:
            try:
                print(str(s), end="", flush=True)
            except Exception:
                pass

    def writeln_raw(self, s: str = "") -> None:
        try:
            sys.stdout.write(str(s) + "\n")
            sys.stdout.flush()
        except Exception:
            try:
                print(str(s))
            except Exception:
                pass

    def info_box(self, title: str, lines: List[str]) -> None:
        """Render a list of lines inside an outlined box. Uses rich Panel when available,
        otherwise falls back to a simple ASCII box.
        """
        try:
            text = "\n".join([str(x) for x in lines])
        except Exception:
            text = "\n".join([str(x) for x in lines])
        if self.rich and Panel:
            try:
                self.console.print(Panel(text, title=title, border_style=self.theme["subtitle"]))
                return
            except Exception:
                pass
        # ASCII fallback
        try:
            content_lines = [title] + lines if title else lines
            width = max((len(l) for l in content_lines), default=0) + 2
            border_top = "+" + ("-" * width) + "+"
            print(border_top)
            if title:
                print("| " + title.ljust(width - 1) + "|")
                print("|" + ("-" * width) + "|")
            for ln in lines:
                print("| " + str(ln).ljust(width - 1) + "|")
            print(border_top)
        except Exception:
            # Last resort: plain print
            print(title)
            print("\n".join(lines))

    def prompt(self, message: str, default: Optional[str] = None) -> str:
        if self.rich and Prompt:
            return Prompt.ask(message, default=default) if default is not None else Prompt.ask(message)
        else:
            inp = input(f"{message}{f' [{default}]' if default else ''}: ")
            if inp.strip():
                return inp
            return default or ""

    def confirm(self, message: str, default: bool = True) -> bool:
        if self.rich and Confirm:
            return Confirm.ask(message, default=default)
        else:
            suffix = "Y/n" if default else "y/N"
            val = input(f"{message} ({suffix}): ").strip().lower()
            if val == "" and default:
                return True
            if val in ("y", "yes", "1", "true", "t"):
                return True
            return False

    def ensure_newline(self, text_so_far: str) -> None:
        if text_so_far and not text_so_far.endswith("\n"):
            self.print()

    def table(self, title: str, rows: List[Tuple[str, str, str]]) -> None:
        if self.rich and Table:
            t = Table(title=title, show_lines=False, header_style=self.theme["subtitle"])
            t.add_column("Name")
            t.add_column("Type")
            t.add_column("Size")
            for r in rows:  # Assuming rows is List[Tuple[str, str, str]]
                t.add_row(*r)
            self.console.print(t)
        else:
            print(title)
            print("-" * len(title))
            for n, ty, sz in rows:
                print(f"{n:<40} {ty:<8} {sz}")

class ChatCLI:
    def __init__(
        self,
        server: str,
        model: Optional[str],
        system_prompt: Optional[str],
        timeout: Optional[float],
        map_prefix: Optional[bool] = None,
        log_enabled: bool = True,
        log_dir: Optional[str] = None,
        ctx_window: Optional[int] = None,
        save_to_threads: bool = True,
        server_usage_commit: bool = True,
        title: Optional[str] = None,
        verbose: bool = False,
        # Raw log capture
        raw_log: bool = False,
        raw_log_file: Optional[str] = None,
        # Agent Mode flags
        agent_mode: bool = False,
        agent_host: str = "127.0.0.1",
        agent_port: int = 8700,
        agent_allow_remote: bool = False,
        # Multi-terminal sandboxing
        workspace_dir: Optional[str] = None,
        terminal_id: Optional[str] = None,
        # Agent scope explicit override for this session
        agent_scope: Optional[str] = None,
    ):
        self.ui = UI(verbose=verbose)
        # Version tracking for display and update hints
        self._cli_version: Optional[str] = None
        self._latest_version: Optional[str] = None
        self._version_outdated: Optional[bool] = None
        # Resolve server base, honoring --dev shortcut
        self.server = server
        self.model = model
        self.system_prompt = system_prompt
        self.timeout = timeout

        # Session settings
        self.requested_tools: Optional[bool] = None  # None=server default, True=on, False=off
        self.fs_scope: Optional[str] = None          # None=server default, "workspace" or "host"
        self.host_base: Optional[str] = None         # Absolute path, used when fs_scope="host"
        # Host filesystem mode (client-side governance): any | cwd | custom
        self.fs_host_mode: Optional[str] = None
        # Whether host_base should be persisted to server settings (False for auto per-terminal binding)
        self._host_base_ephemeral: bool = False
        # History is always enabled; toggle feature removed. Kept for compatibility in UI strings.
        self.history_enabled: bool = True
        self.control_level: Optional[int] = None     # 1|2|3; None=server default
        self.auto_approve: List[str] = []           # Tool names to auto-approve at L2
        # Trust registries for Level 2 client-side approvals
        self.trust_tools_always: List[str] = []
        self.trust_tools_session: List[str] = []
        self.trust_cmds_always: List[str] = []
        self.trust_cmds_session: List[str] = []
        # OpenAI web search controls
        self.web_search_enabled: bool = False
        self.web_search_allowed_domains: List[str] = []
        self.web_search_include_sources: bool = False
        self.web_search_location: Dict[str, str] = {}

        # Conversation history
        self.history: List[Dict[str, str]] = []
        if self.system_prompt:
            self.history.append({"role": "system", "content": self.system_prompt})

        # Use the base URL as provided (minus trailing slash). No automatic '/api' is appended.
        # For dev, provide a base ending with '/api' (e.g., http://127.0.0.1:8000/api).
        self.api_base = normalize_api_base(self.server)

        # Primary adapter endpoints: mimic auth base paths
        # Use the same base as auth (no automatic /v0 prefix). Keep /v0 variants as fallbacks.
        self.stream_url = join_url(self.api_base, "/chat/stream")
        self.stream_url_alt = join_url(self.api_base, "/v0/chat/stream")
        self.approvals_url = join_url(self.api_base, "/approvals")
        self.tools_callback_url = join_url(self.api_base, "/tools/callback")
        # Auth endpoints
        self.login_url = join_url(self.api_base, "/login")
        self.logout_url = join_url(self.api_base, "/logout")
        self.check_auth_url = join_url(self.api_base, "/check-auth")
        self.refresh_url = join_url(self.api_base, "/refresh")
        # CLI settings endpoints (server persistence)
        self.cli_settings_url = join_url(self.api_base, "/cli/settings")
        # Registration endpoints (optional on server)
        self.register_url = join_url(self.api_base, "/register")
        self.verify_email_url = join_url(self.api_base, "/verify_email")

        # Debug: log resolved core endpoints for quick diagnosis of base/path issues
        try:
            self.ui.debug_log(
                "[endpoints-cli] base="
                + self.api_base
                + f" | stream={self.stream_url} | stream_alt={self.stream_url_alt} | approvals={self.approvals_url} | tools_cb={self.tools_callback_url}"
            )
        except Exception:
            pass

        # Tool display toggles
        self.show_tool_calls: bool = True
        self.max_dir_items: int = 12  # show up to N items for list_dir

        # Settings persistence (legacy local file for fallback only)
        self.settings_file = Path.home() / ".henosis_cli_settings.json"
        self._settings_migrated = False  # if we load from legacy name on first run
        # Default: inject codebase map once at session start
        self.inject_codebase_map: bool = True
        # Preflight estimator removed from UX; keep flag for settings compatibility (default OFF)
        self.preflight_enabled: bool = False
        # Optional local-only preferences from onboarding
        self.telemetry_enabled: Optional[bool] = None
        self.output_format: Optional[str] = None  # e.g. plain|markdown
        # Usage & Info box rendering mode: 'concise' | 'verbose'
        # - concise: only model (+thinking level when applicable) and context meter
        # - verbose: full details (current behavior)
        self.usage_info_mode: str = "verbose"
        # Reasoning effort selector for OpenAI reasoning models (low|medium|high). Default: medium
        self.reasoning_effort: str = "medium"
        # Retain provider-native tool results between turns (e.g., Kimi reasoning/tool messages)
        self.retain_native_tool_results: bool = False
        # Anthropic thinking-mode budget tokens (applies to '-thinking' models; None = server default)
        self.thinking_budget_tokens: Optional[int] = None
        # Anthropic prompt cache TTL preference: None=server default, or "5m" | "1h"
        self.anthropic_cache_ttl: Optional[str] = None
        # Text verbosity selector (UI only; not sent to server requests by default)
        self.text_verbosity: str = "medium"  # low | medium | high
        # Tool call preambles (UI toggle only)
        self.preambles_enabled: bool = False
        # Codex developer prompt injection (system) for Codex models only
        self.codex_prompt_enabled: bool = True
        # Custom first-turn injection (like codebase map) — toggle + editable text
        self.custom_first_turn_enabled: bool = False
        self.custom_first_turn_text: str = ""
        # Load local settings as initial defaults; will sync with server after auth
        self.load_settings()
        self._apply_model_side_effects()

        # After loading settings, bind Agent scope per terminal instance by default.
        # Priority: explicit CLI flag/env > previously saved settings > CWD
        try:
            # Determine current working directory as a safe default
            _cwd_default = str(Path(os.getcwd()).resolve())
        except Exception:
            _cwd_default = None
        try:
            # If an explicit agent scope was provided via CLI or env, honor it and persistable
            # Otherwise, force a per-terminal default to CWD without persisting to server settings.
            explicit_scope = None
            # A later assignment from amain passes args via constructor namespace; detect via introspection
            # Fallback to environment variable already parsed in build_arg_parser
        except Exception:
            explicit_scope = None
        # The constructor receives no direct args reference; infer from environment variable for explicit
        # Prefer constructor param over env override
        if agent_scope and str(agent_scope).strip():
            explicit_scope = agent_scope
        else:
            explicit_scope = os.getenv("HENOSIS_AGENT_SCOPE") or explicit_scope
        # If host_base was loaded from settings and no explicit override requested, prefer CWD for this session
        try:
            if explicit_scope and str(explicit_scope).strip():
                self.host_base = str(Path(explicit_scope).expanduser().resolve())
                self._host_base_ephemeral = False
            elif _cwd_default:
                self.host_base = _cwd_default
                # Mark as ephemeral so we don't persist per-terminal default to server settings
                self._host_base_ephemeral = True
        except Exception:
            # Leave host_base as-is on failure
            pass

        # Prefer host scope by default when an Agent scope is bound
        try:
            if self.host_base and not self.fs_scope:
                self.fs_scope = "host"
                # Constrain host operations to the bound root by default
                if not self.fs_host_mode:
                    self.fs_host_mode = "custom"
        except Exception:
            pass

        # Codebase map injection (hidden from CLI; wrapped for UIs to detect)
        self._codebase_map_raw: Optional[str] = self._load_codebase_map_raw()
        self._did_inject_codebase_map: bool = False
        self._did_inject_custom_first_turn: bool = False
        # If CLI flag provided, override persisted/default
        if map_prefix is not None:
            self.inject_codebase_map = bool(map_prefix)

        # No manual per-message character limits; providers/server will enforce their own limits
        # Track last tool call args by call_id for troubleshooting failed results
        self._tool_args_by_call_id: Dict[str, Any] = {}
        # Working memory (context summarization) injection controls
        self._memory_paths_for_first_turn: List[str] = []
        self._did_inject_working_memory: bool = False
        self._restart_after_summary: bool = False
        # Track the exact user content sent to the server for the last turn
        # (includes code map injection on first turn when enabled)
        self._last_built_user_content: Optional[str] = None

        # Auth state (cookies kept in-memory for this process)
        self.cookies = httpx.Cookies()
        self.auth_user: Optional[str] = None
        # Persisted auth state path (optional "stay logged in" on this machine)
        self.auth_state_file = Path.home() / ".henosis_cli_auth.json"
        # Device identity for device-bound refresh tokens (stable per machine)
        self.device_id: Optional[str] = None
        self.device_name: str = f"{socket.gethostname()} cli"

        # Logging + cost tracking (forced ON by default)
        self.log_enabled: bool = True if log_enabled is None else bool(log_enabled)
        self.log_dir = Path(log_dir or "logs").resolve()
        self.session_log_path: Optional[Path] = None
        self.ctx_window: Optional[int] = int(ctx_window) if isinstance(ctx_window, int) else None
        self.cumulative_cost_usd: float = 0.0
        # Server-authoritative cumulative cost (from /api/usage/commit responses)
        self.server_cumulative_cost_usd: float = 0.0
        # Track last client-side estimated cost for the most recent turn
        self._last_estimated_cost_usd: float = 0.0
        # Local cumulative token counters (fallback when server doesn't send cumulative usage)
        self._cum_input_tokens: int = 0
        self._cum_output_tokens: int = 0
        self._cum_total_tokens: int = 0
        # Track cumulative reasoning/thinking tokens (session-level)
        self._cum_reasoning_tokens: int = 0
        self._session_local_id: str = uuid.uuid4().hex
        # Subscription/tier awareness (populated from /profile when available)
        self.subscription_tier: Optional[str] = None
        self.subscription_status: Optional[str] = None
        self.is_free_tier: Optional[bool] = None  # None = unknown, True/False when profile loaded
        # Per-terminal identity and workspace root. Default to the terminal's CWD as the root.
        try:
            self.terminal_id: str = (terminal_id or os.getenv("HENOSIS_TERMINAL_ID") or uuid.uuid4().hex)
        except Exception:
            self.terminal_id = uuid.uuid4().hex
        try:
            cwd_path = Path(os.getcwd()).resolve()
        except Exception:
            cwd_path = Path(".").resolve()
        try:
            # Resolve workspace directory preference/override; default to CWD
            ws_override = workspace_dir or os.getenv("HENOSIS_WORKSPACE_DIR")
            if ws_override and str(ws_override).strip():
                ws_base = Path(ws_override).expanduser().resolve()
            else:
                ws_base = cwd_path
            # Do not create a dedicated per-terminal subfolder; operate directly in the chosen root
            if not ws_base.exists():
                # If the provided override path does not exist, create it to avoid surprises
                ws_base.mkdir(parents=True, exist_ok=True)
            self.local_workspace_dir: str = str(ws_base)
            # Hint to shared tool library for any defaults
            os.environ["HENOSIS_WORKSPACE_DIR"] = self.local_workspace_dir
        except Exception:
            # Fallback to current directory
            self.local_workspace_dir = str(cwd_path)

        # Raw request/response logging to file in CWD (opt-in)
        def _env_true(name: str) -> bool:
            val = os.getenv(name, "").strip().lower()
            return val in ("1", "true", "yes", "on")
        try:
            self.raw_log_enabled: bool = bool(raw_log) or _env_true("HENOSIS_RAW_LOG")
        except Exception:
            self.raw_log_enabled = bool(raw_log)
        try:
            self.raw_log_path: Optional[Path] = (Path(raw_log_file).expanduser().resolve() if (raw_log_file and str(raw_log_file).strip()) else None)
        except Exception:
            self.raw_log_path = None
        self._rawlog_initialized: bool = False

        # Server-side thread save
        # Force saving to threads by default
        self.save_chat_history: bool = True if save_to_threads is None else bool(save_to_threads)
        self.thread_uid: Optional[str] = None
        self._manual_title: bool = bool(title)
        self.thread_name: str = title or self._default_thread_name()
        self.messages_for_save: List[Dict[str, Any]] = []
        self.create_thread_url = join_url(self.api_base, "/create_thread")
        self.save_convo_url = join_url(self.api_base, "/save_conversation")
        # Server-side usage commit (optional)
        # Force committing usage by default
        self.server_usage_commit: bool = True if server_usage_commit is None else bool(server_usage_commit)
        self.commit_usage_url = join_url(self.api_base, "/usage/commit")
        
        # Agent Mode (WebSocket bridge) state
        self.agent_mode: bool = bool(agent_mode)
        self.agent_host: str = str(agent_host or "127.0.0.1")
        self.agent_port: int = int(agent_port or 8700)
        self.agent_allow_remote: bool = bool(agent_allow_remote)
        self._ws_server: Optional[Any] = None
        self._ws_client: Optional[Any] = None
        self._ws_client_lock = asyncio.Lock()
        self._busy: bool = False
        # approvals: call_id -> Future[(approved: bool, note: Optional[str])]
        self._pending_approvals: Dict[str, asyncio.Future] = {}
        # Recovery helpers for provider 'string too long' errors
        self._tail_next_paths: set[str] = set()
        self._auto_retry_after_tailed: bool = False
        self._last_dispatch_ctx: Optional[Dict[str, Any]] = None
        # Track current in-progress turn so late WS connections can sync mid-conversation
        self._current_turn: Dict[str, Any] = {
            "active": False,
            "session_id": None,
            "model": None,
            "assistant_so_far": "",
            "tool_events": [],  # list of {type: 'tool.call'|'tool.result', data: {...}}
        }
        # Track last used model for display
        self._last_used_model: Optional[str] = None
        # Provider-native history for Kimi (preserve reasoning_content across turns)
        self._kimi_raw_history: List[Dict[str, Any]] = []
        # Last server billing info from /api/usage/commit
        self._last_commit_cost_usd: float = 0.0
        self._last_remaining_credits: Optional[float] = None
        self._last_commit_model: Optional[str] = None
        # Cache of model -> input context length (tokens) for context meter
        self._model_ctx_map: Optional[Dict[str, int]] = None
        # Fun thinking indicator word bank (for pre-response animation)
        # One word (chosen at random) is shown with a rainbow animation until first tokens arrive
        try:
            self._thinking_words: List[str] = [
                "thinking",
                "noodling",
                "vibing",
                "contemplating",
                "pondering",
                "brewing",
                "crunching",
                "weaving",
                "exploring",
                "daydreaming",
                # Added fun extras
                "tinkering",
                "brainstorming",
                "musing",
                "percolating",
                "riffing",
                "scheming",
                "ideating",
                "dreamweaving",
                "marinating",
                "cogitating",
            ]
        except Exception:
            self._thinking_words = ["thinking", "working..."]
        # Make rainbow thinking indicator 3x as wide by inserting spaces between letters
        try:
            self._thinking_rainbow_spacing: int = 3  # 3 => adds 2 spaces between characters
        except Exception:
            self._thinking_rainbow_spacing = 3
        # Thinking indicator (animated status while waiting for first tokens)
        # Enabled by default for better perceived responsiveness. Set
        # HENOSIS_THINKING_INDICATOR=0/false/no/off to disable.
        try:
            env_val = os.getenv("HENOSIS_THINKING_INDICATOR", "").strip().lower()
            if env_val in ("0", "false", "no", "off"):
                self._thinking_indicator_enabled = False
            else:
                self._thinking_indicator_enabled = True
        except Exception:
            self._thinking_indicator_enabled = True
        # Track Ctrl+C timing for double-press-to-exit behavior
        self._last_interrupt_ts: Optional[float] = None

        # Timers: session-level and per-turn wall-clock timers
        self._session_started_at: Optional[float] = None  # time.perf_counter() at session start
        self._turn_started_at: Optional[float] = None     # time.perf_counter() per turn start

        # Slash command catalog and enhanced input session
        self._commands_catalog: List[Dict[str, str]] = self._build_commands_catalog()
        # Low-level input engine (supports Shift+Enter newlines where possible)
        self._input_engine = make_engine() if HAS_INPUT_ENGINE else None
        # Optional prompt_toolkit session for inline slash-command completion
        self._pt_session = None
        if HAS_PT and PromptSession:
            try:
                # Build completer and simple key bindings: Enter submits, Ctrl+J inserts newline
                self._pt_completer = self._commands_word_completer()
                kb = KeyBindings()

                @kb.add("enter")
                def _submit(event):
                    # Submit entire buffer
                    event.app.exit(result=event.current_buffer.text)

                @kb.add("c-j")
                def _newline(event):
                    # Insert literal newline
                    event.current_buffer.insert_text("\n")

                # Bottom toolbar with quick hints
                def _toolbar() -> str:
                    return " Type / then Tab to complete, or Enter on '/' to open the palette. Ctrl+J inserts a newline. "

                # Create session
                self._pt_session = PromptSession(
                    key_bindings=kb,
                    bottom_toolbar=_toolbar,
                )
            except Exception:
                self._pt_session = None

    # ----------------------- Provider heuristics -----------------------
    def _is_openai_reasoning_model(self, model: Optional[str]) -> bool:
        """Return True when the model is an OpenAI reasoning-capable model.
        Mirrors server-side heuristic: prefixes 'gpt-5' or 'o4'.
        """
        try:
            if not model:
                return False
            m = str(model).lower().strip()
            return m.startswith("gpt-5") or m.startswith("o4")
        except Exception:
            return False

    # ----------------------- Update checker ----------------------------
    async def maybe_check_for_updates(self) -> None:
        """Check PyPI for a newer henosis-cli version and offer to update.

        Skips when:
        - HENOSIS_CLI_NO_UPDATE_CHECK=1
        - offline or PyPI unavailable (quietly)
        - current version cannot be determined
        """
        try:
            if os.getenv("HENOSIS_CLI_NO_UPDATE_CHECK", "").strip() in ("1", "true", "yes"):  # opt-out
                return
            # Resolve current version from installed metadata; fallback to pyproject when running from source
            pkg_candidates = ("henosis-cli", "henosis-tools")
            # Determine current by trying each package name
            current = None
            picked_pkg = None
            for name in pkg_candidates:
                current = self._resolve_current_version(name)
                if current:
                    picked_pkg = name
                    break
            # If still not found, last resort: generic resolve without name
            if not current:
                current = self._resolve_current_version()
            # Persist for later display in UI boxes
            try:
                self._cli_version = current
            except Exception:
                pass
            if not current:
                return

            # Query PyPI for latest version
            latest = None
            try:
                timeout = httpx.Timeout(connect=2.0, read=3.0, write=2.0, pool=2.0) if self.timeout is None else httpx.Timeout(min(self.timeout, 5.0))
                async with httpx.AsyncClient(timeout=timeout) as client:
                    # Try each candidate name until one resolves
                    for name in (picked_pkg,) if picked_pkg else pkg_candidates:
                        url = f"https://pypi.org/pypi/{name}/json"
                        r = await client.get(url)
                        if r.status_code == 200 and r.headers.get("content-type", "").startswith("application/json"):
                            data = r.json()
                            info = data.get("info") or {}
                            ver = info.get("version")
                            if isinstance(ver, str) and ver.strip():
                                latest = ver.strip()
                                picked_pkg = name
                                break
            except Exception:
                latest = None
            if not latest:
                return
            # Persist latest for UI display
            try:
                self._latest_version = latest
            except Exception:
                pass

            # Compare versions (best-effort)
            def _newer(a: str, b: str) -> bool:
                # return True if b > a
                try:
                    from packaging.version import Version  # type: ignore
                    return Version(b) > Version(a)
                except Exception:
                    # Fallback: compare dotted integers, ignoring non-digits
                    def to_tuple(s: str):
                        parts = []
                        for p in s.split('.'):
                            try:
                                # strip non-digit suffix/prefix
                                num = ''.join(ch for ch in p if (ch.isdigit() or ch == '-'))
                                parts.append(int(num) if num not in ("", "-") else 0)
                            except Exception:
                                parts.append(0)
                        return tuple(parts)
                    return to_tuple(b) > to_tuple(a)

            is_outdated = _newer(current, latest)
            try:
                self._version_outdated = bool(is_outdated)
            except Exception:
                pass
            if not is_outdated:
                return

            # Inform user (no interactive Y/N and no in-CLI install attempt)
            # Use the actual package name in the upgrade instructions
            pkg = picked_pkg or "henosis-cli"
            self.ui.warn(f"A newer {pkg} is available: {current} -> {latest}")
            self.ui.print("Update from your shell:")
            self.ui.print(f"- pipx:    pipx upgrade {pkg}", style=self.ui.theme["dim"])  # type: ignore
            self.ui.print(f"- pip:     {os.path.basename(sys.executable)} -m pip install -U {pkg}", style=self.ui.theme["dim"])  # type: ignore
            return
        except SystemExit:
            raise
        except Exception:
            # Never block CLI start due to update checks
            return

    def _resolve_current_version(self, pkg_name: Optional[str] = None) -> Optional[str]:
        """Best-effort resolution of the current CLI version.
        Prefer importlib.metadata when installed; otherwise read local pyproject.toml.
        """
        try:
            # First, if a distribution name was provided, try that
            if pkg_name:
                try:
                    return importlib.metadata.version(pkg_name)
                except importlib.metadata.PackageNotFoundError:
                    pass
            # Try common distribution names
            for name in ("henosis-cli", "henosis-tools"):
                try:
                    return importlib.metadata.version(name)
                except importlib.metadata.PackageNotFoundError:
                    continue
            # Fallback: read local pyproject.toml when running from source
            pp = Path(__file__).resolve().parent / "pyproject.toml"
            if pp.exists():
                # Robust TOML parse for project.version
                try:
                    import tomllib  # Python 3.11+
                except Exception:
                    tomllib = None
                if tomllib is not None:
                    try:
                        data = tomllib.loads(pp.read_text(encoding="utf-8", errors="ignore"))
                        proj = data.get("project") or {}
                        ver = proj.get("version")
                        if isinstance(ver, str) and ver.strip():
                            return ver.strip()
                    except Exception:
                        pass
                # Fallback naive scan
                txt = pp.read_text(encoding="utf-8", errors="ignore")
                for line in txt.splitlines():
                    ls = line.strip()
                    if ls.startswith("version") and "=" in ls:
                        val = ls.split("=", 1)[1].strip().strip('\"\'')
                        if val:
                            return val
        except Exception:
            return None
        return None

    async def check_server_version_compatibility(self) -> None:
        """Query the server /health for version info and warn on incompatibility.

        Expects keys: min_cli_version, latest_cli_version (optional), api_version (optional).
        Never blocks execution.
        """
        try:
            # Resolve health URL regardless of /api prefix handling in constructor
            health_url = join_url(self.server, "/health")
            timeout = httpx.Timeout(connect=3.0, read=3.0, write=3.0, pool=3.0) if self.timeout is None else httpx.Timeout(min(self.timeout, 5.0))
            async with httpx.AsyncClient(timeout=timeout, cookies=self.cookies) as client:
                r = await client.get(health_url)
                if r.status_code != 200:
                    return
                if not r.headers.get("content-type", "").startswith("application/json"):
                    return
                h = r.json()
                min_cli = h.get("min_cli_version")
                latest_cli = h.get("latest_cli_version") or h.get("recommended_cli_version")
                api_version = h.get("api_version") or h.get("version")
                # Determine current CLI version
                cur = self._cli_version or self._resolve_current_version()
                # Nothing to compare
                if not cur:
                    return
                # Compare using packaging when available
                def newer(a: str, b: str) -> bool:
                    try:
                        from packaging.version import Version
                        return Version(b) > Version(a)
                    except Exception:
                        return b != a
                def lower(a: str, b: str) -> bool:
                    try:
                        from packaging.version import Version
                        return Version(a) < Version(b)
                    except Exception:
                        return a != b
                if isinstance(min_cli, str) and min_cli.strip() and lower(cur, min_cli.strip()):
                    self.ui.warn(f"Your CLI v{cur} is older than server minimum v{min_cli}. Please update to avoid incompatibilities.")
                elif isinstance(latest_cli, str) and latest_cli.strip() and newer(cur, latest_cli.strip()):
                    # This case rarely happens (server recommends older), so ignore
                    pass
                elif isinstance(latest_cli, str) and latest_cli.strip() and lower(cur, latest_cli.strip()):
                    self.ui.print(
                        f"A newer CLI v{latest_cli} is recommended by the server (you have v{cur}).",
                        style=self.ui.theme.get("dim"),
                    )
                # Surface API version in a dim line for visibility
                if isinstance(api_version, str) and api_version.strip():
                    self.ui.print(f"Server API version: {api_version}", style=self.ui.theme.get("dim"))
        except Exception:
            return

    def _port_in_use(self, host: str, port: int) -> bool:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.25)
                return s.connect_ex((host, port)) == 0
        except Exception:
            return False

    def _find_free_port(self, host: str = "127.0.0.1", start: int = 8700, end: int = 8900) -> int:
        # Try range first
        for p in range(start, end + 1):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind((host, p))
                    return p
            except Exception:
                continue
        # Fallback: let OS pick ephemeral
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((host, 0))
                return s.getsockname()[1]
        except Exception:
            return 0

    def _clip(self, s: Any, max_len: int = 300) -> str:
        s = str(s)
        return s if len(s) <= max_len else (s[: max_len//2] + " ... (truncated) ... " + s[- max_len//2 :])

    # ----------------------- Pricing + costs -----------------------

    def _pricing_table(self) -> Dict[str, Dict[str, Any]]:
        # Match server chat_adapter PRICING_PER_MILLION (subset is fine; unknown -> 0)
        return {
            # OpenAI
            "gpt-5.1": {"input": 1.75, "output": 14.00, "provider": "openai"},
            "gpt-5.1-codex": {"input": 1.75, "output": 14.00, "provider": "openai"},
            "gpt-5.1-codex-max": {"input": 1.75, "output": 14.00, "provider": "openai"},
            "gpt-5.1-codex": {"input": 1.75, "output": 14.00, "provider": "openai"},
            "gpt-5.1-mini": {"input": 0.35, "output": 2.80, "provider": "openai"},
            "gpt-5": {"input": 1.75, "output": 14.00, "provider": "openai"},
            "gpt-5-2025-08-07": {"input": 1.75, "output": 14.00, "provider": "openai"},
            "gpt-5-codex": {"input": 1.75, "output": 14.00, "provider": "openai"},
            "gpt-5-pro": {"input": 15.00, "output": 120.00, "provider": "openai"},
            "gpt-5-pro-2025-10-06": {"input": 15.00, "output": 120.00, "provider": "openai"},
            "gpt-5-mini-2025-08-07": {"input": 0.35, "output": 2.80, "provider": "openai"},
            "gpt-4o-mini": {"input": 0.21, "output": 0.84, "provider": "openai"},
            # Codex Mini (fine-tuned o4-mini for CLI). Pricing includes 1.4x margin per codex-mini.txt.
            # Cached input tokens override: $0.375 * 1.4 = $0.525 per 1M (25% of input rate).
            "codex-mini-latest": {"input": 2.10, "output": 8.40, "cached_input": 0.525, "provider": "openai"},
            # Anthropic
            "claude-sonnet-4-20250514": {"input": 4.20, "output": 21.00, "provider": "anthropic"},
            "claude-sonnet-4-20250514-thinking": {"input": 4.20, "output": 21.00, "provider": "anthropic"},
            "claude-haiku-4-5-20251001": {"input": 1.40, "output": 7.00, "provider": "anthropic"},
            "claude-haiku-4-5-20251001-thinking": {"input": 1.40, "output": 7.00, "provider": "anthropic"},
            "claude-sonnet-4-5-20250929": {"input": 4.20, "output": 21.00, "provider": "anthropic"},
            "claude-sonnet-4-5-20250929-thinking": {"input": 4.20, "output": 21.00, "provider": "anthropic"},
            "claude-opus-4-1-20250805": {"input": 21.00, "output": 105.00, "provider": "anthropic"},
            "claude-opus-4-1-20250805-thinking": {"input": 21.00, "output": 105.00, "provider": "anthropic"},
            # New Opus 4.5 (provider base $5/$25 with 1.4x margin -> $7.00/$35.00)
            "claude-opus-4-5-20251101": {"input": 7.00, "output": 35.00, "provider": "anthropic"},
            "claude-opus-4-5-20251101-thinking": {"input": 7.00, "output": 35.00, "provider": "anthropic"},
            # Gemini
            "gemini-2.5-pro": {"input": 1.75, "output": 14.00, "provider": "gemini"},
            "gemini-2.5-flash": {"input": 0.21, "output": 0.84, "provider": "gemini"},
            # Gemini 3 Pro Preview ("newgem"). Base: $2/$12 and $4/$18 per 1M;
            # CLI uses the low-tier 1.4x margin rates for estimates. High-tier
            # pricing based on total_tokens > 200K is applied on the server.
            "gemini-3-pro-preview": {"input": 2.80, "output": 16.80, "provider": "gemini"},
            # xAI
            "grok-4-1-fast-reasoning": {"input": 0.28, "output": 0.70, "provider": "xai"},
            "grok-4-1-fast-non-reasoning": {"input": 0.28, "output": 0.70, "provider": "xai"},
            "grok-4": {"input": 4.20, "output": 21.00, "provider": "xai"},
            "grok-code-fast-1": {"input": 0.28, "output": 2.10, "provider": "xai"},
            # DeepSeek V3.2 (+$0.25 per 1M margin)
            "deepseek-chat-3.2": {"input": 0.53, "output": 0.67, "provider": "deepseek"},
            "deepseek-reasoner-3.2": {"input": 0.53, "output": 0.67, "provider": "deepseek"},
            "deepseek-3.2-speciale": {"input": 0.53, "output": 0.67, "provider": "deepseek"},
            # Kimi
            "kimi-k2-0905-preview": {"input": 0.84, "output": 3.50, "provider": "kimi"},
            "kimi-k2-0711-preview": {"input": 0.84, "output": 3.50, "provider": "kimi"},
            "kimi-k2-thinking": {"input": 0.84, "output": 3.50, "provider": "kimi"},
            # GLM (Z.AI)
            # Pricing with 1.4x margin applied (base: in $0.60, out $2.20)
            "glm-4.6": {"input": 0.84, "output": 3.08, "provider": "glm"},
        }

    def _resolve_price(self, model: Optional[str]) -> Dict[str, Any]:
        if not model:
            return {"input": 0.0, "output": 0.0, "provider": "unknown"}
        table = self._pricing_table()
        if model in table:
            return table[model]
        # soft alias
        if model == "gpt-5":
            return table.get("gpt-5-2025-08-07", {"input": 0.0, "output": 0.0, "provider": "unknown"})
        return {"input": 0.0, "output": 0.0, "provider": "unknown"}

    def _resolve_model_alias(self, raw_name: Optional[str]) -> Optional[str]:
        """Normalize model aliases to their canonical server identifiers."""
        if not raw_name:
            return None
        name = raw_name.strip()
        lower = name.lower()
        aliases = {
            "gemini-3": "gemini-3-pro-preview",
            "gemini-3-pro": "gemini-3-pro-preview",
            "gemini-3-preview": "gemini-3-pro-preview",
            "gemini-new": "gemini-3-pro-preview",
            "new-gemini": "gemini-3-pro-preview",
            "gemini-pro-3": "gemini-3-pro-preview",
            "gpt5": "gpt-5",
            "gpt4": "gpt-4o",
            # Anthropic Claude Opus 4.5 (thinking OFF) short aliases
            # Map common shorthand variants to the canonical non-thinking model id
            "claude-opus-4-5": "claude-opus-4-5-20251101",
            "claude-opus-4.5": "claude-opus-4-5-20251101",
            "opus-4-5": "claude-opus-4-5-20251101",
            "opus-4.5": "claude-opus-4-5-20251101",
            "opus45": "claude-opus-4-5-20251101",
            "claude-opus45": "claude-opus-4-5-20251101",
        }
        return aliases.get(lower, name)

    def _apply_model_side_effects(self) -> None:
        """Adjust related settings when certain models are selected."""
        try:
            model_name = (self.model or "").strip().lower()
        except Exception:
            model_name = ""
        try:
            if model_name in {"gpt-5-pro", "gpt-5-pro-2025-10-06"}:
                if getattr(self, "reasoning_effort", None) != "high":
                    self.reasoning_effort = "high"
            # Codex family: disable preambles for better behavior
            if "codex" in model_name:
                self.preambles_enabled = False
            # Codex Max: default web search OFF when this model is selected (user can re-enable manually)
            if model_name == "gpt-5.1-codex-max":
                try:
                    self.web_search_enabled = False
                except Exception:
                    pass
        except Exception:
            try:
                self.reasoning_effort = "high"
            except Exception:
                pass
    def _is_codex_model(self, model: Optional[str]) -> bool:
        try:
            return bool(model) and ("codex" in str(model).lower())
        except Exception:
            return False
    def _is_codex_max(self, model: Optional[str]) -> bool:
        try:
            return bool(model) and (str(model).strip().lower() == "gpt-5.1-codex-max")
        except Exception:
            return False

    def _is_deepseek_like(self, model: Optional[str]) -> bool:
        try:
            return bool(model) and ("deepseek" in str(model).lower())
        except Exception:
            return False

    def compute_cost_usd(self, model: Optional[str], usage: Dict[str, Any]) -> float:
        price = self._resolve_price(model)
        provider = (price.get("provider") or "").lower()
        # prefer detailed fields when present
        prompt_tokens = int(usage.get("prompt_tokens") or usage.get("turn", {}).get("input_tokens", 0) or 0)
        completion_tokens = int(usage.get("completion_tokens") or usage.get("turn", {}).get("output_tokens", 0) or 0)
        total_tokens = int(usage.get("total_tokens") or usage.get("turn", {}).get("total_tokens", 0) or (prompt_tokens + completion_tokens) or 0)
        image_tokens = int(usage.get("image_tokens", 0) or 0)
        thinking_tokens = int(usage.get("thinking_tokens", 0) or 0)
        # Reasoning gap: bill as completion-side if total > (prompt + completion)
        reasoning_gap = 0
        try:
            if total_tokens > (prompt_tokens + completion_tokens):
                reasoning_gap = total_tokens - (prompt_tokens + completion_tokens)
        except Exception:
            reasoning_gap = 0
        # Anthropic: count image tokens as prompt-side
        if provider == "anthropic" and image_tokens:
            prompt_tokens += image_tokens
        # Anthropic prompt caching: pricing logic (reads @ 10%, creation @ 1.25x/2x)
        if provider == "anthropic":
            cache_read = int(usage.get("cache_read_input_tokens", 0) or 0)
            cache_creation = int(usage.get("cache_creation_input_tokens", 0) or 0)
            # Try to detect creation breakdown if available
            cc_5m = 0
            cc_1h = 0
            try:
                cc_map = usage.get("cache_creation") if isinstance(usage, dict) else None
                if isinstance(cc_map, dict):
                    cc_5m = int(cc_map.get("ephemeral_5m_input_tokens", 0) or 0)
                    cc_1h = int(cc_map.get("ephemeral_1h_input_tokens", 0) or 0)
            except Exception:
                pass
            # If breakdown is missing but total creation exists, assume 5m (1.25x) as default/safe estimate
            if cache_creation > 0 and (cc_5m + cc_1h) == 0:
                cc_5m = cache_creation
            
            # Only apply special pricing if cache fields are present
            if cache_read > 0 or cache_creation > 0:
                in_rate = float(price.get("input", 0.0))
                out_rate = float(price.get("output", 0.0))
                
                # Non-cached prompt part
                non_cached = max(0, int(prompt_tokens) - int(cache_read) - int(cache_creation))
                
                cost = 0.0
                # Standard input
                cost += (non_cached / 1_000_000.0) * in_rate
                # Cache reads (10% of input rate)
                cost += (cache_read / 1_000_000.0) * (in_rate * 0.10)
                # Cache creation (1.25x for 5m, 2.0x for 1h)
                if cc_5m > 0:
                    cost += (cc_5m / 1_000_000.0) * (in_rate * 1.25)
                if cc_1h > 0:
                    cost += (cc_1h / 1_000_000.0) * (in_rate * 2.00)
                
                # Output + reasoning gap
                completion_total = completion_tokens
                if total_tokens and (prompt_tokens + completion_tokens) != total_tokens:
                    completion_total += reasoning_gap
                else:
                    if thinking_tokens and not usage.get("total_tokens"):
                        completion_total += thinking_tokens
                
                cost += (completion_total / 1_000_000.0) * out_rate
                return float(cost)

        # reasoning_gap already computed above
        # DeepSeek cache pricing nuance (best-effort; needs provider-specific fields to be precise)
        if self._is_deepseek_like(model):
            hit = int(usage.get("prompt_cache_hit_tokens", 0) or 0)
            miss = int(usage.get("prompt_cache_miss_tokens", 0) or 0)
            if (hit + miss) <= 0:
                miss = prompt_tokens
                hit = 0
            # V3.2 cache hit pricing per docs with +$0.25 margin -> $0.278 / 1M
            cache_hit_rate_per_m = 0.278
            cost = (hit / 1_000_000.0) * cache_hit_rate_per_m
            cost += (miss / 1_000_000.0) * float(price.get("input", 0.0))
            cost += ((completion_tokens + reasoning_gap) / 1_000_000.0) * float(price.get("output", 0.0))
            return float(cost)
        # OpenAI prompt caching: cached input tokens billed at 10% of input price by default
        # Allow per-model override via price["cached_input"] when provided
        if provider == "openai":
            cached_tokens = 0
            try:
                itd = usage.get("input_tokens_details") if isinstance(usage, dict) else None
                if isinstance(itd, dict):
                    cached_tokens = int(itd.get("cached_tokens", 0) or 0)
                else:
                    cached_tokens = int(usage.get("cached_input_tokens", 0) or 0)
            except Exception:
                cached_tokens = 0
            try:
                cached_tokens = max(0, min(int(cached_tokens), int(prompt_tokens)))
            except Exception:
                cached_tokens = 0
            non_cached = max(0, prompt_tokens - cached_tokens)
            in_rate = float(price.get("input", 0.0))
            try:
                cached_rate = float(price.get("cached_input", None)) if (price.get("cached_input", None) is not None) else (in_rate * 0.10)
            except Exception:
                cached_rate = in_rate * 0.10
            cost = (non_cached / 1_000_000.0) * in_rate
            cost += (cached_tokens / 1_000_000.0) * cached_rate
            cost += ((completion_tokens + reasoning_gap) / 1_000_000.0) * float(price.get("output", 0.0))
            return float(cost)
        # Gemini dynamic premium omitted for brevity; default pricing used.
        completion_total = completion_tokens
        if total_tokens and (prompt_tokens + completion_tokens) != total_tokens:
            completion_total += reasoning_gap
        else:
            if thinking_tokens and not usage.get("total_tokens"):
                completion_total += thinking_tokens
        cost = (prompt_tokens / 1_000_000.0) * float(price.get("input", 0.0)) + (completion_total / 1_000_000.0) * float(price.get("output", 0.0))
        return float(cost)

    # ----------------------- File logging -----------------------

    def _ensure_session_log(self) -> None:
        if not self.log_enabled:
            return
        try:
            self.log_dir.mkdir(parents=True, exist_ok=True)
            if not self.session_log_path:
                _now_utc = datetime.now(timezone.utc)
                ts = _now_utc.strftime("%Y%m%d-%H%M%S")
                fname = f"session-{ts}-{self._session_local_id[:8]}.jsonl"
                self.session_log_path = self.log_dir / fname
                # Write an initial header record
                hdr = {
                    "ts": _now_utc.isoformat().replace("+00:00", "Z"),
                    "event": "session.init",
                    "client": "henosis-cli",
                    "server": self.server,
                    "model": self.model,
                    "system_prompt": (self.system_prompt or None),
                    "tools": self._tools_label(),
                    "fs_scope": self._fs_label(),
                    "control_level": self.control_level,
                    "auto_approve": self.auto_approve,
                    "reasoning_effort": self.reasoning_effort,
                    "ctx_window": self.ctx_window,
                    "session_local_id": self._session_local_id,
                    "terminal_id": self.terminal_id,
                    "workspace_dir": self.local_workspace_dir,
                }
                with self.session_log_path.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(hdr, ensure_ascii=False) + "\n")
        except Exception:
            pass

    # ----------------------- Raw log helpers -----------------------
    def _ensure_raw_log(self) -> None:
        if not self.raw_log_enabled:
            return
        try:
            if self._rawlog_initialized and self.raw_log_path and self.raw_log_path.exists():
                return
            # Default to CWD when no explicit file provided
            if not self.raw_log_path:
                now = datetime.now(timezone.utc)
                ts = now.strftime("%Y%m%d-%H%M%S")
                fname = f"henosis_raw-{ts}-{self._session_local_id[:8]}.log"
                try:
                    base = Path(os.getcwd()).resolve()
                except Exception:
                    base = Path('.')
                self.raw_log_path = base / fname
            # Write header
            hdr_lines = [
                f"=== henosis-cli RAW LOG start {datetime.now(timezone.utc).isoformat().replace('+00:00','Z')} ===",
                f"server: {self.server}",
                f"api_base: {self.api_base}",
                f"model: {self.model or '(server default)'}",
                f"cwd: {os.getcwd()}",
            ]
            with self.raw_log_path.open('a', encoding='utf-8') as f:
                for ln in hdr_lines:
                    f.write(ln + "\n")
            self._rawlog_initialized = True
        except Exception:
            # Disable on failure to avoid repeated errors
            try:
                self.raw_log_enabled = False
            except Exception:
                pass

    def _rawlog_write(self, text: str) -> None:
        if not (self.raw_log_enabled):
            return
        try:
            self._ensure_raw_log()
            if self.raw_log_path:
                with self.raw_log_path.open('a', encoding='utf-8') as f:
                    ts = datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
                    f.write(f"[{ts}] {text}\n")
        except Exception:
            pass

    def _rawlog_write_json(self, obj: Any, prefix: Optional[str] = None) -> None:
        try:
            s = json.dumps(obj, ensure_ascii=False)
        except Exception:
            s = str(obj)
        if prefix:
            self._rawlog_write(prefix)
        # Write on its own line for easy grepping
        self._rawlog_write(s)

    # ----------------------- Thread naming -----------------------

    def _detect_project_name(self) -> str:
        # Priority order for project name detection:
        # 1) HENOSIS_PROJECT or HENOSIS_PROJECT_NAME env vars
        # 2) Git repo top-level directory name (if available)
        # 3) host_base setting (basename)
        # 4) Current working directory basename
        env_name = os.getenv("HENOSIS_PROJECT") or os.getenv("HENOSIS_PROJECT_NAME")
        if env_name and env_name.strip():
            return env_name.strip()
        # Try git
        try:
            import subprocess
            top = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], stderr=subprocess.DEVNULL).decode("utf-8").strip()
            if top:
                return os.path.basename(top)
        except Exception:
            pass
        # Host base
        if self.host_base:
            try:
                return os.path.basename(os.path.abspath(self.host_base))
            except Exception:
                pass
        # CWD
        try:
            return os.path.basename(os.getcwd()) or "project"
        except Exception:
            return "project"

    def _default_thread_name(self) -> str:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        project = self._detect_project_name()
        return f"{ts} - {project}"

    def _log_line(self, record: Dict[str, Any]) -> None:
        if not (self.log_enabled and self.session_log_path):
            return
        try:
            record = {"ts": datetime.now(timezone.utc).isoformat() + "Z", **record}
            with self.session_log_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception:
            pass

    # ----------------------- Threads save -----------------------

    async def _ensure_thread(self, client: httpx.AsyncClient) -> None:
        if not (self.save_chat_history and self.auth_user and not self.thread_uid):
            return
        try:
            # Refresh auto title at creation time if not manually set
            if not self._manual_title:
                self.thread_name = self._default_thread_name()
            r = await client.post(self.create_thread_url, json={"name": self.thread_name})
            if r.status_code == 200:
                data = r.json()
                self.thread_uid = data.get("thread_uid")
                self._log_line({"event": "thread.created", "thread_uid": self.thread_uid, "name": self.thread_name})
                if self.thread_uid:
                    self.ui.print(f"[saved] Created thread {self.thread_uid}", style=self.ui.theme["dim"])
        except Exception:
            pass

    async def _save_conversation(self, client: httpx.AsyncClient, selected_model: Optional[str]) -> None:
        if not (self.save_chat_history and self.auth_user and self.thread_uid):
            return
        try:
            payload = {
                "thread_uid": self.thread_uid,
                "thread_name": self.thread_name,
                "messages": self.messages_for_save,
                "paste_counter": 0,
                "selected_model": selected_model or self.model,
                "share_settings": None,
            }
            r = await client.post(self.save_convo_url, json=payload)
            if r.status_code == 200:
                self._log_line({"event": "thread.saved", "thread_uid": self.thread_uid, "message_count": len(self.messages_for_save)})
                self.ui.print(f"[saved] Conversation synced to server", style=self.ui.theme["dim"])
            else:
                self._log_line({"event": "thread.save_failed", "status": r.status_code, "body": r.text})
        except Exception as e:
            self._log_line({"event": "thread.save_exception", "error": str(e)})

    async def _commit_usage(self, client: httpx.AsyncClient, session_id: Optional[str], model_used: Optional[str], usage: Dict[str, Any]) -> None:
        if not (self.server_usage_commit and self.auth_user and session_id and model_used):
            return
        try:
            payload = {
                "session_id": session_id,
                "model": model_used,
                "usage": usage,
                "thread_uid": self.thread_uid,
                "meta": {"source": "henosis-cli"},
            }
            r = await client.post(self.commit_usage_url, json=payload)
            if r.status_code == 200:
                data = r.json()
                rem = data.get("remaining_credits")
                cost = data.get("cost_usd")
                sess_cum = data.get("session_cumulative") or {}
                sess_cum_cost = None
                try:
                    if isinstance(sess_cum, dict):
                        sess_cum_cost = float(sess_cum.get("cost_usd") or 0.0)
                except Exception:
                    sess_cum_cost = None
                self._log_line({"event": "usage.commit_ok", "server": True, "cost_usd": cost, "remaining_credits": rem, "session_cumulative": sess_cum})
                # Print authoritative server cost line only
                try:
                    cost_f = float(cost or 0.0)
                except Exception:
                    cost_f = 0.0
                # If server provided cumulative, prefer that for display; otherwise derive from running sum
                # Always accumulate locally across CLI turns. The server's session_cumulative in this endpoint
                # is scoped to the per-stream session_id (a new one each turn), so it is not a chat-session total.
                self.server_cumulative_cost_usd += cost_f
                # Store last commit details for Usage & Info box rendering
                self._last_commit_cost_usd = cost_f
                # Normalize remaining credits to float when possible
                try:
                    if rem is not None:
                        self._last_remaining_credits = float(rem)
                except Exception:
                    pass
                self._last_commit_model = model_used or None
            else:
                self._log_line({"event": "usage.commit_failed", "status": r.status_code, "body": r.text})
        except Exception as e:
            self._log_line({"event": "usage.commit_exception", "error": str(e)})

    async def check_auth(self) -> bool:
        """Check current auth status using stored cookies; set self.auth_user on success."""
        try:
            # Log a compact summary of cookies relevant to auth before any calls
            try:
                access = self.cookies.get("access_token_cookie")
                refresh = self.cookies.get("refresh_token_cookie")
                self.ui.debug_log(
                    f"[auth-cli] check_auth: start access={'set' if access else 'missing'}, refresh={'set' if refresh else 'missing'}"
                )
            except Exception:
                pass
            # Build an SSE-friendly timeout config when no explicit timeout provided
            if self.timeout is None:
                http_timeout = httpx.Timeout(connect=10.0, read=None, write=10.0, pool=10.0)
            else:
                http_timeout = httpx.Timeout(self.timeout)

            async with httpx.AsyncClient(timeout=http_timeout, cookies=self.cookies) as client:
                # First try to refresh tokens to ensure they're current
                try:
                    if self.cookies.get('refresh_token_cookie'):
                        self.ui.debug_log("[auth-cli] check_auth: calling /refresh before /check-auth")
                        refresh_resp = await client.post(self.refresh_url, timeout=30.0)
                        if refresh_resp.status_code == 200:
                            data = refresh_resp.json()
                            # If token was rotated, persist the new one
                            if data.get('rotated'):
                                self.ui.debug_log("[auth-cli] check_auth: refresh rotated token; saving state")
                                self._save_auth_state_to_disk()
                        else:
                            self.ui.debug_log(
                                f"[auth-cli] check_auth: /refresh returned {refresh_resp.status_code}: {refresh_resp.text[:200]}"
                            )
                except Exception:
                    pass  # Non-fatal; proceed with check-auth
                
                self.ui.debug_log("[auth-cli] check_auth: calling /check-auth")
                resp = await client.get(self.check_auth_url)
                if resp.status_code == 200:
                    data = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
                    if data.get("authenticated"):
                        self.auth_user = str(data.get("user") or "")
                        try:
                            access_after = self.cookies.get("access_token_cookie")
                            refresh_after = self.cookies.get("refresh_token_cookie")
                            self.ui.debug_log(
                                f"[auth-cli] check_auth: authenticated as {self.auth_user!r}, access={'set' if access_after else 'missing'}, refresh={'set' if refresh_after else 'missing'}"
                            )
                        except Exception:
                            pass
                        return True
                    # Explicitly unauthenticated
                    self.auth_user = None
                    self.ui.debug_log("[auth-cli] check_auth: /check-auth returned authenticated=False")
                    return False
                # Non-200 usually means unauthenticated or endpoint disabled
                self.auth_user = None
                try:
                    self.ui.debug_log(
                        f"[auth-cli] check_auth: /check-auth returned {resp.status_code}: {resp.text[:200]}"
                    )
                except Exception:
                    pass
                return False
        except Exception:
            # If auth endpoints disabled or network error, treat as unauthenticated
            self.auth_user = None
            try:
                self.ui.debug_log("[auth-cli] check_auth: exception; treating as unauthenticated")
            except Exception:
                pass
            return False

    # ----------------------- Settings persistence -----------------------

    def load_settings(self) -> None:
        """Load local settings (legacy JSON) as defaults. Server settings will override after auth."""
        settings_path = self.settings_file
        if not settings_path.exists():
            legacy = Path.home() / ".fastapi_cli_settings.json"
            if legacy.exists():
                settings_path = legacy
                self._settings_migrated = True
        if not settings_path.exists():
            return
        try:
            with open(settings_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._apply_settings_dict(data)
        except Exception as e:
            self.ui.warn(f"Failed to load local settings: {e}")

    def _collect_settings_dict(self) -> Dict[str, Any]:
        data = {
            "model": self.model,
            "requested_tools": self.requested_tools,
            "fs_scope": self.fs_scope,
            # host_base is per-terminal by default; only persist if explicitly set by the user
            "save_chat_history": self.save_chat_history,
            "fs_host_mode": self.fs_host_mode,
            "system_prompt": self.system_prompt,
            "show_tool_calls": self.show_tool_calls,
            "max_dir_items": self.max_dir_items,
            "control_level": self.control_level,
            "auto_approve": self.auto_approve,
            "trust_tools_always": self.trust_tools_always,
            "trust_tools_session": self.trust_tools_session,
            "trust_cmds_always": self.trust_cmds_always,
            "trust_cmds_session": self.trust_cmds_session,
            "inject_codebase_map": self.inject_codebase_map,
            "preflight_enabled": self.preflight_enabled,
            # local-only preferences
            "telemetry_enabled": self.telemetry_enabled,
            "output_format": self.output_format,
            # Usage & Info panel mode
            "usage_info_mode": self.usage_info_mode,
            # reasoning effort
            "reasoning_effort": self.reasoning_effort,
            # retain provider-native tool results
            "retain_native_tool_results": self.retain_native_tool_results,
            # Anthropic thinking budget
            "thinking_budget_tokens": self.thinking_budget_tokens,
            # Anthropic cache TTL preference
            "anthropic_cache_ttl": self.anthropic_cache_ttl,
            # web search
            "web_search_enabled": self.web_search_enabled,
            "web_search_allowed_domains": self.web_search_allowed_domains,
            "web_search_include_sources": self.web_search_include_sources,
            "web_search_location": self.web_search_location,
            # verbosity & preambles & custom first-turn injection
            "text_verbosity": self.text_verbosity,
            "preambles_enabled": self.preambles_enabled,
            "custom_first_turn_enabled": self.custom_first_turn_enabled,
            "custom_first_turn_text": self.custom_first_turn_text,
            "codex_prompt_enabled": self.codex_prompt_enabled,
        }
        try:
            if not getattr(self, "_host_base_ephemeral", False) and self.host_base:
                data["host_base"] = self.host_base
        except Exception:
            pass
        return data

    def _apply_settings_dict(self, data: Dict[str, Any]) -> None:
        try:
            self.model = data.get("model", self.model)
            if "save_chat_history" in data:
                try:
                    self.save_chat_history = bool(data.get("save_chat_history"))
                except Exception:
                    pass
            self.requested_tools = data.get("requested_tools", self.requested_tools)
            self.fs_scope = data.get("fs_scope", self.fs_scope)
            self.host_base = data.get("host_base", self.host_base)
            self.fs_host_mode = data.get("fs_host_mode", self.fs_host_mode)
            self.system_prompt = data.get("system_prompt", self.system_prompt)
            self.show_tool_calls = data.get("show_tool_calls", self.show_tool_calls)
            self.max_dir_items = data.get("max_dir_items", self.max_dir_items)
            self.control_level = data.get("control_level", self.control_level)
            self.auto_approve = data.get("auto_approve", self.auto_approve) or []
            if "web_search_enabled" in data:
                try:
                    self.web_search_enabled = bool(data.get("web_search_enabled"))
                except Exception:
                    self.web_search_enabled = False
            if "web_search_allowed_domains" in data:
                domains = data.get("web_search_allowed_domains")
                if isinstance(domains, list):
                    cleaned_domains: List[str] = []
                    for dom in domains:
                        if isinstance(dom, str):
                            s = dom.strip()
                            if s:
                                cleaned_domains.append(s)
                    self.web_search_allowed_domains = cleaned_domains
            if "web_search_include_sources" in data:
                try:
                    self.web_search_include_sources = bool(data.get("web_search_include_sources"))
                except Exception:
                    self.web_search_include_sources = False
            if "web_search_location" in data:
                loc = data.get("web_search_location")
                if isinstance(loc, dict):
                    cleaned_loc: Dict[str, str] = {}
                    for key, value in loc.items():
                        if isinstance(key, str) and isinstance(value, str):
                            v = value.strip()
                            if v:
                                cleaned_loc[key.strip()] = v
                    self.web_search_location = cleaned_loc
                else:
                    self.web_search_location = {}
            # Trust registries
            self.trust_tools_always = data.get("trust_tools_always", []) or []
            self.trust_tools_session = data.get("trust_tools_session", []) or []
            self.trust_cmds_always = data.get("trust_cmds_always", []) or []
            self.trust_cmds_session = data.get("trust_cmds_session", []) or []
            # Codebase map injection toggle
            if "inject_codebase_map" in data:
                try:
                    self.inject_codebase_map = bool(data.get("inject_codebase_map"))
                except Exception:
                    pass
            # Preflight toggle
            if "preflight_enabled" in data:
                try:
                    self.preflight_enabled = bool(data.get("preflight_enabled"))
                except Exception:
                    pass
            # Local-only prefs
            if "telemetry_enabled" in data:
                self.telemetry_enabled = data.get("telemetry_enabled")
            if "output_format" in data:
                self.output_format = data.get("output_format")
            # Usage & Info panel mode
            if "usage_info_mode" in data:
                try:
                    val = str(data.get("usage_info_mode") or "").strip().lower()
                    if val in ("concise", "verbose"):
                        self.usage_info_mode = val
                except Exception:
                    pass
            # Reasoning effort (default medium if missing/invalid)
            try:
                val = data.get("reasoning_effort")
                if isinstance(val, str) and val in ("low", "medium", "high"):
                    self.reasoning_effort = val
            except Exception:
                pass
            # Text verbosity selector
            try:
                v = data.get("text_verbosity")
                if isinstance(v, str) and v in ("low", "medium", "high"):
                    self.text_verbosity = v
            except Exception:
                pass
            # Tool preambles toggle
            if "preambles_enabled" in data:
                try:
                    self.preambles_enabled = bool(data.get("preambles_enabled"))
                except Exception:
                    self.preambles_enabled = False
            if "codex_prompt_enabled" in data:
                try:
                    self.codex_prompt_enabled = bool(data.get("codex_prompt_enabled"))
                except Exception:
                    self.codex_prompt_enabled = True
            # Custom first-turn injection
            if "custom_first_turn_enabled" in data:
                try:
                    self.custom_first_turn_enabled = bool(data.get("custom_first_turn_enabled"))
                except Exception:
                    self.custom_first_turn_enabled = False
            if "custom_first_turn_text" in data:
                try:
                    txt = data.get("custom_first_turn_text")
                    if isinstance(txt, str):
                        self.custom_first_turn_text = txt
                except Exception:
                    pass
            # retain provider-native tool results
            if "retain_native_tool_results" in data:
                try:
                    self.retain_native_tool_results = bool(data.get("retain_native_tool_results"))
                except Exception:
                    self.retain_native_tool_results = False
            # Anthropic thinking budget tokens
            try:
                tbt = data.get("thinking_budget_tokens")
                if isinstance(tbt, int) and tbt > 0:
                    self.thinking_budget_tokens = int(tbt)
                elif tbt in (None, "", 0, "0", "default"):
                    self.thinking_budget_tokens = None
            except Exception:
                pass
            # Anthropic cache TTL preference
            try:
                ttl = data.get("anthropic_cache_ttl")
                if isinstance(ttl, str) and ttl.strip() in ("5m", "1h"):
                    self.anthropic_cache_ttl = ttl.strip()
                elif ttl in (None, "", "default"):
                    self.anthropic_cache_ttl = None
            except Exception:
                pass
            # Rebuild history if system prompt changed
            self.history = []
            if self.system_prompt:
                self.history.append({"role": "system", "content": self.system_prompt})
            # On settings load, do not assume the custom first-turn was injected yet
            try:
                self._did_inject_custom_first_turn = False
            except Exception:
                pass
            self._apply_model_side_effects()
        except Exception as e:
            self.ui.warn(f"Failed to apply settings: {e}")

    async def _fetch_server_settings(self) -> Optional[Dict[str, Any]]:
        try:
            timeout = httpx.Timeout(connect=10.0, read=20.0, write=10.0, pool=10.0) if self.timeout is None else httpx.Timeout(self.timeout)
            params = {}
            if self.device_id:
                params["device_id"] = self.device_id
            async with httpx.AsyncClient(timeout=timeout, cookies=self.cookies) as client:
                r = await client.get(self.cli_settings_url, params=params)
                if r.status_code == 200 and r.headers.get("content-type", "").startswith("application/json"):
                    obj = r.json()
                    st = obj.get("settings")
                    if isinstance(st, dict):
                        return st
                return None
        except Exception:
            return None

    async def _save_server_settings(self, settings: Optional[Dict[str, Any]] = None) -> bool:
        try:
            timeout = httpx.Timeout(connect=10.0, read=20.0, write=10.0, pool=10.0) if self.timeout is None else httpx.Timeout(self.timeout)
            payload = {
                "settings": settings if isinstance(settings, dict) else self._collect_settings_dict(),
                "device_id": self.device_id,
                "device_name": self.device_name,
            }
            async with httpx.AsyncClient(timeout=timeout, cookies=self.cookies) as client:
                r = await client.post(self.cli_settings_url, json=payload)
                return r.status_code == 200
        except Exception:
            return False

    async def _sync_settings_with_server(self) -> None:
        """On first authenticated run: if server has settings, apply them; else upload local defaults."""
        # Try to load server settings
        st = await self._fetch_server_settings()
        if isinstance(st, dict) and st:
            try:
                self.ui.debug_log(
                    f"[settings-cli] sync: applying server settings user={self.auth_user!r} "
                    f"device_id={self.device_id!r} keys={sorted(st.keys())}"
                )
            except Exception:
                pass
            self._apply_settings_dict(st)
            self.ui.print("[settings] Loaded from server.", style=self.ui.theme["dim"])		
            return
        # No server settings: upload current local state
        try:
            self.ui.debug_log(
                f"[settings-cli] sync: no server settings; initializing user={self.auth_user!r} "
                f"device_id={self.device_id!r} model={self.model!r} tools={self.requested_tools!r} "
                f"fs_scope={self.fs_scope!r} level={self.control_level!r} host_base={self.host_base!r}"
            )
        except Exception:
            pass
        ok = await self._save_server_settings()
        if ok:
            self.ui.print("[settings] Initialized on server.", style=self.ui.theme["dim"])		
        else:
            self.ui.warn("[settings] Failed to initialize settings on server; continuing with local defaults.")

    async def _load_profile_for_tier(self) -> None:
        """Best-effort load of the user's subscription tier via /profile.

        Populates self.subscription_tier, self.subscription_status, and self.is_free_tier.
        Fails quietly so older servers without /profile continue to work.
        """
        try:
            # Build /profile URL relative to the same API base used for chat/settings.
            profile_url = join_url(self.api_base, "/profile")
        except Exception:
            return
        try:
            timeout = (
                httpx.Timeout(connect=10.0, read=20.0, write=10.0, pool=10.0)
                if self.timeout is None
                else httpx.Timeout(self.timeout)
            )
        except Exception:
            timeout = httpx.Timeout(10.0)
        try:
            async with httpx.AsyncClient(timeout=timeout, cookies=self.cookies) as client:
                r = await client.get(profile_url)
                if r.status_code != 200 or not r.headers.get("content-type", "").startswith("application/json"):
                    return
                obj = r.json()
        except Exception:
            return
        try:
            user = obj.get("user") if isinstance(obj, dict) else None
            if not isinstance(user, dict):
                return
            tier = user.get("subscription_tier")
            status = user.get("subscription_status")
            self.subscription_tier = str(tier) if tier is not None else None
            self.subscription_status = str(status) if status is not None else None
            tier_lower = str(tier).strip().lower() if tier is not None else ""
            status_lower = str(status).strip().lower() if status is not None else ""
            # Treat explicit "free" tier (and absence of any active subscription) as free-tier.
            is_free = False
            if tier_lower in ("free", "free_tier", "free-tier"):
                is_free = True
            elif not tier_lower and status_lower in ("none", "free", "trial", "inactive"):
                is_free = True
            self.is_free_tier = is_free
            # Extract remaining credits if available
            try:
                c = user.get("credits")
                tc = user.get("tier_monthly_credits")
                found = False
                val = 0.0
                if c is not None:
                    val += float(c)
                    found = True
                if tc is not None:
                    val += float(tc)
                    found = True
                if found:
                    self._last_remaining_credits = val
                try:
                    self.ui.debug_log(f"[profile-cli] credits check: c={c} tc={tc} -> {self._last_remaining_credits}")
                except Exception:
                    pass
            except Exception:
                pass
            try:
                self.ui.debug_log(
                    f"[profile-cli] loaded profile tier={self.subscription_tier!r} "
                    f"status={self.subscription_status!r} is_free_tier={self.is_free_tier!r} credits={self._last_remaining_credits}"
                )
            except Exception:
                pass
        except Exception:
            # Do not treat profile parsing errors as fatal
            return

    def save_settings(self) -> None:
        """Persist settings to the server in the background. Fallback to local file only if needed."""
        # Fire-and-forget background task when running inside an event loop
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self._save_server_settings())
                return
        except Exception:
            pass
        # Fallback: best-effort synchronous save
        try:
            asyncio.run(self._save_server_settings())
        except Exception:
            pass

    # ----------------------- Codebase map loader ------------------------

    def _load_codebase_map_raw(self) -> Optional[str]:
        """Locate CODEBASE_MAP.md content for first-turn injection.

        Preference order (all best-effort, quiet on failure):
        1) Under the configured Agent scope / host_base (CODEBASE_MAP.md or codebase_map.md).
        2) Under the current working directory (common when running from a project checkout).
        3) Next to this cli.py file (only when the map is shipped with the installed package).
        """
        roots: List[Path] = []
        # 1) Agent scope / host_base
        try:
            if isinstance(self.host_base, str) and self.host_base.strip():
                roots.append(Path(self.host_base).expanduser().resolve())
        except Exception:
            pass
        # 2) Current working directory
        try:
            roots.append(Path(os.getcwd()).resolve())
        except Exception:
            pass

        for root in roots:
            try:
                p1 = root / "CODEBASE_MAP.md"
                p2 = root / "codebase_map.md"
                if p1.exists():
                    return p1.read_text(encoding="utf-8", errors="ignore")
                if p2.exists():
                    return p2.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

        # 3) Package-local fallback (may not exist when installed from wheel)
        try:
            p = Path(__file__).resolve().parent / "CODEBASE_MAP.md"
            if p.exists():
                return p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            pass
        return None

    def _session_overview(self) -> str:
        """Build a one-line status bar of session settings"""
        parts = [
            f"Server: {self.server}",
            f"Model: {self.model or '(server default)'}",
            f"Tools: {self._tools_label()}",
            f"History: {'ON' if self.save_chat_history else 'OFF'}",
            f"Scope: {self._fs_label()}",
            f"Agent scope: {self.host_base or '(none)'}",
            f"Level: {self.control_level or '(default)'}",
            f"Auto-approve: {','.join(self.auto_approve) if self.auto_approve else '(none)'}",
            f"Reasoning: {self.reasoning_effort}",
            f"ThinkBudget: {self.thinking_budget_tokens if self.thinking_budget_tokens else 'default'}",
            f"WebSearch: {'ON' if self.web_search_enabled else 'OFF'}",
            f"Map Prefix: {'ON' if self.inject_codebase_map else 'OFF'}",
        ]
        return " | ".join(parts)

    # ----------------------- Auth state persistence ---------------------

    def _load_auth_state_from_disk(self) -> bool:
        """Load persisted cookies from disk if present. Returns True if any were loaded."""
        try:
            p = self.auth_state_file
            if not p.exists():
                # No persisted auth yet; normal on first run
                try:
                    self.ui.debug_log(f"[auth-cli] no auth state file at {p}")
                except Exception:
                    pass
                return False
            data = json.loads(p.read_text(encoding="utf-8"))
            # Load persisted device identity if present
            did = data.get("device_id")
            if isinstance(did, str) and did.strip():
                self.device_id = did.strip()
            dname = data.get("device_name")
            if isinstance(dname, str) and dname.strip():
                self.device_name = dname.strip()
            cookies = data.get("cookies") or []
            loaded_any = False
            # Clear current jar first
            self.cookies.clear()
            for c in cookies:
                try:
                    name = str(c.get("name"))
                    value = str(c.get("value"))
                    domain = c.get("domain") or None
                    path = c.get("path") or "/"
                    # httpx Cookies.set accepts domain/path kwargs
                    if name and value is not None:
                        self.cookies.set(name, value, domain=domain, path=path)
                        loaded_any = True
                except Exception:
                    continue
            # Best-effort: set cached username for UI hint
            au = data.get("auth_user")
            if isinstance(au, str) and au.strip():
                self.auth_user = au.strip()
            try:
                self.ui.debug_log(
                    f"[auth-cli] loaded auth state: user={self.auth_user!r}, device_id={self.device_id!r}, cookies={len(cookies)}"
                )
            except Exception:
                pass
            return loaded_any
        except Exception:
            # Corrupt or unreadable auth state; ignore and start clean
            try:
                self.ui.debug_log("[auth-cli] failed to load auth state from disk; ignoring")
            except Exception:
                pass
            return False

    def _save_auth_state_to_disk(self) -> None:
        """Persist current cookie jar and username to disk."""
        try:
            jar_list = []
            # httpx Cookies jar contains Cookie objects
            jar = getattr(self.cookies, "jar", [])
            # Iterate and extract all cookie data
            try:
                iter_cookies = iter(jar)
            except Exception:
                iter_cookies = []
            for c in iter_cookies:
                try:
                    # Ensure we capture expiration if present
                    cookie_data = {
                        "name": getattr(c, "name", ""),
                        "value": getattr(c, "value", ""),
                        "domain": getattr(c, "domain", None),
                        "path": getattr(c, "path", "/"),
                    }
                    # Add expires if available (as ISO string for JSON)
                    expires = getattr(c, "expires", None)
                    if expires:
                        try:
                            if isinstance(expires, (int, float)):
                                from datetime import datetime, timezone
                                exp_dt = datetime.fromtimestamp(float(expires), tz=timezone.utc)
                                cookie_data["expires"] = exp_dt.isoformat()
                            elif hasattr(expires, 'isoformat'):
                                cookie_data["expires"] = expires.isoformat()
                        except Exception:
                            pass
                    jar_list.append(cookie_data)
                except Exception:
                    continue
            payload = {
                "server": self.server,
                "auth_user": self.auth_user,
                "device_id": self.device_id,
                "device_name": self.device_name,
                "saved_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "cookies": jar_list,
            }
            self.auth_state_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            try:
                self.ui.debug_log(
                    f"[auth-cli] saved auth state: user={self.auth_user!r}, device_id={self.device_id!r}, cookies={len(jar_list)} to {self.auth_state_file}"
                )
            except Exception:
                pass
        except Exception:
            # Non-fatal
            pass

    def _clear_auth_state_on_disk(self) -> None:
        try:
            if self.auth_state_file.exists():
                self.auth_state_file.unlink()
                try:
                    self.ui.debug_log(f"[auth-cli] cleared auth state file {self.auth_state_file}")
                except Exception:
                    pass
        except Exception:
            pass

    # -------------------------- Menu helpers ---------------------------

    def _tools_label(self) -> str:
        if self.requested_tools is True:
            return "ON (per request)"
        if self.requested_tools is False:
            return "OFF (per request)"
        return "SERVER DEFAULT"

    def _fs_label(self) -> str:
        if self.fs_scope is None:
            return "SERVER DEFAULT"
        return self.fs_scope.upper()

    def _build_commands_catalog(self) -> List[Dict[str, str]]:
        cmds = [
            {"name": "/settings", "usage": "/settings", "desc": "Open settings menu"},
            {"name": "/configure", "usage": "/configure", "desc": "Run configuration wizard now"},
            {"name": "/history", "usage": "/history on|off", "desc": "Toggle saving chat history to unified memory"},
            {"name": "/infomode", "usage": "/infomode concise|verbose", "desc": "Set Usage & Info panel mode"},
            {"name": "/tools", "usage": "/tools on|off|default", "desc": "Toggle per-request tools"},
            {"name": "/websearch", "usage": "/websearch on|off|domains|sources|location", "desc": "Configure OpenAI web search"},
            {"name": "/reasoning", "usage": "/reasoning low|medium|high", "desc": "Set OpenAI reasoning effort (default: medium)"},
            {"name": "/thinkingbudget", "usage": "/thinkingbudget <tokens>|default", "desc": "Set Anthropic thinking budget tokens for -thinking models"},
            {"name": "/fs", "usage": "/fs workspace|host|default", "desc": "Set filesystem scope"},
            {"name": "/agent-scope", "usage": "/agent-scope <absolute path>", "desc": "Alias for /hostbase (set Agent scope)"},
            {"name": "/hostmode", "usage": "/hostmode any|cwd|custom", "desc": "Set host directory mode (client-enforced roots)"},
            {"name": "/trust", "usage": "/trust", "desc": "Manage Level 2 trust (tools/commands)"},
            {"name": "/model", "usage": "/model [name]", "desc": "Open settings model picker (no arg) or set directly"},
            {"name": "/level", "usage": "/level 1|2|3", "desc": "Set control level"},
            {"name": "/autoapprove", "usage": "/autoapprove name1,name2", "desc": "Auto-approve tools at L2"},
            {"name": "/system", "usage": "/system <text>", "desc": "Set system prompt"},
            {"name": "/title", "usage": "/title <name>", "desc": "Set thread title"},
            {"name": "/clear", "usage": "/clear", "desc": "Clear chat history"},
            {"name": "/toolslog", "usage": "/toolslog", "desc": "Toggle tool call logs"},
            {"name": "/map", "usage": "/map on|off", "desc": "Toggle codebase map prefix"},
            {"name": "/login", "usage": "/login", "desc": "Log in"},
            {"name": "/logout", "usage": "/logout", "desc": "Log out"},
            {"name": "/whoami", "usage": "/whoami", "desc": "Show authentication status"},
        ]
        return cmds

    def _model_presets(self) -> List[Tuple[str, str]]:
        """Shared list of (model, label) used by settings UI and /model menu."""
        return [
            ("gpt-5.1", "OpenAI: gpt-5.1"),
            ("gpt-5", "OpenAI: gpt-5"),
            ("gpt-5-codex", "OpenAI: gpt-5-codex"),
            ("gpt-5.1-codex", "OpenAI: gpt-5.1-codex"),
            ("gpt-5.1-codex-max", "OpenAI: gpt-5.1-codex-max"),
            ("gpt-5.1-mini", "OpenAI: gpt-5.1-mini"),
            ("gpt-5-pro", "OpenAI: gpt-5-pro (non-streaming, very expensive)"),
            ("gpt-5-mini-2025-08-07", "OpenAI: gpt-5-mini-2025-08-07"),
            ("codex-mini-latest", "OpenAI: codex-mini-latest (fast reasoning)"),
            ("deepseek-chat-3.2", "DeepSeek: deepseek-chat 3.2"),
            ("deepseek-reasoner-3.2", "DeepSeek: deepseek-reasoner 3.2"),
            ("deepseek-3.2-speciale", "DeepSeek: deepseek 3.2 Speciale (no tools)"),
            ("kimi-k2-thinking", "Kimi: kimi-k2-thinking"),
            ("kimi-k2-0905-preview", "Kimi: kimi-k2-0905-preview"),
            ("gemini-2.5-pro", "Gemini: gemini-2.5-pro"),
            ("gemini-2.5-flash", "Gemini: gemini-2.5-flash"),
            ("gemini-3-pro-preview", "Gemini: gemini-3-pro-preview"),
            ("grok-4-1-fast-reasoning", "xAI: grok-4-1-fast-reasoning"),
            ("grok-4-1-fast-non-reasoning", "xAI: grok-4-1-fast-non-reasoning"),
            ("grok-4", "xAI: grok-4"),
            ("grok-code-fast-1", "xAI: grok-code-fast-1"),
            ("claude-haiku-4-5-20251001", "Anthropic: claude-haiku-4-5-20251001 (thinking OFF)"),
            ("claude-haiku-4-5-20251001-thinking", "Anthropic: claude-haiku-4-5-20251001 (thinking ON)"),
            ("claude-sonnet-4-5-20250929", "Anthropic: claude-sonnet-4-5-20250929 (thinking OFF)"),
            ("claude-sonnet-4-5-20250929-thinking", "Anthropic: claude-sonnet-4-5-20250929 (thinking ON)"),
            ("claude-opus-4-1-20250805", "Anthropic: claude-opus-4-1-20250805 (thinking OFF)"),
            ("claude-opus-4-1-20250805-thinking", "Anthropic: claude-opus-4-1-20250805 (thinking ON)"),
            ("claude-opus-4-5-20251101", "Anthropic: claude-opus-4-5-20251101 (thinking OFF)"),
            ("claude-opus-4-5-20251101-thinking", "Anthropic: claude-opus-4-5-20251101 (thinking ON)"),
            ("glm-4.6", "GLM: glm-4.6"),
        ]

    async def open_settings(self, focus: Optional[str] = None) -> None:
        """Open the new dependency-free settings UI. Falls back to legacy only when
        HENOSIS_SETTINGS_LEGACY=1 is set or the UI module is unavailable.
        """
        use_legacy = os.getenv("HENOSIS_SETTINGS_LEGACY", "").strip() in ("1", "true", "yes")
        if (not HAS_SETTINGS_UI) or use_legacy:
            # Legacy path: use the old menu loop
            while True:
                choice = await self.main_menu()
                try:
                    cont = await self.handle_choice(choice)
                except SystemExit:
                    raise
                except Exception as e:
                    self.ui.error(f"[menu error] {e}")
                    cont = True
                if not cont:
                    break
            return

        # Build defaults map for reset behavior
        defaults: Dict[str, Any] = {
            "model": None,
            "requested_tools": None,
            "fs_scope": None,
            "host_base": None,
            "fs_host_mode": None,
            "system_prompt": None,
            "show_tool_calls": True,
            "max_dir_items": 12,
            "control_level": None,
            "auto_approve": [],
            "trust_tools_always": [],
            "trust_tools_session": [],
            "trust_cmds_always": [],
            "trust_cmds_session": [],
            "inject_codebase_map": True,
            "preflight_enabled": False,
            "telemetry_enabled": None,
            "output_format": None,
            "usage_info_mode": "verbose",
            "reasoning_effort": "medium",
            "retain_native_tool_results": False,
            "thinking_budget_tokens": None,
            "anthropic_cache_ttl": None,
            "web_search_enabled": False,
            "web_search_allowed_domains": [],
            "web_search_include_sources": False,
            "web_search_location": {},
        }
        initial = self._collect_settings_dict()

        # Model presets list (shared)
        model_presets: List[Tuple[str, str]] = self._model_presets()
        # Reorder with a Recommended section at the top. Avoid decorative symbols; instead,
        # annotate recommended models with plain text for clarity.
        # Recommended set per request: opus 4-5 (no thinking), gemini 3, gpt 5, kimi k2 thinking,
        # grok code fast 1, and deepseek reasoner 3.2
        rec_keys = {
            "deepseek-reasoner-3.2",
            "claude-opus-4-5-20251101",
            "gemini-3-pro-preview",
            "gpt-5",
            "kimi-k2-thinking",
            "grok-code-fast-1",
            "gpt-5.1-codex-max",
        }
        rec_list: List[Tuple[str, str]] = [(m, lbl) for (m, lbl) in model_presets if m in rec_keys]
        other_list: List[Tuple[str, str]] = [(m, lbl) for (m, lbl) in model_presets if m not in rec_keys]
        # Build enum options in the order: Server default, Recommended, Others, Custom
        model_enum_options: List[Optional[str]] = [None] + [m for (m, _l) in rec_list] + [m for (m, _l) in other_list] + ["custom"]
        # Build render map without any star/marker characters; use a simple "(recommended)" suffix
        # for recommended models EXCEPT DeepSeek Reasoner 3.2, which should not display the suffix.
        render_map: Dict[Any, str] = {None: "Server default"}
        for m, lbl in rec_list:
            if m == "deepseek-reasoner-3.2":
                render_map[m] = lbl
            else:
                render_map[m] = f"{lbl} (recommended)"
        for m, lbl in other_list:
            render_map[m] = lbl
        render_map["custom"] = "Custom..."

        # Build items schema
        items: List[Dict[str, Any]] = [
            {"label": "General", "type": "group", "items": [
                {
                    "id": "save_chat_history",
                    "label": "Save to unified memory",
                    "type": "bool",
                    "description": "When ON, chats sync to your account and appear in the web portal. When OFF, chats are ephemeral (local only)."
                },
                {
                    "id": "model",
                    "label": "Model",
                    "type": "enum",
                    "options": model_enum_options,
                    "render": render_map,
                },
                {"id": "system_prompt", "label": "System prompt", "type": "multiline"},
                {"id": "usage_info_mode", "label": "Usage panel", "type": "enum", "options": ["concise", "verbose"], "render": {"concise": "Concise", "verbose": "Verbose"}},
                {"id": "text_verbosity", "label": "Text verbosity", "type": "enum", "options": ["low", "medium", "high"], "render": {"low": "Low", "medium": "Medium", "high": "High"}},
            ]},
            {"label": "Tools & Security", "type": "group", "items": [
                {
                    "id": "requested_tools",
                    "label": "Tools",
                    "type": "enum",
                    "options": [None, True, False],
                    "render": {None: "Server default", True: "ON", False: "OFF"},
                },
                {
                    "id": "control_level",
                    "label": "Control level",
                    "type": "enum",
                    "options": [None, 1, 2, 3],
                    "render": {None: "Server default", 1: "1 (read)", 2: "2 (approval)", 3: "3 (full)"},
                },
                {"id": "auto_approve", "label": "Auto-approve tools (comma)", "type": "text"},
                {"id": "show_tool_calls", "label": "Show tool call logs", "type": "bool"},
                {"id": "reasoning_effort", "label": "OpenAI reasoning effort", "type": "enum", "options": (["low", "medium", "high", "xhigh"] if self._is_codex_max(self.model) else ["low", "medium", "high"]), "render": {"low": "Low", "medium": "Medium", "high": "High", "xhigh": "XHigh (Codex Max)"}},
                {"id": "retain_native_tool_results", "label": "Retain provider-native tool results across turns", "type": "bool"},
                {"id": "thinking_budget_tokens", "label": "Anthropic thinking budget (tokens)", "type": "int"},
                {"id": "anthropic_cache_ttl", "label": "Anthropic prompt cache TTL", "type": "enum", "options": [None, "5m", "1h"], "render": {None: "Server default (5m)", "5m": "5 minutes (lower write cost)", "1h": "1 hour (higher write cost)"}},
                # Agent scope & filesystem controls
                {"id": "host_base", "label": "Agent scope directory", "type": "text"},
                {
                    "id": "fs_scope",
                    "label": "Filesystem scope",
                    "type": "enum",
                    "options": [None, "workspace", "host"],
                    "render": {
                        None: "Server default",
                        "workspace": "Workspace (sandbox)",
                        "host": "Host (Agent scope)",
                    },
                },
                {
                    "id": "fs_host_mode",
                    "label": "Host mode",
                    "type": "enum",
                    "options": [None, "any", "cwd", "custom"],
                    "render": {
                        None: "Server default / any",
                        "any": "any (no extra client restriction)",
                        "cwd": "Current working directory",
                        "custom": "Custom (use Agent scope)",
                    },
                },
            ]},
            {"label": "Code Map", "type": "group", "items": [
                {"id": "inject_codebase_map", "label": "Inject codebase map on first turn", "type": "bool"},
            ]},
            {"label": "Preambles & First-turn", "type": "group", "items": [
                {"id": "preambles_enabled", "label": "Enable tool call preambles (supported models only)", "type": "bool"},
                {"id": "custom_first_turn_enabled", "label": "Enable custom first-turn injection", "type": "bool"},
                {"id": "custom_first_turn_text", "label": "Custom first-turn text", "type": "multiline"},
                {"id": "codex_prompt_enabled", "label": "Inject Codex developer system prompt (Codex models only)", "type": "bool"},
            ]},
            {"label": "Web search", "type": "group", "items": [
                {"id": "web_search_enabled", "label": "Enable web search (OpenAI)", "type": "bool"},
                {"id": "web_search_allowed_domains", "label": "Allowed domains (comma)", "type": "text"},
                {"id": "web_search_include_sources", "label": "Include sources in response", "type": "bool"},
                {"id": "web_search_location", "label": "Location hint (key=value pairs)", "type": "text"},
            ]},
        ]

        # Prepare initial values with enum placeholder for model when custom text set
        init_for_ui = dict(initial)
        if isinstance(init_for_ui.get("model"), str) and init_for_ui["model"] not in [m for m, _ in model_presets]:
            # Represent as 'custom' for cycling, but keep original model in working copy for edit with 'e'
            pass  # We'll keep exact model string; enum will show the raw value when not matched

        footer = "↑/↓ move, Enter select, Esc back"
        def _on_setting_change(rid: str, value: Any, working: Dict[str, Any]) -> None:
            try:
                if rid == "model":
                    if value == "custom":
                        typed = self.ui.prompt(
                            "Enter model name (e.g., deepseek-chat, gpt-5, gemini-2.5-flash)",
                            default=self.model or "",
                        )
                        working["model"] = typed.strip() or None
                    self._apply_model_side_effects()
                elif rid == "text_verbosity" and isinstance(value, str):
                    if value not in ("low", "medium", "high"):
                        working[rid] = "medium"
                elif rid == "thinking_budget_tokens":
                    tbt = value
                    if tbt in ("", None, 0, "0", "default"):
                        working[rid] = None
                    else:
                        try:
                            working[rid] = int(tbt)
                        except Exception:
                            working[rid] = None
                elif rid == "web_search_allowed_domains" and isinstance(value, str):
                    working[rid] = [d.strip() for d in value.replace("\n", ",").split(",") if d.strip()]
                elif rid == "web_search_location" and isinstance(value, str):
                    kv: Dict[str, str] = {}
                    for tok in value.replace(",", " ").split():
                        if "=" in tok:
                            k, v = tok.split("=", 1)
                            if k.strip() and v.strip():
                                kv[k.strip()] = v.strip()
                    working[rid] = kv
                elif rid == "auto_approve" and isinstance(value, str):
                    working[rid] = [t.strip() for t in value.split(",") if t.strip()]
                elif rid == "anthropic_cache_ttl":
                    if value in ("5m", "1h"):
                        working[rid] = value
                    else:
                        working[rid] = None
                self._apply_settings_dict({rid: working.get(rid)})
                if rid == "host_base":
                    try:
                        self._host_base_ephemeral = False
                    except Exception:
                        pass
                    try:
                        self._codebase_map_raw = self._load_codebase_map_raw()
                    except Exception:
                        pass
                if rid in ("custom_first_turn_enabled", "custom_first_turn_text"):
                    # Reset the first-turn custom injection flag so the change applies on next first turn
                    try:
                        self._did_inject_custom_first_turn = False
                    except Exception:
                        pass
                self.save_settings()
            except Exception:
                pass
        ui = SettingsUI("henosis-cli Settings", items, init_for_ui, defaults, footer=footer, on_change=_on_setting_change)
        # Optional: start focused on a specific control (e.g., the Model picker)
        try:
            if isinstance(focus, str) and focus.strip().lower() in ("model",):
                # Find the first category/item with id == 'model' and open items view there
                for _ci, _cat in enumerate(getattr(ui, "categories", []) or []):
                    rows = _cat.get("items") or []
                    for _ri, _row in enumerate(rows):
                        if str(_row.get("id") or "").strip().lower() == "model":
                            try:
                                ui.mode = "items"  # type: ignore[attr-defined]
                                ui.cat_index = _ci  # type: ignore[attr-defined]
                                ui.item_index = _ri  # type: ignore[attr-defined]
                            except Exception:
                                pass
                            raise StopIteration  # break both loops
        except StopIteration:
            pass
        committed, updated = ui.run()
        if not committed or not isinstance(updated, dict):
            return

        # Post-process and validate specific fields
        # Model: if enum landed on 'custom', keep existing model; if None -> default
        if updated.get("model") == "custom":
            # No change unless user edited explicitly via 'e'
            updated["model"] = initial.get("model")
        # thinking_budget_tokens ensure None or positive int
        tbt = updated.get("thinking_budget_tokens")
        if tbt in ("", None, 0, "0", "default"):
            updated["thinking_budget_tokens"] = None
        else:
            try:
                updated["thinking_budget_tokens"] = int(tbt) if tbt is not None else None
            except Exception:
                updated["thinking_budget_tokens"] = None
        # web_search_allowed_domains: normalize comma list
        dom = updated.get("web_search_allowed_domains")
        if isinstance(dom, str):
            toks = [d.strip() for d in dom.replace("\n", ",").split(",") if d.strip()]
            updated["web_search_allowed_domains"] = toks
        # web_search_location: parse key=value
        loc = updated.get("web_search_location")
        if isinstance(loc, str):
            kv: Dict[str, str] = {}
            for tok in loc.replace(",", " ").split():
                if "=" in tok:
                    k, v = tok.split("=", 1)
                    if k.strip() and v.strip():
                        kv[k.strip()] = v.strip()
            updated["web_search_location"] = kv

        # Apply to running CLI and persist
        try:
            self._apply_settings_dict(updated)
            if isinstance(updated.get("host_base"), str) and updated.get("host_base").strip():
                try:
                    self._host_base_ephemeral = False
                except Exception:
                    pass
            # Refresh code map source when host_base changed
            try:
                self._codebase_map_raw = self._load_codebase_map_raw()
            except Exception:
                pass
            # Reset first-turn custom injection flag after settings update so it can apply on next first turn
            try:
                self._did_inject_custom_first_turn = False
            except Exception:
                pass
        except Exception as e:
            self.ui.warn(f"Failed to apply updated settings: {e}")
        ok = await self._save_server_settings(updated)
        if ok:
            self.ui.success("Settings saved.")
        else:
            self.ui.warn("Failed to save settings to server; using local changes for this session.")
        # Summarize changes compared to settings when UI opened
        try:
            before = initial or {}
            after = self._collect_settings_dict()
            changed: List[str] = []
            lines: List[str] = []
            keys = sorted(set(list(before.keys()) + list(after.keys())))
            def _to_str(v: Any) -> str:
                try:
                    if isinstance(v, (dict, list)):
                        s = json.dumps(v, ensure_ascii=False)
                    else:
                        s = str(v)
                except Exception:
                    s = str(v)
                s = s if len(s) <= 160 else (s[:120] + " ... " + s[-20:])
                return s
            for k in keys:
                b = before.get(k)
                a = after.get(k)
                if b != a:
                    changed.append(k)
                    lines.append(f"- {k}: {_to_str(b)} -> {_to_str(a)}")
            if changed:
                self.ui.info_box("Settings changed", [f"{len(changed)} item(s) updated:"] + lines[:20])
                if len(lines) > 20:
                    self.ui.print(f"... and {len(lines)-20} more", style=self.ui.theme["dim"])  # type: ignore
            else:
                self.ui.print("No changes from previous settings.", style=self.ui.theme["dim"])
        except Exception:
            pass

    def _commands_word_completer(self) -> Optional[Any]:
        if not (HAS_PT and WordCompleter):
            return None
        words = [c["name"] for c in self._commands_catalog]
        meta = {c["name"]: c["usage"] for c in self._commands_catalog}
        try:
            return WordCompleter(words, meta_dict=meta, ignore_case=False, sentence=True)
        except Exception:
            return None

    def _read_multiline_input(self, prompt: str = "You: ") -> str:
        """Plain fallback multiline reader using built-in input().
        Rules:
        - Print prompt once.
        - Collect lines until the user enters an empty line, then submit.
        - EOF (Ctrl+D/Ctrl+Z) submits if we have content; otherwise raises to exit.
        No leading/trailing whitespace is stripped from lines; formatting is preserved.
        """
        try:
            print(prompt, end="", flush=True)
        except Exception:
            # Fallback if stdout is odd
            sys.stdout.write(prompt)
            sys.stdout.flush()
        lines: List[str] = []
        while True:
            try:
                line = input()
            except EOFError:
                if lines:
                    return "\n".join(lines)
                raise
            if line == "":
                # Empty line submits (if any content gathered)
                if lines:
                    return "\n".join(lines)
                return ""
            lines.append(line)

    async def _command_palette(self) -> Optional[str]:
        items = [(c["usage"], f"{c['name']} — {c['desc']}") for c in self._commands_catalog]
        total = len(items)
        if False and HAS_PT and RadioList and Application and Layout and HSplit and Window and FormattedTextControl and Frame:
            try:
                radio = RadioList(items)
                # Layout: hint, list (scrollable), status (index/total)
                container = HSplit([
                    Window(height=1, content=FormattedTextControl(lambda: "Use ↑/↓, Enter to select, Esc to cancel"), style="class:hint"),
                    Frame(radio, title="Commands"),
                    Window(height=1, content=FormattedTextControl(lambda: f"({radio._selected_index + 1}/{total})"), style="class:status"),
                ])
                kb = KeyBindings()

                @kb.add("enter")
                def _enter(event):
                    event.app.exit(result=radio.current_value)

                @kb.add("escape")
                def _esc(event):
                    event.app.exit(result=None)

                style = Style.from_dict({
                    "hint": "fg:#888888",
                    # Primary accent -> orange
                    "status": "fg:#ff8700",
                })
                app = Application(layout=Layout(container), key_bindings=kb, style=style, full_screen=False)
                return await app.run_async()
            except Exception:
                pass
        # Fallback: simple paginated list (7 per page)
        page = 0
        page_size = 7
        while True:
            start = page * page_size
            chunk = items[start : start + page_size]
            if not chunk:
                return None
            self.ui.print("\nCommands (page {}/{}):".format(page + 1, (total + page_size - 1) // page_size), style=self.ui.theme["subtitle"])
            for i, (val, label) in enumerate(chunk, start=1):
                idx = start + i
                self.ui.print(f"{i}. {label} ({idx}/{total})", style=self.ui.theme["dim"])
            self.ui.print("n=next page, p=prev page, q=cancel", style=self.ui.theme["dim"])
            raw = input("Select: ").strip().lower()
            if raw == "q":
                return None
            if raw == "n":
                if (start + page_size) < total:
                    page += 1
                continue
            if raw == "p":
                if page > 0:
                    page -= 1
                continue
            if raw.isdigit():
                k = int(raw)
                if 1 <= k <= len(chunk):
                    return chunk[k - 1][0]
            self.ui.warn("Invalid selection.")

    async def _menu_choice(self, title: str, text: str, choices: List[Tuple[str, str]]) -> Optional[str]:
        # Arrow-key navigable menu when prompt_toolkit is available; numeric fallback otherwise.
        # choices: list of (value, label)
        if False and HAS_PT and RadioList and Application and Layout and HSplit and Window and FormattedTextControl and Frame and Style:
            try:
                items = [(val, label) for (val, label) in choices]
                radio = RadioList(items)
                container = HSplit([
                    Window(height=1, content=FormattedTextControl(lambda: text or "Use ↑/↓, Enter to select, Esc to cancel"), style="class:hint"),
                    Frame(radio, title=title),
                ])
                kb = KeyBindings()

                @kb.add("enter")
                def _enter(event):
                    event.app.exit(result=radio.current_value)

                @kb.add("escape")
                def _esc(event):
                    event.app.exit(result=None)

                style = Style.from_dict({
                    "hint": "fg:#888888",
                })
                app = Application(layout=Layout(container), key_bindings=kb, style=style, full_screen=False)
                return await app.run_async()
            except Exception:
                pass

        # Fallback: simple numeric menu
        self.ui.header(title, text)
        for i, (_, label) in enumerate(choices, start=1):
            style = None
            try:
                lbl = str(label)
                if ("VERY expensive" in lbl) or ("[DANGER]" in lbl) or ("!!!" in lbl and "expensive" in lbl.lower()):
                    style = self.ui.theme.get("err")
            except Exception:
                style = None
            self.ui.print(f"{i}. {label}", style=style)
        self.ui.print()
        while True:
            raw = input("Choose an option: ").strip()
            if raw.lower() in ("q", "quit", "exit"):
                return None
            if not raw.isdigit():
                self.ui.warn("Enter a number from the list.")
                continue
            idx = int(raw)
            if not (1 <= idx <= len(choices)):
                self.ui.warn("Invalid selection.")
                continue
            return choices[idx - 1][0]

    # NOTE: select_model_menu moved below (single definition) and updated with DeepSeek presets

    async def set_scope_menu(self) -> None:
        val = await self._menu_choice(
            "Filesystem Scope", 
            "Choose filesystem scope (Agent scope applies when host is enabled):",
            [
                ("workspace", "Workspace - Safe sandbox directory, relative paths only"),
                ("host", "Host - Full host filesystem access (requires server permission and host_base)"),
                ("default", "Server Default - Let server decide based on config"),
            ],
        )
        if val == "workspace":
            self.fs_scope = "workspace"
        elif val == "host":
            self.fs_scope = "host"
        elif val == "default":
            self.fs_scope = None
        self.ui.success(f"FS Scope set to: {self._fs_label()}")
        self.save_settings()

    async def set_level_menu(self) -> None:
        val = await self._menu_choice(
            "Control Level",
            "Choose control level (1=read-only, 2=approval on write/exec, 3=unrestricted within sandbox):",
            [
                ("1", "Level 1: Read-Only - Only read_file and list_dir available, no writes or executions"),
                ("2", "Level 2: Approval Required - Write/edit/exec tools require user approval"),
                ("3", "Level 3: Full Access - No approvals needed, all tools unrestricted"),
                ("default", "Server Default - Use server's CONTROL_LEVEL_DEFAULT setting"),
            ],
        )
        if val == "default":
            self.control_level = None
        elif val in ("1", "2", "3"):
            self.control_level = int(val)
        self.ui.success(f"Control level set to: {self.control_level or 'server default'}")
        self.save_settings()

    async def set_auto_approve_menu(self) -> None:
        self.ui.header("Auto-Approve Tools", "Choose tools to auto-approve at Level 2. Select multiple with commas, or choose common presets.")
        choices = [
            ("none", "None - Require approval for all writes/edits/execs"),
            ("writes", "Writes Only - Auto-approve write_file, append_file"),
            ("edits", "Edits Only - Auto-approve edit_file"),
            ("execs", "Execs Only - Auto-approve run_command"),
            ("all", "All - Auto-approve write_file, append_file, edit_file, run_command"),
            ("custom", "Custom - Enter your own list"),
        ]
        val = await self._menu_choice("Auto-Approve Presets", "Select a preset or custom:", choices)
        if val == "none":
            self.auto_approve = []
        elif val == "writes":
            self.auto_approve = ["write_file", "append_file"]
        elif val == "edits":
            self.auto_approve = ["edit_file"]
        elif val == "execs":
            self.auto_approve = ["run_command"]
        elif val == "all":
            self.auto_approve = ["write_file", "append_file", "edit_file", "run_command"]
        elif val == "custom":
            s = self.ui.prompt(
                "Enter comma-separated tool names (e.g., write_file,append_file)", 
                default=",".join(self.auto_approve) if self.auto_approve else "",
            )
            names = [t.strip() for t in s.split(",") if t.strip()]
            self.auto_approve = names
        self.ui.success(f"Auto-approve set to: {','.join(self.auto_approve) if self.auto_approve else '(none)'}")
        self.save_settings()

    # ---------------------- Payload building helpers -------------------

    def _build_codebase_injection(self, user_input: str) -> Optional[str]:
        """Build a <codebase_map>...</codebase_map> block without pre-truncation.
        No client-side truncation is applied."""
        if not self._codebase_map_raw:
            # Lazy-load so newly created CODEBASE_MAP.md files are picked up before first turn.
            try:
                self._codebase_map_raw = self._load_codebase_map_raw()
            except Exception:
                self._codebase_map_raw = None
        if not self._codebase_map_raw:
            return None
        prefix = "<codebase_map>\n"
        suffix = "\n</codebase_map>"
        return f"{prefix}{self._codebase_map_raw}{suffix}"

    def _build_first_turn_injection(self, user_input: str) -> Optional[str]:
        """Compose first-turn-only prefix blocks (code map, custom text, preamble, working memory)."""
        blocks: List[str] = []

        # 1) Codebase map (only once per conversation)
        try:
            if self.inject_codebase_map and (not self._did_inject_codebase_map):
                inj = self._build_codebase_injection(user_input)
                if inj:
                    blocks.append(inj)
                    self._did_inject_codebase_map = True
        except Exception:
            pass

        # 2) Custom first-turn user text (only once per conversation)
        try:
            if bool(getattr(self, "custom_first_turn_enabled", False)) and (not getattr(self, "_did_inject_custom_first_turn", False)):
                txt = getattr(self, "custom_first_turn_text", "") or ""
                if isinstance(txt, str) and txt.strip():
                    blocks.append(txt.strip())
                    self._did_inject_custom_first_turn = True
        except Exception:
            pass

        # 3) Tool usage preamble (UX hint)
        try:
            if bool(getattr(self, "preambles_enabled", False)) and not self._is_codex_model(self.model):
                blocks.append(
                    "Tool usage: when you need to read or modify files or run commands, "
                    "explicitly explain why you're using a tool, what you'll do, and how it "
                    "advances the user's goal before calling the tool."
                )
        except Exception:
            pass

        # 4) Working memory (context-summary file), injected once on fresh session restart
        try:
            if (not self._did_inject_working_memory) and self._memory_paths_for_first_turn:
                wm_block = self._build_working_memory_injection()
                if wm_block:
                    blocks.append(wm_block)
                    self._did_inject_working_memory = True
                    # Clear after successful injection so it doesn't repeat
                    self._memory_paths_for_first_turn = []
        except Exception:
            pass

        if not blocks:
            return None
        return "\n\n".join(blocks)

    def _build_messages(self, user_input: str) -> List[Dict[str, str]]:
        msgs: List[Dict[str, str]] = []
        # Inject a concise Codex developer system prompt for Codex models (optional)
        try:
            if self._is_codex_model(self.model) and bool(getattr(self, "codex_prompt_enabled", True)):
                msgs.append({"role": "system", "content": self._codex_system_prompt()})
        except Exception:
            pass
        # Always send the system prompt as-is (do NOT inject the code map here)
        if self.system_prompt:
            msgs.append({"role": "system", "content": self.system_prompt})

        # Replay prior conversation (excluding any system message already added)
        for msg in self.history:
            if msg["role"] != "system":
                msgs.append({"role": msg["role"], "content": msg["content"]})

        # For the first user turn only, prefix any configured injections to the user's content
        content = user_input
        prefix = self._build_first_turn_injection(user_input)
        if prefix:
            content = f"{prefix}\n\n{user_input}"

        # Remember exactly what we sent as the user content for this turn
        try:
            self._last_built_user_content = content
        except Exception:
            self._last_built_user_content = user_input

        msgs.append({"role": "user", "content": content})
        return msgs

    def _codex_system_prompt(self) -> str:
        """Minimal developer system prompt for GPT-5 Codex family."""
        return (
            "You are Codex, based on GPT-5. You are running as a coding agent in the Codex CLI on a user's computer.\n"
            "Note: In this CLI, the terminal tool is named 'run_command' (not 'shell'). Use run_command and always set the 'cwd' parameter; avoid using 'cd'.\n\n"
            "## General\n"
            "- Always set the 'cwd' param when using run_command. Do not use 'cd' unless absolutely necessary.\n"
            "- When searching for text or files, prefer using `rg` or `rg --files` respectively because `rg` is much faster than alternatives like `grep`. (If the `rg` command is not found, then use alternatives.)\n\n"
            "## Editing constraints\n"
            "- Default to ASCII when editing or creating files. Only introduce non-ASCII or other Unicode characters when there is a clear justification and the file already uses them.\n"
            "- Add succinct code comments that explain what is going on if code is not self-explanatory. You should not add comments like \"Assigns the value to the variable\", but a brief comment might be useful ahead of a complex code block that the user would otherwise have to spend time parsing out. Usage of these comments should be rare.\n"
            "- You may be in a dirty git worktree.\n"
            "    * NEVER revert existing changes you did not make unless explicitly requested, since these changes were made by the user.\n"
            "    * If asked to make a commit or code edits and there are unrelated changes to your work or changes that you didn't make in those files, don't revert those changes.\n"
            "    * If the changes are in files you've touched recently, you should read carefully and understand how you can work with the changes rather than reverting them.\n"
            "    * If the changes are in unrelated files, just ignore them and don't revert them.\n"
            "- While you are working, you might notice unexpected changes that you didn't make. If this happens, STOP IMMEDIATELY and ask the user how they would like to proceed.\n\n"
            "## Plan tool\n"
            "When using the planning tool:\n"
            "- Skip using the planning tool for straightforward tasks (roughly the easiest 25%).\n"
            "- Do not make single-step plans.\n"
            "- When you made a plan, update it after having performed one of the sub-tasks that you shared on the plan.\n\n"
            "## Codex CLI harness, sandboxing, and approvals\n"
            "The Codex CLI harness supports several different configurations for sandboxing and escalation approvals that the user can choose from.\n"
            "Filesystem sandboxing defines which files can be read or written. The options for `sandbox_mode` are:\n"
            "- read-only: The sandbox only permits reading files.\n"
            "- workspace-write: The sandbox permits reading files, and editing files in `cwd` and `writable_roots`. Editing files in other directories requires approval.\n"
            "- danger-full-access: No filesystem sandboxing - all commands are permitted.\n"
            "Network sandboxing defines whether network can be accessed without approval. Options for `network_access` are:\n"
            "- restricted: Requires approval\n"
            "- enabled: No approval needed\n"
            "Approvals are your mechanism to get user consent to run shell/terminal commands without the sandbox. Possible configuration options for `approval_policy` are\n"
            "- untrusted: The harness will escalate most commands for user approval, apart from a limited allowlist of safe 'read' commands.\n"
            "- on-failure: The harness will allow all commands to run in the sandbox (if enabled), and failures will be escalated to the user for approval to run again without the sandbox.\n"
            "- on-request: Commands will be run in the sandbox by default, and you can specify in your tool call if you want to escalate a command to run without sandboxing.\n"
            "- never: This is a non-interactive mode where you may NEVER ask the user for approval to run commands. Instead, you must always persist and work around constraints to solve the task for the user.\n\n"
            "When requesting approval to execute a command that will require escalated privileges:\n"
            "  - Provide the `with_escalated_permissions` parameter with the boolean value true (when available).\n"
            "  - Include a short, 1 sentence explanation for why you need to enable `with_escalated_permissions` in the justification parameter.\n\n"
            "## Special user requests\n"
            "- If the user makes a simple request (such as asking for the time) which you can fulfill by running a terminal command (such as `date`), you should do so.\n"
            "- If the user asks for a 'review', default to a code review mindset: prioritise identifying bugs, risks, behavioural regressions, and missing tests. Findings must be the primary focus of the response - keep summaries or overviews brief and only after enumerating the issues. Present findings first (ordered by severity with file/line references), follow with open questions or assumptions, and offer a change-summary only as a secondary detail. If no findings are discovered, state that explicitly and mention any residual risks or testing gaps.\n\n"
            "## Presenting your work and final message\n"
            "You are producing plain text that will later be styled by the CLI. Follow these rules exactly. Formatting should make results easy to scan, but not feel mechanical. Use judgment to decide how much structure adds value.\n"
            "- Default: be very concise; friendly coding teammate tone.\n"
            "- Ask only when needed; suggest ideas; mirror the user's style.\n"
            "- For substantial work, summarize clearly; follow final-answer formatting.\n"
            "- Skip heavy formatting for simple confirmations.\n"
            "- Don't dump large files you've written; reference paths only.\n"
            "- No 'save/copy this file' - User is on the same machine.\n"
            "- Offer logical next steps (tests, commits, build) briefly; add verify steps if you couldn't do something.\n"
            "- For code changes:\n"
            "  * Lead with a quick explanation of the change, and then give more details on the context covering where and why a change was made. Do not start this explanation with 'summary', just jump right in.\n"
            "  * When suggesting multiple options, use numeric lists for the suggestions so the user can quickly respond with a single number.\n"
            "- File References: When referencing files in your response, include the relevant start line and follow these rules: use inline code for paths; each reference should have a standalone path; accepted: absolute, workspace-relative, a/ or b/ diff prefixes, or bare filename/suffix; optional line/column uses :line[:column] or #LlineCcolumn; do not use URIs; do not provide line ranges.\n\n"
            "Apply Patch\n"
            "As shared previously in the GPT-5 prompting guide, use apply_patch for file edits to match the training distribution.\n\n"
            "Preambles\n"
            "GPT-5-Codex does not emit preambles. Do not ask for them.\n\n"
            "Frontend Guidance\n"
            "Use the following libraries unless the user or repo specifies otherwise:\n"
            "Framework: React + TypeScript\n"
            "Styling: Tailwind CSS\n"
            "Components: shadcn/ui\n"
            "Icons: lucide-react\n"
            "Animation: Framer Motion\n"
            "Charts: Recharts\n"
            "Fonts: San Serif, Inter, Geist, Mona Sans, IBM Plex Sans, Manrope\n"
        )

    def _build_kimi_raw_messages(self, user_input: str) -> List[Dict[str, Any]]:
        """Build provider-native messages for Kimi preserving prior assistant reasoning_content.
        Includes prior provider-native turns and the current user message with first-turn injections.
        """
        # Build the current user content with first-turn injections (code map, custom text, preamble, working memory)
        content = user_input
        prefix = self._build_first_turn_injection(user_input)
        if prefix:
            content = f"{prefix}\n\n{user_input}"
        # Compose new list: prior provider-native history plus current user
        raw = []
        # Always include system prompt first if present
        if self.system_prompt:
            raw.append({"role": "system", "content": self.system_prompt})
        # Append previously captured provider-native conversation (already includes user/assistant/tool)
        for m in (self._kimi_raw_history or []):
            raw.append(m)
        # Append current user message
        raw.append({"role": "user", "content": content})
        return raw

    def _build_working_memory_injection(self) -> Optional[str]:
        try:
            if not self._memory_paths_for_first_turn:
                return None
            # Use the first provided path
            first = self._memory_paths_for_first_turn[0]
            p = Path(first)
            if not p.is_absolute():
                # Resolve relative to local workspace dir
                p = Path(self.local_workspace_dir).joinpath(first).resolve()
            if not p.exists():
                return None
            text = p.read_text(encoding="utf-8", errors="replace")
            explainer = (
                "Context was near full on the previous attempt. A compact working memory file was created; "
                "prefer this summary and reference files by path when needed."
            )
            block = (
                "<working_memory>\n"
                f"<explainer>{explainer}</explainer>\n\n"
                "<working_memory_md>\n"
                f"{text}\n"
                "</working_memory_md>\n"
                "</working_memory>"
            )
            return block
        except Exception:
            return None

    def _web_search_location_payload(self) -> Optional[Dict[str, str]]:
        if not self.web_search_location:
            return None
        payload: Dict[str, str] = {}
        for key, value in self.web_search_location.items():
            if isinstance(key, str) and isinstance(value, str):
                val = value.strip()
                if val:
                    payload[key.strip()] = val
        if not payload:
            return None
        if "type" not in payload:
            payload["type"] = "approximate"
        return payload

    # ----------------------- Codebase map helpers ----------------------

    def _code_map_exists_at(self, root: str) -> bool:
        try:
            if not root:
                return False
            p1 = Path(root) / "CODEBASE_MAP.md"
            p2 = Path(root) / "codebase_map.md"
            return p1.exists() or p2.exists()
        except Exception:
            return False

    async def _offer_generate_code_map(self, root: str) -> None:
        """Offer to generate CODEBASE_MAP.md for the given root if missing, and, if accepted,
        stream a one-off prompt that guides the agent to read the directory and create it.

        This runs as a normal chat turn so the user can watch tool usage and file creation.
        """
        try:
            if not root:
                return
            if self._code_map_exists_at(root):
                return
            # Ask user via menu instead of Y/N typing
            choice = await self._menu_choice(
                "Codebase map",
                f"No CODEBASE_MAP.md found under '{root}'. Generate one now using tools?",
                [
                    ("generate", "Generate CODEBASE_MAP.md now"),
                    ("skip", "Skip for now"),
                ],
            )
            if choice != "generate":
                return
            await self._generate_code_map_for(root)
        except Exception as e:
            self.ui.warn(f"Code map offer failed: {e}")

    async def _generate_code_map_for(self, root: str) -> None:
        """Temporarily enable tools + host scope and ask the model to create CODEBASE_MAP.md at root.

        We include this project's CODEBASE_MAP.md content as an example of style/intent.
        """
        # Build prompt
        example = (self._codebase_map_raw or "").strip()
        example_block = f"\n<example_codebase_map>\n{example}\n</example_codebase_map>\n" if example else ""
        root_abs = str(Path(root).expanduser().resolve())
        prompt_lines = [
            "go read this codebase directory structure & files to make a codebase map.",
            "",
            "Task: Generate a CODEBASE_MAP.md for the host project at this absolute path:",
            root_abs,
            "",
            "Agent role (addressing you, the model):",
            (
                "You are an expert coding agent operating on the user's machine. "
                "You use the available tools in a deliberate, stepwise sequence to complete requests. "
                "If requirements are unclear, ask clarifying questions. "
                "For multi-step or complex tasks, propose a brief plan first, then execute and iterate with user feedback."
            ),
            "",
            "Instructions:",
            "- Use file tools to inspect the directory structure and key files. Start at the project root.",
            "- Prefer list_dir at the root first, then drill into only important folders (avoid exhaustive traversal).",
            "- Read a few representative files to infer purpose where helpful.",
            "- Add this single instruction line: 'When completing tasks commiting as we make progress is encouraged. Ask the user before you add or commit changes with a proposal of the changes.'",
            "- Produce a concise, human-readable CODEBASE_MAP.md that explains:",
            "  - Purpose of the project",
            "  - Top-level layout (folders and notable files)",
            "  - Key components and what they do",
            "  - Any quickstart or run/dev tips if obvious",
            "- When done, write the file to CODEBASE_MAP.md at the project root.",
            "",
            "Conventions:",
            "- Keep it brief and skimmable; do not list every file.",
            "- Use simple bullet points and short descriptions.",
            "- If a codebase map already exists (case-insensitive), update/replace it; otherwise create it.",
            "",
            "Tooling context:",
            "- Filesystem scope is 'host' for this turn, with the above path as the root.",
            "- You may call list_dir/read_file/write_file/apply_patch as needed.",
            "- To list the root, you can use list_dir with an empty path ('') or with the absolute root path.",
        ]
        if example_block:
            prompt_lines.append("\nStyle example (not the same project, just for reference do not mention this example to the user unless asked):")
            prompt_lines.append(example_block)
        prompt_lines.append("Now begin by listing the top-level directory, then proceed.")

        user_prompt = "\n".join(prompt_lines)

        # Temporarily adjust settings for this one turn
        prev_tools = self.requested_tools
        prev_scope = self.fs_scope
        prev_host_base = self.host_base
        prev_host_mode = self.fs_host_mode
        prev_level = self.control_level
        try:
            # Ensure tools on and host scope applied to this request
            self.requested_tools = True
            self.fs_scope = "host"
            self.host_base = root_abs
            # Constrain host roots to the selected base for safety
            self.fs_host_mode = "custom"
            # Prefer Level 2 so the user can approve writes visibly; fallback to user's setting otherwise
            if self.control_level not in (1, 2, 3):
                self.control_level = 2

            self.ui.info("Starting codebase map generation turn...")
            await self._stream_once(user_prompt)
        finally:
            # Restore prior settings
            self.requested_tools = prev_tools
            self.fs_scope = prev_scope
            self.host_base = prev_host_base
            self.fs_host_mode = prev_host_mode
            self.control_level = prev_level

    # -------------------------- Tool rendering -------------------------
    def _base_command(self, cmd: Optional[str]) -> str:
        try:
            return (cmd or "").strip().split()[0].lower()
        except Exception:
            return ""

    def _approval_prompt_ui(self, label: str, args: Dict[str, Any]) -> str:
        """Interactive approval prompt for Level 2.

        Uses the same highlighted, arrow-key-driven menu UX as the rest of the CLI
        when TTY input is available, and falls back to numeric input otherwise.
        Returns one of: "once", "session", "always", "deny".
        """
        self.ui.print(f"\n[Level 2] Approval required for: {label}")
        # Show a compact summary
        summary = self._tool_summary(label.split(":")[0], args)
        self.ui.print(summary, style=self.ui.theme["dim"])

        choices: List[Tuple[str, str]] = [
            ("once", "Approve once"),
            ("session", "Trust for this session"),
            ("always", "Always trust"),
            ("deny", "Deny"),
        ]
        labels = [lbl for (_val, lbl) in choices]

        # Pure numeric fallback when TTY-style key handling is unavailable
        if not _hn_supports_tty_io_v2():
            self.ui.print("1) Approve once   2) Trust for this session   3) Always trust   4) Deny")
            while True:
                raw = input("Choose (1-4): ").strip()
                if raw in ("1", "2", "3", "4"):
                    return {"1": "once", "2": "session", "3": "always", "4": "deny"}[raw]
                self.ui.warn("Enter 1, 2, 3, or 4.")

        # Highlighted, arrow-key-driven menu using the same helpers as settings menus
        index = 0
        title = "Approval required"
        text = "Use / to move, Enter=select, Esc=deny; 1-4 to jump directly"
        _hn_render_menu_v2(self.ui, title, text, labels, index)
        while True:
            key = _hn_read_key_v2()
            if key is None:
                # Fall back to numeric prompt if key-reading fails
                self.ui.print("\nNumeric selection fallback.")
                self.ui.print("1) Approve once   2) Trust for this session   3) Always trust   4) Deny")
                while True:
                    raw = input("Choose (1-4): ").strip()
                    if raw in ("1", "2", "3", "4"):
                        return {"1": "once", "2": "session", "3": "always", "4": "deny"}[raw]
                    self.ui.warn("Enter 1, 2, 3, or 4.")
            elif key == "UP":
                index = (index - 1) % len(labels)
                _hn_render_menu_v2(self.ui, title, text, labels, index)
            elif key == "DOWN":
                index = (index + 1) % len(labels)
                _hn_render_menu_v2(self.ui, title, text, labels, index)
            elif key == "PGUP":
                index = max(0, index - 7)
                _hn_render_menu_v2(self.ui, title, text, labels, index)
            elif key == "PGDN":
                index = min(len(labels) - 1, index + 7)
                _hn_render_menu_v2(self.ui, title, text, labels, index)
            elif key == "HOME":
                index = 0
                _hn_render_menu_v2(self.ui, title, text, labels, index)
            elif key == "END":
                index = len(labels) - 1
                _hn_render_menu_v2(self.ui, title, text, labels, index)
            elif key == "ENTER":
                return choices[index][0]
            elif key == "ESC":
                # Treat cancel as an explicit deny for safety
                return "deny"
            elif isinstance(key, str) and key.isdigit():
                k = int(key)
                if 1 <= k <= len(labels):
                    index = k - 1
                    _hn_render_menu_v2(self.ui, title, text, labels, index)

    def _cli_approval_for(self, name: Optional[str], args: Dict[str, Any]) -> bool:
        # Gate only at Level 2; Levels 1 and 3 are handled elsewhere.
        try:
            lvl = int(self.control_level) if isinstance(self.control_level, int) else None
        except Exception:
            lvl = None
        if lvl != 2:
            return True
        key = (name or "").strip().lower()
        # Auto-approve list for backwards compatibility
        if key in (self.auto_approve or []):
            return True
        # run_command per-base trust
        if key == "run_command":
            base = self._base_command(args.get("cmd", ""))
            if not base:
                # empty commands are denied
                return False
            if base in self.trust_cmds_session or base in self.trust_cmds_always:
                return True
            label = f"run_command:{base}"
            choice = self._approval_prompt_ui(label, args)
            if choice == "deny":
                return False
            if choice == "session":
                if base not in self.trust_cmds_session:
                    self.trust_cmds_session.append(base)
                return True
            if choice == "always":
                if base not in self.trust_cmds_always:
                    self.trust_cmds_always.append(base)
                self.save_settings()
                return True
            return True  # once
        # Other destructive tools: trust by tool name
        destructive = {"write_file", "append_file", "edit_file", "apply_patch", "string_replace"}
        if key in destructive:
            if key in self.trust_tools_session or key in self.trust_tools_always:
                return True
            choice = self._approval_prompt_ui(key, args)
            if choice == "deny":
                return False
            if choice == "session":
                if key not in self.trust_tools_session:
                    self.trust_tools_session.append(key)
                return True
            if choice == "always":
                if key not in self.trust_tools_always:
                    self.trust_tools_always.append(key)
                self.save_settings()
                return True
            return True
        # Non-destructive tools do not require approval
        return True

    async def _trust_menu(self) -> None:
        # Simple interactive editor for trust lists
        while True:
            self.ui.header("Level 2 Trust", "Approve Once / Session / Always for tools and commands")
            self.ui.print(f"Tools (always): {', '.join(self.trust_tools_always) if self.trust_tools_always else '(none)'}", style=self.ui.theme["dim"])
            self.ui.print(f"Tools (session): {', '.join(self.trust_tools_session) if self.trust_tools_session else '(none)'}", style=self.ui.theme["dim"])
            self.ui.print(f"Commands (always): {', '.join(self.trust_cmds_always) if self.trust_cmds_always else '(none)'}", style=self.ui.theme["dim"])
            self.ui.print(f"Commands (session): {', '.join(self.trust_cmds_session) if self.trust_cmds_session else '(none)'}", style=self.ui.theme["dim"])
            choice = await self._menu_choice(
                "Manage Trust",
                "Choose an action:",
                [
                    ("add_tool_always", "Add tool to Always trust (write_file, append_file, edit_file, apply_patch)"),
                    ("add_cmd_always", "Add base command to Always trust (e.g., grep, rg)"),
                    ("clear_session", "Clear session trust (tools and commands)"),
                    ("back", "Back"),
                ],
            )
            if choice in (None, "back"):
                return
            if choice == "add_tool_always":
                s = self.ui.prompt("Enter tool name", default="write_file")
                k = s.strip().lower()
                if k:
                    if k not in self.trust_tools_always:
                        self.trust_tools_always.append(k)
                        self.save_settings()
                        self.ui.success(f"Added '{k}' to always-trusted tools")
            elif choice == "add_cmd_always":
                s = self.ui.prompt("Enter base command (e.g., grep)", default="grep")
                k = s.strip().lower()
                if k:
                    if k not in self.trust_cmds_always:
                        self.trust_cmds_always.append(k)
                        self.save_settings()
                        self.ui.success(f"Added '{k}' to always-trusted commands")
            elif choice == "clear_session":
                self.trust_tools_session = []
                self.trust_cmds_session = []
                self.ui.success("Cleared session trust lists")
    def _tool_summary(self, name: str, args: Dict[str, Any]) -> str:
        # Friendly, one-line explanation per tool
        if name == "read_file":
            p = args.get("path", "")
            return f"🔍 Reading file: {p}"
        if name == "write_file":
            p = args.get("path", "")
            n = len(args.get("content", "") or "")
            return f"📝 Writing file: {p} ({n} chars, overwrite)"
        if name == "append_file":
            p = args.get("path", "")
            n = len(args.get("content", "") or "")
            return f"📎 Appending to file: {p} (+{n} chars)"
        if name == "list_dir":
            p = args.get("path", "") or "."
            try:
                cwd = os.getcwd()
            except Exception:
                cwd = "n/a"
            return f"📂 Listing directory: {p} (scope: {self._fs_label()}, CLI cwd: {cwd})"
        if name == "edit_file":
            p = args.get("path", "")
            return f"✏️ Editing file: {p}"
        if name == "run_command":
            c = args.get("cmd", "")
            return f"💻 Running: {c}"
        return f"🔧 Tool call: {name}"

    def _render_tool_call(self, name: str, args: Dict[str, Any]) -> None:
        """Compact tool call notifier (non-yellow). Respects self.show_tool_calls.
        Prints a single line with an emoji summary and, when verbose, a dim args preview.
        """
        if not self.show_tool_calls:
            return
        try:
            # Determine the most accurate model label available for this turn
            try:
                model_prefix = (self._current_turn.get("model") or self._last_used_model or self.model or "(server default)")
            except Exception:
                model_prefix = self.model or "(server default)"
            summary = self._tool_summary(name, args)
            # Make certain tools even more human-readable by enriching the summary
            if isinstance(name, str) and isinstance(args, dict):
                if name == "run_command":
                    cwd = args.get("cwd")
                    if cwd and isinstance(cwd, str) and cwd.strip():
                        # Append working directory context
                        summary = summary + f" (in {cwd})"
                elif name == "apply_patch":
                    # Extract affected files from simplified patch format
                    patch_text = args.get("patch", "") or ""
                    dry = bool(args.get("dry_run", False))
                    affected = []
                    for line in str(patch_text).splitlines():
                        line = line.strip()
                        if not line:
                            continue
                        if line.startswith("*** Add File: ") or line.startswith("*** Update File: ") or line.startswith("*** Delete File: ") or line.startswith("*** Move to: "):
                            try:
                                affected.append(line.split(": ", 1)[1].strip())
                            except Exception:
                                continue
                    # Deduplicate in-order
                    seen = set(); uniq = []
                    for a in affected:
                        if a and a not in seen:
                            uniq.append(a); seen.add(a)
                    if uniq:
                        max_show = 3
                        shown = ", ".join(uniq[:max_show])
                        more = len(uniq) - max_show
                        more_str = f", +{more} more" if more > 0 else ""
                        extra = " (dry-run)" if dry else ""
                        summary = f"Patching: {shown}{more_str}{extra}"
                    else:
                        extra = " (dry-run)" if dry else ""
                        summary = f"Patching files{extra}"
            # Use the orange accent for tool calls; include model name prefix for clarity
            self.ui.print(f"{model_prefix}: ", style=self.ui.theme["tool_call"], end="")
            self.ui.print("⇒ " + str(summary), style="white")
            # When verbose, include a short dim arg preview for troubleshooting
            if self.ui.verbose and isinstance(args, dict) and args:
                self.ui.print(self._clip(truncate_json(args, 400), 400), style=self.ui.theme["dim"])
        except Exception:
            # Never fail UI on notifier issues
            pass
    def _tool_concise_label(self, name: str, args: Dict[str, Any], result: Optional[Dict[str, Any]] = None) -> str:
        """Return a professional, natural-language one-liner describing the action.
        Used for the default concise tool result line.
        """
        n = (name or "").strip()
        a = args or {}
        data = (result or {}).get("data") if isinstance(result, dict) else None
        data = data if isinstance(data, dict) else {}

        # Anthropic server-handled context handoff tool
        if n.lower() in ("context", "to_next"):
            return "Context handoff to next turn"

        def _arg_path() -> str:
            p = a.get("path") or data.get("path") or ""
            try:
                return str(p)
            except Exception:
                return ""

        if n == "read_file":
            p = _arg_path() or "file"
            return f"Reading {p}"
        if n == "write_file":
            p = _arg_path() or "file"
            return f"Writing {p}"
        if n == "append_file":
            p = _arg_path() or "file"
            return f"Appending to {p}"
        if n == "list_dir":
            p = a.get("path") or data.get("path") or "."
            try:
                p = str(p) if str(p).strip() else "."
            except Exception:
                p = "."
            return f"Listing directory {p}"
        if n == "edit_file":
            p = _arg_path() or "file"
            return f"Editing {p}"
        if n == "run_command":
            cmd = a.get("cmd") or data.get("cmd") or "command"
            try:
                cmd_str = self._clip(str(cmd), 160)
            except Exception:
                cmd_str = "command"
            return f"Executing command: {cmd_str}"
        if n == "apply_patch":
            # Attempt to extract a few affected files
            patch_text = a.get("patch", "") or ""
            affected = []
            try:
                for line in str(patch_text).splitlines():
                    s = line.strip()
                    if not s:
                        continue
                    if s.startswith("*** Add File: ") or s.startswith("*** Update File: ") or s.startswith("*** Delete File: ") or s.startswith("*** Move to: "):
                        try:
                            affected.append(s.split(": ", 1)[1].strip())
                        except Exception:
                            continue
            except Exception:
                affected = []
            # Dedup + keep order
            uniq = []
            seen = set()
            for x in affected:
                if x and x not in seen:
                    uniq.append(x); seen.add(x)
            if uniq:
                first = uniq[:2]
                more = len(uniq) - len(first)
                base = ", ".join(first)
                suffix = f" (+{more} more)" if more > 0 else ""
                return f"Applying patch to {base}{suffix}"
            return "Applying patch"
        if n == "string_replace":
            try:
                summ = data.get("summary") if isinstance(data, dict) else {}
            except Exception:
                summ = {}
            try:
                total = int((summ or {}).get("total_replacements", 0) or 0)
                targets = int((summ or {}).get("total_targets", 0) or 0)
                files_changed = int((summ or {}).get("files_changed", 0) or 0)
                fc = int((summ or {}).get("files_considered", 0) or 0)
            except Exception:
                total, targets, files_changed, fc = 0, 0, 0, 0
            scope = f"across {files_changed}/{fc} file(s)" if fc else (f"in {files_changed} file(s)" if files_changed else "")
            if targets:
                return f"String replace: {total}/{targets} replaced {scope}".strip()
            return f"String replace: {total} replaced {scope}".strip()
        # Default fallback
        return f"Running tool: {n or 'unknown'}"
    def _render_tool_result(self, name: str, result: Dict[str, Any], call_id: Optional[str] = None) -> None:
        ok = bool(result.get("ok"))
        if not ok:
            err = result.get("error", "Unknown error")
            self.ui.print(f"⇐ [{self.ui.theme['tool_result_err']}]❌ {name} failed: {err}[/{self.ui.theme['tool_result_err']}]")
            # Print the full result payload for troubleshooting
            self.ui.print(self._clip(truncate_json(result, 2000), 2000), style=self.ui.theme["dim"])
            # Troubleshooting: show last args for this call_id if available
            if call_id and call_id in self._tool_args_by_call_id:
                args = self._tool_args_by_call_id.get(call_id, {})
                self.ui.print(self._clip(truncate_json(args, 1200), 1200), style=self.ui.theme["dim"])
            # Extra context for list_dir failures
            if name == "list_dir":
                try:
                    cli_cwd = os.getcwd()
                except Exception:
                    cli_cwd = "n/a"
                requested_path = None
                try:
                    args_ctx = self._tool_args_by_call_id.get(call_id, {}) if call_id else {}
                    requested_path = args_ctx.get("path", None) if isinstance(args_ctx, dict) else None
                except Exception:
                    requested_path = None
                self.ui.print(
                    f"[{self.ui.theme['dim']}]list_dir context — requested path: {requested_path if requested_path is not None else '(unknown)'} | scope: {self._fs_label()} | CLI cwd: {cli_cwd}[/{self.ui.theme['dim']}]"
                )
            return

        data = result.get("data", {}) or {}
        if name == "read_file":
            path = data.get("path", "")
            content = data.get("content", "") or ""
            tokens = data.get("tokens_used", None)
            if isinstance(tokens, int):
                extra = f"~{tokens} tokens"
            else:
                # Backward-compat fallback to chars
                chars = len(content)
                extra = f"{chars} chars"
            self.ui.print(f"⇐ [{self.ui.theme['tool_result']}]✅ Read {extra} from {path}[/{self.ui.theme['tool_result']}]")
            # If the client truncated a read (post-error tailing), surface a brief notice
            try:
                if bool(data.get("truncated")):
                    pol = data.get("truncation_policy") or {}
                    tail_lines = int(pol.get("tail_lines", 50) or 50)
                    char_cap = int(pol.get("char_cap", 30000) or 30000)
                    orig_chars = pol.get("original_chars")
                    reason = pol.get("reason") or "auto-large-file"
                    note = (
                        f"[tail] {reason}; returned only the last {tail_lines} lines (capped to {char_cap} chars)"
                        + (f" from {int(orig_chars)} chars" if isinstance(orig_chars, int) else "")
                    )
                    self.ui.print(note, style=self.ui.theme["warn"]) 
            except Exception:
                pass
            # Show a short preview
            preview = content.strip().splitlines()
            if preview:
                preview_text = "\n".join(preview[:8])
                if len(preview) > 8:
                    preview_text += "\n... (truncated)"
                if self.ui.rich:
                    self.ui.print(Panel(preview_text, title="Preview", border_style=self.ui.theme["dim"]))
                else:
                    self.ui.print("Preview:")
                    self.ui.print(preview_text)

        elif name == "write_file":
            path = data.get("path", "")
            tokens = data.get("tokens_used", None)
            if isinstance(tokens, int):
                extra = f"~{tokens} tokens written"
            else:
                # Backward-compat fallback
                n = data.get("bytes_written", None)
                extra = f"{n} bytes written" if isinstance(n, int) else "written"
            self.ui.print(f"⇐ [{self.ui.theme['tool_result']}]✅ Wrote to {path} ({extra})[/{self.ui.theme['tool_result']}]")

        elif name == "append_file":
            path = data.get("path", "")
            tokens = data.get("tokens_used", None)
            if isinstance(tokens, int):
                extra = f"~{tokens} tokens appended"
            else:
                # Backward-compat fallback
                n = data.get("bytes_appended", None)
                extra = f"{n} bytes appended" if isinstance(n, int) else "appended"
            self.ui.print(f"⇐ [{self.ui.theme['tool_result']}]✅ Appended to {path} ({extra})[/{self.ui.theme['tool_result']}]")

        elif name == "list_dir":
            path = data.get("path", "")
            items = data.get("items", []) or []
            self.ui.print(f"⇐ [{self.ui.theme['tool_result']}]✅ Listed {len(items)} item(s) under {path}[/{self.ui.theme['tool_result']}]")
            # Show working directory context for clarity
            try:
                cli_cwd = os.getcwd()
            except Exception:
                cli_cwd = "n/a"
            self.ui.print(f"[{self.ui.theme['dim']}]Working dir (resolved): {path} | scope: {self._fs_label()} | CLI cwd: {cli_cwd}[/{self.ui.theme['dim']}]")
            # Summarize first N items in a small table
            rows: List[Tuple[str, str, str]] = []
            for it in items[: self.max_dir_items]:
                itype = "📁 dir" if it.get("is_dir") else "📄 file"
                size = str(it.get("size", "")) if not it.get("is_dir") else ""
                rows.append((str(it.get("name", "")), itype, size))
            if rows:
                self.ui.table("Contents (preview)", rows)
            if len(items) > self.max_dir_items:
                self.ui.print(f"[{self.ui.theme['dim']}]... plus {len(items) - self.max_dir_items} more[/{self.ui.theme['dim']}]")

        elif name == "edit_file":
            path = data.get("path", "")
            applied = data.get("operations_applied", 0)
            lines_before = data.get("lines_before")
            lines_after = data.get("lines_after")
            delta_lines = data.get("delta_lines")
            growth_factor = data.get("growth_factor")
            ops_counts = data.get("ops_counts") or {}
            sr_matches = data.get("search_replace_total_matches")
            diff_stats = data.get("diff_stats") or {}

            # Compose a concise summary
            growth_str = ""
            if isinstance(growth_factor, (int, float)):
                try:
                    growth_str = f", x{growth_factor:.2f}"
                except Exception:
                    growth_str = ""

            lines_str = ""
            if lines_before is not None and lines_after is not None:
                lines_str = f" | lines: {lines_before} -> {lines_after} ({'+' if (delta_lines or 0) >= 0 else ''}{delta_lines}{growth_str})"

            self.ui.print(
                f"⇐ [{self.ui.theme['tool_result']}]✅ Edited {path} ({applied} op(s)){lines_str}[/{self.ui.theme['tool_result']}]"
            )

            # Ops breakdown
            if ops_counts:
                parts = [f"{k}:{v}" for k, v in sorted(ops_counts.items())]
                self.ui.print(f"[{self.ui.theme['dim']}]ops: " + ", ".join(parts) + f"{f' | search_replace_matches:{sr_matches}' if sr_matches else ''}[/{self.ui.theme['dim']}]")

            # Diff stats
            if diff_stats:
                la = diff_stats.get("lines_added")
                lr = diff_stats.get("lines_removed")
                self.ui.print(f"[{self.ui.theme['dim']}]diff stats: +{la} / -{lr}[/{self.ui.theme['dim']}]")

            safeguard = data.get("safeguard_triggered", False)
            if safeguard:
                msg = data.get("message") or "Safeguard triggered for large result."
                self.ui.print(f"[{self.ui.theme['warn']}]⚠ {msg}[/{self.ui.theme['warn']}]")
                self.ui.print(f"[{self.ui.theme['dim']}]You should receive an approval prompt to apply or cancel this change.[/{self.ui.theme['dim']}]")
            # Show warnings if present
            warns = data.get("warnings") or []
            if warns:
                self.ui.print(f"[{self.ui.theme['warn']}]Warnings:[/{self.ui.theme['warn']}]")
                for w in warns[:10]:
                    self.ui.print(f"- {self._clip(w, 300)}", style=self.ui.theme["dim"])
                if len(warns) > 10:
                    self.ui.print(f"[{self.ui.theme['dim']}]... {len(warns)-10} more warning(s)[/{self.ui.theme['dim']}]")
            # Ops debug (compact)
            dbg = data.get("ops_debug") or []
            if dbg:
                self.ui.print(f"[{self.ui.theme['dim']}]debug (first {min(10, len(dbg))} ops):[/{self.ui.theme['dim']}]")
                for d in dbg[:10]:
                    line = f"op#{d.get('idx')} {d.get('type')}"
                    if d.get("type") == "search_replace":
                        line += f" matches={d.get('matches')} flags='{d.get('flags')}' use_regex={d.get('use_regex')} pattern='{self._clip(d.get('pattern_preview'), 120)}'"
                    if d.get("type") == "smart_anchor_insert":
                        line += f" anchor='{self._clip(d.get('anchor_preview'), 120)}'"
                    self.ui.print(line, style=self.ui.theme["dim"])

        elif name == "string_replace":
            summ = data.get("summary", {}) or {}
            try:
                total = int(summ.get("total_replacements", 0) or 0)
                targets = int(summ.get("total_targets", 0) or 0)
                files_changed = int(summ.get("files_changed", 0) or 0)
                files_considered = int(summ.get("files_considered", 0) or 0)
            except Exception:
                total = targets = files_changed = files_considered = 0
            scope = f"across {files_changed}/{files_considered} file(s)" if files_considered else (f"in {files_changed} file(s)" if files_changed else "")
            if targets:
                self.ui.print(f"\u21d0 [{self.ui.theme['tool_result']}]\u2705 Replaced {total}/{targets} {scope}[/{self.ui.theme['tool_result']}]")
            else:
                self.ui.print(f"\u21d0 [{self.ui.theme['tool_result']}]\u2705 Replaced {total} {scope}[/{self.ui.theme['tool_result']}]")
            # Verbose per-file breakdown and example pairs
            if self.ui.verbose:
                details = data.get("details", []) or []
                max_examples = 5
                for d in details[:50]:
                    try:
                        path = d.get("path")
                        reps = int(d.get("replacements", 0) or 0)
                        tgts = int(d.get("targets", 0) or 0)
                        changed = bool(d.get("changed"))
                        self.ui.print(f"- {path}: {reps}/{tgts} replaced{' (changed)' if changed else ''}", style=self.ui.theme["dim"])  # type: ignore
                        # Examples of 'from' -> 'to'
                        exs = d.get("examples") or []
                        shown = 0
                        for ex in exs:
                            if shown >= max_examples:
                                break
                            frm = self._clip(ex.get("from", ""), 160)
                            to = self._clip(ex.get("to", ""), 160)
                            self.ui.print(f"    '{frm}' -> '{to}'", style=self.ui.theme["dim"])  # type: ignore
                            shown += 1
                        if exs and len(exs) > shown:
                            self.ui.print(f"    ... +{len(exs)-shown} more", style=self.ui.theme["dim"])  # type: ignore
                    except Exception:
                        continue
        elif name == "run_command":
            data = result.get("data", {}) or {}
            exit_code = data.get("exit_code")
            timed_out = data.get("timed_out", False)
            dur = data.get("duration_ms")
            self.ui.print(f"⇐ [{self.ui.theme['tool_result']}]✅ Command finished (exit={exit_code}, timed_out={timed_out}, {dur} ms)[/{self.ui.theme['tool_result']}]")

            stdout = (data.get("stdout") or "").strip("\n")
            stderr = (data.get("stderr") or "").strip("\n")

            if stdout:
                preview = "\n".join(stdout.splitlines()[:40])
                if self.ui.rich:
                    self.ui.print(Panel(preview, title="STDOUT (preview)", border_style=self.ui.theme["dim"]))
                else:
                    self.ui.print("STDOUT (preview):")
                    self.ui.print(preview)
            if stderr:
                preview = "\n".join(stderr.splitlines()[:40])
                if self.ui.rich:
                    self.ui.print(Panel(preview, title="STDERR (preview)", border_style=self.ui.theme["dim"]))
                else:
                    self.ui.print("STDERR (preview):")
                    self.ui.print(preview)

        else:
            # Unknown tool; just show JSON
            self.ui.print(f"⇐ [{self.ui.theme['tool_result']}]✅ {name} succeeded[/{self.ui.theme['tool_result']}]")
            self.ui.print(truncate_json(result, 600), style=self.ui.theme["dim"])
    def _render_web_search_summary(self, calls: List[Dict[str, Any]]) -> None:
        if not calls:
            return
        try:
            self.ui.print("\n\ud83d\udd0d Web search", style=self.ui.theme["info"])
        except Exception:
            pass
        for idx, call in enumerate(calls, 1):
            action = call.get("action") if isinstance(call, dict) else None
            if not isinstance(action, dict):
                action = {}
            query = action.get("query") or action.get("search_query") or "(no query)"
            try:
                self.ui.print(f"  [{idx}] {query}", style=self.ui.theme["dim"])
            except Exception:
                pass
            sources = action.get("sources")
            if not sources:
                sources = action.get("results")
            if isinstance(sources, list) and sources:
                for src_idx, source in enumerate(sources[:5], 1):
                    if not isinstance(source, dict):
                        continue
                    title = source.get("title") or source.get("url") or f"source {src_idx}"
                    url = source.get("url") or ""
                    try:
                        if url:
                            self.ui.print(f"     - {title} — {url}", style=self.ui.theme["dim"])
                        else:
                            self.ui.print(f"     - {title}", style=self.ui.theme["dim"])
                    except Exception:
                        pass
                if len(sources) > 5:
                    try:
                        self.ui.print(f"     - ... {len(sources) - 5} more", style=self.ui.theme["dim"])
                    except Exception:
                        pass

    # ---------------------------- Commands ----------------------------

    async def login(self) -> bool:
        """Authenticate against the FastAPI backend and persist cookies in-memory.
        Returns True on success, False on non-fatal failure. For a 401 Invalid username or password,
        the CLI will exit to prevent proceeding while unauthenticated.
        """
        username = self.ui.prompt("Username")
        password = getpass.getpass("Password: ")
        # Ask up-front so we can request a persistent refresh cookie from the server
        stay_logged_in = True
        try:
            choice = await self._menu_choice(
                "Stay logged in?",
                "Do you want to stay logged in on this machine (device-bound refresh tokens)?",
                [
                    ("yes", "Yes - keep me logged in"),
                    ("no", "No - only this session"),
                ],
            )
            stay_logged_in = (choice != "no")
        except Exception:
            stay_logged_in = True
        # Ensure we have a stable device identity for device-bound refresh tokens
        if stay_logged_in and not self.device_id:
            try:
                # Load existing device_id from disk if any
                self._load_auth_state_from_disk()
            except Exception:
                pass
            if not self.device_id:
                # Generate and keep in memory; will be persisted only if user confirms saving
                self.device_id = uuid.uuid4().hex
        try:
            # Build an SSE-friendly timeout config when no explicit timeout provided
            if self.timeout is None:
                http_timeout = httpx.Timeout(connect=10.0, read=None, write=10.0, pool=10.0)
            else:
                http_timeout = httpx.Timeout(self.timeout)

            async with httpx.AsyncClient(timeout=http_timeout, cookies=self.cookies) as client:
                body = {
                    "username": username,
                    "password": password,
                    # Request persistent refresh cookie when user asked to stay logged in
                    "remember_me": bool(stay_logged_in),
                }
                if stay_logged_in and self.device_id:
                    body.update({
                        "device_id": self.device_id,
                        "device_name": self.device_name or f"{socket.gethostname()} cli",
                    })
                resp = await client.post(self.login_url, json=body)
                if resp.status_code >= 400:
                    # Read body safely
                    raw_text = ""
                    try:
                        body = await resp.aread()
                        raw_text = body.decode("utf-8", errors="replace")
                    except Exception:
                        raw_text = resp.text
                    # Try JSON parse to inspect detail
                    detail = None
                    try:
                        if raw_text:
                            j = json.loads(raw_text)
                            if isinstance(j, dict):
                                detail = j.get("detail")
                    except Exception:
                        detail = None
                    # Specific gate: 401 Invalid username or password -> do not proceed
                    if resp.status_code == 401 and isinstance(detail, str) and detail.lower() == "invalid username or password":
                        self.ui.error(f"Login failed: 401 {{\"detail\":\"Invalid username or password\"}}")
                        # Hard exit per requirement: do not let the user proceed
                        raise SystemExit(1)
                    # Generic failure (non-401 or different detail): report and allow retry
                    self.ui.error(f"Login failed: {resp.status_code} {raw_text}")
                    return False

                # Persist cookies returned by server (includes refresh when remember_me=true)
                self.cookies.update(resp.cookies)

                # Optional: confirm
                try:
                    chk = await client.get(self.check_auth_url)
                    if chk.status_code == 200:
                        data = chk.json()
                        if data.get("authenticated"):
                            self.auth_user = str(data.get("user") or username)
                            self.ui.success(f"Login successful. Authenticated as: {self.auth_user}")
                            # Persist auth state if user opted to stay logged in
                            try:
                                if stay_logged_in:
                                    self._save_auth_state_to_disk()
                                    self.ui.print("[auth] Login state saved locally.", style=self.ui.theme["dim"])
                                else:
                                    # Ensure any previous persisted state is cleared
                                    self._clear_auth_state_on_disk()
                            except Exception:
                                pass
                            return True
                except Exception:
                    pass

                self.ui.success("Login successful.")
                # Persist state based on original choice even if check-auth skipped
                try:
                    if stay_logged_in:
                        self._save_auth_state_to_disk()
                        self.ui.print("[auth] Login state saved locally.", style=self.ui.theme["dim"])
                    else:
                        self._clear_auth_state_on_disk()
                except Exception:
                    pass
                return True
        except SystemExit:
            # Re-raise hard exit so callers don't swallow it
            raise
        except Exception as e:
            self.ui.error(f"Login error: {e}")
            return False

    async def logout(self) -> None:
        try:
            async with httpx.AsyncClient(timeout=self.timeout, cookies=self.cookies) as client:
                resp = await client.post(self.logout_url)
                if resp.status_code >= 400:
                    try:
                        body = await resp.aread()
                        msg = body.decode("utf-8", errors="replace")
                    except Exception:
                        msg = resp.text
                    self.ui.warn(f"Logout request returned {resp.status_code}: {msg}")
                # Clear local cookie jar regardless
                self.cookies.clear()
                self.auth_user = None
                self.ui.success("Logged out.")
                # Also clear persisted auth on disk
                self._clear_auth_state_on_disk()
        except Exception as e:
            self.ui.error(f"Logout error: {e}")

    async def handle_command(self, user_input: str) -> bool:
        # Slash commands for power users
        cmd = user_input.strip()

        # Common typo alias
        if cmd == "/clera":
            cmd = "/clear"

        if cmd in ("/menu", "/settings"):
            # Open new settings UI (no dependencies). Legacy menu behind HENOSIS_SETTINGS_LEGACY=1
            await self.open_settings()
            return True

        if cmd.startswith("/history"):
            parts = cmd.split(maxsplit=1)
            if len(parts) == 1:
                self.ui.info("Usage: /history on|off")
                self.ui.info(f"Current: {'ON (synced to unified memory)' if self.save_chat_history else 'OFF (ephemeral)'}")
                return True
            arg = parts[1].strip().lower()
            if arg == "on":
                self.save_chat_history = True
                self.ui.success("Chat history will be saved to unified memory.")
            elif arg == "off":
                self.save_chat_history = False
                self.ui.success("Chat history is now ephemeral (local only, not synced).")
            else:
                self.ui.warn("Usage: /history on|off")
                return True
            self.save_settings()
            return True

        if cmd.startswith("/tools"):
            parts = cmd.split(maxsplit=1)
            if len(parts) == 1:
                self.ui.info("Usage: /tools on | /tools off | /tools default")
                self.ui.info(f"Current: {self._tools_label()}")
                return True
            arg = parts[1].strip().lower()
            if arg == "on":
                self.requested_tools = True
            elif arg == "off":
                self.requested_tools = False
            elif arg == "default":
                self.requested_tools = None
            else:
                self.ui.warn("Invalid value. Use: on, off, or default")
                return True
            self.ui.success(f"Tools set to: {self._tools_label()}")
            self.save_settings()
            return True

        if cmd.startswith("/websearch"):
            parts = cmd.split(maxsplit=2)
            if len(parts) == 1:
                self.ui.info(f"Web search: {'ON' if self.web_search_enabled else 'OFF'}")
                if self.web_search_allowed_domains:
                    self.ui.info(f"Allowed domains ({len(self.web_search_allowed_domains)}): {', '.join(self.web_search_allowed_domains)}")
                else:
                    self.ui.info("Allowed domains: (none)")
                self.ui.info(f"Include sources: {'ON' if self.web_search_include_sources else 'OFF'}")
                if self.web_search_location:
                    loc_str = ", ".join(f"{k}={v}" for k, v in self.web_search_location.items())
                    self.ui.info(f"Location hint: {loc_str}")
                else:
                    self.ui.info("Location hint: (none)")
                self.ui.info("Usage: /websearch on|off | /websearch domains <comma-separated> | /websearch domains clear | /websearch sources on|off | /websearch location country=US city=London | /websearch location clear")
                return True
            sub = parts[1].strip().lower()
            arg = parts[2].strip() if len(parts) > 2 else ""
            if sub in ("on", "off"):
                self.web_search_enabled = (sub == "on")
                self.ui.success(f"Web search {'enabled' if self.web_search_enabled else 'disabled'}.")
                self.save_settings()
                return True
            if sub == "domains":
                if not arg:
                    if self.web_search_allowed_domains:
                        self.ui.info(f"Allowed domains ({len(self.web_search_allowed_domains)}): {', '.join(self.web_search_allowed_domains)}")
                    else:
                        self.ui.info("Allowed domains: (none)")
                    self.ui.info("Usage: /websearch domains example.com,another.com | /websearch domains clear")
                    return True
                if arg.lower() in ("clear", "none"):
                    self.web_search_allowed_domains = []
                    self.ui.success("Cleared web search domain allow-list.")
                else:
                    raw = arg.replace("\n", ",")
                    domains = [d.strip() for d in raw.split(",") if d.strip()]
                    if not domains:
                        self.ui.warn("No valid domains provided.")
                        return True
                    if len(domains) > 20:
                        self.ui.warn("Only the first 20 domains are allowed. Excess entries were ignored.")
                        domains = domains[:20]
                    self.web_search_allowed_domains = domains
                    self.ui.success(f"Web search allowed domains set ({len(domains)}).")
                self.save_settings()
                return True
            if sub == "sources":
                val = arg.lower()
                if val not in ("on", "off"):
                    self.ui.warn("Usage: /websearch sources on|off")
                    return True
                self.web_search_include_sources = (val == "on")
                self.ui.success(f"Include sources in web search response payload: {'ON' if self.web_search_include_sources else 'OFF'}")
                self.save_settings()
                return True
            if sub == "location":
                if not arg:
                    if self.web_search_location:
                        loc_str = ", ".join(f"{k}={v}" for k, v in self.web_search_location.items())
                        self.ui.info(f"Current web search location hint: {loc_str}")
                    else:
                        self.ui.info("No web search location hint set.")
                    self.ui.info("Usage: /websearch location country=US city=Seattle region=Washington | /websearch location clear")
                    return True
                if arg.lower() == "clear":
                    self.web_search_location = {}
                    self.ui.success("Cleared web search location hint.")
                    self.save_settings()
                    return True
                tokens = arg.replace(",", " ").split()
                loc: Dict[str, str] = {}
                for token in tokens:
                    if "=" not in token:
                        continue
                    key, value = token.split("=", 1)
                    key = key.strip()
                    value = value.strip()
                    if key and value:
                        loc[key] = value
                if not loc:
                    self.ui.warn("No valid key=value pairs provided. Example: /websearch location country=US city=Seattle")
                    return True
                if "type" not in loc:
                    loc["type"] = "approximate"
                self.web_search_location = loc
                self.ui.success("Web search location hint updated.")
                self.save_settings()
                return True
            self.ui.warn("Unknown /websearch subcommand. Use on, off, domains, sources, or location.")
            return True

        if cmd.startswith("/reasoning"):
            parts = cmd.split(maxsplit=1)
            if len(parts) == 1:
                self.ui.info("Usage: /reasoning low|medium|high")
                self.ui.info(f"Current: {self.reasoning_effort}")
                return True
            arg = (parts[1] or "").strip().lower()
            if arg in ("low", "medium", "high"):
                self.reasoning_effort = arg
                self.ui.success(f"Reasoning effort set to: {self.reasoning_effort}")
                self.save_settings()
            else:
                self.ui.warn("Invalid value. Use: low, medium, or high")
            return True

        if cmd.startswith("/thinkingbudget"):
            parts = cmd.split(maxsplit=1)
            if len(parts) == 1:
                cur = self.thinking_budget_tokens if isinstance(self.thinking_budget_tokens, int) else "default"
                self.ui.info("Usage: /thinkingbudget <tokens>|default")
                self.ui.info(f"Current: {cur}")
                self.ui.info("Note: Applies only to Anthropic models with '-thinking' suffix; server default is used when set to 'default'.")
                return True
            arg = (parts[1] or "").strip().lower()
            if arg in ("default", "none", "off"):
                self.thinking_budget_tokens = None
                self.ui.success("Thinking budget set to server default.")
                self.save_settings()
                return True
            # Accept integers with optional 'k' suffix (e.g., 20k)
            val_str = arg
            mul = 1
            if val_str.endswith("k"):
                val_str = val_str[:-1]
                mul = 1000
            try:
                n = int(val_str)
                n = n * mul
                if n <= 0:
                    raise ValueError()
                if n > 100_000_000:
                    self.ui.warn("Value too large; capping at 100,000,000 tokens.")
                    n = 100_000_000
                self.thinking_budget_tokens = n
                self.ui.success(f"Thinking budget set to: {n} tokens (applies to '-thinking' Anthropic models)")
                self.save_settings()
            except ValueError:
                self.ui.warn("Invalid value. Use an integer (e.g., 20000 or 20k) or 'default'.")
            return True

        if cmd.startswith("/fs "):
            arg = cmd[len("/fs ") :].strip().lower()
            if arg in ("workspace", "host"):
                self.fs_scope = arg
                self.ui.success(f"FS Scope set to: {self._fs_label()}")
            elif arg == "default":
                self.fs_scope = None
                self.ui.success("FS Scope set to: SERVER DEFAULT")
            else:
                self.ui.warn("Usage: /fs workspace | /fs host | /fs default")
                return True
            self.save_settings()
            return True

        if cmd.startswith("/agent-scope "):
            path = cmd[len("/agent-scope ") :].strip()
            if not path:
                self.ui.warn("Usage: /agent-scope <absolute path>")
                return True
            self.host_base = path
            self._host_base_ephemeral = False
            self.ui.success(f"Agent scope set to: {self.host_base}")
            self.save_settings()
            try:
                self._codebase_map_raw = self._load_codebase_map_raw()
            except Exception:
                pass
            try:
                await self._offer_generate_code_map(self.host_base)
            except Exception:
                pass
            return True

        if cmd.startswith("/hostbase "):
            path = cmd[len("/hostbase ") :].strip()
            if not path:
                self.ui.warn("Usage: /hostbase <absolute path>")
                return True
            self.host_base = path
            self._host_base_ephemeral = False
            self.ui.success(f"Agent scope set to: {self.host_base}")
            self.save_settings()
            # Refresh codebase map source to prefer the configured host base
            try:
                self._codebase_map_raw = self._load_codebase_map_raw()
            except Exception:
                pass
            # Offer code map generation when newly set
            try:
                await self._offer_generate_code_map(self.host_base)
            except Exception:
                pass
            return True

        if cmd.startswith("/hostmode "):
            mode = cmd[len("/hostmode ") :].strip().lower()
            if mode not in ("any", "cwd", "custom"):
                self.ui.warn("Usage: /hostmode any|cwd|custom")
                return True
            self.fs_host_mode = mode
            if mode == "cwd":
                try:
                    self.host_base = os.getcwd()
                    self._host_base_ephemeral = False
                except Exception:
                    pass
            if mode == "custom" and not self.host_base:
                self.ui.warn("Host mode 'custom' selected but host_base is unset. Use /hostbase <path>.")
            self.ui.success(f"Host mode set to: {self.fs_host_mode} (host_base={self.host_base or '(none)'})")
            self.save_settings()
            return True

        if cmd == "/trust":
            await self._trust_menu()
            return True

        if cmd.startswith("/model "):
            raw = cmd[len("/model ") :].strip() or None
            self.model = self._resolve_model_alias(raw)
            if not self.model:
                self.ui.info("Model cleared; server default will be used.")
            else:
                self.ui.success(f"Model set to: {self.model}")
            self._apply_model_side_effects()
            self.save_settings()
            return True

        if cmd.startswith("/infomode"):
            parts = cmd.split(maxsplit=1)
            if len(parts) == 1:
                self.ui.info("Usage: /infomode concise|verbose")
                self.ui.info(f"Current: {self.usage_info_mode}")
                return True
            arg = (parts[1] or "").strip().lower()
            if arg in ("concise", "verbose"):
                self.usage_info_mode = arg
                self.ui.success(f"Usage & Info mode set to: {self.usage_info_mode}")
                self.save_settings()
            else:
                self.ui.warn("Invalid value. Use: concise or verbose")
            return True
        if cmd == "/model":
            # Open the model selection menu directly
            await self.select_model_menu()
            return True

        if cmd.startswith("/level "):
            try:
                lvl = int(cmd[len("/level "):].strip())
                if lvl not in (1, 2, 3):
                    raise ValueError()
                self.control_level = lvl
                self.ui.success(f"Control level set to: {self.control_level}")
            except Exception:
                self.ui.warn("Usage: /level 1|2|3")
                return True
            self.save_settings()
            return True

        if cmd.startswith("/autoapprove "):
            s = cmd[len("/autoapprove "):].strip()
            names = [t.strip() for t in s.split(",") if t.strip()]
            self.auto_approve = names
            self.ui.success(f"Auto-approve set to: {','.join(self.auto_approve) if self.auto_approve else '(none)'}")
            self.save_settings()
            return True

        if cmd.startswith("/system "):
            self.system_prompt = cmd[len("/system ") :].strip()
            self.history = []
            if self.system_prompt:
                self.history.append({"role": "system", "content": self.system_prompt})
            # Treat as a fresh session; allow map re-injection
            self._did_inject_codebase_map = False
            # Also allow custom first-turn injection again
            try:
                self._did_inject_custom_first_turn = False
            except Exception:
                pass
            self.ui.success("System prompt set.")
            self.save_settings()
            return True

        if cmd.startswith("/title "):
            new_title = cmd[len("/title ") :].strip()
            if not new_title:
                self.ui.warn("Usage: /title <name>")
                return True
            self.thread_name = new_title
            self._manual_title = True
            self.ui.success(f"Thread title set to: {self.thread_name}")
            return True

        if cmd == "/clear":
            self.history = [{"role": "system", "content": self.system_prompt}] if self.system_prompt else []
            self._did_inject_codebase_map = False
            try:
                self._did_inject_custom_first_turn = False
            except Exception:
                pass
            # Reset provider-native histories
            try:
                self.messages_for_save = []
                if not self.save_chat_history:
                    self.thread_uid = None
                self._kimi_raw_history = []
            except Exception:
                pass
            # Reset local cumulative token counters on session clear
            self._cum_input_tokens = 0
            self._cum_output_tokens = 0
            self._cum_total_tokens = 0
            # Reset cumulative reasoning tokens as well
            try:
                self._cum_reasoning_tokens = 0
            except Exception:
                pass
            # Reset cost accumulators and last billing details on session clear
            try:
                self.server_cumulative_cost_usd = 0.0
                self.cumulative_cost_usd = 0.0
                self._last_commit_cost_usd = 0.0
                self._last_remaining_credits = None
            except Exception:
                pass
            # Reset session wall-clock timer on clear
            try:
                self._session_started_at = time.perf_counter()
            except Exception:
                self._session_started_at = None
            self.ui.success("History cleared.")
            return True

        if cmd == "/toolslog":
            self.show_tool_calls = not self.show_tool_calls
            self.ui.success(f"Tool call logs: {'ON' if self.show_tool_calls else 'OFF'}")
            self.save_settings()
            return True

        if cmd.startswith("/map "):
            val = cmd[len("/map ") :].strip().lower()
            if val in ("on", "true", "1"):
                self.inject_codebase_map = True
                # allow re-injection on next message
                self._did_inject_codebase_map = False
                self.ui.success("Codebase map prefix: ON")
            elif val in ("off", "false", "0"):
                self.inject_codebase_map = False
                self.ui.success("Codebase map prefix: OFF")
            else:
                self.ui.warn("Usage: /map on | /map off")
                return True
            self.save_settings()
            return True

        if cmd == "/login":
            await self._login_with_retries()
            return True

        if cmd == "/logout":
            await self.logout()
            # Exit the CLI after logging out per request
            print("Goodbye.")
            raise SystemExit(0)

        if cmd == "/configure":
            # Force-run the first-time configuration wizard even for existing users
            await self._maybe_run_first_time_wizard(force=True)
            return True

        # /preflight removed from CLI (server handles any background estimation)

        if cmd == "/whoami":
            authed = await self.check_auth()
            if authed:
                self.ui.success(f"Authenticated as: {self.auth_user}")
            else:
                self.ui.warn("Not authenticated.")
            return True

        return False

    # ---------------------------- Run loop ----------------------------

    async def run(self) -> None:
        # Try persisted auth
        self._load_auth_state_from_disk()
        
        # Proactively refresh tokens at startup if authenticated
        try:
            if self.cookies.get('refresh_token_cookie'):
                timeout = httpx.Timeout(connect=10.0, read=30.0, write=10.0, pool=10.0) if self.timeout is None else httpx.Timeout(self.timeout)
                async with httpx.AsyncClient(timeout=timeout, cookies=self.cookies) as client:
                    # Refresh to get current tokens and persist if rotated
                    r = await client.post(self.refresh_url, timeout=30.0)
                    if r.status_code == 200:
                        data = r.json()
                        if data.get('rotated'):
                            self._save_auth_state_to_disk()
                            self.ui.print("[auth] Tokens refreshed and saved", style=self.ui.theme["dim"])
        except Exception as e:
            # Non-fatal; continue with existing tokens
            if self.ui.verbose:
                self.ui.print(f"[auth] Token refresh check skipped: {e}", style=self.ui.theme["dim"])
        
        # If not authenticated, show a focused welcome screen
        if not await self.check_auth():
            await self._welcome_flow()
            # Re-check after potential login/registration
            if not await self.check_auth():
                self.ui.error("Authentication required. Exiting.")
                raise SystemExit(1)

        # Start Agent Mode WS hub (dev-only)
        if self.agent_mode:
            if not HAS_WS:
                self.ui.warn("Agent Mode requested but 'websockets' is not available. Proceeding without WS.")
            else:
                try:
                    await self._start_ws_hub()
                    self.ui.print(f"[agent] WS listening on ws://{self.agent_host}:{self.agent_port}/agent/ws", style=self.ui.theme["dim"])
                except Exception as e:
                    self.ui.warn(f"Failed to start Agent WS hub: {e}")

        # Once authenticated, sync settings with the server
        try:
            await self._sync_settings_with_server()
        except Exception:
            # Non-fatal; continue with local defaults
            pass
        # Load profile once to detect subscription tier (free vs paid) for UX defaults
        try:
            await self._load_profile_for_tier()
        except Exception:
            # Non-fatal; if /profile is unavailable, keep prior behavior
            pass
        # Ensure per-terminal Agent scope binding after server sync
        try:
            self._rebind_agent_scope_default()
        except Exception:
            pass

        # Run first-run wizard when settings are at defaults
        try:
            await self._maybe_run_first_time_wizard()
        except Exception as e:
            self.ui.warn(f"Wizard skipped: {e}")

        # Header after auth and settings sync
        # Show CLI version from metadata/pyproject when available
        if not self._cli_version:
            try:
                self._cli_version = self._resolve_current_version() or None
            except Exception:
                self._cli_version = None
        # Build opening header: "You are using henosis-cli v.x.x.x in <root>"
        # Determine the session root the CLI is operating in. Prefer the Agent scope (host_base) when set,
        # otherwise fall back to the local workspace directory, and finally the current working directory.
        try:
            session_root = None
            if isinstance(self.host_base, str) and self.host_base.strip():
                session_root = self.host_base
            elif isinstance(self.local_workspace_dir, str) and self.local_workspace_dir.strip():
                session_root = self.local_workspace_dir
            else:
                session_root = str(Path(os.getcwd()).resolve())
        except Exception:
            session_root = self.host_base or self.local_workspace_dir or os.getcwd()

        left_header = (
            f"You are using henosis-cli{(' v' + self._cli_version) if self._cli_version else ''} in {session_root}"
        )
        # For the right-aligned segment, show just the selected model name (omit '(server default)')
        selected_model = None
        try:
            if isinstance(self.model, str) and self.model.strip():
                selected_model = self.model.strip()
        except Exception:
            selected_model = None
        # Render single-line header with left message and optional right model label
        try:
            self.ui.header_inline(left_header, selected_model)
        except Exception:
            # Fallback plain header
            self.ui.header(left_header, subtitle=(selected_model or None))
        # Dev visibility: confirm whether local tools are importable on this client
        try:
            self.ui.print(f"[dev] Local tools available: {HAS_LOCAL_TOOLS}", style=self.ui.theme["dim"]) 
        except Exception:
            pass

        # Start chat immediately (suppress verbose startup banner)
        # Code map status line (prefer host base presence indicator)
        host_map_present = False
        try:
            if isinstance(self.host_base, str) and self.host_base.strip():
                host_map_present = self._code_map_exists_at(self.host_base)
        except Exception:
            host_map_present = False
        if not self.inject_codebase_map:
            self.ui.print("Code Map: OFF — toggle with /map on|off", style=self.ui.theme["dim"])
        else:
            if host_map_present:
                self.ui.print("Code Map: PRESENT at host base and will be prefixed to your first message.", style=self.ui.theme["dim"])
            elif self._codebase_map_raw:
                # We have a fallback map (repo copy) but none at host base
                self.ui.print("Code Map: fallback example in use (host base missing CODEBASE_MAP.md). It will be prefixed.", style=self.ui.theme["dim"])
            else:
                self.ui.print("Code Map: missing at host base — toggle with /map on|off", style=self.ui.theme["dim"])
        # History status
        hist_status = "ON (synced)" if self.save_chat_history else "OFF (ephemeral)"
        self.ui.print(f"Chat history: {hist_status}", style=self.ui.theme["dim"])
        # If a host base is configured and code map injection is enabled, offer to generate when missing
        try:
            if (
                self.inject_codebase_map
                and self.host_base
                and isinstance(self.host_base, str)
                and self.host_base.strip()
            ):
                await self._offer_generate_code_map(self.host_base)
        except Exception:
            pass
        # Tips banner above input
        hint_line = "- " + (getattr(self._input_engine, "info", None).hint if self._input_engine and getattr(self._input_engine, "info", None) else "Enter sends; Ctrl+J inserts a newline.")
        # If no input engine is available, our plain fallback uses multiline input with empty-line submit
        if not self._input_engine:
            hint_line = "- Empty line submits; paste freely."
        tips = [
            "Tips:",
            "- Type / to show the command list.",
            "- Use /clear often, after each task, for best performance.",
        ]
        if self.ui.rich and Panel:
            self.ui.print(Panel("\n".join(tips), title="Getting started", border_style=self.ui.theme["subtitle"]))
        else:
            for t in tips:
                self.ui.print(t)
        # Light status line
        if self.auth_user:
            self.ui.print(f"Authenticated as {self.auth_user}", style=self.ui.theme["dim"])
        # Prepare logging file
        self._ensure_session_log()
        # Prepare raw log file if enabled
        if self.raw_log_enabled:
            try:
                self._ensure_raw_log()
                if self.raw_log_path:
                    self.ui.print(f"[raw] Logging raw request/response to {self.raw_log_path}", style=self.ui.theme["dim"])  # type: ignore
            except Exception:
                pass
        # Start session wall-clock timer
        try:
            self._session_started_at = time.perf_counter()
        except Exception:
            self._session_started_at = None
        # Prepare completer for slash commands (if prompt_toolkit is available)
        pt_completer = self._commands_word_completer()
        while True:
            try:
                if self._pt_session is not None:
                    # Use prompt_toolkit with inline completion when available
                    # Pass completer per-prompt to ensure latest catalog
                    user_input = await self._pt_session.prompt_async(
                        "You: ",
                        completer=pt_completer,
                        complete_while_typing=True,
                    )
                    user_input = user_input.strip()
                elif self._input_engine:
                    # Do not add continuation prefixes on new lines
                    user_input = self._input_engine.read_message("You: ", "")
                else:
                    user_input = self._read_multiline_input("You: ")
                # Successful read resets interrupt window
                self._last_interrupt_ts = None
            except KeyboardInterrupt:
                # First Ctrl+C: interrupt input and warn; second within window exits
                now = time.time()
                try:
                    last = float(self._last_interrupt_ts) if self._last_interrupt_ts is not None else None  # type: ignore
                except Exception:
                    last = None
                if last is not None and (now - last) <= 2.0:
                    self.ui.print("Goodbye.")
                    return
                # Set/refresh first-interrupt timestamp and continue loop
                self._last_interrupt_ts = now
                self.ui.warn("Interrupted. Press Ctrl+C again within 2s to exit.")
                continue
            except EOFError:
                # Graceful exit on Ctrl+D / EOF
                self.ui.print("Goodbye.")
                return

            if not user_input:
                continue

            # Command palette if bare '/'
            if user_input == "/":
                # Build choices from the slash-command catalog and show a unified
                # highlighted menu (arrow keys move, Enter selects, Esc cancels).
                items = [
                    (c["usage"], f"{c['name']} - {c['desc']}") for c in self._commands_catalog
                ]
                picked = await self._menu_choice(
                    "Commands",
                    "Use \u2191/\u2193 to move, Enter to select, Esc to cancel",
                    items,
                )
                if picked:
                    user_input = picked
                else:
                    continue
            if user_input.startswith("/") and ("\n" not in user_input):
                handled = await self.handle_command(user_input)
                if handled:
                    continue

            try:
                # Record user message for local/server save
                if self.save_chat_history:
                    self.messages_for_save.append({
                        "role": "user",
                        "content": user_input,
                        "model": None,
                        "citations": None,
                        "last_turn_input_tokens": 0,
                        "last_turn_output_tokens": 0,
                        "last_turn_total_tokens": 0,
                    })
                self._log_line({"event": "user", "content": user_input})
                # Preflight removed from CLI (handled server-side only)

                # Busy gate for serialized turns
                if self._busy:
                    self.ui.warn("Agent is busy with another turn. Please wait...")
                    continue
                self._busy = True
                try:
                    assistant_text = await self._stream_once(user_input)
                finally:
                    self._busy = False
            except httpx.HTTPStatusError as he:
                try:
                    if he.response is not None:
                        await he.response.aread()
                        body = he.response.text
                    else:
                        body = ""
                except Exception:
                    body = ""
                self.ui.error(f"[HTTP error] {he.response.status_code} {body}")
                continue
            except Exception as e:
                self.ui.error(f"[Client error] {e}")
                continue

            # Skip appending empty assistant messages to avoid 422 on next request
            if assistant_text.strip():
                # Persist the round with exactly what was sent (so first turn keeps the map)
                content_sent = self._last_built_user_content or user_input
                self.history.append({"role": "user", "content": content_sent})
                self.history.append({"role": "assistant", "content": assistant_text})

    # ----------------------------- Menus -----------------------------

    async def main_menu(self) -> Optional[str]:
        self.ui.clear()
        # Suppress verbose session overview in menu header
        self.ui.header("henosis-cli")
        # Dynamic auth action
        auth_action_key = "logout" if self.auth_user else "login"
        auth_action_label = f"🔓 Logout ({self.auth_user})" if self.auth_user else "🔑 Login"
        choices = [
            ("toggle_tools", f"🧰 Toggle Tools ({self._tools_label()}) - Enable/disable file tools per request (ON: request tools, OFF: no tools, DEFAULT: server setting)"),
            ("toggle_history", f"🕘 Toggle History ({'ON' if self.save_chat_history else 'OFF'}) - Save chats to unified memory"),
            ("set_scope", f"📦 Set Filesystem Scope (current: {self._fs_label()}) - Choose workspace (sandbox) or host (full filesystem access if allowed)"),
            ("set_host_base", f"🖥️  Set Agent Scope (current: {self.host_base or '(none)'}) - Absolute path the agent can access when host scope is enabled"),
            ("set_level", f"🔒 Set Control Level (current: {self.control_level or 'server default'}) - Security level: 1=read-only, 2=write/exec with approval, 3=full access"),
            ("set_auto_approve", f"⚙️  Set Auto-approve Tools (current: {','.join(self.auto_approve) if self.auto_approve else '(none)'}) - Tools to auto-approve at Level 2 (e.g., write_file)"),
            (auth_action_key, auth_action_label),
            ("select_model", f"📋 Select Model (current: {self.model or 'server default'}) - Pick from presets (gpt-5, gemini-2.5-pro, grok-4, deepseek-chat) or use Change Model to type one"),
            ("change_model", f"🤖 Change Model (current: {self.model or 'server default'}) - Manually type a model name"),
            ("set_system_prompt", "📝 Set System Prompt - Add initial instructions for the AI"),
            ("clear_history", "🧹 Clear History - Reset chat history"),
            ("toggle_tool_logs", f"🔎 Toggle Tool Call Logs (currently {'ON' if self.show_tool_calls else 'OFF'}) - Show/hide tool call details"),
            ("toggle_map_prefix", f"🗺️  Toggle Codebase Map Prefix (currently {'ON' if self.inject_codebase_map else 'OFF'}) - Control injecting <codebase_map> into first user message"),
            ("toggle_preflight", f"⏱️  Toggle Preflight (currently {'ON' if self.preflight_enabled else 'OFF'}) - Confirm token/cost before sending"),
            ("start_chat", "💬 Start Chatting - Begin interactive chat with the AI"),
            ("quit", "🚪 Quit - Exit the CLI"),
        ]
        # Remove legacy history toggle from menu
        try:
            choices = [c for c in choices if c[0] not in ("toggle_preflight",)]
        except Exception:
            pass
        return await self._menu_choice(
            "Session Settings",
            "Use ↑/↓ to move, Enter to select (or type a number), Esc to cancel",
            choices,
        )

    async def select_model_menu(self) -> None:
        """
        Unified model picker with highlight navigation and a Recommended section.
        - Arrow keys to move; Enter to select; Esc to cancel
        """
        current = self.model or "server default"
        title = "Select Model"
        subtitle = f"Current: {current}"
        presets = self._model_presets()

        # Determine effective tier status
        # User is "effectively free" if they are on free tier AND have no positive credit balance known.
        has_credits = (self._last_remaining_credits is not None and self._last_remaining_credits > 0)
        is_effectively_free = (self.is_free_tier and not has_credits)

        # Recommended models (ordered list for shuffling)
        # Curated list per request (include Codex Max as recommended)
        rec_keys = [
            "gpt-5.1-codex-max",
            "deepseek-reasoner-3.2",
            "claude-opus-4-5-20251101",
            "gemini-3-pro-preview",
            "gpt-5",
            "kimi-k2-thinking",
            "grok-code-fast-1",
        ]

        # If effectively free, shuffle kimi-k2-thinking to the top
        if is_effectively_free:
            target = "kimi-k2-thinking"
            if target in rec_keys:
                rec_keys.remove(target)
                rec_keys.insert(0, target)

        rec_set = set(rec_keys)

        # Build lists preserving rec_keys order
        preset_map = {m: lbl for m, lbl in presets}
        rec_list = []
        for k in rec_keys:
            if k in preset_map:
                rec_list.append((k, preset_map[k]))

        other_list = [(m, lbl) for (m, lbl) in presets if m not in rec_set]

        # Identify paid models by prefix
        paid_prefixes = ("gpt-", "claude-", "gemini-", "o1-")
        
        def is_paid_model(m_name: str) -> bool:
            return m_name.startswith(paid_prefixes)

        # Build choices
        choices: List[Tuple[str, str]] = []
        choices.append(("__hdr_rec__", "--- Recommended ---"))
        
        for m, lbl in rec_list:
            suffix = " [PAID]" if (is_effectively_free and is_paid_model(m)) else ""
            choices.append((m, f"{lbl}{suffix}"))
        
        choices.append(("__hdr_other__", "--- Other Models ---"))
        for m, lbl in other_list:
            suffix = " [PAID]" if (is_effectively_free and is_paid_model(m)) else ""
            choices.append((m, f"{lbl}{suffix}"))
        
        choices.append(("default", "Server Default (no override)"))
        choices.append(("custom", "Custom (enter a model name)"))

        # Render and select using the unified highlighted picker
        picked: Optional[str] = None
        while True:
            val = await self._menu_choice(title, subtitle, choices)
            if val in (None, "__hdr_rec__", "__hdr_other__"):
                # Ignore headers or cancel; on cancel just return
                if val is None:
                    return
                continue
            
            picked = str(val)
            
            # Enforce free tier restrictions
            if picked not in ("default", "custom") and is_effectively_free and is_paid_model(picked):
                self.ui.warn(f"Model '{picked}' is a paid tier model. Access is restricted on the free tier without credits.")
                continue
                
            break

        # Apply selection
        if picked == "default":
            self.model = None
            self.ui.info("Model cleared; server default will be used.")
        elif picked == "custom":
            typed = self.ui.prompt(
                "Enter model name (e.g., deepseek-chat, gpt-5, gemini-2.5-flash)",
                default=self.model or "",
            )
            self.model = self._resolve_model_alias(typed.strip() or None)
            if not self.model:
                self.ui.info("Model cleared; server default will be used.")
        else:
            self.model = picked
            self.ui.success(f"Model set to: {self.model}")

        self._apply_model_side_effects()
        self.save_settings()

    # ---------------------- Menu actions ---------------------------

    async def handle_choice(self, choice: Optional[str]) -> bool:
        # Returns True to continue menu loop, False to go to chat or quit
        if choice is None:
            return True

        if choice == "toggle_tools":
            if self.requested_tools is None:
                self.requested_tools = True
            elif self.requested_tools is True:
                self.requested_tools = False
            else:
                self.requested_tools = None
            self.ui.success(f"Tools set to: {self._tools_label()}")
            self.save_settings()
            return True

        if choice == "toggle_history":
            self.save_chat_history = not self.save_chat_history
            self.ui.success(f"History set to: {'ON' if self.save_chat_history else 'OFF'}")
            self.save_settings()
            return True

        if choice == "set_scope":
            await self.set_scope_menu()
            return True

        if choice == "set_host_base":
            path = self.ui.prompt("Enter absolute path for Agent scope (leave empty to clear)", default=self.host_base or "")
            path = path.strip()
            if path:
                self.host_base = path
                self._host_base_ephemeral = False
                self.ui.success(f"Agent scope set to: {self.host_base}")
            else:
                self.host_base = None
                self.ui.success("Agent scope cleared.")
            self.save_settings()
            # Refresh codebase map source to prefer the configured host base
            try:
                self._codebase_map_raw = self._load_codebase_map_raw()
            except Exception:
                pass
            # Offer to generate a code map when setting a new host base
            try:
                if self.host_base:
                    await self._offer_generate_code_map(self.host_base)
            except Exception:
                pass
            return True

        if choice == "set_level":
            await self.set_level_menu()
            return True

        if choice == "set_auto_approve":
            await self.set_auto_approve_menu()
            return True

        if choice == "login":
            await self._login_with_retries()
            return True

        if choice == "logout":
            await self.logout()
            print("Goodbye.")
            raise SystemExit(0)

        if choice == "select_model":
            await self.select_model_menu()
            return True

        if choice == "change_model":
            model = self.ui.prompt("Enter model name (blank for server default)", default=self.model or "")
            self.model = self._resolve_model_alias(model if model.strip() else None)
            if not self.model:
                self.ui.info("Model cleared; server default will be used.")
            else:
                self.ui.success(f"Model set to: {self.model}")
            self._apply_model_side_effects()
            self.save_settings()
            return True

        if choice == "set_system_prompt":
            prompt = self.ui.prompt("Enter system prompt", default=self.system_prompt or "")
            self.system_prompt = prompt.strip()
            self.history = []
            if self.system_prompt:
                self.history.append({"role": "system", "content": self.system_prompt})
            # Treat as a fresh session; allow map re-injection
            self._did_inject_codebase_map = False
            try:
                self._did_inject_custom_first_turn = False
            except Exception:
                pass
            # Clear provider-native histories on system reset
            try:
                self.messages_for_save = []
                if not self.save_chat_history:
                    self.thread_uid = None
                self._kimi_raw_history = []
            except Exception:
                pass
            self.ui.success("System prompt set.")
            self.save_settings()
            return True

        if choice == "clear_history":
            self.history = [{"role": "system", "content": self.system_prompt}] if self.system_prompt else []
            self._did_inject_codebase_map = False
            try:
                self._did_inject_custom_first_turn = False
            except Exception:
                pass
            try:
                self.messages_for_save = []
                if not self.save_chat_history:
                    self.thread_uid = None
                self._kimi_raw_history = []
            except Exception:
                pass
            # Reset local cumulative token counters on session clear
            self._cum_input_tokens = 0
            self._cum_output_tokens = 0
            self._cum_total_tokens = 0
            # Reset cumulative reasoning tokens as well
            try:
                self._cum_reasoning_tokens = 0
            except Exception:
                pass
            # Reset cost accumulators and last billing details on session clear
            try:
                self.server_cumulative_cost_usd = 0.0
                self.cumulative_cost_usd = 0.0
                self._last_commit_cost_usd = 0.0
                self._last_remaining_credits = None
            except Exception:
                pass
            # Reset session wall-clock timer on clear
            try:
                self._session_started_at = time.perf_counter()
            except Exception:
                self._session_started_at = None
            self.ui.success("History cleared.")
            return True

        if choice == "toggle_tool_logs":
            self.show_tool_calls = not self.show_tool_calls
            self.ui.success(f"Tool call logs: {'ON' if self.show_tool_calls else 'OFF'}")
            self.save_settings()
            return True

        if choice == "toggle_map_prefix":
            self.inject_codebase_map = not self.inject_codebase_map
            # Reset flag so enabling applies to next message
            if self.inject_codebase_map:
                self._did_inject_codebase_map = False
            self.ui.success(f"Codebase map prefix: {'ON' if self.inject_codebase_map else 'OFF'}")
            self.save_settings()
            return True

        # 'toggle_preflight' removed from menu

        if choice == "start_chat":
            return False  # proceed to chatting

        if choice == "quit":
            print("Goodbye.")
            raise SystemExit

        return True

    # ----------------------- SSE Streaming loop ------------------------
    async def _stream_once(self, user_input: str) -> str:
        # Build request payload
        payload: Dict[str, Any] = {"messages": self._build_messages(user_input)}
        if self.model:
            payload["model"] = self.model
        # Include terminal identifier so the server can isolate per-terminal workspace if it executes tools
        try:
            if self.terminal_id:
                payload["terminal_id"] = self.terminal_id
        except Exception:
            pass
        # Per-request tools toggle
        if self.requested_tools is True:
            payload["enable_tools"] = True
        elif self.requested_tools is False:
            payload["enable_tools"] = False
        # Per-request filesystem scope and host base
        if self.fs_scope in ("workspace", "host"):
            payload["fs_scope"] = self.fs_scope
        if self.host_base:
            payload["host_base"] = self.host_base
        # Optional passthrough for transparency (server echoes in requested_policy)
        if self.fs_scope == "host":
            mode = (self.fs_host_mode or "any")
            payload["host_roots_mode"] = mode
            if mode in ("cwd", "custom") and self.host_base:
                payload["host_allowed_dirs"] = [self.host_base]
        # Controls and approvals
        if self.control_level in (1, 2, 3):
            payload["control_level"] = self.control_level
        if self.auto_approve:
            payload["auto_approve"] = self.auto_approve
        # Reasoning effort (OpenAI reasoning models only; server will ignore for others)
        try:
            if isinstance(self.reasoning_effort, str):
                if self.reasoning_effort in ("low", "medium", "high"):
                    payload["reasoning_effort"] = self.reasoning_effort
                elif self.reasoning_effort == "xhigh" and self._is_codex_max(self.model):
                    payload["reasoning_effort"] = "xhigh"
                else:
                    payload["reasoning_effort"] = "medium"
            else:
                payload["reasoning_effort"] = "medium"
        except Exception:
            payload["reasoning_effort"] = "medium"

        # Anthropic thinking-mode budget (server ignores unless model ends with -thinking)
        try:
            if isinstance(self.thinking_budget_tokens, int) and self.thinking_budget_tokens > 0:
                payload["thinking_budget_tokens"] = int(self.thinking_budget_tokens)
        except Exception:
            pass
        # Anthropic prompt cache TTL (server override): send when set to 5m or 1h
        try:
            if isinstance(self.anthropic_cache_ttl, str) and self.anthropic_cache_ttl in ("5m", "1h"):
                payload["anthropic_cache_ttl"] = self.anthropic_cache_ttl
        except Exception:
            pass

        # Text verbosity and tool preambles preference (UI hints for the server)
        try:
            if isinstance(self.text_verbosity, str) and self.text_verbosity in ("low", "medium", "high"):
                payload["text_verbosity"] = self.text_verbosity
        except Exception:
            pass
        try:
            payload["preambles_enabled"] = bool(self.preambles_enabled)
        except Exception:
            pass

        if self.web_search_enabled:
            payload["enable_web_search"] = True
            if self.web_search_allowed_domains:
                payload["web_search_allowed_domains"] = self.web_search_allowed_domains
            if self.web_search_include_sources:
                payload["web_search_include_sources"] = True
            loc_payload = self._web_search_location_payload()
            if loc_payload:
                payload["web_search_user_location"] = loc_payload
        else:
            payload["enable_web_search"] = False

        # Idempotency key for this turn (stable across retries)
        try:
            idempotency_key = uuid.uuid4().hex
            payload["idempotency_key"] = idempotency_key
        except Exception:
            idempotency_key = None
        # Header timeout hint for upstreams that may honor client-provided hints
        try:
            req_timeout_hint = int(self.timeout) if (self.timeout is not None) else 600
            # Ensure a reasonably generous minimum
            if req_timeout_hint < 300:
                req_timeout_hint = 300
        except Exception:
            req_timeout_hint = 600

        assistant_buf: List[str] = []
        # Defer assistant header until we know the actual model used
        header_printed = False

        session_id: Optional[str] = None

        # Initialize current turn tracking for potential mid-stream WS connections
        try:
            self._current_turn = {
                "active": True,
                "session_id": None,
                "model": self.model,
                "assistant_so_far": "",
                "tool_events": [],
            }
        except Exception:
            pass

        # Build an SSE-friendly timeout config when no explicit timeout provided
        if self.timeout is None:
            http_timeout = httpx.Timeout(connect=10.0, read=None, write=10.0, pool=10.0)
        else:
            http_timeout = httpx.Timeout(self.timeout)

        async with httpx.AsyncClient(timeout=http_timeout, cookies=self.cookies) as client:
            # Create a server thread if requested and authenticated
            await self._ensure_thread(client)

            if DEBUG_REQ:
                self.ui.print(f"[debug] POST {self.stream_url}", style=self.ui.theme["dim"]) 
                self.ui.print(truncate_json(payload, 1500), style=self.ui.theme["dim"]) 
            # Raw log: outgoing request payload
            if self.raw_log_enabled:
                try:
                    self._rawlog_write(f">>> POST {self.stream_url}")
                    self._rawlog_write_json(payload)
                except Exception:
                    pass

        async def do_stream(req_payload: Dict[str, Any]) -> str:
                nonlocal session_id
                nonlocal header_printed
                # Retry tracking flags (updated per attempt)
                nonlocal last_completed, last_error, last_bytes_total
                # While streaming assistant text, suppress the thinking indicator to avoid clobbering output
                streaming_assistant = False
                # Initialize per-turn timer and tool call counter
                tool_calls = 0
                # Capture last N SSE events for diagnostics if stream ends without message.completed
                from collections import deque
                last_events = deque(maxlen=SSE_TAIL_MAX)  # keep short, printable summaries
                try:
                    self._turn_started_at = time.perf_counter()
                except Exception:
                    self._turn_started_at = None
                headers = {"Accept": "text/event-stream", "Cache-Control": "no-cache", "Connection": "keep-alive"}
                # Attach idempotency + timeout hint headers
                try:
                    if idempotency_key:
                        headers["X-Idempotency-Key"] = idempotency_key
                except Exception:
                    pass
                try:
                    headers["X-Request-Timeout"] = str(int(req_timeout_hint))
                except Exception:
                    pass
                # If using a Kimi model, include provider-native messages to preserve reasoning_content
                try:
                    if isinstance(self.model, str) and self.model.startswith("kimi-"):
                        req_payload = dict(req_payload)
                        req_payload["raw_provider_messages"] = self._build_kimi_raw_messages(user_input)
                except Exception:
                    pass
                async with httpx.AsyncClient(timeout=http_timeout, cookies=self.cookies) as client:
                    async with client.stream("POST", self.stream_url, json=req_payload, headers=headers, follow_redirects=True) as resp:
                        if resp.status_code == 429:
                            try:
                                content = await resp.aread()
                                err_json = json.loads(content)
                                msg = err_json.get("error", {}).get("message", "")
                                m = re.search(r"retry in (\d+(?:\.\d+)?)s", msg)
                                if m:
                                    delay = float(m.group(1))
                                else:
                                    delay = 45.0
                                    try:
                                        rd = err_json.get("error", {}).get("details", [{}])[-1].get("retryDelay")
                                        if rd and rd.endswith("s"):
                                            delay = float(rd[:-1])
                                    except Exception:
                                        pass
                            except Exception:
                                delay = 45.0
                            self.ui.warn(f"Rate limit exceeded (429). Retrying in {delay:.1f}s...")
                            await asyncio.sleep(delay)
                            return await do_stream(req_payload)
                        resp.raise_for_status()
                        # Validate content type before attempting SSE parsing
                        try:
                            ctype_chk = resp.headers.get("content-type", "") or ""
                        except Exception:
                            ctype_chk = ""
                        if "text/event-stream" not in ctype_chk.lower():
                            # Try alternate endpoint if available to avoid /v0 duplication or legacy path issues
                            alt = getattr(self, "stream_url_alt", None)
                            if isinstance(alt, str) and alt and alt != self.stream_url:
                                try:
                                    self.ui.warn(
                                        f"Non-SSE Content-Type '{ctype_chk or 'unknown'}' from {self.stream_url}. Retrying alternate endpoint..."
                                    )
                                except Exception:
                                    pass
                                orig = self.stream_url
                                self.stream_url = alt
                                try:
                                    return await do_stream(req_payload)
                                finally:
                                    self.stream_url = orig
                            else:
                                # Proceed anyway; some proxies strip Content-Type. Warn and attempt to parse SSE.
                                try:
                                    self.ui.warn(
                                        f"Expected 'text/event-stream' but got '{ctype_chk or 'unknown'}'. Attempting to parse SSE anyway."
                                    )
                                except Exception:
                                    pass
                        # Connection diagnostics (once)
                        try:
                            if DEBUG_SSE or self.ui.verbose:
                                ctype = resp.headers.get("content-type")
                                te = resp.headers.get("transfer-encoding")
                                clen = resp.headers.get("content-length")
                                xab = resp.headers.get("x-accel-buffering") or resp.headers.get("X-Accel-Buffering")
                                cache = resp.headers.get("cache-control")
                                date = resp.headers.get("date")
                                self.ui.print(
                                    f"[debug] SSE connected: {resp.status_code} ctype={ctype} te={te} clen={clen} x-accel-buffering={xab} cache={cache} date={date}",
                                    style=self.ui.theme["dim"],
                                )
                        except Exception:
                            pass
                        # Capture all x-* headers for deep diagnostics
                        try:
                            sse_headers_diag = {k: v for k, v in resp.headers.items() if isinstance(k, str) and k.lower().startswith("x-")}
                        except Exception:
                            sse_headers_diag = {}

                        # Basic counters for this stream
                        _events_total = 0
                        _deltas_total = 0
                        _bytes_total = 0
                        # Reset per-attempt flags
                        last_completed = False
                        last_error = False
                        last_bytes_total = 0

                        # Raw log: response headers (once)
                        try:
                            if self.raw_log_enabled:
                                hdrs = {k: v for k, v in resp.headers.items()}
                                self._rawlog_write(f"<<< HTTP {resp.status_code}")
                                self._rawlog_write_json(hdrs)
                        except Exception:
                            pass
                        # Combined SSE debugger: prints to console when --debug-sse and always writes to raw log when enabled
                        def _sse_debug(msg: str) -> None:
                            try:
                                if DEBUG_SSE:
                                    self.ui.print(f"[debug] {msg}", style=self.ui.theme["dim"])  # type: ignore
                            except Exception:
                                pass
                            try:
                                if self.raw_log_enabled:
                                    self._rawlog_write(msg)
                            except Exception:
                                pass
                        # Idle "thinking" indicator shown while waiting for the next event (first tokens or next tool call)
                        indicator_task = None
                        indicator_active = False
                        indicator_started = False  # used only to adjust leading newline behavior on first assistant header
                        # Mode: animate or static (default static for stability)
                        try:
                            _animate_indicator = (os.getenv("HENOSIS_THINKING_ANIMATE", "").strip().lower() in ("1", "true", "yes", "on"))
                        except Exception:
                            _animate_indicator = False

                        async def _thinking_indicator_loop(chosen_word: str, spacing: int = 3) -> None:
                            """Animate a transient thinking word on a single line until indicator_active becomes False.
                            Always clears its line on exit so no remnants remain in history.
                            """
                            colors = [196, 208, 226, 46, 51, 27, 201]  # red, orange, yellow, green, cyan, blue, magenta
                            joiner = " " * max(0, spacing - 1)
                            tick = 0
                            try:
                                while indicator_active:
                                    try:
                                        out_chars = []
                                        for i, ch in enumerate(str(chosen_word)):
                                            c = colors[(i + tick) % len(colors)]
                                            out_chars.append(f"\x1b[38;5;{c}m{ch}\x1b[0m")
                                        line = " " + joiner.join(out_chars) + " "
                                        sys.stdout.write("\r\x1b[2K" + line)
                                        sys.stdout.flush()
                                    except Exception:
                                        try:
                                            sys.stdout.write("\r\x1b[2K" + (" " + joiner.join(list(str(chosen_word))) + " "))
                                            sys.stdout.flush()
                                        except Exception:
                                            pass
                                    tick = (tick + 1) % 1024
                                    try:
                                        await asyncio.sleep(0.25)
                                    except asyncio.CancelledError:
                                        break
                                    except Exception:
                                        break
                            finally:
                                try:
                                    sys.stdout.write("\r\x1b[2K")
                                    sys.stdout.flush()
                                except Exception:
                                    pass

                        async def _indicator_start() -> None:
                            nonlocal indicator_task, indicator_active, indicator_started
                            # Choose a random word and spacing each start
                            word_bank = list(self._thinking_words or ["thinking", "working..."])
                            if not word_bank:
                                word_bank = ["thinking"]
                            try:
                                chosen = random.choice(word_bank)
                            except Exception:
                                chosen = word_bank[0]
                            try:
                                spacing = int(getattr(self, "_thinking_rainbow_spacing", 3) or 3)
                            except Exception:
                                spacing = 3
                            if spacing < 1:
                                spacing = 1
                            # If already active, do nothing
                            if indicator_task and not indicator_task.done() and indicator_active:
                                return
                            # Synchronous first-frame render so the word is visible even if the
                            # animation is stopped quickly by the next event.
                            try:
                                colors = [196, 208, 226, 46, 51, 27, 201]
                                joiner = " " * max(0, spacing - 1)
                                out_chars = []
                                for i, ch in enumerate(str(chosen)):
                                    c = colors[i % len(colors)]
                                    out_chars.append(f"\x1b[38;5;{c}m{ch}\x1b[0m")
                                line = " " + joiner.join(out_chars) + " "
                                # Start on a dedicated new line so we never clobber prior output
                                sys.stdout.write("\n")
                                sys.stdout.write("\r\x1b[2K" + line)
                                sys.stdout.flush()
                                # File debug
                                try:
                                    self.ui.debug_log(f"indicator.start word='{chosen}' animate={_animate_indicator}")
                                except Exception:
                                    pass
                            except Exception:
                                try:
                                    sys.stdout.write("\n" + (" " + joiner.join(list(str(chosen))) + " "))
                                    sys.stdout.flush()
                                except Exception:
                                    pass
                            indicator_started = True
                            if _animate_indicator:
                                try:
                                    indicator_active = True
                                    indicator_task = asyncio.create_task(_thinking_indicator_loop(chosen, spacing))
                                except Exception:
                                    indicator_task = None
                                    indicator_active = False

                        async def _indicator_stop(clear: bool = False) -> None:
                            nonlocal indicator_task, indicator_active, indicator_started
                            # Only clear the line if an indicator was actually started.
                            was_started = bool(indicator_started)
                            indicator_active = False
                            try:
                                if indicator_task and not indicator_task.done():
                                    indicator_task.cancel()
                                    try:
                                        await indicator_task
                                    except asyncio.CancelledError:
                                        pass
                                    except Exception:
                                        pass
                            except Exception:
                                pass
                            finally:
                                indicator_task = None
                                # Default to not clearing to avoid erasing streamed content lines
                                if was_started and clear:
                                    try:
                                        sys.stdout.write("\r\x1b[2K")
                                        sys.stdout.flush()
                                    except Exception:
                                        pass
                                elif was_started:
                                    # Move to the next line to separate subsequent output
                                    try:
                                        sys.stdout.write("\n")
                                        sys.stdout.flush()
                                    except Exception:
                                        pass
                                # Reset started flag after stopping
                                indicator_started = False
                                try:
                                    self.ui.debug_log(f"indicator.stop clear={clear} was_started={was_started}")
                                except Exception:
                                    pass

                        # Start indicator immediately (optional); will be stopped on first delta/tool event
                        # Start the animated rainbow "thinking" indicator immediately (no dim/static line)
                        try:
                            if bool(getattr(self, "_thinking_indicator_enabled", False)):
                                await _indicator_start()
                        except Exception:
                            # Ignore indicator errors silently
                            pass

                        async for event, data_raw in parse_sse_lines(resp, debug=_sse_debug):
                            try:
                                if isinstance(data_raw, str):
                                    _bytes_total += len(data_raw)
                                    last_bytes_total = _bytes_total
                                _events_total += 1
                            except Exception:
                                pass
                            try:
                                data = json.loads(data_raw) if data_raw else {}
                            except json.JSONDecodeError:
                                data = {"_raw": data_raw}
    
                            if event == "session.started":
                                # Keep indicator until first token; do not stop here
                                session_id = data.get("session_id")
                                lvl = data.get("level")
                                scope = data.get("fs_scope")
                                self.ui.print(f"[session] id={session_id} level={lvl} scope={scope}", style=self.ui.theme["dim"])
                                self._log_line({"event": "session.started", "server_session_id": session_id, "level": lvl, "fs_scope": scope})
                                try:
                                    await self._ws_broadcast("session.started", data)
                                except Exception:
                                    pass
                                try:
                                    self._current_turn["session_id"] = session_id
                                except Exception:
                                    pass
                                try:
                                    last_events.append({"event": "session.started", "level": lvl, "fs_scope": scope, "session_id": session_id})
                                except Exception:
                                    pass
                                continue
    
                            elif event == "message.delta":
                                # Stop any transient indicator before printing content and clear the line
                                try:
                                    await _indicator_stop(clear=True)
                                except Exception:
                                    pass
                                text = data.get("text", "")
                                if text:
                                    try:
                                        _deltas_total += 1
                                    except Exception:
                                        pass
                                    # Mark that we're actively streaming assistant tokens
                                    streaming_assistant = True
                                    try:
                                        self.ui.debug_log(f"delta bytes={len(text)} header_printed={header_printed}")
                                    except Exception:
                                        pass
                                    try:
                                        last_events.append({"event": "message.delta", "bytes": len(text)})
                                    except Exception:
                                        pass
                                    # Print the header with the actual model name on first delta
                                    if not header_printed:
                                        try:
                                            model_label = data.get("model") or self.model or "(server default)"
                                        except Exception:
                                            model_label = self.model or "(server default)"
                                        # Track the actual model used for this turn so tool events can prefix it
                                        try:
                                            if isinstance(data.get("model"), str) and data.get("model").strip():
                                                self._current_turn["model"] = data.get("model")
                                        except Exception:
                                            pass
                                        # Print assistant header; indicator line has been cleared, so no leading newline
                                        try:
                                            self.ui.print(str(model_label) + ": ", style=self.ui.theme["assistant"], end="")
                                        except Exception:
                                            try:
                                                print(str(model_label) + ": ", end="", flush=True)
                                            except Exception:
                                                pass
                                        header_printed = True
                                        try:
                                            self.ui.debug_log(f"header.printed model='{model_label}' on_first_delta")
                                        except Exception:
                                            pass
                                    assistant_buf.append(text)
                                    # Print the token delta raw to avoid any wrapping/markup side-effects
                                    try:
                                        self.ui.print(text, style=self.ui.theme["assistant"], end="")
                                    except Exception:
                                        try:
                                            print(str(text), end="", flush=True)
                                        except Exception:
                                            pass
                                    # Deep debug: show each delta's size/preview
                                    try:
                                        if DEBUG_SSE:
                                            prev = text[:40].replace("\n", "\\n")
                                            self.ui.print(f"[debug] delta bytes={len(text)} preview={prev!r}", style=self.ui.theme["dim"])  # type: ignore
                                    except Exception:
                                        pass
                                    try:
                                        payload_ws = {"text": text}
                                        if data.get("model"):
                                            payload_ws["model"] = data.get("model")
                                        await self._ws_broadcast("message.delta", payload_ws)
                                    except Exception:
                                        pass
                                    try:
                                        self._current_turn["assistant_so_far"] = (self._current_turn.get("assistant_so_far") or "") + text
                                    except Exception:
                                        pass
    
                            elif event == "tool.call":
                                # Ensure any prior indicator state is reset cleanly, then restart
                                # a fresh indicator while waiting for the tool to run.
                                try:
                                    await _indicator_stop(clear=True)
                                except Exception:
                                    pass

                                name = data.get("name")
                                args = data.get("args", {}) or {}
                                call_id = data.get("call_id")
                                try:
                                    self.ui.debug_log(f"tool.call name='{name}' call_id={call_id}")
                                except Exception:
                                    pass

                                # Do NOT show the initial tool.call line per UX request; results will be
                                # rendered on tool.result. We still keep internal state and WS broadcasts.
                                # While the tool executes (server or client), show a subtle thinking
                                # indicator so users see progress during potentially long operations.
                                try:
                                    # Do not start the indicator if we're in the middle of assistant token streaming
                                    if (not streaming_assistant) and bool(getattr(self, "_thinking_indicator_enabled", False)):
                                        await _indicator_start()
                                except Exception:
                                    pass
                                # Count tool calls
                                try:
                                    tool_calls += 1
                                except Exception:
                                    pass
    
                                # Track args for troubleshooting and broadcast to WS clients
                                if call_id:
                                    self._tool_args_by_call_id[str(call_id)] = args
                                try:
                                    await self._ws_broadcast("tool.call", {"name": name, "args": args, "call_id": call_id})
                                except Exception:
                                    pass
                                try:
                                    self._current_turn["tool_events"].append({"type": "tool.call", "data": {"name": name, "args": args, "call_id": call_id}})
                                except Exception:
                                    pass
                                try:
                                    last_events.append({"event": "tool.call", "name": name, "call_id": call_id})
                                except Exception:
                                    pass
    
                            elif event == "approval.request":
                                # First reply wins (web or CLI)
                                await self._handle_approval_request(client, session_id, data)
                                continue
    
                            elif event == "approval.result":
                                appr = data.get("approved")
                                note = data.get("note")
                                self.ui.print(f"Approval result: {'APPROVED' if appr else 'DENIED'} ({note or ''})", style=self.ui.theme["info"])
                                try:
                                    await self._ws_broadcast("approval.result", data)
                                except Exception:
                                    pass
                                try:
                                    last_events.append({"event": "approval.result", "approved": bool(appr)})
                                except Exception:
                                    pass
                                continue
    
                            elif event == "context.near_full":
                                # Friendly banner when the server warns about context fullness
                                try:
                                    pct = data.get("pct")
                                    pct_str = f"{float(pct)*100:.1f}%" if isinstance(pct, (int, float)) and pct is not None else "~90%+"
                                except Exception:
                                    pct_str = "~90%+"
                                self.ui.warn(f"Heads up: the context window is nearly full ({pct_str}). You'll be offered a Summarize option.")
                                continue
    
                            elif event == "context.summary.ready":
                                # Server indicates the working memory file exists; restart a fresh convo with first-turn injections
                                mem_dir = data.get("dir") or "memory"
                                files = data.get("files") or []
                                if isinstance(files, list) and files:
                                    rel = f"{mem_dir}/{files[0]}"
                                    # Store relative path under workspace; resolve on injection
                                    try:
                                        self._memory_paths_for_first_turn = [rel]
                                    except Exception:
                                        self._memory_paths_for_first_turn = []
                                self._did_inject_working_memory = False
                                self._restart_after_summary = bool(data.get("auto_restart_with_injection", True))
                                self.ui.info("Working memory created. Restarting conversation with a fresh first-turn injection...")
                                return ""
    
                            elif event == "tool.result":
                                name = str(data.get("name"))
                                result = data.get("result", {}) or {}
                                call_id = data.get("call_id")
                                # Stop any indicator before rendering results
                                try:
                                    await _indicator_stop(clear=True)
                                except Exception:
                                    pass
                                # Ensure tool result starts on a fresh line if assistant text was mid-line
                                try:
                                    buf_str = "".join(assistant_buf)
                                except Exception:
                                    buf_str = ""
                                self.ui.ensure_newline(buf_str)
                                # Concise default: one professional, natural-language line per tool call.
                                if not self.ui.verbose:
                                    try:
                                        # Recover original args (for filenames/cmds) when available
                                        args_ctx = {}
                                        try:
                                            if call_id and str(call_id) in self._tool_args_by_call_id:
                                                args_ctx = self._tool_args_by_call_id.get(str(call_id), {}) or {}
                                        except Exception:
                                            args_ctx = {}
                                        # Build natural-language action label
                                        label = self._tool_concise_label(name, args_ctx, result)
                                        # Prefix with the current model label for clarity in multi-provider runs
                                        try:
                                            model_prefix = (self._current_turn.get("model") or self._last_used_model or self.model or "(server default)")
                                        except Exception:
                                            model_prefix = self.model or "(server default)"
                                        ok = bool(result.get("ok"))
                                        # Explicit segment coloring per request:
                                        # - model name: orange
                                        # - status tag: green (success) or red (failure)
                                        # - main text (label and optional reason): white
                                        if self.ui.rich:
                                            # Model name in orange
                                            self.ui.print(f"{model_prefix}: ", style=self.ui.theme["tool_call"], end="")
                                            # Status tag
                                            if ok:
                                                self.ui.print("[SUCCESS]", style=self.ui.theme["tool_result"], end=" ")
                                            else:
                                                self.ui.print("[FAILURE]", style=self.ui.theme["tool_result_err"], end=" ")
                                            # Main text in white (+ optional reason)
                                            err = result.get("error")
                                            if (not ok) and isinstance(err, str) and err.strip():
                                                reason = self._clip(err, 160)
                                                self.ui.print(f"{label}: {reason}", style="white")
                                            else:
                                                self.ui.print(f"{label}", style="white")
                                        else:
                                            # ANSI fallback when Rich is unavailable
                                            ORANGE = "\x1b[38;5;214m"
                                            GREEN  = "\x1b[32m"
                                            RED    = "\x1b[31m"
                                            WHITE  = "\x1b[97m"
                                            RESET  = "\x1b[0m"
                                            status_seg = f"{GREEN}[SUCCESS]{RESET}" if ok else f"{RED}[FAILURE]{RESET}"
                                            err = result.get("error")
                                            if (not ok) and isinstance(err, str) and err.strip():
                                                reason = self._clip(err, 160)
                                                msg = f"{ORANGE}{model_prefix}{RESET}: {status_seg} {WHITE}{label}: {reason}{RESET}"
                                            else:
                                                msg = f"{ORANGE}{model_prefix}{RESET}: {status_seg} {WHITE}{label}{RESET}"
                                            self.ui.print(msg)
                                    except Exception:
                                        # Fall back to legacy renderer on unexpected issues
                                        self._render_tool_result(name, result, call_id=call_id)
                                else:
                                    # Verbose mode retains the richer summary with previews
                                    self._render_tool_result(name, result, call_id=call_id)
                                try:
                                    await self._ws_broadcast("tool.result", {"name": name, "result": result, "call_id": call_id})
                                except Exception:
                                    pass
                                # For Kimi, append provider-native tool result to raw history so it's threaded correctly
                                try:
                                    if bool(getattr(self, "retain_native_tool_results", False)) and isinstance(self.model, str) and self.model.startswith("kimi-") and call_id:
                                        payload_tool = json.dumps(result) if not isinstance(result, str) else result
                                        self._kimi_raw_history.append({
                                            "role": "tool",
                                            "tool_call_id": call_id,
                                            "name": name,
                                            "content": payload_tool,
                                        })
                                except Exception:
                                    pass
                                try:
                                    self._current_turn["tool_events"].append({"type": "tool.result", "data": {"name": name, "result": result, "call_id": call_id}})
                                except Exception:
                                    pass
                                try:
                                    last_events.append({"event": "tool.result", "name": name, "ok": bool(result.get("ok")), "call_id": call_id})
                                except Exception:
                                    pass
                                # Do not auto-restart the indicator here; wait for the next model event

                            elif event == "tool.dispatch":
                                # Client-executed tool flow
                                if not HAS_LOCAL_TOOLS:
                                    self.ui.warn("Received tool.dispatch but local tools are unavailable (henosis_cli_tools not installed)")
                                    continue
                                # Keep the indicator running while the local tool executes; it will be
                                # cleared on tool.result or message.delta.
                                # Do not increment tool_calls here: we already counted the logical
                                # tool invocation on the corresponding 'tool.call' event. Counting
                                # dispatch would double-count a single tool call.
    
                                session_id_d = data.get("session_id")
                                call_id = data.get("call_id")
                                name = data.get("name")
                                args = data.get("args", {}) or {}
                                job_token = data.get("job_token")
                                reqp = data.get("requested_policy", {}) or {}
    
                                if DEBUG_SSE:
                                    self.ui.print(f"[debug] dispatch name={name} call_id={call_id}", style=self.ui.theme["dim"])
                                    self.ui.print(f"[debug] requested_policy={truncate_json(reqp, 1000)}", style=self.ui.theme["dim"])
                                    self.ui.print(f"[debug] args={truncate_json(args, 1000)}", style=self.ui.theme["dim"])
                                try:
                                    last_events.append({"event": "tool.dispatch", "name": name, "call_id": call_id})
                                except Exception:
                                    pass
    
                                # Level gating and CLI approvals (Level 2)
                                try:
                                    lvl = int(self.control_level) if isinstance(self.control_level, int) else None
                                except Exception:
                                    lvl = None
                                # Hard block at Level 1 for anything other than read/list
                                if lvl == 1:
                                    disallowed = str(name) not in ("read_file", "list_dir")
                                    if disallowed:
                                        denied_result = {"ok": False, "error": "Tool not allowed at Level 1", "denied": True}
                                        # Best-effort callback to server
                                        try:
                                            if session_id_d and call_id and job_token:
                                                payload_cb = {
                                                    "session_id": session_id_d,
                                                    "call_id": call_id,
                                                    "name": name,
                                                    "result": denied_result,
                                                    "job_token": job_token,
                                                }
                                                r = await client.post(self.tools_callback_url, json=payload_cb, timeout=self.timeout)
                                                if r.status_code >= 400:
                                                    self.ui.warn(f"tools.callback POST failed (L1 block): {r.status_code} {r.text}")
                                        except Exception as e:
                                            self.ui.warn(f"tools.callback error (L1 block): {e}")
                                        # Skip execution
                                        continue
                                # Level 2: require CLI approval unless trusted/auto-approved
                                if lvl == 2:
                                    approved = False
                                    try:
                                        approved = self._cli_approval_for(name, args)
                                    except Exception:
                                        approved = False
                                    if not approved:
                                        denied_result = {"ok": False, "error": "User denied execution", "denied": True}
                                        # Best-effort callback to server
                                        try:
                                            if session_id_d and call_id and job_token:
                                                payload_cb = {
                                                    "session_id": session_id_d,
                                                    "call_id": call_id,
                                                    "name": name,
                                                    "result": denied_result,
                                                    "job_token": job_token,
                                                }
                                                r = await client.post(self.tools_callback_url, json=payload_cb, timeout=self.timeout)
                                                if r.status_code >= 400:
                                                    self.ui.warn(f"tools.callback POST failed (L2 deny): {r.status_code} {r.text}")
                                        except Exception as e:
                                            self.ui.warn(f"tools.callback error (L2 deny): {e}")
                                        # Skip execution when denied
                                        continue
    
                                # Build local policy: CLI governs scope and host roots
                                scope = self.fs_scope if self.fs_scope in ("workspace", "host") else (reqp.get("scope") if reqp.get("scope") in ("workspace", "host") else "workspace")
                                allowed_roots: List[Path] = []
                                host_base = None
                                if scope == "host":
                                    mode = (self.fs_host_mode or "any").lower()
                                    if mode == "cwd":
                                        try:
                                            host_base = os.getcwd()
                                        except Exception:
                                            host_base = self.host_base
                                        if host_base:
                                            allowed_roots = [Path(host_base).expanduser().resolve()]
                                    elif mode == "custom":
                                        host_base = self.host_base or os.getcwd()
                                        if host_base:
                                            allowed_roots = [Path(host_base).expanduser().resolve()]
                                    else:
                                        # any
                                        host_base = self.host_base
                                        allowed_roots = []
                                else:
                                    host_base = None
                                    allowed_roots = []
    
                                policy = LocalFileToolPolicy(
                                    scope=scope,
                                    workspace_base=Path(self.local_workspace_dir).expanduser().resolve(),
                                    host_base=(Path(host_base).expanduser().resolve() if (scope == "host" and host_base) else None),
                                    allowed_roots=allowed_roots,
                                )
    
                                # Log inputs before execution
                                self._log_line({
                                    "event": "client.tool.exec",
                                    "name": name,
                                    "call_id": call_id,
                                    "args": args,
                                    "requested_policy": reqp,
                                    "local_policy": {
                                        "scope": scope,
                                        "host_base": str(host_base) if host_base else None,
                                        "allowed_roots": [str(p) for p in allowed_roots],
                                    },
                                })
    
                                # Execute
                                try:
                                    if name == "read_file":
                                        path_arg = args.get("path", "")
                                        result = local_read_file(path_arg, policy)
                                        # Apply tailing ONLY if we've marked this path due to a prior provider size-limit error
                                        try:
                                            if isinstance(path_arg, str) and path_arg in self._tail_next_paths:
                                                if isinstance(result, dict) and result.get("ok") and isinstance(result.get("data"), dict):
                                                    d = result.get("data") or {}
                                                    content = d.get("content")
                                                    if isinstance(content, str):
                                                        lines = content.splitlines()
                                                        tail_lines = 50
                                                        tailed = "\n".join(lines[-tail_lines:]) if lines else ""
                                                        if len(tailed) > 30_000:
                                                            tailed = tailed[-30_000:]
                                                        d["content"] = tailed
                                                        # Best-effort token estimate
                                                        try:
                                                            d["tokens_used"] = int(len(tailed) / 0.3) if tailed else 0
                                                        except Exception:
                                                            pass
                                                        d["truncated"] = True
                                                        d["truncation_policy"] = {
                                                            "reason": "post-error-retry",
                                                            "tail_lines": tail_lines,
                                                            "char_cap": 30000,
                                                            "original_chars": len(content),
                                                        }
                                                        result["data"] = d
                                                # Clear the flag so future reads of this path are not truncated unless another error occurs
                                                try:
                                                    self._tail_next_paths.discard(path_arg)
                                                except Exception:
                                                    pass
                                        except Exception:
                                            # Non-fatal; if tailing fails, keep original result
                                            pass
                                    elif name == "write_file":
                                        result = local_write_file(args.get("path", ""), args.get("content", ""), policy)
                                    elif name == "append_file":
                                        result = local_append_file(args.get("path", ""), args.get("content", ""), policy)
                                    elif name == "list_dir":
                                        result = local_list_dir(args.get("path", ""), policy)
                                    elif name == "run_command":
                                        # Intersect allowlists
                                        req_allow = (reqp.get("command_allow_csv") or "").strip()
                                        local_allow = os.getenv("HENOSIS_ALLOW_COMMANDS", "")
                                        if req_allow and local_allow:
                                            req_set = {c.strip().lower() for c in req_allow.split(",") if c.strip()}
                                            loc_set = {c.strip().lower() for c in local_allow.split(",") if c.strip()}
                                            allow_csv = ",".join(sorted(req_set & loc_set))
                                        else:
                                            allow_csv = local_allow or req_allow or ""
                                        # Include trusted commands from CLI settings (session + always)
                                        try:
                                            allow_set = {c.strip().lower() for c in allow_csv.split(",") if c.strip()}
                                            for k in (self.trust_cmds_session or []):
                                                allow_set.add(str(k).strip().lower())
                                            for k in (self.trust_cmds_always or []):
                                                allow_set.add(str(k).strip().lower())
                                            allow_csv = ",".join(sorted(allow_set))
                                        except Exception:
                                            pass
                                        timeout = args.get("timeout", None)
                                        result = local_run_command(args.get("cmd", ""), policy, cwd=args.get("cwd", "."), timeout=timeout, allow_commands_csv=allow_csv)
                                        # If denied due to allowlist, offer to approve once/session/always and retry
                                        try:
                                            ok_flag = bool(result.get("ok"))
                                        except Exception:
                                            ok_flag = False
                                        if (not ok_flag):
                                            err_msg = str(result.get("error") or "")
                                            err_low = err_msg.lower()
                                            denied_for_allow = ("not allowed" in err_low) or ("no commands allowed" in err_low)
                                            if denied_for_allow:
                                                # Determine base exe name
                                                try:
                                                    cmd_tok = (args.get("cmd") or "").strip().split()[0]
                                                    base_exe = os.path.basename(cmd_tok).lower() if cmd_tok else ""
                                                except Exception:
                                                    base_exe = ""
                                                if base_exe:
                                                    # Reuse approval prompt UI for consistent UX
                                                    choice = self._approval_prompt_ui(f"run_command:{base_exe}", args)
                                                    if choice != "deny":
                                                        # Update trust lists and env if needed
                                                        if choice == "session":
                                                            try:
                                                                if base_exe not in self.trust_cmds_session:
                                                                    self.trust_cmds_session.append(base_exe)
                                                            except Exception:
                                                                pass
                                                        elif choice == "always":
                                                            try:
                                                                if base_exe not in self.trust_cmds_always:
                                                                    self.trust_cmds_always.append(base_exe)
                                                                # Also update env allowlist for this process
                                                                cur_env = os.getenv("HENOSIS_ALLOW_COMMANDS", "")
                                                                cur_set = {c.strip().lower() for c in cur_env.split(",") if c.strip()}
                                                                cur_set.add(base_exe)
                                                                os.environ["HENOSIS_ALLOW_COMMANDS"] = ",".join(sorted(cur_set))
                                                                self.save_settings()
                                                            except Exception:
                                                                pass
                                                        # Approve once or after updating trust: retry with extended allow list for this call
                                                        try:
                                                            retry_set = {c.strip().lower() for c in (allow_csv or "").split(",") if c.strip()}
                                                        except Exception:
                                                            retry_set = set()
                                                        retry_set.add(base_exe)
                                                        retry_csv = ",".join(sorted(retry_set))
                                                        result = local_run_command(args.get("cmd", ""), policy, cwd=args.get("cwd", "."), timeout=timeout, allow_commands_csv=retry_csv)
                                    elif name == "apply_patch":
                                        result = local_apply_patch(
                                            patch=args.get("patch", ""),
                                            policy=policy,
                                            cwd=args.get("cwd", "."),
                                            lenient=bool(args.get("lenient", True)),
                                            dry_run=bool(args.get("dry_run", False)),
                                            backup=bool(args.get("backup", True)),
                                            safeguard_max_lines=int(args.get("safeguard_max_lines", 3000) or 3000),
                                            safeguard_confirm=bool(args.get("safeguard_confirm", False)),
                                        )
                                    elif name == "planning":
                                        # Persist plan under plans/ at the current root (workspace or host base)
                                        try:
                                            plan_text = str(args.get("plan", "") or "").strip()
                                            ctx_text = args.get("context")
                                            if not plan_text:
                                                result = {"ok": False, "error": "plan is required"}
                                            else:
                                                base = policy.workspace_base if policy.scope != "host" else (policy.host_base or Path(os.getcwd()).resolve())
                                                plans_dir = Path(base) / "plans"
                                                plans_dir.mkdir(parents=True, exist_ok=True)
                                                from datetime import datetime as _dt
                                                import re as _re, uuid as _uuid
                                                ts = _dt.utcnow().strftime("%Y%m%d-%H%M%S")
                                                first_line = plan_text.splitlines()[0] if plan_text else "plan"
                                                slug = _re.sub(r"[^a-zA-Z0-9_-]+", "-", first_line).strip("-") or "plan"
                                                slug = slug[:40]
                                                fname = f"plan-{ts}-{_uuid.uuid4().hex[:6]}-{slug}.md"
                                                fpath = plans_dir / fname
                                                body_lines = [f"# Plan ({ts} UTC)\n"]
                                                if ctx_text:
                                                    body_lines.append("## Context\n")
                                                    body_lines.append(str(ctx_text).strip() + "\n\n")
                                                body_lines.append("## Steps\n")
                                                body_lines.append(plan_text.rstrip() + "\n")
                                                content = "\n".join(body_lines)
                                                with fpath.open("w", encoding="utf-8", newline="") as f:
                                                    f.write(content)
                                                result = {"ok": True, "data": {"path": str(fpath), "bytes_written": len(content.encode('utf-8'))}}
                                        except Exception as _pe:
                                            result = {"ok": False, "error": str(_pe)}
                                    elif name == "string_replace":
                                        result = local_string_replace(
                                            pattern=args.get("pattern", ""),
                                            replacement=args.get("replacement", ""),
                                            policy=policy,
                                            cwd=args.get("cwd", "."),
                                            file_globs=[str(g) for g in (args.get("file_globs") or [])],
                                            exclude_globs=[str(e) for e in (args.get("exclude_globs") or [])],
                                            is_regex=bool(args.get("is_regex", False)),
                                            expected_total_matches=(int(args.get("expected_total_matches")) if args.get("expected_total_matches") is not None else None),
                                            max_replacements_per_file=int(args.get("max_replacements_per_file", 5) or 5),
                                            max_total_replacements=int(args.get("max_total_replacements", 5) or 5),
                                            dry_run=bool(args.get("dry_run", False)),
                                        )
                                    else:
                                        result = {"ok": False, "error": f"unknown tool '{name}'"}
                                except Exception as e:
                                    result = {"ok": False, "error": str(e)}
    
                                # Log outcome after execution
                                self._log_line({
                                    "event": "client.tool.result",
                                    "name": name,
                                    "call_id": call_id,
                                    "ok": bool(result.get("ok")),
                                    "error": result.get("error"),
                                    "data_keys": list((result.get("data") or {}).keys())
                                })
    
                                # Remember last dispatch context for targeted recovery on provider errors
                                try:
                                    self._last_dispatch_ctx = {
                                        "session_id": session_id_d,
                                        "call_id": call_id,
                                        "name": name,
                                        "args": args,
                                        "job_token": job_token,
                                    }
                                except Exception:
                                    self._last_dispatch_ctx = None
    
                                # POST callback
                                try:
                                    if session_id_d and call_id and job_token:
                                        payload_cb = {
                                            "session_id": session_id_d,
                                            "call_id": call_id,
                                            "name": name,
                                            "result": result,
                                            "job_token": job_token,
                                        }
                                        r = await client.post(self.tools_callback_url, json=payload_cb, timeout=self.timeout)
                                        if r.status_code >= 400:
                                            self.ui.warn(f"tools.callback POST failed: {r.status_code} {r.text}")
                                except Exception as e:
                                    self.ui.warn(f"tools.callback error: {e}")
    
                            elif event == "message.completed":
                                # Safety: this block handles only 'message.completed'.
                                usage = data.get("usage", {})
                                model_used = data.get("model") or self.model
                                # Mark completion for retry controller
                                try:
                                    last_completed = True
                                except Exception:
                                    pass
                                # No longer streaming assistant tokens
                                streaming_assistant = False
                                web_search_calls_raw = data.get("web_search") if isinstance(data, dict) else None
                                web_search_calls: List[Dict[str, Any]] = (
                                    web_search_calls_raw if isinstance(web_search_calls_raw, list) else []
                                )
                                # If no delta ever arrived (empty completion), still print the header once
                                if not header_printed:
                                    try:
                                        label = model_used or self.model or "(server default)"
                                    except Exception:
                                        label = self.model or "(server default)"
                                    # Stop and clear indicator before writing the header
                                    try:
                                        await _indicator_stop(clear=True)
                                    except Exception:
                                        pass
                                    # Print assistant header on the current line (indicator line cleared already)
                                    try:
                                        self.ui.print(str(label) + ": ", style=self.ui.theme["assistant"], end="")
                                    except Exception:
                                        try:
                                            print(str(label) + ": ", end="", flush=True)
                                        except Exception:
                                            pass
                                    header_printed = True
                                    try:
                                        self.ui.debug_log(f"header.printed model='{label}' on_completed_no_delta")
                                    except Exception:
                                        pass
                                buf_str = "".join(assistant_buf)
                                self.ui.ensure_newline(buf_str)
                                # Stream summary for debugging
                                try:
                                    if DEBUG_SSE or self.ui.verbose:
                                        self.ui.print(
                                            f"[debug] stream stats: events={_events_total} deltas={_deltas_total} bytes={_bytes_total}",
                                            style=self.ui.theme["dim"],
                                        )
                                except Exception:
                                    pass
    
                                # Timing: wall-clock from turn start; and session elapsed
                                try:
                                    now_pc = time.perf_counter()
                                    turn_secs = (now_pc - (self._turn_started_at or now_pc))
                                except Exception:
                                    turn_secs = 0.0
                                    now_pc = time.time()  # type: ignore
                                try:
                                    session_secs = (now_pc - (self._session_started_at or now_pc)) if (self._session_started_at is not None) else 0.0
                                except Exception:
                                    session_secs = 0.0
    
                                # Usage summary line
                                turn = (usage.get("turn") or {})
                                cum = (usage.get("cumulative") or {})
                                
                                # Base turn tokens from server's usage.turn
                                turn_in = int(turn.get("input_tokens", 0) or 0)
                                turn_out = int(turn.get("output_tokens", 0) or 0)
                                turn_total = int(turn.get("total_tokens", 0) or 0)
                                
                                # Fallback values from usage.turn/top-level
                                if turn_total == 0:
                                    turn_in = int(usage.get("prompt_tokens", 0) or 0)
                                    turn_out = int(usage.get("completion_tokens", 0) or 0)
                                    turn_total = int(usage.get("total_tokens", 0) or 0)
                                
                                # If turn_total still zero but we have input+output, derive it
                                if turn_total == 0 and (turn_in > 0 or turn_out > 0):
                                    turn_total = turn_in + turn_out
    
                                # Anthropic prompt caching: include cache creation/read input tokens when provided by server
                                # This adjusts per-turn display only; cumulative handling below will pick up from server when present.
                                try:
                                    cache_create = int(usage.get("cache_creation_input_tokens", 0) or 0)
                                    cache_read = int(usage.get("cache_read_input_tokens", 0) or 0)
                                    cache_add = cache_create + cache_read
                                except Exception:
                                    cache_add = 0
                                if cache_add > 0:
                                    # Only add when server's turn_total equals in+out (i.e., cache not already included)
                                    try:
                                        if turn_total == (turn_in + turn_out):
                                            turn_in += cache_add
                                            turn_total += cache_add
                                    except Exception:
                                        # Fallback: still add to input and recompute total
                                        turn_in += cache_add
                                        turn_total = turn_in + turn_out
    
                                # Compute proposed local cumulative including this turn (ensures final response counted)
                                prev_cum_in = int(self._cum_input_tokens)
                                prev_cum_out = int(self._cum_output_tokens)
                                prev_cum_total = int(self._cum_total_tokens)
    
                                local_cum_in = prev_cum_in + int(turn_in)
                                local_cum_out = prev_cum_out + int(turn_out)
                                local_cum_total = prev_cum_total + (int(turn_total) if turn_total else (int(turn_in) + int(turn_out)))
    
                                # Prefer server cumulative when available and not less than local (some providers may omit final step)
                                cum_source = "client"
                                server_cum_in = int(cum.get("input_tokens", 0) or 0)
                                server_cum_out = int(cum.get("output_tokens", 0) or 0)
                                server_cum_total = int(cum.get("total_tokens", 0) or 0)
    
                                if server_cum_total > 0 and server_cum_total >= local_cum_total:
                                    # Server provided cumulative and it already includes this turn's final response
                                    cum_in = server_cum_in
                                    cum_out = server_cum_out
                                    cum_total = server_cum_total
                                    cum_source = "server"
                                    # Sync client-side counters to match server
                                    self._cum_input_tokens = cum_in
                                    self._cum_output_tokens = cum_out
                                    self._cum_total_tokens = cum_total
                                else:
                                    # Use local cumulative to ensure we include the final response tokens
                                    self._cum_input_tokens = local_cum_in
                                    self._cum_output_tokens = local_cum_out
                                    self._cum_total_tokens = local_cum_total
                                    cum_in = int(self._cum_input_tokens)
                                    cum_out = int(self._cum_output_tokens)
                                    cum_total = int(self._cum_total_tokens)
                                    # If server attempted cumulative but was lower (e.g., Anthropic missing final), note source
                                    if server_cum_total > 0:
                                        cum_source = "client+final"
    
                                # Percentage based on last turn's total (input + output)
                                context_window = self.ctx_window or 400000
                                if context_window > 0:
                                    percent_filled = (turn_total / context_window) * 100
                                    percent_str = f"{percent_filled:.1f}%"
                                else:
                                    percent_str = "N/A"
    
                                # Commit usage to server billing/logs (best-effort) before rendering info box so cost line is available
                                await self._commit_usage(
                                    client,
                                    # Use the server-assigned session_id so the server can read its own usage logs
                                    session_id=session_id,
                                    model_used=model_used,
                                    usage=usage or {
                                        "prompt_tokens": turn_in,
                                        "completion_tokens": turn_out,
                                        "total_tokens": turn_total,
                                    },
                                )
    
                                # Diagnostic logging when tokens or costs appear as zero
                                try:
                                    diag_needed = False
                                    zero_tokens = (int(turn_in) == 0 and int(turn_out) == 0 and int(turn_total) == 0)
                                    zero_costs = (float(self._last_commit_cost_usd) == 0.0 and float(self.server_cumulative_cost_usd) == 0.0)
                                    if zero_tokens or zero_costs:
                                        diag_needed = True
                                    if diag_needed:
                                        # Sum provider step tokens (if the server sent them)
                                        steps = usage.get("provider_steps") if isinstance(usage, dict) else None
                                        sum_in_steps = 0
                                        sum_out_steps = 0
                                        if isinstance(steps, list):
                                            for st in steps:
                                                try:
                                                    sum_in_steps += int(st.get("input_tokens", 0) or 0)
                                                    sum_out_steps += int(st.get("output_tokens", 0) or 0)
                                                except Exception:
                                                    continue
                                        # Local cost estimates from two sources: turn tokens and provider_steps sums
                                        def _safe_cost_for(mi: Optional[int], mo: Optional[int]) -> float:
                                            try:
                                                u = {
                                                    "prompt_tokens": int(mi or 0),
                                                    "completion_tokens": int(mo or 0),
                                                    "total_tokens": int((mi or 0) + (mo or 0)),
                                                }
                                                return float(self.compute_cost_usd(model_used, u))
                                            except Exception:
                                                return 0.0
                                        est_cost_turn = _safe_cost_for(turn_in, turn_out)
                                        est_cost_steps = _safe_cost_for(sum_in_steps, sum_out_steps)
    
                                        diag_lines: List[str] = []
                                        diag_lines.append("Diagnostics: token/cost appear as 0 — investigating sources")
                                        # Stream evidence
                                        try:
                                            diag_lines.append(f"- stream: events={_events_total}, deltas={_deltas_total}, bytes={_bytes_total}")
                                        except Exception:
                                            pass
                                        # Server usage as sent
                                        try:
                                            klist = ",".join(sorted(list(usage.keys()))) if isinstance(usage, dict) else "(not a dict)"
                                            diag_lines.append(f"- usage keys: {klist}")
                                        except Exception:
                                            pass
                                        diag_lines.append(f"- usage.turn -> in {int(turn_in)} | out {int(turn_out)} | total {int(turn_total)}")
                                        # Provider steps evidence
                                        if (sum_in_steps + sum_out_steps) > 0:
                                            diag_lines.append(f"- provider_steps sum -> in {int(sum_in_steps)} | out {int(sum_out_steps)}")
                                        else:
                                            diag_lines.append("- provider_steps: (none or zero)")
                                        # Server cumulative tokens if present
                                        try:
                                            diag_lines.append(
                                                f"- usage.cumulative (server) -> in {int((usage.get('cumulative') or {}).get('input_tokens', 0) or 0)} | out {int((usage.get('cumulative') or {}).get('output_tokens', 0) or 0)} | total {int((usage.get('cumulative') or {}).get('total_tokens', 0) or 0)}"
                                            )
                                        except Exception:
                                            pass
                                        # Cost lines (server commit vs local estimates)
                                        try:
                                            diag_lines.append(
                                                f"- commit cost (server): last=${float(self._last_commit_cost_usd):.6f}, chat_total=${float(self.server_cumulative_cost_usd):.6f}"
                                            )
                                        except Exception:
                                            diag_lines.append("- commit cost (server): n/a")
                                        diag_lines.append(f"- est cost (from usage.turn): ${est_cost_turn:.6f}")
                                        diag_lines.append(f"- est cost (from provider_steps): ${est_cost_steps:.6f}")
                                        # Commit path evidence
                                        try:
                                            diag_lines.append(
                                                f"- commit path: enabled={bool(self.server_usage_commit)} | session_id={'set' if session_id else 'missing'} | model={model_used or '(unknown)'}"
                                            )
                                        except Exception:
                                            pass
                                        # Truncated raw usage preview
                                        try:
                                            diag_lines.append("- raw usage (truncated):")
                                            diag_lines.append(self._clip(truncate_json(usage, 1500), 1500))
                                        except Exception:
                                            pass
                                        # Render diagnostics block above the usage/info box
                                        try:
                                            if self.ui.rich and Panel:
                                                self.ui.console.print(Panel("\n".join(diag_lines), title="Diagnostics (usage/cost)", border_style=self.ui.theme["warn"]))
                                            else:
                                                self.ui.print("Diagnostics (usage/cost):", style=self.ui.theme["warn"])  # type: ignore
                                                for ln in diag_lines:
                                                    self.ui.print(ln, style=self.ui.theme["dim"])  # type: ignore
                                        except Exception:
                                            # Best-effort plain prints
                                            self.ui.print("Diagnostics (usage/cost):")
                                            for ln in diag_lines:
                                                self.ui.print(ln)
                                        # Also persist to session log for later analysis
                                        try:
                                            self._log_line({
                                                "event": "diagnostics.usage_cost_zero",
                                                "turn": {"in": int(turn_in), "out": int(turn_out), "total": int(turn_total)},
                                                "steps_sum": {"in": int(sum_in_steps), "out": int(sum_out_steps)},
                                                "est_cost_turn": float(est_cost_turn),
                                                "est_cost_steps": float(est_cost_steps),
                                                "commit_cost": float(self._last_commit_cost_usd),
                                                "chat_cost": float(self.server_cumulative_cost_usd),
                                                "session_id": session_id,
                                                "model": model_used,
                                                "usage_keys": (sorted(list(usage.keys())) if isinstance(usage, dict) else None),
                                            })
                                        except Exception:
                                            pass
                                except Exception:
                                    # Never let diagnostics crash the UI
                                    pass
    
                                # Prepare a consolidated info box with usage, timing, and context
                                box_lines: List[str] = []
                                context_line_str: Optional[str] = None
                                # henosis-cli version (from pyproject/installed metadata) with update hint when available
                                try:
                                    if not self._cli_version:
                                        self._cli_version = self._resolve_current_version() or None
                                    if self._cli_version:
                                        ver_line = f"henosis-cli v{self._cli_version}"
                                        if (self._version_outdated is True) and self._latest_version:
                                            ver_line += f" → v{self._latest_version} available | update: {os.path.basename(sys.executable)} -m pip install -U henosis-cli"
                                        box_lines.append(ver_line)
                                except Exception:
                                    pass
                                # Add requested billing line with model, cost, session cumulative, and remaining credits
                                try:
                                    rem_line = (
                                        f" | remaining credits: ${float(self._last_remaining_credits):.6f}"
                                        if (self._last_remaining_credits is not None)
                                        else ""
                                    )
                                except Exception:
                                    rem_line = ""
                                # Compact style: include reasoning effort inline with model name when applicable
                                try:
                                    effort_seg = ""
                                    if self._is_openai_reasoning_model(model_used):
                                        # Convert low|medium|high -> Low|Medium|High for display
                                        lvl = str(self.reasoning_effort or "medium").strip().lower()
                                        if lvl not in ("low", "medium", "high"):
                                            lvl = "medium"
                                        effort_seg = f" {lvl.capitalize()}"
                                except Exception:
                                    effort_seg = ""
                                model_only_line = f"model: {model_used or '(unknown)'}{effort_seg}"
                                box_lines.append(
                                    f"model: {model_used or '(unknown)'}{effort_seg} | cost charged: ${float(self._last_commit_cost_usd):.6f} | chat cost: ${float(self.server_cumulative_cost_usd):.6f}{rem_line}"
                                )
                                # Reasoning tokens: include inline with turn/session math
                                turn_reason = 0
                                try:
                                    explicit_rt = None
                                    # 1) usage.thinking_tokens (generic key used by server for reasoning tokens)
                                    if isinstance(usage.get("thinking_tokens"), (int, float)):
                                        explicit_rt = int(usage.get("thinking_tokens") or 0)
                                    # 2) usage.reasoning_tokens (alternate naming)
                                    elif isinstance(usage.get("reasoning_tokens"), (int, float)):
                                        explicit_rt = int(usage.get("reasoning_tokens") or 0)
                                    # 3) Nested details (xAI/OpenAI/OpenAI completion details)
                                    elif isinstance(usage.get("completion_tokens_details"), dict):
                                        ctd = usage.get("completion_tokens_details") or {}
                                        rt2 = ctd.get("reasoning_tokens")
                                        if isinstance(rt2, (int, float)):
                                            explicit_rt = int(rt2)
                                    elif isinstance(usage.get("output_tokens_details"), dict):
                                        otd = usage.get("output_tokens_details") or {}
                                        rt3 = otd.get("reasoning_tokens")
                                        if isinstance(rt3, (int, float)):
                                            explicit_rt = int(rt3)
                                    if isinstance(explicit_rt, int) and explicit_rt > 0:
                                        turn_reason = int(explicit_rt)
                                    else:
                                        # Fallback: infer from turn_total gap when available
                                        gap = int(max(0, (int(turn_total or 0) - (int(turn_in or 0) + int(turn_out or 0)))))
                                        if gap > 0:
                                            turn_reason = gap
                                except Exception:
                                    turn_reason = 0
    
                                # Session-level reasoning: prefer server cumulative when available
                                cum_reason = int(self._cum_reasoning_tokens or 0)
                                try:
                                    server_cum_reason = 0
                                    if isinstance(usage.get("cumulative"), dict):
                                        cu = usage.get("cumulative") or {}
                                        if isinstance(cu.get("thinking_tokens"), (int, float)):
                                            server_cum_reason = int(cu.get("thinking_tokens") or 0)
                                        elif isinstance(cu.get("reasoning_tokens"), (int, float)):
                                            server_cum_reason = int(cu.get("reasoning_tokens") or 0)
                                        else:
                                            # Nested under details
                                            for key in ("completion_tokens_details", "output_tokens_details"):
                                                det = cu.get(key)
                                                if isinstance(det, dict) and isinstance(det.get("reasoning_tokens"), (int, float)):
                                                    server_cum_reason = int(det.get("reasoning_tokens") or 0)
                                                    break
                                    if server_cum_total > 0 and server_cum_total >= local_cum_total and server_cum_reason > 0:
                                        self._cum_reasoning_tokens = int(server_cum_reason)
                                    else:
                                        # Roll forward locally with this turn's reasoning tokens
                                        self._cum_reasoning_tokens = int(self._cum_reasoning_tokens) + int(turn_reason)
                                    cum_reason = int(self._cum_reasoning_tokens)
                                except Exception:
                                    # Still roll forward locally
                                    try:
                                        self._cum_reasoning_tokens = int(self._cum_reasoning_tokens) + int(turn_reason)
                                        cum_reason = int(self._cum_reasoning_tokens)
                                    except Exception:
                                        cum_reason = int(turn_reason or 0)
    
                                # Turn and session math lines with inline reasoning when available
                                if int(turn_reason) > 0:
                                    box_lines.append(f"Turn tokens: in {int(turn_in)} + out {int(turn_out)} + reason {int(turn_reason)} = {int(turn_total)}")
                                else:
                                    box_lines.append(f"Turn tokens: in {int(turn_in)} + out {int(turn_out)} = {int(turn_total)}")
                                if int(cum_reason) > 0:
                                    box_lines.append(f"Session tokens: in {int(cum_in)} + out {int(cum_out)} + reason {int(cum_reason)} = {int(cum_total)}")
                                else:
                                    box_lines.append(f"Session tokens: in {int(cum_in)} + out {int(cum_out)} = {int(cum_total)}")
    
                                # Track last used model for potential future display/use
                                try:
                                    self._last_used_model = model_used
                                except Exception:
                                    pass
    
                                # Always show timing summary
                                def _fmt(sec: float) -> str:
                                    try:
                                        if sec < 60:
                                            return f"{sec:.2f}s"
                                        m, s = divmod(int(sec), 60)
                                        if m < 60:
                                            return f"{m}m {s}s"
                                        h, m = divmod(m, 60)
                                        return f"{h}h {m}m {s}s"
                                    except Exception:
                                        return f"{sec:.2f}s"
    
                                box_lines.append(f"Time: {_fmt(turn_secs)} (turn) | {_fmt(session_secs)} (session) | Tools: {tool_calls} call(s)")
    
                                # Compact web search summary (if any)
                                try:
                                    if web_search_calls:
                                        # Include up to 3 queries
                                        qs: List[str] = []
                                        for call in web_search_calls[:3]:
                                            action = call.get("action") if isinstance(call, dict) else None
                                            if isinstance(action, dict):
                                                q = action.get("query") or action.get("search_query")
                                                if isinstance(q, str) and q.strip():
                                                    qs.append(q.strip())
                                        if qs:
                                            box_lines.append("Web search: " + "; ".join(qs) + (" ..." if len(web_search_calls) > 3 else ""))
                                        else:
                                            box_lines.append(f"Web search: {len(web_search_calls)} call(s)")
                                except Exception:
                                    pass
    
                                # Render a simple bar showing current cumulative context usage against the window
                                try:
                                    # Use model-specific context window when known
                                    model_ctx = self._get_model_ctx_window(model_used)
                                    context_window = int(model_ctx) if model_ctx else (self.ctx_window or 400000)
                                    if context_window > 0:
                                        # Show bar based on the last assistant reply's input+output (prefer final provider step)
                                        last_in = 0
                                        last_out = 0
                                        steps_for_last = None
                                        try:
                                            steps_for_last = usage.get("provider_steps") if isinstance(usage, dict) else None
                                        except Exception:
                                            steps_for_last = None
                                        if isinstance(steps_for_last, list) and steps_for_last:
                                            for st in reversed(steps_for_last):
                                                try:
                                                    so = int(st.get("output_tokens", 0) or 0)
                                                    si = int(st.get("input_tokens", 0) or 0)
                                                    if so > 0:
                                                        last_out = so
                                                        last_in = si
                                                        break
                                                except Exception:
                                                    continue
                                        else:
                                            last_out = int(turn_out)
                                            last_in = 0
                                        last_total = float(last_in + last_out)
                                        cum_pct = max(0.0, min(100.0, (last_total / float(context_window)) * 100.0))
                                        bar_width = 30
                                        filled = int(round((cum_pct / 100.0) * bar_width))
                                        empty = bar_width - filled
                                        if self.ui.rich:
                                            filled_str = "█" * filled if filled > 0 else ""
                                            empty_str = "░" * empty if empty > 0 else ""
                                            bar = (
                                                f"[white][[/white]"
                                                f"[{self.ui.theme['assistant']}]{filled_str}[/{self.ui.theme['assistant']}]"
                                                f"[white]{empty_str}[/white]"
                                                f"[white]][/white]"
                                            )
                                        else:
                                            filled_str = "#" * filled if filled > 0 else ""
                                            empty_str = "-" * empty if empty > 0 else ""
                                            bar = "[" + filled_str + empty_str + "]"
                                        # Show the bar for this reply's usage and include token count (in+out) and percent
                                        context_line_str = f"Context: {int(last_total)} {bar} {cum_pct:.1f}%"
                                        box_lines.append(context_line_str)
                                except Exception:
                                    # Non-fatal UI enhancement
                                    pass
    
                                # OpenAI prompt caching banner when detected (cached input tokens billed at 10%)
                                try:
                                    price = self._resolve_price(model_used)
                                    provider = (price.get("provider") or "").lower()
                                    cached_tokens_banner = 0
                                    # Prefer top-level input_tokens_details
                                    itd = usage.get("input_tokens_details") if isinstance(usage, dict) else None
                                    if isinstance(itd, dict):
                                        cached_tokens_banner = int(itd.get("cached_tokens", 0) or 0)
                                    # Fallback: some servers may nest under turn.input_tokens_details
                                    if not cached_tokens_banner:
                                        itd2 = (usage.get("turn") or {}).get("input_tokens_details") if isinstance(usage, dict) else None
                                        if isinstance(itd2, dict):
                                            cached_tokens_banner = int(itd2.get("cached_tokens", 0) or 0)
                                    if provider == "openai" and cached_tokens_banner and cached_tokens_banner > 0:
                                        # Compute savings relative to full input price (cache billed at 10% input rate)
                                        try:
                                            in_rate_per_m = float(price.get("input", 0.0))
                                        except Exception:
                                            in_rate_per_m = 0.0
                                        try:
                                            saved_usd = (int(cached_tokens_banner) / 1_000_000.0) * in_rate_per_m * 0.90
                                        except Exception:
                                            saved_usd = 0.0
                                        # Short copy per request: say "saved $x.xx with prompt cache"
                                        box_lines.append(f"saved ${saved_usd:.2f} with prompt cache")
                                except Exception:
                                    pass
    
                                # Anthropic prompt caching banner when detected (reads @10% input rate; creation billed at TTL multiplier)
                                try:
                                    price = self._resolve_price(model_used)
                                    provider = (price.get("provider") or "").lower()
                                    if provider == "anthropic":
                                        cr = int(usage.get("cache_read_input_tokens", 0) or 0)
                                        cc = int(usage.get("cache_creation_input_tokens", 0) or 0)
                                        # Optional breakdown
                                        cc_5m = 0
                                        cc_1h = 0
                                        try:
                                            ccmap = usage.get("cache_creation") if isinstance(usage, dict) else None
                                            if isinstance(ccmap, dict):
                                                cc_5m = int(ccmap.get("ephemeral_5m_input_tokens", 0) or 0)
                                                cc_1h = int(ccmap.get("ephemeral_1h_input_tokens", 0) or 0)
                                        except Exception:
                                            cc_5m = cc_5m or 0
                                            cc_1h = cc_1h or 0
                                        if (cr > 0) or (cc > 0) or (cc_5m > 0) or (cc_1h > 0):
                                            # Build a concise line similar to OpenAI banner
                                            line = f"Billing: Anthropic prompt cache read {int(cr)} token(s) @10% input rate"
                                            if (cc_5m > 0) or (cc_1h > 0):
                                                line += f" | created {int(cc_5m)} @1.25x + {int(cc_1h)} @2x"
                                            else:
                                                if cc > 0:
                                                    line += f" | created {int(cc)} token(s) (billed at 1.25x/2x based on TTL)"
                                            # Calculate savings (reported on a separate line to match OpenAI style)
                                            saved_line = None
                                            if cr > 0:
                                                try:
                                                    in_rate_per_m = float(price.get("input", 0.0))
                                                    # Savings = cache_read * (1.0 - 0.1) * price
                                                    saved_usd = (int(cr) / 1_000_000.0) * in_rate_per_m * 0.90
                                                    saved_line = f"saved ${saved_usd:.2f} with prompt cache"
                                                except Exception:
                                                    saved_line = None
                                            box_lines.append(line)
                                            if saved_line:
                                                box_lines.append(saved_line)
                                except Exception:
                                    pass
    
                                # Show consolidated usage summary
                                try:
                                    if str(getattr(self, 'usage_info_mode', 'verbose')).lower() == 'concise':
                                        # Concise mode: render a single tokens-used line. Recompute the bar to avoid markup tags.
                                        if context_line_str and isinstance(context_line_str, str) and ":" in context_line_str:
                                            try:
                                                _, tail = context_line_str.split(":", 1)
                                                tail = tail.strip()
                                                # Expected tail form: "<total> [bar] <pct>%". Parse total and pct.
                                                parts = tail.split()
                                                total_val = None
                                                pct_val = None
                                                if parts:
                                                    # First token should be integer total
                                                    try:
                                                        total_val = int(parts[0])
                                                    except Exception:
                                                        total_val = None
                                                # Last token should be like '12.3%'
                                                if parts:
                                                    last_tok = parts[-1]
                                                    if isinstance(last_tok, str) and last_tok.endswith('%'):
                                                        try:
                                                            pct_val = float(last_tok[:-1])
                                                        except Exception:
                                                            pct_val = None
                                                # Build bar anew
                                                bar_width = 30
                                                if isinstance(pct_val, (int, float)):
                                                    filled = int(round((float(pct_val) / 100.0) * bar_width))
                                                else:
                                                    filled = 0
                                                empty = max(0, bar_width - filled)
                                                if self.ui.rich:
                                                    # Segmented color render without markup parsing
                                                    self.ui.print("tokens used:", style="white", end=" ")
                                                    self.ui.print(str(total_val if total_val is not None else 0), end=" ")
                                                    self.ui.print("[", style="white", end="")
                                                    self.ui.print("\u2588" * filled, style=self.ui.theme.get("assistant"), end="")
                                                    self.ui.print("\u2591" * empty, style="white", end="")
                                                    self.ui.print("]", style="white", end=" ")
                                                    self.ui.print(f"{(pct_val if pct_val is not None else 0.0):.1f}%")
                                                else:
                                                    # Plain ASCII fallback
                                                    bar_ascii = "[" + ("#" * filled) + ("-" * empty) + "]"
                                                    self.ui.print(f"tokens used: {total_val if total_val is not None else 0} {bar_ascii} {(pct_val if pct_val is not None else 0.0):.1f}%")
                                            except Exception:
                                                # Replace leading label only
                                                try:
                                                    _, tail = context_line_str.split(":", 1)
                                                    self.ui.print("tokens used:", style="white", end="")
                                                    self.ui.print(tail)
                                                except Exception:
                                                    self.ui.print(context_line_str)
                                        else:
                                            # No context line available; show info box in verbose mode only
                                            self.ui.info_box("Usage & Info", box_lines)
                                    else:
                                        self.ui.info_box("Usage & Info", box_lines)
                                except Exception:
                                    # Fallback to plain prints if box fails
                                    try:
                                        if str(getattr(self, 'usage_info_mode', 'verbose')).lower() == 'concise' and context_line_str:
                                            try:
                                                _, tail = context_line_str.split(":", 1)
                                                self.ui.print("tokens used:", style="white", end="")
                                                self.ui.print(tail)
                                            except Exception:
                                                self.ui.print(context_line_str, style="white")
                                        else:
                                            for ln in box_lines:
                                                self.ui.print(ln)
                                    except Exception:
                                        pass
    
                                # Print a one-liner usage by category only when verbose (silenced by default)
                                try:
                                    by_cat = usage.get("by_category") or {}
                                    if isinstance(by_cat, dict) and by_cat:
                                        order = ["read", "nav", "write", "exec"]
                                        segs = []
                                        for k in order:
                                            v = by_cat.get(k)
                                            if not isinstance(v, dict):
                                                continue
                                            vin = int(v.get("input_tokens", 0) or 0)
                                            vout = int(v.get("output_tokens", 0) or 0)
                                            segs.append(f"{k} in {vin}/out {vout}")
                                        for k, v in by_cat.items():
                                            if k in order or not isinstance(v, dict):
                                                continue
                                            vin = int(v.get("input_tokens", 0) or 0)
                                            vout = int(v.get("output_tokens", 0) or 0)
                                            segs.append(f"{k} in {vin}/out {vout}")
                                        if segs and self.ui.verbose:
                                            self.ui.print(
                                                "Usage by category: " + " | ".join(segs),
                                                style=self.ui.theme["dim"],
                                            )
                                except Exception:
                                    pass
    
                                # Grey debug line: show provider raw step usages if present and their summed totals
                                try:
                                    steps = usage.get("provider_steps") if isinstance(usage, dict) else None
                                    if isinstance(steps, list) and steps:
                                        sum_in = 0
                                        sum_out = 0
                                        parts = []
                                        for st in steps[:10]:
                                            try:
                                                si = int(st.get("input_tokens", 0) or 0)
                                                so = int(st.get("output_tokens", 0) or 0)
                                                sum_in += si
                                                sum_out += so
                                                stage = str(st.get("stage") or "turn")
                                                parts.append(f"{stage}: in {si}, out {so}")
                                            except Exception:
                                                continue
                                        cum_dbg = usage.get("cumulative") or {}
                                        cin = int(cum_dbg.get("input_tokens", sum_in) or sum_in) if isinstance(cum_dbg, dict) else sum_in
                                        cout = int(cum_dbg.get("output_tokens", sum_out) or sum_out) if isinstance(cum_dbg, dict) else sum_out
                                        ctot = int(cum_dbg.get("total_tokens", cin + cout) or (cin + cout)) if isinstance(cum_dbg, dict) else (cin + cout)
                                        # Wording tweak: say "tool calls" instead of "provider steps" for clarity
                                        # Show only in verbose mode (silenced by default)
                                        if self.ui.verbose:
                                            self.ui.print(f"[raw] tool calls -> {'; '.join(parts)} | sum: in {cin} + out {cout} = {ctot}", style=self.ui.theme["dim"])
                                except Exception:
                                    pass
    
                                # Append assistant message with token stats to messages_for_save
                                if self.save_chat_history:
                                    try:
                                        self.messages_for_save.append({
                                            "role": "assistant",
                                            "content": "".join(assistant_buf),
                                            "model": model_used,
                                            "citations": None,
                                            "last_turn_input_tokens": int(turn_in),
                                            "last_turn_output_tokens": int(turn_out),
                                            "last_turn_total_tokens": int(turn_total),
                                        })
                                        if web_search_calls and self.messages_for_save:
                                            citations: List[Dict[str, Any]] = []
                                            for call in web_search_calls:
                                                action = call.get("action") if isinstance(call, dict) else None
                                                if isinstance(action, dict):
                                                    sources = action.get("sources")
                                                    if isinstance(sources, list):
                                                        for src in sources:
                                                            if isinstance(src, dict):
                                                                citations.append(src)
                                            if citations:
                                                self.messages_for_save[-1]["citations"] = citations
                                    except Exception:
                                        pass
    
                                # Log JSONL
                                self._log_line({
                                    "event": "usage",
                                    "model": model_used,
                                    "turn": {"in": turn_in, "out": turn_out, "total": turn_total},
                                    "cumulative": {"in": cum_in, "out": cum_out, "total": cum_total},
                                    "by_category": usage.get("by_category") or None,
                                    "cumulative_source": cum_source,
                                    "assistant_text_len": len("".join(assistant_buf)),
                                    "timing": {
                                        "turn_duration_ms": int(round(turn_secs * 1000.0)),
                                        "session_elapsed_ms": int(round(session_secs * 1000.0)),
                                        "tool_calls": int(tool_calls),
                                    },
                                    "web_search": web_search_calls or None,
                                })
                                self._log_line({
                                    "event": "assistant",
                                    "content": "".join(assistant_buf),
                                    "model": model_used,
                                    "web_search": web_search_calls or None,
                                })
    
                                # Save to server threads (best-effort)
                                await self._save_conversation(client, selected_model=model_used)
    
                                # Optional category breakdown when --verbose
                                by_cat = usage.get("by_category") or {}
                                if self.ui.verbose and isinstance(by_cat, dict) and by_cat:
                                    order = ["read", "nav", "write", "exec"]
                                    rows: List[Tuple[str, int, int, int]] = []
                                    for k in order:
                                        v = by_cat.get(k)
                                        if not isinstance(v, dict):
                                            continue
                                        vin = int(v.get("input_tokens", 0) or 0)
                                        vout = int(v.get("output_tokens", 0) or 0)
                                        vtot = int(v.get("total_tokens", vin + vout) or 0)
                                        rows.append((k, vin, vout, vtot))
                                    for k, v in by_cat.items():
                                        if k in order or not isinstance(v, dict):
                                            continue
                                        vin = int(v.get("input_tokens", 0) or 0)
                                        vout = int(v.get("output_tokens", 0) or 0)
                                        vtot = int(v.get("total_tokens", vin + vout) or 0)
                                        rows.append((k, vin, vout, vtot))
                                    if rows:
                                        if self.ui.rich and Table:
                                            t = Table(title=None, show_lines=False, header_style=self.ui.theme["subtitle"])
                                            t.add_column("Category")
                                            t.add_column("Input", justify="right")
                                            t.add_column("Output", justify="right")
                                            t.add_column("Total", justify="right")
                                            for k, vin, vout, vtot in rows:
                                                t.add_row(k, str(vin), str(vout), str(vtot))
                                            self.ui.print("by_category:", style=self.ui.theme["dim"])
                                            self.ui.console.print(t)
                                        else:
                                            self.ui.print("by_category:", style=self.ui.theme["dim"])
                                            for k, vin, vout, vtot in rows:
                                                self.ui.print(f"  - {k}: in {vin}, out {vout}, tot {vtot}", style=self.ui.theme["dim"])
    
                                try:
                                    await self._ws_broadcast("message.completed", {"model": model_used, "usage": usage, "by_category": usage.get("by_category")})
                                except Exception:
                                    pass
                                if web_search_calls:
                                    try:
                                        await self._ws_broadcast("web_search.summary", {"model": model_used, "calls": web_search_calls})
                                    except Exception:
                                        pass
    
                                # Clear current turn tracking
                                try:
                                    self._current_turn = {
                                        "active": False,
                                        "session_id": None,
                                        "model": None,
                                        "assistant_so_far": "",
                                        "tool_events": [],
                                    }
                                except Exception:
                                    pass
    
                                return "".join(assistant_buf)
    
                            if event == "warning":
                                # Handle warning events (e.g., model swap with tools)
                                msg = data.get("message", "")
                                self.ui.warn(msg)
                                try:
                                    await self._ws_broadcast("warning", {"message": msg})
                                except Exception:
                                    pass
                                try:
                                    last_events.append({"event": "warning", "message": (msg[:160] if isinstance(msg, str) else str(msg))})
                                except Exception:
                                    pass
                                continue
    
                            elif event == "error":
                                # Stop and clear indicator before printing the error
                                try:
                                    await _indicator_stop(clear=True)
                                except Exception:
                                    pass
                                buf_str = "".join(assistant_buf)
                                self.ui.ensure_newline(buf_str)
                                err_msg = data.get("message", "Unknown error") or "Unknown error"
                                self.ui.error(err_msg)
                                try:
                                    last_error = True
                                except Exception:
                                    pass
                                streaming_assistant = False
                                # Heuristic: detect provider size-limit errors and mark next read_file on same path for tailing
                                try:
                                    em = str(err_msg).lower()
                                    too_long = (
                                        ("string too long" in em) or ("above_max_length" in em) or ("too long" in em and "input[0].output" in em)
                                    )
                                    if too_long and isinstance(self._last_dispatch_ctx, dict):
                                        if str(self._last_dispatch_ctx.get("name") or "") == "read_file":
                                            args_ctx = self._last_dispatch_ctx.get("args") or {}
                                            pth = args_ctx.get("path")
                                            if isinstance(pth, str) and pth:
                                                self._tail_next_paths.add(pth)
                                                self._auto_retry_after_tailed = True
                                                self.ui.warn(f"Provider refused large tool output; will tail next read of: {pth}")
                                except Exception:
                                    pass
                                try:
                                    await self._ws_broadcast("error", {"message": err_msg})
                                except Exception:
                                    pass
                                try:
                                    last_events.append({"event": "error", "message": (err_msg[:200] if isinstance(err_msg, str) else str(err_msg))})
                                except Exception:
                                    pass
                                return "".join(assistant_buf)
    
                            elif event == "provider.message":
                                # Provider-native message snapshot (e.g., Kimi assistant with reasoning_content)
                                provider = (data.get("provider") or "").lower()
                                msg = data.get("message")
                                if bool(getattr(self, "retain_native_tool_results", False)) and provider == "kimi" and isinstance(msg, dict):
                                    # Append as-is to local raw history for the next turn
                                    try:
                                        self._kimi_raw_history.append(dict(msg))
                                    except Exception:
                                        try:
                                            self._kimi_raw_history.append(msg)  # type: ignore
                                        except Exception:
                                            pass
                                continue
    
                            else:
                                # TEMP DEBUG: show unknown/unhandled events
                                if DEBUG_SSE:
                                    self.ui.print(f"[debug] unhandled event: {event} payload={truncate_json(data, 800)}", style=self.ui.theme["dim"])
    
                    # If stream ended without a message.completed, render a fallback info box
                    # Ensure the indicator is stopped on abnormal termination and fully cleared
                    try:
                        await _indicator_stop(clear=True)
                    except Exception:
                        pass
                    buf_str2 = "".join(assistant_buf)
                    self.ui.ensure_newline(buf_str2)
                    # Use a visible notice (non-dim) so users are aware something ended unexpectedly
                    self.ui.warn("Stream ended without a completed event (no usage reported)")
                    try:
                        if DEBUG_SSE or self.ui.verbose:
                            self.ui.print(
                                f"[debug] stream ended without completed (events={_events_total} deltas={_deltas_total} bytes={_bytes_total})",
                                style=self.ui.theme["dim"],
                            )
                    except Exception:
                        pass
                    # Diagnostic block when the server omits message.completed
                    try:
                        diag_lines_fb: List[str] = []
                        diag_lines_fb.append("Diagnostics: no message.completed event received — usage missing")
                        diag_lines_fb.append(f"- stream: events={_events_total}, deltas={_deltas_total}, bytes={_bytes_total}")
                        diag_lines_fb.append(f"- commit path: enabled={bool(self.server_usage_commit)} | session_id={'set' if session_id else 'missing'} | model={(self._current_turn.get('model') or self._last_used_model or self.model or '(server default)')}" )
                        # Summarize last events (up to 8)
                        try:
                            if last_events:
                                diag_lines_fb.append("- last events (most recent first):")
                                shown = list(last_events)[-8:][::-1]
                                for ev in shown:
                                    try:
                                        et = ev.get("event")
                                        if et == "message.delta":
                                            diag_lines_fb.append(f"  • message.delta bytes={ev.get('bytes')}")
                                        elif et in ("tool.call", "tool.result", "tool.dispatch"):
                                            base = f"  • {et} name={ev.get('name')}"
                                            if et != "tool.call":
                                                base += f" ok={ev.get('ok')}"
                                            diag_lines_fb.append(base)
                                        elif et in ("warning", "error"):
                                            diag_lines_fb.append(f"  • {et} {self._clip(ev.get('message'), 140)}")
                                        elif et == "session.started":
                                            diag_lines_fb.append(f"  • session.started level={ev.get('level')} scope={ev.get('fs_scope')}")
                                        else:
                                            diag_lines_fb.append(f"  • {et}")
                                    except Exception:
                                        continue
                        except Exception:
                            pass
                        # Show x-* response headers when present (can hint at proxy behavior)
                        try:
                            if sse_headers_diag:
                                diag_lines_fb.append("- response x-* headers:")
                                for k, v in sse_headers_diag.items():
                                    diag_lines_fb.append(f"  • {k}: {v}")
                        except Exception:
                            pass
                        # Render above the fallback Usage & Info box
                        try:
                            if self.ui.rich and Panel:
                                self.ui.console.print(Panel("\n".join(diag_lines_fb), title="Diagnostics (usage/cost)", border_style=self.ui.theme["warn"]))
                            else:
                                self.ui.print("Diagnostics (usage/cost):", style=self.ui.theme["warn"])  # type: ignore
                                for ln in diag_lines_fb:
                                    self.ui.print(ln, style=self.ui.theme["dim"])  # type: ignore
                        except Exception:
                            # Best-effort plain prints
                            self.ui.print("Diagnostics (usage/cost):")
                            for ln in diag_lines_fb:
                                self.ui.print(ln)
                        # Persist
                        try:
                            self._log_line({
                                "event": "diagnostics.no_completed",
                                "stream": {"events": _events_total, "deltas": _deltas_total, "bytes": _bytes_total},
                                "session_id": session_id,
                                "model": (self._current_turn.get('model') or self._last_used_model or self.model),
                                "resp_headers_x": sse_headers_diag or None,
                                "last_events": list(last_events) if last_events else None,
                            })
                        except Exception:
                            pass
                    except Exception:
                        pass
                    # Timing summary even if server omitted usage
                    try:
                        now_pc = time.perf_counter()
                        turn_secs = (now_pc - (self._turn_started_at or now_pc))
                        session_secs = (now_pc - (self._session_started_at or now_pc)) if (self._session_started_at is not None) else 0.0
                    except Exception:
                        turn_secs = 0.0
                        session_secs = 0.0
                    def _fmt(sec: float) -> str:
                        try:
                            if sec < 60:
                                return f"{sec:.2f}s"
                            m, s = divmod(int(sec), 60)
                            if m < 60:
                                return f"{m}m {s}s"
                            h, m = divmod(m, 60)
                            return f"{h}h {m}m {s}s"
                        except Exception:
                            return f"{sec:.2f}s"

                    # Build a compact fallback Usage & Info box so users still see context
                    box_lines_fb: List[str] = []
                    context_line_fb: Optional[str] = None
                    # Version + update hint
                    try:
                        if not self._cli_version:
                            self._cli_version = self._resolve_current_version() or None
                        if self._cli_version:
                            ver_line = f"henosis-cli v{self._cli_version}"
                            if (self._version_outdated is True) and self._latest_version:
                                ver_line += f" → v{self._latest_version} available | update: {os.path.basename(sys.executable)} -m pip install -U henosis-cli"
                            box_lines_fb.append(ver_line)
                    except Exception:
                        pass
                    # Model/cost line (costs remain at previous totals since no usage was reported)
                    try:
                        # Prefer the most accurate model label we saw this turn
                        model_label = (self._current_turn.get("model") or self._last_used_model or self.model or "(server default)")
                    except Exception:
                        model_label = self.model or "(server default)"
                    # Reasoning effort tag for OpenAI reasoning models
                    try:
                        effort_seg = ""
                        if self._is_openai_reasoning_model(model_label):
                            lvl = str(self.reasoning_effort or "medium").strip().lower()
                            if lvl not in ("low", "medium", "high"):
                                lvl = "medium"
                            effort_seg = f" {lvl.capitalize()}"
                    except Exception:
                        effort_seg = ""
                    try:
                        rem_line = (
                            f" | remaining credits: ${float(self._last_remaining_credits):.6f}"
                            if (self._last_remaining_credits is not None)
                            else ""
                        )
                    except Exception:
                        rem_line = ""
                    model_only_fb = f"model: {model_label}{effort_seg}"
                    box_lines_fb.append(
                        f"model: {model_label}{effort_seg} | cost charged: ${float(self._last_commit_cost_usd):.6f} | chat cost: ${float(self.server_cumulative_cost_usd):.6f}{rem_line}"
                    )
                    # Tokens unknown without completed usage; show zeros to signal missing metrics
                    box_lines_fb.append("Turn tokens: in 0 + out 0 = 0")
                    try:
                        cin = int(self._cum_input_tokens or 0)
                        cout = int(self._cum_output_tokens or 0)
                        ctot = int(self._cum_total_tokens or (cin + cout))
                    except Exception:
                        cin, cout, ctot = 0, 0, 0
                    box_lines_fb.append(f"Session tokens: in {cin} + out {cout} = {ctot}")
                    box_lines_fb.append(f"Time: {_fmt(turn_secs)} (turn) | {_fmt(session_secs)} (session) | Tools: {tool_calls} call(s)")
                    # Context bar (0 when usage missing)
                    try:
                        if self.ui.rich:
                            bar = "[" + f"[{self.ui.theme['dim']}]{'░'*30}[/{self.ui.theme['dim']}]" + "]"
                        else:
                            bar = "[" + ("-" * 30) + "]"
                        box_lines_fb.append(f"Context: 0 {bar} 0.0%")
                    except Exception:
                        pass
                    # Extract context line for concise mode if not already captured
                    if context_line_fb is None:
                        try:
                            for _ln in reversed(box_lines_fb):
                                if isinstance(_ln, str) and _ln.startswith("Context: "):
                                    context_line_fb = _ln
                                    break
                        except Exception:
                            context_line_fb = None
                    # Final render
                    try:
                        if str(getattr(self, 'usage_info_mode', 'verbose')).lower() == 'concise':
                            # Concise mode: only show the context line, relabeled
                            if context_line_fb:
                                try:
                                    if ":" in context_line_fb:
                                        _, tail = context_line_fb.split(":", 1)
                                        # Two-part render: white label, default-styled tail
                                        self.ui.print("tokens used:", style="white", end="")
                                        self.ui.print(tail)
                                    else:
                                        self.ui.print(context_line_fb, style="white")
                                except Exception:
                                    self.ui.print(context_line_fb, style="white")
                        else:
                            self.ui.info_box("Usage & Info", box_lines_fb)
                    except Exception:
                        # Fallback to a single-line time summary if box fails
                        self.ui.print(
                            f"[time] turn: {_fmt(turn_secs)} | session: {_fmt(session_secs)} | tools: {tool_calls} call(s)",
                            style=self.ui.theme["dim"],
                            force=True,
                        )
                    try:
                        await self._ws_broadcast("message.completed", {"model": self.model, "usage": {}, "by_category": {}})
                    except Exception:
                        pass
                    return "".join(assistant_buf)
        try:
                # Per-turn retry controller: up to 3 total attempts (original + 2 retries)
                attempts_done = 1
                # Flags shared with do_stream
                last_completed = False
                last_error = False
                last_bytes_total = 0
                result_text = await do_stream(payload)

                # Auto-restart after summarization: clear conversation and resend same user input with injections
                if self._restart_after_summary:
                    self._restart_after_summary = False
                    # Reset conversation to a fresh session (preserve system prompt)
                    self.history = [{"role": "system", "content": self.system_prompt}] if self.system_prompt else []
                    # Allow codebase map to be injected again
                    self._did_inject_codebase_map = False
                    # Ensure working-memory first-turn flag remains False so we inject now
                    self._did_inject_working_memory = False                    # Allow custom first-turn text to inject again
                    try:
                        self._did_inject_custom_first_turn = False
                    except Exception:
                        pass
                    # Reset provider-native histories
                    self.messages_for_save = []
                    if not self.save_chat_history:
                        self.thread_uid = None
                    self._kimi_raw_history = []

                    # Build a fresh payload so the first-turn injections (code map + working memory) are applied
                    new_payload: Dict[str, Any] = {"messages": self._build_messages(user_input)}
                    if self.model:
                        new_payload["model"] = self.model
                    try:
                        if self.terminal_id:
                            new_payload["terminal_id"] = self.terminal_id
                    except Exception:
                        pass
                    if self.requested_tools is True:
                        new_payload["enable_tools"] = True
                    elif self.requested_tools is False:
                        new_payload["enable_tools"] = False
                    if self.fs_scope in ("workspace", "host"):
                        new_payload["fs_scope"] = self.fs_scope
                    if self.host_base:
                        new_payload["host_base"] = self.host_base
                    if self.fs_scope == "host":
                        mode = (self.fs_host_mode or "any")
                        new_payload["host_roots_mode"] = mode
                        if mode in ("cwd", "custom") and self.host_base:
                            new_payload["host_allowed_dirs"] = [self.host_base]
                    if self.control_level in (1, 2, 3):
                        new_payload["control_level"] = self.control_level
                    if self.auto_approve:
                        new_payload["auto_approve"] = self.auto_approve
                    try:
                        if isinstance(self.reasoning_effort, str):
                            if self.reasoning_effort in ("low", "medium", "high"):
                                new_payload["reasoning_effort"] = self.reasoning_effort
                            elif self.reasoning_effort == "xhigh" and self._is_codex_max(self.model):
                                new_payload["reasoning_effort"] = "xhigh"
                            else:
                                new_payload["reasoning_effort"] = "medium"
                        else:
                            new_payload["reasoning_effort"] = "medium"
                    except Exception:
                        new_payload["reasoning_effort"] = "medium"
                    try:
                        if isinstance(self.thinking_budget_tokens, int) and self.thinking_budget_tokens > 0:
                            new_payload["thinking_budget_tokens"] = int(self.thinking_budget_tokens)
                    except Exception:
                        pass
                    # Anthropic prompt cache TTL (server override): send when set to 5m or 1h
                    try:
                        if isinstance(self.anthropic_cache_ttl, str) and self.anthropic_cache_ttl in ("5m", "1h"):
                            new_payload["anthropic_cache_ttl"] = self.anthropic_cache_ttl
                    except Exception:
                        pass
                    if self.web_search_enabled:
                        new_payload["enable_web_search"] = True
                        if self.web_search_allowed_domains:
                            new_payload["web_search_allowed_domains"] = self.web_search_allowed_domains
                        if self.web_search_include_sources:
                            new_payload["web_search_include_sources"] = True
                        loc_payload = self._web_search_location_payload()
                        if loc_payload:
                            new_payload["web_search_user_location"] = loc_payload
                    else:
                        new_payload["enable_web_search"] = False
                    self.ui.print("Resending your last message with Code Map + Working Memory prefix...", style=self.ui.theme["dim"])
                    return await do_stream(new_payload)

                # If we marked an auto-retry due to provider output size limits, retry once using the same payload
                if self._auto_retry_after_tailed:
                    self._auto_retry_after_tailed = False
                    self.ui.warn("Retrying turn with tailed file content due to provider output size limit...")
                    return await do_stream(payload)

                # Generic retry: when stream ended without a message.completed, retry the last model turn
                max_attempts = 3
                while (not last_completed) and (attempts_done < max_attempts):
                    attempts_done += 1
                    # Emit CLI/WS notice
                    try:
                        self.ui.print(f"[retry] restarting last model turn (attempt {attempts_done}/{max_attempts}) …", style=self.ui.theme["info"])  # type: ignore
                        await self._ws_broadcast("retry.notice", {"attempt": attempts_done, "max_attempts": max_attempts})
                        # Persist a brief log line
                        self._log_line({
                            "event": "retry.attempt",
                            "attempt": int(attempts_done),
                            "max": int(max_attempts),
                            "bytes_prev_attempt": int(last_bytes_total),
                            "completed_prev_attempt": bool(last_completed),
                            "had_error_prev_attempt": bool(last_error),
                            "idempotency_key": idempotency_key,
                        })
                        if self.raw_log_enabled:
                            self._rawlog_write(f"[retry] attempt {attempts_done}/{max_attempts} idemp={idempotency_key} prev_bytes={last_bytes_total} completed={last_completed} error={last_error}")
                    except Exception:
                        pass
                    # Reset local stream buffers so we don't prefill or suppress headers on new attempt
                    try:
                        assistant_buf = []
                        header_printed = False
                        session_id = None
                    except Exception:
                        pass
                    # Reset per-attempt flags before calling do_stream again
                    last_completed = False
                    last_error = False
                    last_bytes_total = 0
                    result_text = await do_stream(payload)

                # If still not completed after retries, emit a final failure notice
                if not last_completed:
                    try:
                        self.ui.print(f"[retry] failed after {attempts_done} attempt(s)", style=self.ui.theme["warn"])  # type: ignore
                        await self._ws_broadcast("retry.failed", {"attempts": attempts_done, "max_attempts": max_attempts})
                        self._log_line({
                            "event": "retry.give_up",
                            "attempts": int(attempts_done),
                            "max": int(max_attempts),
                            "bytes_last_attempt": int(last_bytes_total),
                            "idempotency_key": idempotency_key,
                        })
                        if self.raw_log_enabled:
                            self._rawlog_write(f"[retry] give up after {attempts_done}/{max_attempts} attempts idemp={idempotency_key} last_bytes={last_bytes_total}")
                    except Exception:
                        pass
                return result_text

        except httpx.HTTPStatusError as he:
            status = he.response.status_code if he.response is not None else None
            # Try to refresh auth on 401 and retry once
            if status == 401:
                try:
                    async with httpx.AsyncClient(timeout=http_timeout, cookies=self.cookies) as client:
                        r = await client.post(self.refresh_url)
                        if r.status_code == 200:
                            # Persist rotated tokens if rotation occurred
                            try:
                                refresh_data = r.json()
                                if refresh_data.get('rotated'):
                                    self._save_auth_state_to_disk()
                            except Exception:
                                pass
                            try:
                                return await do_stream(payload)
                            except Exception:
                                pass
                except Exception:
                    pass
            # If refresh failed, offer a quick re-login flow for better UX
            try:
                self.ui.warn("Your session has expired. Let's refresh your login.")
                ok = await self._login_with_retries()
                if ok:
                    try:
                        return await do_stream(payload)
                    except Exception:
                        pass
            except SystemExit:
                raise
            except Exception:
                pass
            raw_text = ""
            body_json: Any = None
            try:
                if he.response is not None:
                    await he.response.aread()
                    raw_text = he.response.text
                    ctype = he.response.headers.get("content-type", "")
                    if "application/json" in ctype.lower() and raw_text:
                        body_json = json.loads(raw_text)
            except Exception:
                body_json = None
            # Friendly header
            self.ui.warn(f"HTTP {status} received from server. Context:")
            self.ui.print(f"- Endpoint: {self.stream_url}", style=self.ui.theme["dim"])
            self.ui.print(f"- Model: {self.model or '(server default)'}", style=self.ui.theme["dim"])
            # Provider guess from model
            provider = "unknown"
            try:
                m = (self.model or "").lower() if self.model else ""
                if m.startswith("gemini-"):
                    provider = "gemini"
                elif m.startswith("grok-"):
                    provider = "xai"
                elif m.startswith("deepseek-"):
                    provider = "deepseek"
                elif m.startswith("kimi-"):
                    provider = "kimi"
                elif m.startswith("claude-"):
                    provider = "anthropic"
                elif m:
                    provider = "openai"
            except Exception:
                provider = "unknown"
            if provider != "unknown":
                self.ui.print(f"- Provider: {provider}", style=self.ui.theme["dim"])
            # Show parsed JSON error details when possible
            if isinstance(body_json, dict):
                detail = body_json.get("detail")
                error_type = body_json.get("error") or body_json.get("type")
                if error_type:
                    self.ui.error(f"{error_type}")
                if detail:
                    self.ui.print(truncate_json(detail, 1500), style=self.ui.theme["dim"])
            else:
                if raw_text:
                    self.ui.print(self._clip(raw_text, 4000), style=self.ui.theme["dim"])
                else:
                    self.ui.print("(no response text available)", style=self.ui.theme["dim"])
            # Heuristics and suggested fixes
            tips: List[str] = []
            body_lower = (raw_text or "").lower()
            if provider == "gemini" and ("gemini_api_key" in body_lower or ("gemini" in body_lower and "key" in body_lower)):
                tips.append("Set GEMINI_API_KEY in the server .env (no quotes) and restart the server.")
                tips.append("Ensure google-genai is installed: pip install google-genai")
            if provider == "anthropic" and ("anthropic_api_key" in body_lower or ("anthropic" in body_lower and "key" in body_lower)):
                tips.append("Set ANTHROPIC_API_KEY in the server .env and restart.")
                tips.append("Install anthropic: pip install anthropic")
            if provider == "xai" and ("xai_api_key" in body_lower or "x.ai" in body_lower):
                tips.append("Set XAI_API_KEY in the server .env and restart.")
            if provider == "deepseek" and ("deepseek_api_key" in body_lower or "deepseek" in body_lower):
                tips.append("Set DEEPSEEK_API_KEY in the server .env and restart.")
            if provider == "kimi" and ("kimi_api_key" in body_lower or "moonshot" in body_lower or "kimi" in body_lower):
                tips.append("Set KIMI_API_KEY in the server .env and restart.")
            if "not installed" in body_lower or "module not found" in body_lower:
                tips.append("Install missing provider SDK on the server environment.")
            if tips:
                self.ui.print("Possible fixes:")
                for t in tips:
                    self.ui.print(f"- {t}", style=self.ui.theme["dim"])
            # Best-effort: query /health for quick diagnostics
            try:
                health_url = join_url(self.server, "/health")
                async with httpx.AsyncClient(timeout=self.timeout, cookies=self.cookies) as hc:
                    h = await hc.get(health_url)
                    if h.status_code == 200 and "application/json" in (h.headers.get("content-type", "")):
                        hjson = h.json()
                        tools_enabled = hjson.get("tools_enabled")
                        workspace = hjson.get("workspace")
                        version = hjson.get("version") or hjson.get("status")
                        self.ui.print(f"- /health: tools_enabled={tools_enabled}, workspace={workspace}, version={version}", style=self.ui.theme["dim"])
            except Exception:
                pass
            # Log to the session log file
            try:
                self._log_line({
                    "event": "http_error",
                    "status": int(status) if status else 0,
                    "body": body_json if isinstance(body_json, dict) else self._clip(raw_text, 4000),
                    "provider": provider,
                    "model": self.model,
                    "endpoint": self.stream_url,
                })
            except Exception:
                pass
            # Raw log the HTTP error as well
            try:
                if self.raw_log_enabled:
                    self._rawlog_write(f"<<< HTTP {status} ERROR from {self.stream_url}")
                    if isinstance(body_json, dict):
                        self._rawlog_write_json(body_json)
                    elif raw_text:
                        # Write raw body text if not JSON
                        self._rawlog_write(raw_text[:4000])
            except Exception:
                pass
            # Do not re-raise; return empty to keep caller logic simple
            return ""

        # Fallback return (should not reach)
        return ""

    # ----------------------- Model context helpers ----------------------
    def _load_model_ctx_map(self) -> Dict[str, int]:
        """Load mapping of model -> input context length (tokens) from models.txt when available.
        Falls back to a small built-in map for common models if parsing fails.
        """
        if isinstance(getattr(self, "_model_ctx_map", None), dict):
            return self._model_ctx_map  # type: ignore
        ctx_map: Dict[str, int] = {}
        # Try to locate models.txt near this script or in current working directory
        candidates: List[Path] = []
        try:
            candidates.append(Path(__file__).resolve().parent / "models.txt")
        except Exception:
            pass
        try:
            candidates.append(Path(os.getcwd()) / "models.txt")
        except Exception:
            pass
        text: Optional[str] = None
        for p in candidates:
            try:
                if p.exists():
                    text = p.read_text(encoding="utf-8", errors="ignore")
                    break
            except Exception:
                continue
        if text:
            try:
                import re
                # Match entries like: { value: 'model', ... inputContextLength: 123456, ... }
                entry_pattern = re.compile(r"\{[^}]*?value:\s*'([^']+)'[^}]*?inputContextLength:\s*(null|\d+)[^}]*?\}", re.DOTALL)
                for m in entry_pattern.finditer(text):
                    model = m.group(1)
                    val = m.group(2)
                    if val and val.isdigit():
                        ctx_map[model] = int(val)
            except Exception:
                pass
        # Fallback defaults for common models
        if not ctx_map:
            try:
                ctx_map.update({
                    "gpt-5.1": 400000,
                    "gpt-5.1-mini": 400000,
                    "gpt-5": 400000,
                    "gpt-5-2025-08-07": 400000,
                    "gpt-5-mini-2025-08-07": 400000,
                    "codex-mini-latest": 200000,
                    "gemini-2.5-pro": 1048576,
                    "gemini-2.5-flash": 1048576,
                    "gemini-3-pro-preview": 1000000,
                    "grok-4-1-fast-reasoning": 2000000,
                    "grok-4-1-fast-non-reasoning": 2000000,
                    "grok-4": 200000,
                    "grok-code-fast-1": 262144,
                    "deepseek-chat": 128000,
                    "deepseek-reasoner": 128000,
                    "kimi-k2-thinking": 262144,
                    "kimi-k2-0905-preview": 262144,
                    "claude-sonnet-4-20250514": 1000000,
                    "claude-sonnet-4-20250514-thinking": 1000000,
                    "claude-sonnet-4-5-20250929": 1000000,
                    "claude-sonnet-4-5-20250929-thinking": 1000000,
                    "claude-haiku-4-5-20251001": 200000,
                    "claude-haiku-4-5-20251001-thinking": 200000,
                    "claude-opus-4-1-20250805": 200000,
                    "claude-opus-4-1-20250805-thinking": 200000,
                    "claude-opus-4-5-20251101": 200000,
                    "claude-opus-4-5-20251101-thinking": 200000,
                    "glm-4.6": 200000,
                })
            except Exception:
                pass
        self._model_ctx_map = ctx_map
        return ctx_map

    def _get_model_ctx_window(self, model: Optional[str]) -> Optional[int]:
        """Return input context length for model if known; respects explicit ctx_window override."""
        try:
            if isinstance(self.ctx_window, int) and self.ctx_window > 0:
                return int(self.ctx_window)
        except Exception:
            pass
        if not model:
            return None
        cmap = self._load_model_ctx_map()
        if model in cmap:
            return cmap[model]
        lm = model.lower()
        for k, v in cmap.items():
            try:
                if k.lower() == lm:
                    return v
            except Exception:
                continue
        return None

    # --------------------- Tier-aware defaults -------------------------

    def _recommended_default_model(self) -> str:
        """Return the tier-aware recommended default model.

        - Free-tier users: recommend Kimi k2-thinking (free-tier friendly reasoning model).
        - All other users: recommend gpt-5.1 (best overall default).
        When tier is unknown, fall back to gpt-5.1.
        """
        try:
            if bool(self.is_free_tier):
                return "kimi-k2-thinking"
        except Exception:
            pass
        return "gpt-5.1"

    # --------------------- Onboarding and Welcome ---------------------
    async def _welcome_flow(self) -> None:
        # Render a friendly welcome screen and drive actions via a selectable menu
        self.ui.clear()
        if self.ui.rich and Panel:
            body = (
                "The command-line interface for Henosis Chat. You can:\n"
                "- Chat with multiple providers (OpenAI, Gemini, xAI, DeepSeek, Anthropic, Kimi)\n"
                "- Let the agent read and modify files within a selected Agent scope\n"
                "- Save threads, track usage/costs, and manage approvals"
            )
            self.ui.console.print(
                Panel(body, title="Welcome to henosis-cli", border_style=self.ui.theme["subtitle"])
            )
        else:
            self.ui.header("Welcome to henosis-cli")
            self.ui.print("- Multi-provider chat with optional file tools")
            self.ui.print("- Agent scope to safely limit local file access")
            self.ui.print("- Threads and usage tracking with approvals")

        while True:
            choice = await self._menu_choice(
                "Get started",
                "Choose how you’d like to get started:",
                [
                    ("login", "Login"),
                    ("register", "Register"),
                    ("quit", "Quit"),
                ],
            )
            if choice == "login":
                ok = await self._login_with_retries()
                if ok:
                    return
                # If login failed or was canceled, loop back to the menu
            elif choice == "register":
                await self.register()
                # After registration, loop back so the user can pick Login or Quit
            elif choice in ("quit", None):
                raise SystemExit(0)

    async def register(self) -> bool:
        """Registration path. Attempts CLI-native register if server supports; otherwise prints web URL."""
        web_url = "https://henosis.us/register"
        # Ask user which path (menu-based, no Y/N typing)
        choice = await self._menu_choice(
            "Registration",
            "How would you like to register?",
            [
                ("web", "Open web signup URL in your browser (recommended)"),
                ("cli", "Use CLI-native registration in this terminal"),
                ("cancel", "Cancel registration"),
            ],
        )
        if choice in (None, "cancel"):
            self.ui.info(f"You can register on the web at: {web_url}")
            return False
        if choice == "web":
            self.ui.info(f"Register on the web: {web_url}\nReturn here and choose Login when done.")
            return False
        # CLI-native attempt
        try:
            username = self.ui.prompt("Choose a username")
            email = self.ui.prompt("Email")
            password = getpass.getpass("Password (will be sent to server over HTTPS): ")
            payload = {"username": username, "email": email, "password": password}
            timeout = httpx.Timeout(connect=10.0, read=30.0, write=10.0, pool=10.0) if self.timeout is None else httpx.Timeout(self.timeout)
            async with httpx.AsyncClient(timeout=timeout) as client:
                r = await client.post(self.register_url, json=payload)
                if r.status_code >= 400:
                    self.ui.warn(f"Register returned {r.status_code}: {r.text}")
                    self.ui.info(f"You can register on the web instead: {web_url}")
                    return False
                # Dev mode: skip email verification flow in CLI
                # Some servers auto-login after registration; attempt a login to finalize the flow.
                # If server still enforces verification, the login may fail, but we won't prompt for a code.
                self.ui.success("Registration successful (dev mode: skipping email verification step).")
                try:
                    lr = await client.post(self.login_url, json={"username": username, "password": password, "remember_me": True})
                    if lr.status_code < 400:
                        # Copy cookies into CLI session and confirm auth if possible
                        self.cookies.update(lr.cookies)
                        try:
                            chk = await client.get(self.check_auth_url, cookies=self.cookies)
                            if chk.status_code == 200 and (chk.headers.get("content-type", "").startswith("application/json")):
                                data = chk.json()
                                if data.get("authenticated"):
                                    self.auth_user = str(data.get("user") or username)
                                    self._save_auth_state_to_disk()
                                    self.ui.success(f"Logged in as {self.auth_user}.")
                                    return True
                        except Exception:
                            pass
                        # If no check-auth, still consider registration done; user can /login manually
                        self.ui.info("You can now run /login to start chatting.")
                        return True
                    else:
                        # If login failed (likely because server requires verification), just finish here
                        self.ui.info("Registration complete. If your server requires email verification, complete it in the web UI, then /login.")
                        return True
                except Exception:
                    # Best-effort: finish registration without auto-login
                    self.ui.info("Registration complete. Run /login to sign in.")
                    return True
        except Exception as e:
            self.ui.warn(f"Registration not available: {e}\nUse the web: {web_url}")
            return False

    async def _login_with_retries(self, max_attempts: int = 3) -> bool:
        attempts = 0
        while attempts < max_attempts:
            ok, fatal = await self._login_once_allow_retry()
            if ok:
                return True
            if fatal:
                # do not retry
                break
            attempts += 1
            if attempts < max_attempts:
                # Menu-based retry choice instead of Y/N typing
                choice = await self._menu_choice(
                    "Login failed",
                    "Invalid username or password.",
                    [
                        ("retry", f"Try again ({attempts}/{max_attempts} attempts used)"),
                        ("stop", "Stop trying for now"),
                    ],
                )
                if choice != "retry":
                    break
        # Offer next steps via menu (register / login again / return)
        self.ui.print("Login not successful.")
        choice = await self._menu_choice(
            "Login not successful",
            "What would you like to do?",
            [
                ("register", "Register for an account"),
                ("login", "Try logging in again"),
                ("back", "Return to the previous menu"),
            ],
        )
        if choice == "register":
            await self.register()
            return False
        if choice == "login":
            return await self._login_with_retries(max_attempts)
        return False

    async def _login_once_allow_retry(self) -> Tuple[bool, bool]:
        """Perform a single login attempt. Returns (ok, fatal). Fatal means don't retry."""
        try:
            username = self.ui.prompt("Username")
            password = getpass.getpass("Password: ")
            # Menu-based choice instead of Y/N typing
            stay_choice = await self._menu_choice(
                "Stay logged in?",
                "Do you want to stay logged in on this machine (device-bound refresh tokens)?",
                [
                    ("yes", "Yes - keep me logged in"),
                    ("no", "No - only this session"),
                ],
            )
            stay_logged_in = (stay_choice != "no")
            if stay_logged_in and not self.device_id:
                try:
                    self._load_auth_state_from_disk()
                except Exception:
                    pass
                if not self.device_id:
                    self.device_id = uuid.uuid4().hex
            if self.timeout is None:
                http_timeout = httpx.Timeout(connect=10.0, read=None, write=10.0, pool=10.0)
            else:
                http_timeout = httpx.Timeout(self.timeout)
            async with httpx.AsyncClient(timeout=http_timeout, cookies=self.cookies) as client:
                body = {"username": username, "password": password, "remember_me": bool(stay_logged_in)}
                if stay_logged_in and self.device_id:
                    body.update({"device_id": self.device_id, "device_name": self.device_name or f"{socket.gethostname()} cli"})
                resp = await client.post(self.login_url, json=body)
                if resp.status_code >= 400:
                    raw_text = ""
                    try:
                        b = await resp.aread(); raw_text = b.decode("utf-8", errors="replace")
                    except Exception:
                        raw_text = resp.text
                    detail = None
                    try:
                        j = json.loads(raw_text) if raw_text else {}
                        if isinstance(j, dict):
                            detail = j.get("detail")
                    except Exception:
                        detail = None
                    if resp.status_code == 401 and isinstance(detail, str) and detail.lower() == "invalid username or password":
                        # Non-fatal invalid creds; allow retry
                        self.ui.warn("Invalid username or password.")
                        return False, False
                    self.ui.warn(f"Login failed: {resp.status_code} {raw_text}")
                    return False, False
                self.cookies.update(resp.cookies)
                try:
                    chk = await client.get(self.check_auth_url)
                    if chk.status_code == 200:
                        data = chk.json()
                        if data.get("authenticated"):
                            self.auth_user = str(data.get("user") or username)
                            self.ui.success(f"Login successful. Authenticated as: {self.auth_user}")
                            if stay_logged_in:
                                self._save_auth_state_to_disk()
                            else:
                                self._clear_auth_state_on_disk()
                            return True, True
                except Exception:
                    pass
                # Consider success if no check-auth
                self.ui.success("Login successful.")
                if stay_logged_in:
                    self._save_auth_state_to_disk()
                else:
                    self._clear_auth_state_on_disk()
                return True, True
        except Exception as e:
            self.ui.error(f"Login error: {e}")
            return False, True

    async def _wizard_model_step(self) -> None:
        """First-time wizard: pick the default model via the full picker."""
        self.ui.print("Please select a default model for new chats.")
        await self.select_model_menu()

    async def _wizard_agent_scope_step(self) -> None:
        """First-time wizard: choose Agent scope root and mode via menus.

        Only asks user to type when 'custom path' is selected.
        """
        try:
            cwd = os.getcwd()
        except Exception:
            cwd = ""

        # 1) Where should the Agent scope root live?
        scope_choices: List[Tuple[str, str]] = []
        if cwd:
            scope_choices.append(("cwd", f"Use current directory ({cwd}) as Agent scope"))
        scope_choices.append(("custom", "Enter a different absolute path"))
        scope_choices.append(("workspace-only", "Skip Agent scope; use workspace sandbox only"))

        scope_val = await self._menu_choice(
            "Agent scope root",
            "Choose where the agent is allowed to operate when host scope is enabled:",
            scope_choices,
        )

        chosen_scope_root: Optional[str] = None
        if scope_val == "cwd" and cwd:
            chosen_scope_root = cwd
        elif scope_val == "custom":
            # This is the only place we require typing for Agent scope.
            path = self.ui.prompt(
                "Enter absolute path for Agent scope (leave blank to cancel)",
                default=self.host_base or "",
            )
            if path.strip():
                chosen_scope_root = path.strip()
        elif scope_val == "workspace-only":
            chosen_scope_root = None  # handled below

        # Fallback: if still unset and cwd is available, use cwd
        if chosen_scope_root is None and cwd:
            chosen_scope_root = cwd

        if chosen_scope_root:
            self.host_base = chosen_scope_root
            self._host_base_ephemeral = False
        else:
            self.host_base = None

        # 2) How much of that directory is accessible?
        if self.host_base:
            # Full vs ./workspace inside that root
            scope_mode = await self._menu_choice(
                "Agent scope mode",
                (
                    "We recommend granting access to the entire Agent scope directory.\n"
                    "Alternatively, you can restrict access to a 'workspace' folder inside it."
                ),
                [
                    ("full", "Full Agent scope (recommended)"),
                    ("workspace", "Restrict to ./workspace subfolder inside Agent scope"),
                ],
            )
            if scope_mode == "workspace":
                try:
                    ws_path = os.path.join(self.host_base, "workspace")
                    os.makedirs(ws_path, exist_ok=True)
                    self.host_base = ws_path
                    self._host_base_ephemeral = False
                    self.fs_host_mode = "custom"
                    self.fs_scope = "host"
                    self.ui.info(f"Restricted Agent scope to workspace folder: {ws_path}")
                except Exception as e:
                    self.ui.warn(
                        f"Failed to prepare workspace folder; using full Agent scope. ({e})"
                    )
                    self.fs_host_mode = "custom"
                    self.fs_scope = "host"
            else:
                # full or cancel → treat as full Agent scope but constrained to that root
                self.fs_host_mode = "custom"
                self.fs_scope = "host"
        else:
            # No Agent scope root selected: default to workspace scope
            self.fs_scope = "workspace"

        # Refresh code map source based on the final host_base
        try:
            self._codebase_map_raw = self._load_codebase_map_raw()
        except Exception:
            pass

        self.save_settings()

    async def _maybe_run_first_time_wizard(self, force: bool = False) -> None:
        # Determine if key settings are at defaults
        needs = (
            (self.model is None)
            or (self.requested_tools is None)
            or (self.fs_scope is None)
            or (self.control_level is None)
            or (not self.host_base)
        )
        try:
            self.ui.debug_log(
                f"[wizard-cli] maybe_run_first_time_wizard force={force} needs={needs} "
                f"model={self.model!r} tools={self.requested_tools!r} fs_scope={self.fs_scope!r} "
                f"level={self.control_level!r} host_base={self.host_base!r}"
            )
        except Exception:
            pass
        if not force and not needs:
            return

        self.ui.header(
            "First-time setup",
            "We’ll configure a few defaults. You can change these later via /settings.",
        )

        # --- 1) Default model (menu, no Y/N) ---
        await self._wizard_model_step()

        # --- 2) Tools (always ON per design) ---
        self.requested_tools = True

        # --- 3) Control level (menu) ---
        self.ui.print(
            "Control levels: 1=read-only, 2=approval on write/exec, 3=no approvals"
        )
        await self.set_level_menu()
        if self.control_level not in (1, 2, 3):
            # Default to Level 2 if user aborted
            self.control_level = 2

        # --- 4) Agent scope (menus; only type on custom path) ---
        self.ui.print(
            "Agent scope is the local directory tree the agent can access when host scope is enabled."
        )
        await self._wizard_agent_scope_step()

        # --- 5) Code map injection & generation (menus) ---
        code_map_choice = await self._menu_choice(
            "Codebase map",
            (
                "CODEBASE_MAP.md is a short overview of your project that can be prefixed to "
                "your first message to help the agent understand the codebase."
            ),
            [
                (
                    "inject-generate",
                    "Inject the codebase map and generate CODEBASE_MAP.md now if missing (recommended)",
                ),
                (
                    "inject-only",
                    "Inject the codebase map when present, but do not auto-generate",
                ),
                ("off", "Do not inject CODEBASE_MAP.md"),
            ],
        )

        if code_map_choice == "off":
            self.inject_codebase_map = False
        else:
            self.inject_codebase_map = True
            # If we have an Agent scope and no map, optionally generate it now
            if (
                code_map_choice == "inject-generate"
                and self.host_base
                and not self._code_map_exists_at(self.host_base)
            ):
                # This is an action, not another question: user already selected it.
                await self._generate_code_map_for(self.host_base)

        # --- 6) Text verbosity (menu instead of free-typed low/medium/high) ---
        try:
            curv = (
                self.text_verbosity
                if isinstance(getattr(self, "text_verbosity", None), str)
                else "medium"
            )
        except Exception:
            curv = "medium"

        verb_choice = await self._menu_choice(
            "Text verbosity",
            "How verbose should responses be by default?",
            [
                ("low", "Low – short, to-the-point answers"),
                ("medium", "Medium – balanced detail (recommended)"),
                ("high", "High – more verbose explanations"),
            ],
        )
        if verb_choice in ("low", "medium", "high"):
            self.text_verbosity = verb_choice
        else:
            self.text_verbosity = curv or "medium"

        # --- 7) Tool preambles (menu) ---
        preamble_choice = await self._menu_choice(
            "Tool call preambles",
            "Before using tools, the agent can briefly explain what it will do and why (supported models only).",
            [
                ("on", "Enable preambles"),
                ("off", "Disable preambles (default)"),
            ],
        )
        self.preambles_enabled = preamble_choice == "on"

        # --- 8) Optional custom first-turn note (menu + text only when chosen) ---
        custom_choice = await self._menu_choice(
            "Custom first-turn note",
            "Optionally add a custom note that will be included in your first message.",
            [
                ("none", "No custom note"),
                ("add", "Add a custom note"),
            ],
        )
        if custom_choice == "add":
            self.custom_first_turn_enabled = True
            try:
                txt_default = (
                    self.custom_first_turn_text
                    if isinstance(self.custom_first_turn_text, str)
                    else ""
                )
            except Exception:
                txt_default = ""
            entered = self.ui.prompt(
                "Enter custom first-turn text (you can edit this later via /settings)",
                default=txt_default,
            )
            try:
                self.custom_first_turn_text = str(entered or "")
            except Exception:
                self.custom_first_turn_text = ""
            try:
                self._did_inject_custom_first_turn = False
            except Exception:
                pass
        else:
            self.custom_first_turn_enabled = False

        # --- 9) Default Usage & Info panel to concise on first setup ---
        try:
            self.usage_info_mode = "concise"
        except Exception:
            pass

        # Save settings to server
        await self._save_server_settings()

        # Refresh local code map source
        try:
            self._codebase_map_raw = self._load_codebase_map_raw()
        except Exception:
            pass



    # ----------------- Preflight token/cost estimation -----------------
    async def _preflight_estimate_and_confirm(self, user_input: str) -> bool:
        # Build a preview of the messages including code map injection WITHOUT mutating state
        msgs = self._build_messages_preview(user_input)
        model = self.model or "gpt-5"
        # Try Gemini token counter
        used_gemini = False
        tokens_in = 0
        try:
            api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
            if api_key:
                try:
                    import google.genai as genai  # type: ignore
                    client = genai.Client(api_key=api_key)
                    # Convert messages into a simple list of strings
                    contents = []
                    for m in msgs:
                        role = m.get("role", "user")
                        text = m.get("content", "")
                        contents.append({"role": role, "parts": [{"text": text}]})
                    # Pick a Gemini model for counting; fall back if current isn't Gemini
                    count_model = "gemini-2.5-pro"
                    res = client.models.count_tokens(model=count_model, contents=contents)
                    t = int(getattr(res, "total_tokens", 0) or 0)
                    if t > 0:
                        tokens_in = t
                        used_gemini = True
                except Exception:
                    used_gemini = False
        except Exception:
            used_gemini = False
        if not used_gemini:
            # Heuristic fallback: 1 token ~= 4 chars
            total_chars = 0
            try:
                for m in msgs:
                    total_chars += len(m.get("content", "") or "")
            except Exception:
                total_chars = len(user_input)
            tokens_in = max(1, int(round(total_chars / 4.0)))
        # Assume 30% additional output tokens
        tokens_out = int(round(tokens_in * 0.3))
        est_total = tokens_in + tokens_out
        price = self._resolve_price(model)
        cost = (tokens_in / 1_000_000.0) * float(price.get("input", 0.0)) + (tokens_out / 1_000_000.0) * float(price.get("output", 0.0))
        label = "Gemini token counter" if used_gemini else "heuristic estimator"
        choice = await self._menu_choice(
            "Estimated cost",
            f"Estimated cost: ${cost:.6f} (in {tokens_in} + out ~{tokens_out} = {est_total} tokens) via {label}.",
            [
                ("proceed", "Proceed with this request"),
                ("cancel", "Cancel"),
            ],
        )
        return choice == "proceed"

    def _build_messages_preview(self, user_input: str) -> List[Dict[str, str]]:
        msgs: List[Dict[str, str]] = []
        if self.system_prompt:
            msgs.append({"role": "system", "content": self.system_prompt})
        for msg in self.history:
            if msg["role"] != "system":
                msgs.append({"role": msg["role"], "content": msg["content"]})
        # Preview first-turn injections WITHOUT mutating state flags
        content = user_input
        blocks: List[str] = []
        # Codebase map (use loader directly; ignore _did_inject flag for preview)
        if self.inject_codebase_map:
            inj = self._build_codebase_injection(user_input)
            if inj:
                blocks.append(inj)
        # Custom first-turn text
        try:
            if bool(getattr(self, "custom_first_turn_enabled", False)):
                txt = getattr(self, "custom_first_turn_text", "") or ""
                if isinstance(txt, str) and txt.strip():
                    blocks.append(txt.strip())
        except Exception:
            pass
        # Tool preamble
        try:
            if bool(getattr(self, "preambles_enabled", False)):
                blocks.append(
                    "Tool usage: when you need to read or modify files or run commands, "
                    "explicitly explain why you're using a tool, what you'll do, and how it "
                    "advances the user's goal before calling the tool."
                )
        except Exception:
            pass
        # Working memory preview (does not touch _did_inject_working_memory or paths)
        try:
            if self._memory_paths_for_first_turn:
                wm_block = self._build_working_memory_injection()
                if wm_block:
                    blocks.append(wm_block)
        except Exception:
            pass
        if blocks:
            content = "\n\n".join(blocks + [user_input])
        msgs.append({"role": "user", "content": content})
        return msgs

    # ----------------------- Agent scope rebind ------------------------
    def _rebind_agent_scope_default(self) -> None:
        """Bind Agent scope to this terminal's CWD for the current session unless explicitly overridden.
        Avoid persisting this default to server settings.
        """
        try:
            # If user explicitly set a scope (via CLI flag or command), do nothing
            if self.host_base and not getattr(self, "_host_base_ephemeral", False):
                return
        except Exception:
            pass
        try:
            cwd = str(Path(os.getcwd()).resolve())
        except Exception:
            cwd = None
        if cwd:
            self.host_base = cwd
            self._host_base_ephemeral = True

    # ----------------------- Agent Mode (WS bridge) --------------------
    async def _start_ws_hub(self) -> None:
        if not HAS_WS:
            return
        # Bind host: in dev, default 127.0.0.1; guard remote if flag not set
        host = self.agent_host
        if not self.agent_allow_remote and host not in ("127.0.0.1", "localhost", "::1"):
            host = "127.0.0.1"
        # Start server and log explicit startup + diagnostics
        port_to_use = int(self.agent_port)
        # If requested port is in use, pick a free one
        if port_to_use > 0 and self._port_in_use(host, port_to_use):
            picked = self._find_free_port(host)
            if picked:
                port_to_use = picked
        # Try to serve; if it still fails, fallback to auto-pick
        # Provide a light HTTP response for non-WS requests to avoid scary tracebacks
        async def _ws_process_request(path, request_headers):  # type: ignore
            try:
                # Only accept /agent/ws (and trailing slash). Others -> 404
                if path not in ("/agent/ws", "/agent/ws/"):
                    body = b"404 Not Found: This port is a WebSocket endpoint for Agent Mode. Use ws://HOST:PORT/agent/ws.\n"
                    return 404, [("Content-Type", "text/plain; charset=utf-8"), ("Content-Length", str(len(body)))], body
                # Check Upgrade header; if missing, guide the user
                up = (request_headers.get("Upgrade") or request_headers.get("upgrade") or "").lower()
                if up != "websocket":
                    body = (
                        b"426 Upgrade Required\n\n"
                        b"This endpoint expects a WebSocket (Agent Mode).\n"
                        b"Use a WS client or the Henosis UI.\n"
                        b"Path: /agent/ws\n"
                    )
                    return 426, [("Content-Type", "text/plain; charset=utf-8"), ("Content-Length", str(len(body)))], body
            except Exception:
                # On any unexpected issue, let websockets proceed with the normal handshake
                return None  # type: ignore
            return None  # Continue with normal WS handshake

        try:
            # Try to pass process_request, and silence internal error logs if supported
            try:
                self._ws_server = await websockets.serve(self._ws_handler, host, port_to_use, process_request=_ws_process_request, logger=None)  # type: ignore
            except TypeError:
                # Older versions may not support logger or process_request
                self._ws_server = await websockets.serve(self._ws_handler, host, port_to_use)  # type: ignore
        except OSError:
            # Last-resort auto-pick
            picked = self._find_free_port(host)
            port_to_use = picked or 0
            try:
                self._ws_server = await websockets.serve(self._ws_handler, host, port_to_use, process_request=_ws_process_request, logger=None)  # type: ignore
            except TypeError:
                self._ws_server = await websockets.serve(self._ws_handler, host, port_to_use)  # type: ignore
        # Update actual bound port if OS picked one
        try:
            if hasattr(self._ws_server, "sockets") and self._ws_server.sockets:
                sock = self._ws_server.sockets[0]
                actual = sock.getsockname()[1]
                self.agent_port = int(actual)
            else:
                self.agent_port = int(port_to_use)
        except Exception:
            self.agent_port = int(port_to_use)
        try:
            self.ui.print(
                f"[agent] WS hub started on ws://{host}:{int(self.agent_port)}/agent/ws (allow_remote={self.agent_allow_remote})",
                style=self.ui.theme["dim"],
            )
            # Friendly hint for folks who open the port in a browser
            self.ui.print(
                "[agent] Note: Opening this URL in a browser will show 'Upgrade Required'. "
                "Use a WebSocket client (the Henosis UI connects automatically).",
                style=self.ui.theme["dim"],
            )
        except Exception:
            pass

    def _ws_is_open(self, ws: Optional[Any]) -> bool:
        """Best-effort cross-version check for websockets connection open state.
        Supports legacy WebSocketServerProtocol (v9/v10) and new ServerConnection (v11+)."""
        try:
            if ws is None:
                return False
            # websockets >= 11 exposes a state enum; prefer that when available
            state = getattr(ws, "state", None)
            if state is not None:
                try:
                    # Enum with .name, e.g., OPEN, CLOSING, CLOSED
                    name = getattr(state, "name", None)
                    if isinstance(name, str):
                        return name.upper() == "OPEN"
                except Exception:
                    pass
                # Some variants expose state as a string
                if isinstance(state, str):
                    return state.upper() == "OPEN"
            # Older versions exposed .open boolean
            open_attr = getattr(ws, "open", None)
            if isinstance(open_attr, bool):
                return open_attr
            # Fallback to .closed boolean (True when closed)
            closed_attr = getattr(ws, "closed", None)
            if isinstance(closed_attr, bool):
                return not closed_attr
            # As a last resort, assume open (send will raise if not)
            return True
        except Exception:
            return False

    async def _ws_handler(self, websocket: WebSocketServerProtocol, path: Optional[str] = None) -> None:
        """
        WebSocket connection handler for Agent Mode.
        Compatible with websockets v9/v10 (handler(websocket, path)) and v11+ (handler(websocket)).
        """
        # Derive path for websockets >= 11 where only (websocket) is passed
        if path is None:
            try:
                path = getattr(websocket, "path", None)
            except Exception:
                path = None
            # Try websockets >=11 request object
            if path is None:
                try:
                    request = getattr(websocket, "request", None)
                    if request is not None:
                        path = getattr(request, "path", None)
                except Exception:
                    path = None
        # Log early handshake info for diagnostics
        try:
            ra = getattr(websocket, "remote_address", None)
            ha = getattr(websocket, "host", None)
            self.ui.print(
                f"[agent] incoming connection remote={ra} path={path} host_hdr={ha}",
                style=self.ui.theme["dim"],
            )
        except Exception:
            pass
        # Restrict to /agent/ws
        # Allow default when path can't be determined
        chk_path = path or "/agent/ws"
        # Be forgiving in dev: accept '/', '' as well as canonical '/agent/ws'
        allowed_paths = ("/agent/ws", "/agent/ws/", "/", "")
        if chk_path not in allowed_paths:
            try:
                # Send a short error frame before closing for easier debugging in browser
                await websocket.send(json.dumps({"type": "error", "data": {"message": f"Invalid WS path '{chk_path}'. Expected '/agent/ws'"}}))
            except Exception:
                pass
            try:
                await websocket.close(code=1008, reason="Invalid path")
            except Exception:
                pass
            return
        # Warn if a non-canonical but accepted path is used (helps spot misconfig)
        if chk_path in ("/", ""):
            try:
                await websocket.send(json.dumps({"type": "warning", "data": {"message": "Connected on '/' – prefer '/agent/ws' to avoid path checks in production."}}))
            except Exception:
                pass
        # Single-client policy: replace old with new
        async with self._ws_client_lock:
            if self._ws_is_open(self._ws_client):
                try:
                    await self._ws_client.close(code=1000, reason="Replaced by new connection")
                except Exception:
                    pass
            self._ws_client = websocket
        # Log connection
        try:
            ra = getattr(websocket, 'remote_address', None)
            self.ui.print(f"[agent] client connected {ra}", style=self.ui.theme["dim"])  # type: ignore
        except Exception:
            pass
        # Notify connected state
        await self._ws_send({"type": "state.connected", "data": {"connected": True}})
        # If a turn is already in progress, replay state so the UI can catch up
        try:
            if self._busy and self._current_turn.get("active"):
                await self._ws_broadcast("state.busy", {"busy": True})
                sess_id = self._current_turn.get("session_id")
                if sess_id is not None:
                    await self._ws_broadcast("session.started", {"session_id": sess_id})
                # Replay prior tool events
                for ev in self._current_turn.get("tool_events", []) or []:
                    await self._ws_broadcast(str(ev.get("type")), ev.get("data") or {})
                # Send snapshot of assistant text so far
                so_far = self._current_turn.get("assistant_so_far") or ""
                if so_far:
                    await self._ws_broadcast("message.sync", {"text": so_far, "model": self._current_turn.get("model")})
        except Exception:
            pass
        try:
            async for raw in websocket:
                try:
                    msg = json.loads(raw)
                except Exception:
                    await self._ws_send({"type": "error", "data": {"message": "Invalid JSON"}})
                    continue
                try:
                    await self._on_ws_message(msg)
                except httpx.HTTPStatusError as he:
                    # Surface backend HTTP errors to the WS client and continue serving
                    body = ""
                    try:
                        await he.response.aread()
                        body = he.response.text
                    except Exception:
                        pass
                    await self._ws_send({"type": "error", "data": {"message": f"HTTP {he.response.status_code} from {self.stream_url}: {body[:4000]}"}})
                except Exception as e:
                    await self._ws_send({"type": "error", "data": {"message": str(e)}})
                    # Keep the loop alive; don't crash the WS connection
                    continue
        except Exception as e:
            # Log unexpected errors during WS loop, but downgrade common close noise
            try:
                closed_err = None
                try:
                    # Detect common closure exceptions without importing types at top level
                    ConnectionClosedError = getattr(websockets.exceptions, "ConnectionClosedError", None) if HAS_WS else None
                    ConnectionClosedOK = getattr(websockets.exceptions, "ConnectionClosedOK", None) if HAS_WS else None
                    if (ConnectionClosedError and isinstance(e, ConnectionClosedError)) or (ConnectionClosedOK and isinstance(e, ConnectionClosedOK)):
                        closed_err = e
                except Exception:
                    closed_err = None
                if closed_err is not None:
                    self.ui.print(
                        "[agent] WebSocket closed by client (no close frame or early disconnect). "
                        "This often happens if a browser hits the WS port directly or the client reloads.",
                        style=self.ui.theme["dim"],
                    )
                else:
                    self.ui.warn(f"[agent] WS handler error: {e}")
            except Exception:
                pass
        finally:
            async with self._ws_client_lock:
                if self._ws_client is websocket:
                    self._ws_client = None
            # Notify disconnected
            try:
                await self._ws_send({"type": "state.connected", "data": {"connected": False}})
            except Exception:
                pass
            # Log disconnection
            try:
                self.ui.print("[agent] client disconnected", style=self.ui.theme["dim"])  # type: ignore
            except Exception:
                pass

    async def _ws_send(self, obj: Dict[str, Any]) -> None:
        if not self._ws_is_open(self._ws_client):
            return
        try:
            await self._ws_client.send(json.dumps(obj, ensure_ascii=False))
        except Exception:
            pass

    async def _ws_broadcast(self, typ: str, data: Dict[str, Any]) -> None:
        await self._ws_send({"type": typ, "data": data or {}})

    async def _on_ws_message(self, msg: Dict[str, Any]) -> None:
        mtype = str(msg.get("type") or "")
        data = msg.get("data", {}) or {}
        # Lightweight ping for connectivity checks (e.g., wscat -x '{"type":"ping"}')
        if mtype == "ping":
            try:
                await self._ws_broadcast("pong", {"ts": time.time()})
            except Exception:
                pass
            return
        if mtype == "user.send":
            # Busy check
            if self._busy:
                await self._ws_broadcast("state.busy", {"busy": True, "reason": "turn in progress"})
                return
            text = data.get("text")
            # Optional direct fields to override settings
            if "model" in data:
                self.model = data.get("model") or self.model
            if "enable_tools" in data:
                val = data.get("enable_tools")
                if isinstance(val, bool):
                    self.requested_tools = val
            if "tool_mode" in data:
                # backwards compat: ANY->True, NONE->False, AUTO->None
                tm = str(data.get("tool_mode") or "").upper()
                if tm == "ANY":
                    self.requested_tools = True
                elif tm == "NONE":
                    self.requested_tools = False
                elif tm == "AUTO":
                    self.requested_tools = None
            if "level" in data:
                try:
                    lvl = int(data.get("level"))
                    if lvl in (1, 2, 3):
                        self.control_level = lvl
                except Exception:
                    pass
            if "fs_scope" in data:
                fs = data.get("fs_scope")
                if fs in ("workspace", "host"):
                    self.fs_scope = fs
            if "auto_approve" in data and isinstance(data.get("auto_approve"), list):
                try:
                    self.auto_approve = [str(x) for x in data.get("auto_approve") if isinstance(x, str)]
                except Exception:
                    pass
            # Start turn
            if not isinstance(text, str) or not text.strip():
                await self._ws_broadcast("error", {"message": "user.send requires 'text'"})
                return
            # Log + run
            if self.save_chat_history:
                self.messages_for_save.append({
                    "role": "user",
                    "content": text,
                    "model": None,
                    "citations": None,
                    "last_turn_input_tokens": 0,
                    "last_turn_output_tokens": 0,
                    "last_turn_total_tokens": 0,
                })
            self._log_line({"event": "user.ws", "content": text})
            self._busy = True
            try:
                assistant_text = ""
                try:
                    assistant_text = await self._stream_once(text)
                except httpx.HTTPStatusError as he:
                    body = ""
                    try:
                        await he.response.aread()
                        body = he.response.text
                    except Exception:
                        pass
                    await self._ws_broadcast("error", {"message": f"HTTP {he.response.status_code} from {self.stream_url}: {body[:4000]}"})
                except Exception as e:
                    await self._ws_broadcast("error", {"message": str(e)})
            finally:
                self._busy = False
            # Mirror CLI run() history behavior so first-turn injections are preserved across WS turns
            try:
                if isinstance(assistant_text, str) and assistant_text.strip():
                    content_sent = self._last_built_user_content or text
                    self.history.append({"role": "user", "content": content_sent})
                    self.history.append({"role": "assistant", "content": assistant_text})
            except Exception:
                pass
        elif mtype == "approval.reply":
            call_id = str(data.get("call_id")) if data.get("call_id") is not None else None
            approve = bool(data.get("approve")) if ("approve" in data) else None
            note = data.get("note")
            if call_id and call_id in self._pending_approvals:
                fut = self._pending_approvals.get(call_id)
                if fut and not fut.done() and (approve is not None):
                    try:
                        fut.set_result((bool(approve), note))
                    except Exception:
                        pass
        elif mtype == "control.set":
            key = str(data.get("key") or "")
            val = data.get("value")
            if key == "model":
                self.model = str(val) if val else None
            elif key == "enable_tools":
                if isinstance(val, bool):
                    self.requested_tools = val
            elif key == "level":
                try:
                    lvl = int(val)
                    if lvl in (1, 2, 3):
                        self.control_level = lvl
                except Exception:
                    pass
            elif key == "fs_scope":
                if val in ("workspace", "host"):
                    self.fs_scope = val
            # No explicit ack needed
        else:
            await self._ws_broadcast("warning", {"message": f"Unknown inbound type: {mtype}"})

    # Handle approval request: first reply wins (web or CLI), then POST to server
    async def _handle_approval_request(self, client: httpx.AsyncClient, session_id: Optional[str], data: Dict[str, Any]) -> None:
        tool = str(data.get("tool"))
        call_id = data.get("call_id")
        args_prev = data.get("args_preview", {}) or {}
        timeout_sec = int(data.get("timeout_sec", 60) or 60)
        # Display summary
        self.ui.print(f"⚠ Approval requested for {tool} (call_id={call_id})", style=self.ui.theme["warn"])
        self.ui.print(truncate_json(args_prev, 600), style=self.ui.theme["dim"])
        # Broadcast to web client
        try:
            await self._ws_broadcast("approval.request", {
                "session_id": session_id,
                "call_id": call_id,
                "tool": tool,
                "args_preview": args_prev,
                "level": data.get("level"),
                "timeout_sec": timeout_sec,
                "note": data.get("note"),
            })
        except Exception:
            pass

        # Create a future to capture decision
        fut: asyncio.Future = asyncio.get_event_loop().create_future()
        if call_id is not None:
            self._pending_approvals[str(call_id)] = fut

        # Run blocking CLI prompt in thread to avoid blocking event loop
        loop = asyncio.get_event_loop()
        def prompt_cli() -> Tuple[bool, str]:
            try:
                # For context.summarize, recommend approval by default to avoid overflow
                default_yes = True if str(tool).strip() == "context.summarize" else False
                approved = self.ui.confirm(f"Approve this action? (timeout in {timeout_sec}s)", default=default_yes)
                return bool(approved), ("Approved via CLI" if approved else "Denied via CLI")
            except Exception:
                return False, "Denied via CLI (error)"

        cli_task = loop.run_in_executor(None, prompt_cli)

        decided: Optional[Tuple[bool, Optional[str]]] = None
        try:
            done, pending = await asyncio.wait({fut, asyncio.ensure_future(cli_task)}, timeout=timeout_sec, return_when=asyncio.FIRST_COMPLETED)
            if fut in done and not fut.cancelled():
                try:
                    decided = fut.result()
                except Exception:
                    decided = (False, "Denied via Web (error)")
            elif cli_task in done:  # type: ignore
                try:
                    decided = await cli_task  # type: ignore
                except Exception:
                    decided = (False, "Denied via CLI (error)")
                # If web future not decided, set it so we can cleanly proceed
                if not fut.done():
                    try:
                        fut.set_result(decided)
                    except Exception:
                        pass
            else:
                # Timeout
                decided = (False, "Timed out")
                if not fut.done():
                    try:
                        fut.set_result(decided)
                    except Exception:
                        pass
        finally:
            # Cleanup pending dict
            if call_id is not None:
                self._pending_approvals.pop(str(call_id), None)

        approved, note = decided if decided is not None else (False, "")
        # Post decision to server
        if session_id:
            try:
                payload = {
                    "session_id": session_id,
                    "call_id": call_id,
                    "approve": bool(approved),
                    "note": note,
                }
                r = await client.post(self.approvals_url, json=payload, timeout=self.timeout)
                if r.status_code >= 400:
                    self.ui.warn(f"Approval POST failed: {r.status_code} {r.text}")
            except Exception as e:
                self.ui.warn(f"Approval POST error: {e}")
async def amain():
    args = build_arg_parser().parse_args()
    # Set global debug flags from args
    global DEBUG_SSE, DEBUG_REQ
    DEBUG_SSE = bool(getattr(args, 'debug_sse', False))
    DEBUG_REQ = bool(getattr(args, 'debug_req', False))
    # Resolve server base, honoring --dev shortcut
    server_base = getattr(args, 'server', None) or os.getenv("HENOSIS_SERVER", "https://henosis.us/api_v2")
    if getattr(args, 'use_dev', False):
        server_base = os.getenv("HENOSIS_DEV_SERVER", "http://127.0.0.1:8000/api")
    cli = ChatCLI(
        server=server_base,
        model=args.model,
        system_prompt=args.system,
        timeout=args.timeout,
        map_prefix=args.map_prefix,
        verbose=getattr(args, 'verbose', False),
        # Force logging + saving + usage commit by default; no flags needed
        log_enabled=True,
        log_dir=None,
        ctx_window=None,
        save_to_threads=True,
        server_usage_commit=True,
        title=getattr(args, 'title', None),
        # Raw log capture
        raw_log=getattr(args, 'raw_log', False) or (os.getenv('HENOSIS_RAW_LOG', '').strip().lower() in ('1','true','yes','on')),
        raw_log_file=getattr(args, 'raw_log_file', None),
        # Agent Mode flags
        agent_mode=getattr(args, 'agent_mode', False),
        agent_host=getattr(args, 'agent_host', '127.0.0.1'),
        agent_port=getattr(args, 'agent_port', 8700),
        agent_allow_remote=getattr(args, 'agent_allow_remote', False),
        # Multi-terminal
        workspace_dir=getattr(args, 'workspace_dir', None),
        terminal_id=getattr(args, 'terminal_id', None),
        agent_scope=getattr(args, 'agent_scope', None),
    )
    # Handle whoami
    if getattr(args, 'whoami', False):
        authed = await cli.check_auth()
        if authed:
            cli.ui.success(f"Authenticated as: {cli.auth_user}")
        else:
            cli.ui.warn("Not authenticated.")
        return
    # Handle reset-config (local only)
    if getattr(args, 'reset_config', False):
        try:
            if cli.settings_file.exists():
                cli.settings_file.unlink()
                cli.ui.success("Local CLI settings cleared. On next run, onboarding will trigger.")
            else:
                cli.ui.info("No local CLI settings file found.")
        except Exception as e:
            cli.ui.warn(f"Failed to clear settings: {e}")
        # Continue to run (wizard will likely trigger)
    # Version checks (non-fatal, quick)
    if not getattr(args, 'no_update_check', False) and os.getenv("HENOSIS_CLI_NO_UPDATE_CHECK", "") not in ("1", "true", "yes"):
        try:
            # Server compatibility first (uses /health)
            await cli.check_server_version_compatibility()
        except SystemExit:
            raise
        except Exception:
            pass
        try:
            # PyPI latest
            await cli.maybe_check_for_updates()
        except SystemExit:
            raise
        except Exception:
            pass
    await cli.run()


# --- UX Hotfix: Replace menu UI with highlighted cursor picker (no radio buttons) ---
# The default RadioList menu can be confusing and, on some terminals, non-interactive.
# We override ChatCLI._menu_choice at runtime with a prompt_toolkit-based list that shows
# a highlighted bar for the current item; Enter selects; Esc cancels. Falls back to
# numeric selection when prompt_toolkit is unavailable.

async def _menu_choice_highlight(self, title: str, text: str, choices: list[tuple[str, str]]):  # type: ignore
    if HAS_PT and Application and Layout and HSplit and Window and FormattedTextControl and Style and KeyBindings:
        try:
            items = [(val, str(label)) for (val, label) in choices]
            index = 0
            blink_on = [True]

            def _lines():
                out = []
                if title:
                    out.append(("class:menu.title", f"{title}\n"))
                for i, (_v, _lbl) in enumerate(items):
                    if i == index:
                        arrow = ">" if blink_on[0] else " "
                        out.append(("class:menu.item.selected", f" {arrow} {_lbl}\n"))
                    else:
                        out.append(("class:menu.item", f"   {_lbl}\n"))
                out.append(("class:menu.status", f"({index+1}/{len(items)})"))
                return out

            body = FormattedTextControl(_lines)
            hint = FormattedTextControl(lambda: text or "Use ↑/↓, Enter=select, Esc=cancel")
            root = HSplit([
                Window(height=1, content=hint, style="class:menu.hint"),
                Window(content=body),
            ])
            kb = KeyBindings()

            @kb.add("up")
            def _up(event):
                nonlocal index
                index = (index - 1) % len(items)
                event.app.invalidate()

            @kb.add("down")
            def _down(event):
                nonlocal index
                index = (index + 1) % len(items)
                event.app.invalidate()

            @kb.add("pageup")
            def _pgup(event):
                nonlocal index
                index = max(0, index - 7)
                event.app.invalidate()

            @kb.add("pagedown")
            def _pgdn(event):
                nonlocal index
                index = min(len(items) - 1, index + 7)
                event.app.invalidate()

            @kb.add("home")
            def _home(event):
                nonlocal index
                index = 0
                event.app.invalidate()

            @kb.add("end")
            def _end(event):
                nonlocal index
                index = len(items) - 1
                event.app.invalidate()

            @kb.add("enter")
            def _enter(event):
                event.app.exit(result=items[index][0])

            @kb.add("escape")
            def _esc(event):
                event.app.exit(result=None)

            style = Style.from_dict({
                "menu.title": "bold",
                "menu.hint": "fg:#888888",
                "menu.status": "fg:#ff8700",
                "menu.item": "",
                # Bright highlighted selection; blink may be ignored on some terminals
                "menu.item.selected": "fg:#ff8700 reverse",
            })

            app = Application(layout=Layout(root), key_bindings=kb, style=style, full_screen=False)

            async def _blinker():
                while True:
                    await asyncio.sleep(0.6)
                    try:
                        blink_on[0] = not blink_on[0]
                        get_app().invalidate()
                    except Exception:
                        break

            try:
                asyncio.create_task(_blinker())
            except Exception:
                pass

            return await app.run_async()
        except Exception:
            pass
    # Fallback: numeric list
    self.ui.header(title, text)
    for i, (_, label) in enumerate(choices, start=1):
        style = None
        try:
            lbl = str(label)
            if ("VERY expensive" in lbl) or ("[DANGER]" in lbl) or ("!!!" in lbl and "expensive" in lbl.lower()):
                style = self.ui.theme.get("err")
        except Exception:
            style = None
        self.ui.print(f"{i}. {label}", style=style)
    self.ui.print()
    while True:
        raw = input("Choose an option: ").strip()
        if raw.lower() in ("q", "quit", "exit"):
            return None
        if not raw.isdigit():
            self.ui.warn("Enter a number from the list.")
            continue
        idx = int(raw)
        if not (1 <= idx <= len(choices)):
            self.ui.warn("Invalid selection.")
            continue
        return choices[idx - 1][0]

# Monkey-patch the method onto ChatCLI
try:
    ChatCLI._menu_choice = _menu_choice_highlight  # type: ignore[attr-defined]
except Exception:
    pass

# --- UX Hotfix v2: dependency-free highlighted menus (Enter selects) ---
# This override ensures the settings menu works without RadioList and that Enter
# activates the currently highlighted option even when prompt_toolkit is absent.

def _hn_supports_tty_io_v2() -> bool:
    """Best-effort check for whether arrow-key TTY interaction is likely to work.

    On Windows, many environments misreport TTY capabilities; the `msvcrt` path we
    use for key handling works even when `isatty()` is False (e.g., some
    PowerShell / VS Code terminals). To avoid silently degrading to the numeric
    menu there, we treat Windows as TTY-capable by default and let the
    lower-level key reader decide.

    On POSIX we still respect isatty() to avoid breaking when stdin/stdout are
    redirected (e.g., piping input from a file).
    """
    try:
        # On Windows, assume interactive capabilities and fall back to numeric
        # selection only if key-reading actually fails.
        if os.name == "nt":
            return True
        return sys.stdin.isatty() and sys.stdout.isatty()
    except Exception:
        return False

def _hn_clear_screen_v2() -> None:
    try:
        sys.stdout.write("\x1b[2J\x1b[H")
        sys.stdout.flush()
    except Exception:
        try:
            os.system("cls" if os.name == "nt" else "clear")
        except Exception:
            pass

def _hn_read_key_win_v2():
    try:
        import msvcrt  # type: ignore
    except Exception:
        return None
    while True:
        ch = msvcrt.getwch()
        if ch in ("\x00", "\xe0"):
            code = msvcrt.getwch()
            mapping = {"H": "UP", "P": "DOWN", "I": "PGUP", "Q": "PGDN", "G": "HOME", "O": "END"}
            return mapping.get(code, None)
        if ch == "\r":
            return "ENTER"
        if ch == "\x1b":
            return "ESC"
        if ch.isprintable():
            return ch

def _hn_read_key_posix_v2(fd):
    import termios, tty, select, os as _os
    old = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        while True:
            r, _, _ = select.select([fd], [], [], 0.5)
            if fd not in r:
                continue
            ch = _os.read(fd, 1)
            if not ch:
                continue
            c = ch.decode(errors="ignore")
            if c == "\x1b":
                seq = _os.read(fd, 2).decode(errors="ignore")
                if seq.startswith("["):
                    rest = seq[1:]
                    if rest and rest[0] in ("A", "B", "H", "F"):
                        return {"A": "UP", "B": "DOWN", "H": "HOME", "F": "END"}[rest[0]]
                    more = _os.read(fd, 2).decode(errors="ignore")
                    if more.startswith("5~"):
                        return "PGUP"
                    if more.startswith("6~"):
                        return "PGDN"
                else:
                    return "ESC"
                continue
            if c in ("\r", "\n"):
                return "ENTER"
            if c.isprintable():
                return c
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

def _hn_read_key_v2():
    if os.name == "nt":
        try:
            return _hn_read_key_win_v2()
        except Exception:
            return None
    try:
        return _hn_read_key_posix_v2(sys.stdin.fileno())
    except Exception:
        return None

def _hn_render_menu_v2(ui: UI, title: str, text: str, labels: list[str], index: int) -> None:
    _hn_clear_screen_v2()
    ui.header(title, text)
    for i, lbl in enumerate(labels):
        selected = (i == index)
        style = None
        try:
            if ("VERY expensive" in lbl) or ("[DANGER]" in lbl) or ("!!!" in lbl and "expensive" in lbl.lower()):
                style = ui.theme.get("err")
        except Exception:
            style = None
        if selected:
            # Orange selector caret to match CLI project accent color
            try:
                ui.print(" >", style=ui.theme.get("subtitle"), end="")
                ui.print(f" {lbl}", style=style)
            except Exception:
                # Fallback single-line when segmented printing fails
                ui.print(f" > {lbl}", style=style)
        else:
            ui.print(f"   {lbl}", style=style)
    ui.print("\nUp/Down to move • Enter to select • Esc to cancel • 1-9 to jump")

async def _menu_choice_highlight_v2(self, title: str, text: str, choices: list[tuple[str, str]]):  # type: ignore
    # Debug: log which implementation path we're about to use
    try:
        self.ui.debug_log(
            f"[menu-cli] _menu_choice_highlight_v2 start title={title!r} choices={len(choices)} "
            f"HAS_PT={HAS_PT} HAS_RICH={HAS_RICH}"
        )
    except Exception:
        pass

    # prompt_toolkit path (no RadioList), if available
    if HAS_PT and Application and Layout and HSplit and Window and FormattedTextControl and Style and KeyBindings:
        try:
            items = [(val, str(label)) for (val, label) in choices]
            index = 0

            def _lines():
                out = []
                if title:
                    out.append(("class:menu.title", f"{title}\n"))
                hint = text or "Use \u2191/\u2193, Enter=select, Esc=cancel"
                out.append(("class:menu.hint", hint + "\n"))
                for i, (_v, _lbl) in enumerate(items):
                    if i == index:
                        out.append(("class:menu.item.selected", f"> {_lbl}\n"))
                    else:
                        out.append(("class:menu.item", f"  {_lbl}\n"))
                return out

            root = HSplit([Window(content=FormattedTextControl(_lines))])
            kb = KeyBindings()

            @kb.add("up")
            def _up(event):
                nonlocal index
                index = (index - 1) % len(items)

            @kb.add("down")
            def _down(event):
                nonlocal index
                index = (index + 1) % len(items)

            @kb.add("enter")
            def _enter(event):
                event.app.exit(result=items[index][0])

            @kb.add("escape")
            def _esc(event):
                event.app.exit(result=None)

            style = Style.from_dict(
                {
                    "menu.title": "bold",
                    "menu.hint": "fg:#888888",
                    "menu.item.selected": "fg:#ff8700 reverse",
                }
            )
            app = Application(
                layout=Layout(root),
                key_bindings=kb,
                style=style,
                full_screen=False,
            )
            try:
                self.ui.debug_log("[menu-cli] using prompt_toolkit highlight menu (v2)")
            except Exception:
                pass
            return await app.run_async()
        except Exception as e:
            # Log and fall through to dependency-free path
            try:
                self.ui.debug_log(f"[menu-cli] prompt_toolkit path failed: {e}")
            except Exception:
                pass

    # Pure-stdin fallback (dependency-free) with arrow-key support
    labels = [str(lbl) for (_v, lbl) in choices]
    index = 0
    try:
        self.ui.debug_log(
            f"[menu-cli] using dependency-free highlight fallback; labels={labels}"
        )
    except Exception:
        pass
    _hn_render_menu_v2(self.ui, title, text, labels, index)
    while True:
        key = _hn_read_key_v2()
        try:
            self.ui.debug_log(f"[menu-cli] key={key!r} index={index}")
        except Exception:
            pass
        if key is None:
            # numeric fallback
            self.ui.print("\nNumeric selection fallback.")
            try:
                self.ui.debug_log("[menu-cli] entering numeric fallback path")
            except Exception:
                pass
            for i, lbl in enumerate(labels, start=1):
                self.ui.print(f"{i}. {lbl}")
            while True:
                raw = input("Choose an option: ").strip()
                if raw.lower() in ("q", "quit", "exit"):
                    return None
                if raw.isdigit():
                    idx = int(raw)
                    if 1 <= idx <= len(choices):
                        return choices[idx - 1][0]
                self.ui.warn("Enter a number from the list.")
        elif key == "UP":
            index = (index - 1) % len(labels)
            _hn_render_menu_v2(self.ui, title, text, labels, index)
        elif key == "DOWN":
            index = (index + 1) % len(labels)
            _hn_render_menu_v2(self.ui, title, text, labels, index)
        elif key == "PGUP":
            index = max(0, index - 7)
            _hn_render_menu_v2(self.ui, title, text, labels, index)
        elif key == "PGDN":
            index = min(len(labels) - 1, index + 7)
            _hn_render_menu_v2(self.ui, title, text, labels, index)
        elif key == "HOME":
            index = 0
            _hn_render_menu_v2(self.ui, title, text, labels, index)
        elif key == "END":
            index = len(labels) - 1
            _hn_render_menu_v2(self.ui, title, text, labels, index)
        elif key == "ENTER":
            try:
                self.ui.debug_log(f"[menu-cli] ENTER on index={index} -> value={choices[index][0]!r}")
            except Exception:
                pass
            return choices[index][0]
        elif key == "ESC":
            try:
                self.ui.debug_log("[menu-cli] ESC -> cancel (None)")
            except Exception:
                pass
            return None
        elif isinstance(key, str) and key.isdigit():
            k = int(key)
            if 1 <= k <= len(labels):
                index = k - 1
                _hn_render_menu_v2(self.ui, title, text, labels, index)

# Override the menu chooser with the dependency-free version
try:
    ChatCLI._menu_choice = _menu_choice_highlight_v2  # type: ignore[attr-defined]
except Exception:
    pass

if __name__ == "__main__":
    try:
        asyncio.run(amain())
    except KeyboardInterrupt:
        print("\nInterrupted.")

# Entry point for console_scripts
def main() -> None:
    try:
        asyncio.run(amain())
    except KeyboardInterrupt:
        print("\nInterrupted.")
