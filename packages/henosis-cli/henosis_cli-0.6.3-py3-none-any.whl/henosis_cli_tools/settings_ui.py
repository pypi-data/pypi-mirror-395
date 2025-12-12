"""
Dependency-free interactive settings UI for henosis-cli.

Simplified UX (categories-first):
- First screen shows categories (groups). Use Up/Down to move, Enter to open.
- Inside a category, Enter acts on the focused item:
  - bool: toggles ON/OFF
  - enum: opens a picker to select from options (no left/right cycling)
  - text/int/multiline: opens an editor prompt
- No single-letter hotkeys (q/r/u/s/e) and no left/right cycling.
- Auto-save on change: every change is applied immediately via on_change callback.
- Categories screen has a single "Exit settings" action (no Save/Discard confirmation).
- Non-interactive fallback also saves on each change and exits without confirmation.

Return
- (committed: bool, updated: dict|None)
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict, List, Optional, Tuple

# 256-color ANSI for orange selector (approx #ff8700). Fallback to plain '>' when not a TTY.
ORANGE_ANSI = "\x1b[38;5;214m"
RESET_ANSI = "\x1b[0m"
def _sel(s: str) -> str:
    try:
        return f"{ORANGE_ANSI}{s}{RESET_ANSI}" if _isatty() else s
    except Exception:
        return s

# Colorize the 'henosis-cli' name inside titles to match the orange caret.
def _colorize_henosis_name(title: str) -> str:
    try:
        if _isatty() and isinstance(title, str) and "henosis-cli" in title:
            return title.replace("henosis-cli", f"{ORANGE_ANSI}henosis-cli{RESET_ANSI}")
    except Exception:
        pass
    return title


def _isatty() -> bool:
    try:
        return sys.stdin.isatty() and sys.stdout.isatty()
    except Exception:
        return False


def _clear_screen() -> None:
    try:
        # ANSI clear + home
        sys.stdout.write("\x1b[2J\x1b[H")
        sys.stdout.flush()
    except Exception:
        try:
            os.system("cls" if os.name == "nt" else "clear")
        except Exception:
            pass


def _read_key_win() -> Optional[str]:
    try:
        import msvcrt  # type: ignore
    except Exception:
        return None
    while True:
        ch = msvcrt.getwch()
        if ch in ("\x00", "\xe0"):
            code = msvcrt.getwch()
            return {
                "H": "UP",
                "P": "DOWN",
                "K": "LEFT",
                "M": "RIGHT",
                "I": "PGUP",
                "Q": "PGDN",
                "G": "HOME",
                "O": "END",
            }.get(code, None)
        if ch == "\r":
            return "ENTER"
        if ch == "\x1b":
            return "ESC"
        if ch == "\t":
            return "TAB"
        if ch == "\b":
            return "BACKSPACE"
        if ch.isprintable():
            return ch


def _read_key_posix(fd: int) -> Optional[str]:
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
                    if rest and rest[0] in ("A", "B", "C", "D", "H", "F"):
                        return {
                            "A": "UP",
                            "B": "DOWN",
                            "C": "RIGHT",
                            "D": "LEFT",
                            "H": "HOME",
                            "F": "END",
                        }[rest[0]]
                    more = _os.read(fd, 2).decode(errors="ignore")
                    if more.startswith("5~"):
                        return "PGUP"
                    if more.startswith("6~"):
                        return "PGDN"
                return "ESC"
            if c in ("\r", "\n"):
                return "ENTER"
            if c == "\t":
                return "TAB"
            if c == "\x7f":
                return "BACKSPACE"
            if c.isprintable():
                return c
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def _read_key() -> Optional[str]:
    if os.name == "nt":
        try:
            return _read_key_win()
        except Exception:
            return None
    try:
        return _read_key_posix(sys.stdin.fileno())
    except Exception:
        return None


def _truncate(s: str, maxw: int) -> str:
    if len(s) <= maxw:
        return s
    if maxw <= 3:
        return s[:maxw]
    return s[: maxw - 3] + "..."


class SettingsUI:
    def __init__(
        self,
        title: str,
        items: List[Dict[str, Any]],
        initial: Dict[str, Any],
        defaults: Dict[str, Any],
        footer: Optional[str] = None,
        # Optional synchronous callback invoked whenever a value changes.
        # Signature: on_change(key: str, value: Any, working: Dict[str, Any]) -> None
        on_change: Optional[Any] = None,
    ) -> None:
        self.title = title
        # Categories from provided groups; if none, create a single implicit category
        self.categories: List[Dict[str, Any]] = []
        has_groups = any((it.get("type") == "group") for it in items)
        if has_groups:
            for g in items:
                if g.get("type") == "group":
                    self.categories.append({
                        "label": str(g.get("label") or ""),
                        "items": list(g.get("items") or []),
                    })
        else:
            self.categories.append({"label": "Settings", "items": list(items)})

        self.defaults = dict(defaults or {})
        self.initial = dict(initial or {})
        # Working copy for edits
        self.working: Dict[str, Any] = dict(initial or {})
        # Navigation state
        self.mode: str = "categories"  # or "items"
        self.cat_index: int = 0
        self.item_index: int = 0
        # Minimal footer per new UX
        self.footer = footer or "\u2191/\u2193 move, Enter select, Esc back"
        self.dirty: bool = False
        # Save-on-change hook (caller may persist/settings-sync per update)
        self.on_change = on_change

    # ---------- render helpers ----------
    def _format_value(self, row: Dict[str, Any]) -> str:
        rid = row.get("id")
        rtype = row.get("type")
        if not rid:
            return ""
        val = self.working.get(rid)
        render = row.get("render") if isinstance(row.get("render"), dict) else None
        if rtype == "bool":
            return "ON" if bool(val) else "OFF"
        if rtype == "enum":
            if render and (val in render):
                try:
                    return str(render[val])
                except Exception:
                    pass
            return str(val)
        if rtype in ("text", "multiline"):
            s = str(val or "")
            return s.replace("\n", " \u23ce ")
        if rtype == "int":
            return "default" if (val is None) else str(val)
        return str(val)

    def _render(self) -> None:
        _clear_screen()
        print("=" * 80)
        # Make 'henosis-cli' in the title orange to match the caret
        _title = _colorize_henosis_name(self.title)
        if self.mode == "categories":
            print(_title)
        else:
            cat = self.categories[self.cat_index]
            print(f"{_title} > {cat.get('label')}")
        print("=" * 80)

        if self.mode == "categories":
            for i, cat in enumerate(self.categories):
                cur = _sel(">") if i == self.cat_index else " "
                label = str(cat.get("label") or f"Category {i+1}")
                # Also color the selected label itself in orange
                if i == self.cat_index and _isatty():
                    label = f"{ORANGE_ANSI}{label}{RESET_ANSI}"
                print(f" {cur} {label}")
            print()
            # Single action row: Exit settings (auto-saved on change)
            total = len(self.categories)
            last_sel = (self.cat_index == total)
            exit_lbl = "Exit settings"
            if last_sel and _isatty():
                exit_lbl = f"{ORANGE_ANSI}{exit_lbl}{RESET_ANSI}"
            print(f" {(_sel('>') if last_sel else ' ')} {exit_lbl}")
        else:
            rows = self.categories[self.cat_index].get("items") or []
            for i, row in enumerate(rows):
                rid = row.get("id")
                label = str(row.get("label") or rid or "")
                dirty_mark = ""
                if rid and (self.working.get(rid) != self.initial.get(rid)):
                    # Mark modified rows with plain text instead of a star to keep the
                    # menu visuals clean and focused on the highlighted selection.
                    dirty_mark = " (modified)"
                cur = _sel(">") if i == self.item_index else " "
                val_str = self._format_value(row)
                try:
                    width = os.get_terminal_size().columns
                except Exception:
                    width = 80
                left_plain = f" {cur} {label}{dirty_mark}: "
                rem = max(10, width - len(left_plain))
                val_tr = _truncate(val_str, rem)
                # Color the selected row (label and value) in orange
                if i == self.item_index and _isatty():
                    left_col = f" {cur} {ORANGE_ANSI}{label}{dirty_mark}{RESET_ANSI}: "
                    val_tr = f"{ORANGE_ANSI}{val_tr}{RESET_ANSI}"
                    print(left_col + val_tr)
                else:
                    print(left_plain + val_tr)
            print()
            back_sel = (self.item_index == len(rows))
            back_lbl = "Back to categories"
            if back_sel and _isatty():
                back_lbl = f"{ORANGE_ANSI}{back_lbl}{RESET_ANSI}"
            print(f" {(_sel('>') if back_sel else ' ')} {back_lbl}")

        print("-" * 80)
        print(self.footer)
        if self.dirty:
            print("(unsaved changes)")

    # ---------- input/edit helpers ----------
    def _pick_from_list(self, title: str, options: List[Tuple[Any, str]], current: Optional[Any]) -> Optional[Any]:
        try:
            idx = [v for (v, _l) in options].index(current)
        except Exception:
            idx = 0
        while True:
            _clear_screen()
            print("=" * 80)
            # Colorize 'henosis-cli' in any titles as well
            print(_colorize_henosis_name(title))
            print("=" * 80)
            for i, (_v, lbl) in enumerate(options):
                cur = _sel(">") if i == idx else " "
                # Make the selected option text orange in addition to the caret
                if i == idx and _isatty():
                    lbl = f"{ORANGE_ANSI}{lbl}{RESET_ANSI}"
                print(f" {cur} {lbl}")
            print("-" * 80)
            print("\u2191/\u2193 move, Enter select, Esc cancel")
            key = _read_key()
            if key == "UP":
                idx = (idx - 1) % len(options)
                continue
            if key == "DOWN":
                idx = (idx + 1) % len(options)
                continue
            if key == "ENTER":
                return options[idx][0]
            if key == "ESC":
                return None

    def _set_value(self, rid: str, new_val: Any) -> None:
        old = self.working.get(rid)
        if old != new_val:
            self.working[rid] = new_val
            self.dirty = True
            # Notify caller immediately so they can persist per-change
            try:
                if callable(self.on_change):
                    # Pass the live working dict so caller may normalize/update it in-place
                    self.on_change(rid, new_val, self.working)
            except Exception:
                # Never break UI due to callback issues
                pass

    def _edit_text(self, prompt: str, default: Optional[str] = None) -> str:
        try:
            msg = f"{prompt} [{default}]> " if default is not None else f"{prompt}> "
            return input(msg)
        except EOFError:
            return default or ""
        except KeyboardInterrupt:
            return default or ""

    def _edit_multiline(self, prompt: str, default: Optional[str] = None) -> str:
        print(prompt)
        print("(finish with an empty line)")
        lines: List[str] = []
        if default:
            lines = [default]
        while True:
            try:
                line = input()
            except EOFError:
                break
            except KeyboardInterrupt:
                break
            if line == "":
                break
            lines.append(line)
        return "\n".join(lines)

    def _edit_int(self, prompt: str, default: Optional[int]) -> Optional[int]:
        ds = "default" if default is None else str(default)
        s = self._edit_text(f"{prompt} (int or 'default')", ds)
        s = (s or "").strip().lower()
        if s in ("", "default", "none"):
            return None
        try:
            return int(s)
        except ValueError:
            print("Invalid integer; keeping previous value.")
            return default

    def _reset_item(self, row: Dict[str, Any]) -> None:
        rid = row.get("id")
        if not rid:
            return
        if rid in self.defaults:
            self._set_value(rid, self.defaults[rid])

    # ---------- public ----------
    def run(self) -> Tuple[bool, Optional[Dict[str, Any]]]:
        # Non-interactive fallback: straightforward prompts within each category
        if not _isatty():
            # Non-interactive mode: apply and save each change immediately via on_change
            print(self.title)
            print("(non-interactive mode)")
            for cat in self.categories:
                print(f"\n[{cat.get('label','')}]")
                for row in (cat.get("items") or []):
                    rid = row.get("id")
                    rtype = row.get("type")
                    if not rid:
                        continue
                    label = str(row.get("label") or rid)
                    cur = self.working.get(rid)
                    if rtype == "bool":
                        ans = self._edit_text(f"{label} (on/off)", "on" if cur else "off").strip().lower()
                        new_val = True if ans in ("on", "true", "1", "yes", "y") else False
                        self._set_value(rid, new_val)
                    elif rtype == "enum":
                        opts = row.get("options") or []
                        render = row.get("render") or {}
                        print(f"{label} options:")
                        for i, o in enumerate(opts, start=1):
                            disp = render.get(o, o)
                            print(f"  {i}. {disp}")
                        raw = self._edit_text(f"Choose 1-{len(opts)}", None)
                        if raw.isdigit():
                            k = int(raw)
                            if 1 <= k <= len(opts):
                                self._set_value(rid, opts[k - 1])
                    elif rtype == "text":
                        self._set_value(rid, self._edit_text(label, str(cur or "")))
                    elif rtype == "multiline":
                        self._set_value(rid, self._edit_multiline(label, str(cur or "")))
                    elif rtype == "int":
                        self._set_value(rid, self._edit_int(label, cur if isinstance(cur, int) else None))
            # Always treat as committed; changes were already saved on change
            return True, dict(self.working)

        # Interactive TTY loop
        while True:
            self._render()
            key = _read_key()
            if key is None:
                # Minimal numeric fallback: select category/item by number
                try:
                    raw = input("Select number (Enter to choose), or Esc to exit: ").strip().lower()
                except EOFError:
                    # Exit and commit; changes have been auto-saved on change
                    return True, dict(self.working)
                if not raw.isdigit():
                    continue
                k = int(raw)
                if self.mode == "categories":
                    total = len(self.categories) + 1
                    if 1 <= k <= total:
                        if k <= len(self.categories):
                            self.cat_index = k - 1
                            self.mode = "items"
                            self.item_index = 0
                        else:
                            return True, dict(self.working)
                    continue
                else:
                    rows = self.categories[self.cat_index].get("items") or []
                    if 1 <= k <= (len(rows) + 1):
                        if k == len(rows) + 1:
                            self.mode = "categories"
                        else:
                            self.item_index = k - 1
                            key = "ENTER"
                    else:
                        continue

            # Categories screen
            if self.mode == "categories":
                total = len(self.categories) + 1
                if key == "UP":
                    self.cat_index = (self.cat_index - 1) % total
                    continue
                if key == "DOWN":
                    self.cat_index = (self.cat_index + 1) % total
                    continue
                if key == "HOME":
                    self.cat_index = 0
                    continue
                if key == "END":
                    self.cat_index = total - 1
                    continue
                if key == "ENTER":
                    if self.cat_index < len(self.categories):
                        self.mode = "items"
                        self.item_index = 0
                        continue
                    # Exit settings (auto-saved)
                    return True, dict(self.working)
                if key == "ESC":
                    # Exit and commit; changes have already been saved on change
                    return True, dict(self.working)
                # ignore others
                continue

            # Item screen
            rows = self.categories[self.cat_index].get("items") or []
            if key == "UP":
                self.item_index = (self.item_index - 1) % (len(rows) + 1)
                continue
            if key == "DOWN":
                self.item_index = (self.item_index + 1) % (len(rows) + 1)
                continue
            if key == "HOME":
                self.item_index = 0
                continue
            if key == "END":
                self.item_index = len(rows)
                continue
            if key == "ESC":
                self.mode = "categories"
                continue
            if key == "ENTER":
                if self.item_index == len(rows):
                    self.mode = "categories"
                    continue
                row = rows[self.item_index]
                rid = row.get("id")
                rtype = row.get("type")
                if not rid:
                    continue
                if rtype == "bool":
                    cur = bool(self.working.get(rid))
                    self._set_value(rid, not cur)
                    continue
                if rtype == "enum":
                    opts = list(row.get("options") or [])
                    render = row.get("render") if isinstance(row.get("render"), dict) else {}
                    choices = [(o, str(render.get(o, o))) for o in opts]
                    picked = self._pick_from_list(str(row.get("label") or rid), choices, self.working.get(rid))
                    if picked is not None:
                        self._set_value(rid, picked)
                    continue
                if rtype == "text":
                    cur = self.working.get(rid)
                    new = self._edit_text(str(row.get("label") or rid), str(cur or ""))
                    self._set_value(rid, new)
                    continue
                if rtype == "multiline":
                    cur = self.working.get(rid)
                    new = self._edit_multiline(str(row.get("label") or rid), str(cur or ""))
                    self._set_value(rid, new)
                    continue
                if rtype == "int":
                    cur = self.working.get(rid)
                    new = self._edit_int(str(row.get("label") or rid), cur if isinstance(cur, int) else None)
                    self._set_value(rid, new)
                    continue

        # Unreachable
        # return False, None
