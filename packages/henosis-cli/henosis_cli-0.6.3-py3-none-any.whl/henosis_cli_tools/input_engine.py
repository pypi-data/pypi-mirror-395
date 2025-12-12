"""
Cross-platform line editor for henosis-cli with Shift+Enter newlines when possible.

Goals
- Windows: True Shift+Enter via Win32 console key events (ctypes).
- POSIX: Try to enable modern terminal keyboard protocols (kitty CSI u and
  xterm modifyOtherKeys). Calibrate whether Shift+Enter is distinguishable; if
  not, fall back to Ctrl+J for newline.

Design
- Blocking read_message(prompt_label, cont_label) that returns the composed
  message when Enter is pressed (without Shift). Raises KeyboardInterrupt on
  Ctrl+C. Minimal editing: printable chars, backspace, newline insertion, and
  submit.
- Rendering: simple echo to stdout; on newline we DO NOT prefix continuation
  lines with any label (no "..." prefixes). We do not implement full cursor
  navigation.

Limitations
- Arrow keys and other navigation keys are ignored (no-op).
"""
from __future__ import annotations

import os
import sys
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class EngineInfo:
    supports_shift_enter: bool
    hint: str
    fallback_key_name: Optional[str] = None  # e.g., "Ctrl+J" when shift not available


class BaseInputEngine:
    def __init__(self) -> None:
        self.info = EngineInfo(supports_shift_enter=False, hint="Enter sends; Ctrl+J inserts a newline.", fallback_key_name="Ctrl+J")

    def read_message(self, prompt_label: str = "\nYou: ", cont_label: str = "... ") -> str:
        raise NotImplementedError


def _is_tty() -> bool:
    try:
        return sys.stdin.isatty() and sys.stdout.isatty()
    except Exception:
        return False


class WindowsKeyEngine(BaseInputEngine):
    def __init__(self) -> None:
        super().__init__()
        import ctypes, msvcrt  # local imports
        self.ctypes = ctypes
        self.msvcrt = msvcrt
        self.user32 = ctypes.windll.user32  # type: ignore[attr-defined]
        self.VK_SHIFT = 0x10
        # Windows supports detecting Shift reliably
        self.info = EngineInfo(supports_shift_enter=True, hint="Shift+Enter inserts a newline; Enter sends.")
        # Best-effort: enable ANSI escape processing so we can move the cursor
        try:
            kernel32 = ctypes.windll.kernel32
            STD_OUTPUT_HANDLE = -11
            handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
            mode = ctypes.c_uint()
            if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
                new_mode = mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING
                kernel32.SetConsoleMode(handle, new_mode)
        except Exception:
            pass

    def read_message(self, prompt_label: str = "\nYou: ", cont_label: str = "... ") -> str:
        buf: list[str] = []
        # Visible prompt is the part after the last newline in the label
        try:
            visible_prompt_len = len(prompt_label.rsplit("\n", 1)[-1])
        except Exception:
            visible_prompt_len = len(prompt_label)
        sys.stdout.write(prompt_label)
        sys.stdout.flush()
        try:
            while True:
                ch = self.msvcrt.getwch()
                # Ctrl+C
                if ch == "\x03":
                    raise KeyboardInterrupt
                # Special keys: consume the next code and ignore
                if ch in ("\x00", "\xe0"):
                    _ = self.msvcrt.getwch()
                    continue
                if ch == "\r":
                    # Check if Shift is currently pressed
                    shift_down = (self.user32.GetKeyState(self.VK_SHIFT) & 0x8000) != 0
                    if shift_down:
                        buf.append("\n")
                        # No continuation label
                        sys.stdout.write("\n")
                        sys.stdout.flush()
                        continue
                    else:
                        sys.stdout.write("\n")
                        sys.stdout.flush()
                        return "".join(buf).strip()
                if ch == "\x08":  # backspace
                    if buf:
                        if buf[-1] == "\n":
                            # Remove the newline and move cursor to end of previous line
                            buf.pop()
                            # Cursor up and carriage return
                            try:
                                sys.stdout.write("\x1b[1A\r")
                                # Compute previous line length (account for prompt on first line)
                                current = "".join(buf)
                                lines = current.split("\n") if current else [""]
                                prev_idx = len(lines) - 1
                                prev_len = len(lines[prev_idx]) if prev_idx >= 0 else 0
                                move_cols = prev_len + (visible_prompt_len if prev_idx == 0 else 0)
                                if move_cols > 0:
                                    sys.stdout.write(f"\x1b[{move_cols}C")
                                sys.stdout.flush()
                            except Exception:
                                # Fallback: just print carriage return
                                sys.stdout.write("\r")
                                sys.stdout.flush()
                        else:
                            buf.pop()
                            sys.stdout.write("\b \b")
                            sys.stdout.flush()
                    continue
                # Regular printable
                if ch not in ("\n",):
                    buf.append(ch)
                    sys.stdout.write(ch)
                    sys.stdout.flush()
        except KeyboardInterrupt:
            raise


class PosixKeyEngine(BaseInputEngine):
    def __init__(self) -> None:
        super().__init__()
        import termios, tty, select  # local imports
        self.termios = termios
        self.tty = tty
        self.select = select
        self.fd = sys.stdin.fileno()
        self._orig_attrs = termios.tcgetattr(self.fd)
        # Enable raw mode
        self.tty.setcbreak(self.fd)
        # Try enabling modern keyboard protocols (best effort)
        try:
            sys.stdout.write("\x1b[>1u")  # kitty CSI u
            sys.stdout.write("\x1b[>4;2m")  # xterm modifyOtherKeys=2
            sys.stdout.flush()
        except Exception:
            pass
        # Calibrate Shift+Enter signature (non-intrusive, one-shot)
        self.shift_sig: Optional[bytes] = None
        self.enter_sigs = {b"\r", b"\n", b"\r\n"}
        try:
            self._calibrate()
        except Exception:
            # If calibration fails, fallback remains
            pass
        if self.shift_sig is not None:
            self.info = EngineInfo(supports_shift_enter=True, hint="Shift+Enter inserts a newline; Enter sends.")
        else:
            self.info = EngineInfo(supports_shift_enter=False, hint="Enter sends; Ctrl+J inserts a newline.", fallback_key_name="Ctrl+J")

    def __del__(self) -> None:  # best effort restore
        try:
            self.termios.tcsetattr(self.fd, self.termios.TCSADRAIN, self._orig_attrs)
        except Exception:
            pass
        # Disable protocols
        try:
            sys.stdout.write("\x1b[>0u")  # disable kitty CSI u
            sys.stdout.write("\x1b[>4;0m")  # disable modifyOtherKeys
            sys.stdout.flush()
        except Exception:
            pass

    def _read_bytes(self, timeout: float = 5.0) -> bytes:
        start = time.time()
        chunks: list[bytes] = []
        while True:
            r, _, _ = self.select.select([self.fd], [], [], max(0, timeout - (time.time() - start)))
            if not r:
                break
            try:
                b = os.read(self.fd, 64)
            except InterruptedError:
                continue
            if not b:
                break
            chunks.append(b)
            # If first byte is not ESC, we likely have a single key
            if chunks[0][:1] != b"\x1b":
                break
            # If ESC sequence, read a little more to complete it (short wait)
            time.sleep(0.01)
            if time.time() - start > timeout:
                break
        return b"".join(chunks)

    def _calibrate(self) -> None:
        # Ask the terminal silently to differentiate Enter vs Shift+Enter by sampling two presses.
        # We'll keep this subtle: short messages to stderr to avoid interfering with stdout rendering
        try:
            sys.stderr.write("[calibration] Press Enter, then Shift+Enter (or Ctrl+J if Shift+Enter unsupported).\n")
            sys.stderr.flush()
        except Exception:
            pass
        # Read Enter
        b1 = self._read_bytes(timeout=10.0)
        if b1:
            # Normalize CRLF
            if b1 == b"\r\n":
                b1 = b"\r"
            self.enter_sigs.add(b1)
        # Read Shift+Enter attempt (or Ctrl+J fallback)
        b2 = self._read_bytes(timeout=10.0)
        if not b2:
            return
        # Common kitty CSI u for Shift+Enter: ESC [ 13 ; 2 u
        if b2.startswith(b"\x1b[") and (b"13;2" in b2) and (b2.endswith(b"u") or b2.endswith(b"~")):
            self.shift_sig = b2
            return
        # Some terminals using modifyOtherKeys can send ESC [ 27 ; 2 ; 13 ~ (varies); accept any non-equal distinct sequence
        if b2 not in self.enter_sigs:
            self.shift_sig = b2
            return
        # If identical, no support detected; fallback remains
        self.shift_sig = None

    def _is_backspace(self, b: bytes) -> bool:
        return b in (b"\x7f", b"\x08")

    def read_message(self, prompt_label: str = "\nYou: ", cont_label: str = "... ") -> str:
        # Visible prompt is the part after the last newline in the label
        try:
            visible_prompt_len = len(prompt_label.rsplit("\n", 1)[-1])
        except Exception:
            visible_prompt_len = len(prompt_label)
        sys.stdout.write(prompt_label)
        sys.stdout.flush()
        buf: list[str] = []
        try:
            while True:
                b = self._read_bytes(timeout=1e6)  # effectively block
                if not b:
                    continue
                # Ctrl+C in raw mode arrives as 0x03
                if b == b"\x03":
                    raise KeyboardInterrupt
                # Ctrl+J fallback for newline when shift unsupported
                if not self.info.supports_shift_enter and b == b"\n":
                    buf.append("\n")
                    # No continuation label
                    sys.stdout.write("\n")
                    sys.stdout.flush()
                    continue
                # Submit on Enter
                if b in self.enter_sigs:
                    sys.stdout.write("\n")
                    sys.stdout.flush()
                    return "".join(buf).strip()
                # Shift+Enter signature insert newline
                if self.info.supports_shift_enter and self.shift_sig is not None and b == self.shift_sig:
                    buf.append("\n")
                    # No continuation label
                    sys.stdout.write("\n")
                    sys.stdout.flush()
                    continue
                # Backspace
                if self._is_backspace(b):
                    if buf:
                        if buf[-1] == "\n":
                            # Remove newline and move cursor to end of previous line
                            buf.pop()
                            try:
                                sys.stdout.write("\x1b[1A\r")
                                current = "".join(buf)
                                lines = current.split("\n") if current else [""]
                                prev_idx = len(lines) - 1
                                prev_len = len(lines[prev_idx]) if prev_idx >= 0 else 0
                                move_cols = prev_len + (visible_prompt_len if prev_idx == 0 else 0)
                                if move_cols > 0:
                                    sys.stdout.write(f"\x1b[{move_cols}C")
                                sys.stdout.flush()
                            except Exception:
                                sys.stdout.write("\r")
                                sys.stdout.flush()
                        else:
                            buf.pop()
                            sys.stdout.write("\b \b")
                            sys.stdout.flush()
                    continue
                # Ignore arrow keys and other escape sequences
                if b.startswith(b"\x1b"):
                    # If the user typed literal ESC followed by something, ignore
                    continue
                # Printable bytes -> decode
                try:
                    s = b.decode("utf-8", errors="ignore")
                except Exception:
                    s = ""
                if s:
                    buf.append(s)
                    sys.stdout.write(s)
                    sys.stdout.flush()
        except KeyboardInterrupt:
            raise


def make_engine() -> BaseInputEngine:
    if not _is_tty():
        # Non-tty: fallback to simple input() composer
        return SimpleInputEngine()
    if os.name == "nt":
        try:
            return WindowsKeyEngine()
        except Exception:
            return SimpleInputEngine()
    else:
        try:
            return PosixKeyEngine()
        except Exception:
            return SimpleInputEngine()


class SimpleInputEngine(BaseInputEngine):
    def __init__(self) -> None:
        super().__init__()
        # Multiline composer using input(): Enter on an empty line submits
        self.info = EngineInfo(
            supports_shift_enter=False,
            hint="Empty line submits; paste freely.",
            fallback_key_name="Ctrl+J",
        )

    def read_message(self, prompt_label: str = "\nYou: ", cont_label: str = "... ") -> str:  # noqa: ARG002
        # Multiline input fallback for non-tty or failure cases.
        # Rules:
        # - Print prompt once.
        # - Read lines until an empty line is entered; submit accumulated text.
        # - EOF (Ctrl+D/Z) submits if buffer has content; otherwise propagates.
        sys.stdout.write(prompt_label)
        sys.stdout.flush()
        lines: list[str] = []
        while True:
            try:
                line = input()
            except EOFError:
                # Submit what we have; if nothing, bubble up for graceful exit
                if lines:
                    return "\n".join(lines)
                raise
            # Empty line submits (if we already have something)
            if line == "":
                if lines:
                    return "\n".join(lines)
                # If first line is empty, treat as empty message
                return ""
            lines.append(line)
