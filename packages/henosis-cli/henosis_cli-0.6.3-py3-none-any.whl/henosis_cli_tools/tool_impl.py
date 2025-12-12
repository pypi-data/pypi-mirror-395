# tool_impl.py
from __future__ import annotations
import hashlib
import json
import os
import re
import shlex
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
import difflib

# ----------------------------- Defaults -----------------------------#
# Reasonable default extension allowlist (lower-case)
_DEFAULT_ALLOWED_EXTS = {
    ".txt",
    ".md",
    ".json",
    ".jsonc",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".env",
    ".xml",
    ".html",
    ".css",
    ".scss",
    ".less",
    ".js",
    ".mjs",
    ".cjs",
    ".ts",
    ".tsx",
    ".jsx",
    ".py",
    ".ipynb",
    ".rb",
    ".go",
    ".rs",
    ".java",
    ".kt",
    ".scala",
    ".c",
    ".cc",
    ".cpp",
    ".h",
    ".hpp",
    ".cs",
    ".php",
    ".sh",
    ".bash",
    ".zsh",
    ".ps1",
    ".sql",
    ".graphql",
    ".proto",
    ".dockerignore",
    ".gitignore",
    ".make",
    ".mk",
    ".cmake",
    ".gradle",
    ".sbt",
    ".nuspec",
    ".conf",
}

_MAX_FILE_BYTES = int(os.getenv("HENOSIS_MAX_FILE_BYTES", str(1_073_741_824)))
_MAX_EDIT_BYTES = int(os.getenv("HENOSIS_MAX_EDIT_BYTES", str(1_073_741_824)))
_EDIT_SAFEGUARD_MAX_LINES = int(os.getenv("HENOSIS_EDIT_SAFEGUARD_MAX_LINES", "3000"))
_COMMAND_TIMEOUT_SEC = float(os.getenv("HENOSIS_COMMAND_TIMEOUT_SEC", "30"))
# Max chars for stdout/stderr before truncation notice is applied
_CMD_OUTPUT_MAX_CHARS = 3000

_VERBOSE_NOTICE = (
    "console output was EXTEREMELY verbose the ouput was truncated as to not overflow your context. here are the last 3k chars:\n"
)

def _parse_allowed_roots(raw: str | None) -> List[Path]:
    roots: List[Path] = []
    if not raw:
        return roots
    for token in raw.split(","):
        s = token.strip()
        if not s:
            continue
        p = Path(s).expanduser().resolve()
        roots.append(p)
    return roots

@dataclass
class FileToolPolicy:
    """Scope and constraints for local file and process operations.
    scope: "workspace" or "host"
    workspace_base: base directory for workspace scope (created if missing)
    host_base: optional base for host scope (must be absolute)
    allowed_roots: optional list of absolute Path roots for host scope
    allowed_exts: lower-case extension allowlist (use empty set to disable)
    max_bytes: max bytes for single read/write
    """
    scope: str = "workspace"
    workspace_base: Path = Path(os.getenv("HENOSIS_WORKSPACE_DIR", "./workspace")).expanduser().resolve()
    host_base: Optional[Path] = None
    allowed_roots: Optional[List[Path]] = None
    allowed_exts: Set[str] = frozenset(
        {e.strip().lower() for e in os.getenv("HENOSIS_ALLOW_EXTENSIONS", "").split(",") if e.strip()} or _DEFAULT_ALLOWED_EXTS
    )
    max_bytes: int = _MAX_FILE_BYTES

    def __post_init__(self) -> None:
        # Ensure workspace dir exists
        try:
            self.workspace_base.mkdir(parents=True, exist_ok=True)
            (self.workspace_base / ".locks").mkdir(parents=True, exist_ok=True)
        except Exception:
            pass

    def all_host_roots(self) -> List[Path]:
        roots = list(self.allowed_roots or [])
        if self.host_base:
            roots.append(self.host_base)
        return roots

def resolve_path(path_input: str, policy: FileToolPolicy) -> Path:
    path_input = (path_input or "").strip()
    is_empty = (path_input == "" or path_input == ".")
    if policy.scope == "workspace":
        if is_empty:
            full = policy.workspace_base
        else:
            p = Path(path_input)
            if p.is_absolute():
                raise ValueError("absolute paths are not allowed in workspace scope")
            full = (policy.workspace_base / p).resolve()
        try:
            full.relative_to(policy.workspace_base)
        except Exception:
            raise ValueError("path escapes workspace")
        return full
    # host scope
    roots = policy.all_host_roots()
    if not roots:
        roots = [Path.cwd().resolve()]
    if is_empty:
        base = policy.host_base or roots[0]
        full = base
    else:
        p = Path(path_input).expanduser()
        full = p.resolve() if p.is_absolute() else (policy.host_base or roots[0]).joinpath(p).resolve()
    for r in roots:
        try:
            full.relative_to(r)
            break
        except Exception:
            continue
    else:
        raise ValueError("path is not under any allowed host root")
    return full

# ------------------------- Encoding helpers -------------------------#
def read_text_auto(p: Path) -> str:
    data = p.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        return data[3:].decode("utf-8", errors="replace")
    if data.startswith(b"\xff\xfe\x00\x00") or data.startswith(b"\x00\x00\xfe\xff"):
        return data.decode("utf-32", errors="replace")
    if data.startswith(b"\xff\xfe"):
        return data.decode("utf-16-le", errors="replace")
    if data.startswith(b"\xfe\xff"):
        return data.decode("utf-16-be", errors="replace")
    sample = data[:4096]
    if sample:
        nul_ratio = sample.count(b"\x00") / max(1, len(sample))
        if nul_ratio > 0.20:
            even_nuls = sum(1 for i in range(0, len(sample), 2) if sample[i] == 0)
            odd_nuls = sum(1 for i in range(1, len(sample), 2) if sample[i] == 0)
            if odd_nuls >= even_nuls:
                try:
                    return data.decode("utf-16-le", errors="replace")
                except Exception:
                    pass
            else:
                try:
                    return data.decode("utf-16-be", errors="replace")
                except Exception:
                    pass
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("utf-8", errors="replace")

def _ensure_size_limit_bytes(content: str, max_bytes: int) -> None:
    b = len(content.encode("utf-8", errors="replace"))
    if b > max_bytes:
        raise ValueError(f"content exceeds {max_bytes} bytes")

def _file_size_ok(p: Path, max_bytes: int) -> None:
    try:
        size = p.stat().st_size
    except FileNotFoundError:
        return
    if size > max_bytes:
        raise ValueError(f"file too large (> {max_bytes} bytes)")


def _truncate_if_verbose(text: str, limit: int = _CMD_OUTPUT_MAX_CHARS) -> str:
    """Return text unchanged if within limit; otherwise prepend notice and keep last `limit` chars.

    The notice text is intentionally spelled exactly as requested by the user.
    """
    if text is None:
        return ""
    try:
        s = str(text)
    except Exception:
        s = ""
    if len(s) <= limit:
        return s
    tail = s[-limit:]
    return _VERBOSE_NOTICE + tail

# ----------------------------- File ops -----------------------------#
def read_file(path: str, policy: FileToolPolicy) -> Dict[str, Any]:
    p = resolve_path(path, policy)
    if not p.exists():
        return {"ok": False, "error": "file does not exist"}
    if not p.is_file():
        return {"ok": False, "error": "path is not a file"}
    _file_size_ok(p, policy.max_bytes)
    text = read_text_auto(p)
    path_label = str(p) if policy.scope == "host" else str(p.relative_to(policy.workspace_base))
    tokens_used = int(len(text) / 0.3) if text else 0
    return {"ok": True, "data": {"path": path_label, "content": text, "tokens_used": tokens_used}}

def write_file(path: str, content: str, policy: FileToolPolicy) -> Dict[str, Any]:
    p = resolve_path(path, policy)
    _ensure_size_limit_bytes(content, policy.max_bytes)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="") as f:
        f.write(content)
    tokens_used = int(len(content) / 0.3) if content else 0
    return {"ok": True, "data": {"path": str(p), "tokens_used": tokens_used}}

def append_file(path: str, content: str, policy: FileToolPolicy) -> Dict[str, Any]:
    p = resolve_path(path, policy)
    _ensure_size_limit_bytes(content, policy.max_bytes)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8", newline="") as f:
        f.write(content)
    tokens_used = int(len(content) / 0.3) if content else 0
    return {"ok": True, "data": {"path": str(p), "tokens_used": tokens_used}}

def list_dir(path: str, policy: FileToolPolicy) -> Dict[str, Any]:
    # Resolve path with explicit error if resolution fails
    try:
        p = resolve_path(path, policy)
    except Exception as e:
        return {"ok": False, "error": f"resolve_path failed: {type(e).__name__}: {e}", "data": {"path_input": path, "scope": policy.scope}}

    if not p.exists():
        return {"ok": False, "error": "directory does not exist", "data": {"path": str(p), "scope": policy.scope}}
    if not p.is_dir():
        return {"ok": False, "error": "path is not a directory", "data": {"path": str(p), "scope": policy.scope}}

    items = []
    try:
        children = list(p.iterdir())
    except (PermissionError, OSError) as e:
        return {"ok": False, "error": f"list_dir error: {type(e).__name__}: {e}", "data": {"path": str(p), "scope": policy.scope}}
    except Exception as e:
        return {"ok": False, "error": f"Failed to list directory: {type(e).__name__}: {e}", "data": {"path": str(p), "scope": policy.scope}}

    for child in sorted(children, key=lambda x: (not x.is_dir(), x.name.lower()))[:1000]:
        info = {"name": child.name, "is_dir": child.is_dir()}
        if child.is_file():
            try:
                info["size"] = child.stat().st_size
            except Exception:
                info["size"] = None
        items.append(info)

    path_label = str(p) if policy.scope == "host" else str(p.relative_to(policy.workspace_base))
    return {"ok": True, "data": {"path": path_label, "items": items}}

# --------------------------- run_command ----------------------------#
def run_command(cmd: str, policy: FileToolPolicy, cwd: Optional[str] = None, timeout: Optional[float] = None,
                allow_commands_csv: Optional[str] = None) -> Dict[str, Any]:
    cmd_str = (cmd or "").strip()
    if not cmd_str:
        return {"ok": False, "error": "cmd is required"}
    cwd_arg = (cwd or ".")
    cwd_path = resolve_path(cwd_arg, policy)
    if cwd_arg in ("", ".") and policy.scope == "host":
        cwd_path = Path.cwd()
    if cwd_path.exists() and cwd_path.is_file():
        cwd_path = cwd_path.parent
    if cwd_arg.strip() and not cwd_path.exists():
        return {"ok": False, "error": "cwd does not exist"}
    if not cwd_path.is_dir():
        return {"ok": False, "error": "cwd is not a directory"}
    allow_set = {c.strip().lower() for c in (allow_commands_csv or os.getenv("HENOSIS_ALLOW_COMMANDS", "")).split(",") if c.strip()}
    if not allow_set:
        return {"ok": False, "error": "no commands allowed (empty allowlist)"}
    posix = (os.name != "nt")
    try:
        parts = shlex.split(cmd_str, posix=posix)
    except Exception as e:
        return {"ok": False, "error": f"invalid cmd: {e}"}
    if not parts:
        return {"ok": False, "error": "cmd is empty after parsing"}
    exe = parts[0]
    base = os.path.basename(exe).lower()
    if base not in allow_set:
        return {"ok": False, "error": f"command '{base}' not allowed"}
    try:
        requested = float(timeout) if timeout is not None else _COMMAND_TIMEOUT_SEC
    except Exception:
        requested = _COMMAND_TIMEOUT_SEC
    timeout_s = min(max(0.01, requested), float(_COMMAND_TIMEOUT_SEC))
    start = time.time()
    try:
        # Force UTF-8 decoding with replacement to avoid locale-dependent decode errors
        # on Windows (e.g., cp1252 UnicodeDecodeError in reader thread).
        proc = subprocess.run(
            parts,
            shell=False,
            cwd=str(cwd_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_s,
        )
        dur_ms = int((time.time() - start) * 1000)
        # Truncate very verbose outputs to protect context size
        out = _truncate_if_verbose(proc.stdout)
        err = _truncate_if_verbose(proc.stderr)
        return {
            "ok": True,
            "data": {
                "cmd": cmd_str,
                "cwd": str(cwd_path),
                "exit_code": proc.returncode,
                "stdout": out,
                "stderr": err,
                "timed_out": False,
                "duration_ms": dur_ms,
            },
        }
    except subprocess.TimeoutExpired as e:
        dur_ms = int((time.time() - start) * 1000)
        # Even in timeout, ensure any captured output is truncated if overly verbose
        out = _truncate_if_verbose(e.stdout or "")
        err = _truncate_if_verbose(e.stderr or "")
        return {
            "ok": True,
            "data": {
                "cmd": cmd_str,
                "cwd": str(cwd_path),
                "exit_code": None,
                "stdout": out,
                "stderr": err,
                "timed_out": True,
                "duration_ms": dur_ms,
            },
        }

# ---------------------------- apply_patch ----------------------------#
def _ap_normalize_unicode(s: str) -> str:
    trans = {
        "\u2010": "-", "\u2011": "-", "\u2012": "-", "\u2013": "-", "\u2014": "-", "\u2015": "-",
        "\u2018": "'", "\u2019": "'", "\u201A": "'", "\u201B": "'",
        "\u201C": '"', "\u201D": '"', "\u201E": '"', "\u201F": '"',
        "\u00A0": " ", "\u2002": " ", "\u2003": " ", "\u2004": " ", "\u2005": " ", "\u2006": " ", "\u2007": " ", "\u2008": " ", "\u2009": " ", "\u200A": " ", "\u202F": " ", "\u205F": " ",
        "\u3000": " ",
    }
    return "".join(trans.get(ch, ch) for ch in s.strip())

def _ap_parse_patch(patch: str, *, lenient: bool = True) -> List[Dict[str, Any]]:
    raw = (patch or "").strip("\n")
    lines = raw.splitlines()
    if lenient and lines:
        first = lines[0].strip()
        last = lines[-1].strip()
        if first in ("<<EOF", "<<'EOF'", '<<"EOF"') and last == "EOF":
            lines = lines[1:-1]
    if not lines or lines[0].strip() != "*** Begin Patch":
        raise ValueError("patch must start with '*** Begin Patch'")
    if lines[-1].strip() != "*** End Patch":
        raise ValueError("patch must end with '*** End Patch'")
    body = lines[1:-1]
    i = 0
    hunks: List[Dict[str, Any]] = []
    def at(n: int) -> str:
        return body[n] if 0 <= n < len(body) else ""
    while i < len(body):
        line = at(i).strip()
        if not line:
            i += 1
            continue
        if line.startswith("*** Add File: "):
            path = line[len("*** Add File: "):]
            i += 1
            contents: List[str] = []
            while i < len(body):
                L = body[i]
                if L.startswith("*** "):
                    break
                if L.startswith("+"):
                    contents.append(L[1:])
                    i += 1
                else:
                    break
            if not contents or contents[-1] != "":
                contents.append("")
            hunks.append({"kind": "add", "path": path, "contents": "\n".join(contents)})
            continue
        if line.startswith("*** Delete File: "):
            path = line[len("*** Delete File: "):]
            hunks.append({"kind": "delete", "path": path})
            i += 1
            continue
        if line.startswith("*** Update File: "):
            path = line[len("*** Update File: "):]
            i += 1
            move_to: Optional[str] = None
            if i < len(body) and body[i].strip().startswith("*** Move to: "):
                move_to = body[i].strip()[len("*** Move to: "):]
                i += 1
            chunks: List[Dict[str, Any]] = []
            first_chunk = True
            while i < len(body):
                s = body[i]
                s_strip = s.strip()
                if not s_strip:
                    i += 1
                    continue
                if s_strip.startswith("*** "):
                    break
                context: Optional[str] = None
                consumed = 0
                had_header = False
                if s_strip == "@@":
                    consumed = 1
                    had_header = True
                elif s_strip.startswith("@@ "):
                    context = s_strip[3:]
                    consumed = 1
                    had_header = True
                else:
                    # Relaxed: allow implicit chunk (even after the first) without an @@ header
                    consumed = 0
                i += consumed
                old_lines: List[str] = []
                new_lines: List[str] = []
                eof_flag = False
                parsed = 0
                while i < len(body):
                    t = body[i]
                    t_strip = t.strip()
                    # Treat encountering a new header as the end of this chunk
                    if t_strip.startswith("*** "):
                        break
                    if t_strip == "@@" or t_strip.startswith("@@ "):
                        # If nothing parsed yet and we just saw a header, allow skipping empty hunks
                        break
                    if t_strip == "*** End of File":
                        eof_flag = True
                        i += 1
                        parsed += 1
                        break
                    if t.startswith("+"):
                        new_lines.append(t[1:])
                    elif t.startswith("-"):
                        old_lines.append(t[1:])
                    elif t.startswith(" "):
                        seg = t[1:]
                        old_lines.append(seg)
                        new_lines.append(seg)
                    else:
                        # Relaxed: treat plain, non-prefixed, non-header lines as unchanged context
                        seg = t
                        old_lines.append(seg)
                        new_lines.append(seg)
                    i += 1
                    parsed += 1
                # If we consumed a header but did not parse any lines, tolerate an empty hunk (skip it)
                if parsed == 0 and had_header:
                    first_chunk = False
                    continue
                if parsed == 0:
                    raise ValueError("empty update chunk")
                chunks.append({"context": context, "old": old_lines, "new": new_lines, "eof": eof_flag})
                first_chunk = False
            if not chunks:
                raise ValueError(f"empty update for path '{path}'")
            hunks.append({"kind": "update", "path": path, "move_to": move_to, "chunks": chunks})
            continue
        raise ValueError(f"invalid hunk header: {line}")
    return hunks

def _ap_resolve_target(base_dir: Path, rel_or_abs: str, policy: FileToolPolicy) -> Path:
    p_in = (rel_or_abs or "").strip()
    if not p_in:
        raise ValueError("empty path in patch")
    p = Path(p_in)
    p = p.resolve() if p.is_absolute() else (base_dir / p).resolve()
    if policy.scope == "workspace":
        try:
            p.relative_to(policy.workspace_base)
        except Exception:
            raise ValueError("path escapes workspace")
    else:
        roots = policy.all_host_roots() or [Path.cwd().resolve()]
        for r in roots:
            try:
                p.relative_to(r)
                break
            except Exception:
                continue
        else:
            raise ValueError("path is not under any allowed host root")
    # Extension policy for files (ignore dirs)
    if p.suffix and policy.allowed_exts and not p.is_dir():
        if p.suffix.lower() not in policy.allowed_exts:
            raise ValueError(f"extension '{p.suffix}' not allowed")
    return p

def _ap_compute_replacements(original: List[str], chunks: List[Dict[str, Any]], path: Path) -> List[Tuple[int, int, List[str]]]:
    repls: List[Tuple[int, int, List[str]]] = []
    line_index = 0
    for ch in chunks:
        ctx = ch.get("context")
        old = ch.get("old") or []
        new = ch.get("new") or []
        eof = bool(ch.get("eof"))
        if ctx:
            idx = _ap_seek_sequence(original, [ctx], line_index, False)
            if idx is None:
                raise ValueError(f"Failed to find context '{ctx}' in {path}")
            line_index = idx + 1
        if not old:
            insertion_idx = (len(original) - 1) if (original and original[-1] == "") else len(original)
            repls.append((insertion_idx, 0, list(new)))
            continue
        pattern = list(old)
        new_slice = list(new)
        if eof and pattern and pattern[-1] == "":
            pattern = pattern[:-1]
            if new_slice and new_slice[-1] == "":
                new_slice = new_slice[:-1]
        found = _ap_seek_sequence(original, pattern, line_index, eof)
        if found is None:
            raise ValueError(f"Failed to find expected lines in {path}")
        repls.append((found, len(pattern), new_slice))
        line_index = found + len(pattern)
    return repls

def _ap_seek_sequence(lines: List[str], pattern: List[str], start: int, eof: bool) -> Optional[int]:
    if not pattern:
        return start
    if len(pattern) > len(lines):
        return None
    search_start = (len(lines) - len(pattern)) if (eof and len(lines) >= len(pattern)) else start
    for i in range(search_start, len(lines) - len(pattern) + 1):
        if lines[i:i + len(pattern)] == pattern:
            return i
    for i in range(search_start, len(lines) - len(pattern) + 1):
        ok = True
        for p_idx, pat in enumerate(pattern):
            if lines[i + p_idx].rstrip() != pat.rstrip():
                ok = False
                break
        if ok:
            return i
    for i in range(search_start, len(lines) - len(pattern) + 1):
        ok = True
        for p_idx, pat in enumerate(pattern):
            if lines[i + p_idx].strip() != pat.strip():
                ok = False
                break
        if ok:
            return i
    for i in range(search_start, len(lines) - len(pattern) + 1):
        ok = True
        for p_idx, pat in enumerate(pattern):
            if _ap_normalize_unicode(lines[i + p_idx]) != _ap_normalize_unicode(pat):
                ok = False
                break
        if ok:
            return i
    return None

def _atomic_write(target: Path, content: str, backup: bool) -> Optional[Path]:
    target.parent.mkdir(parents=True, exist_ok=True)
    backup_path: Optional[Path] = None
    if backup and target.exists():
        backup_path = target.with_suffix(target.suffix + ".bak")
        try:
            if backup_path.exists():
                backup_path.unlink()
        except Exception:
            pass
        try:
            target.replace(backup_path)
        except Exception:
            # If we cannot create a backup, continue without backup.
            backup_path = None
    fd, tmp_path = tempfile.mkstemp(prefix=target.name + ".tmp_", dir=str(target.parent))
    tmp_exists = True
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        # Atomically move temp file into place
        os.replace(tmp_path, target)
        tmp_exists = False
    finally:
        try:
            if tmp_exists and os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass
    return backup_path

def apply_patch(
    patch: str,
    policy: FileToolPolicy,
    *,
    cwd: str | None = ".",
    lenient: bool = True,
    dry_run: bool = False,
    backup: bool = True,
    safeguard_max_lines: int = _EDIT_SAFEGUARD_MAX_LINES,
    safeguard_confirm: bool = False,
) -> Dict[str, Any]:
    patch_text = str(patch or "")
    if not patch_text.strip():
        return {"ok": False, "error": "patch is required"}
    base_dir = resolve_path(cwd or ".", policy)
    if base_dir.exists() and base_dir.is_file():
        base_dir = base_dir.parent
    if not base_dir.exists():
        return {"ok": False, "error": "cwd does not exist"}
    if not base_dir.is_dir():
        return {"ok": False, "error": "cwd is not a directory"}
    hunks = _ap_parse_patch(patch_text, lenient=lenient)
    added: List[str] = []
    modified: List[str] = []
    deleted: List[str] = []
    details: List[Dict[str, Any]] = []
    for h in hunks:
        kind = h.get("kind")
        if kind == "add":
            path_s = h.get("path")
            target = _ap_resolve_target(base_dir, path_s, policy)
            contents = h.get("contents", "")
            _ensure_size_limit_bytes(contents, _MAX_EDIT_BYTES)
            lines_after = len(contents.splitlines())
            if (lines_after > safeguard_max_lines) and not safeguard_confirm and not dry_run:
                details.append({
                    "path": str(target),
                    "action": "A",
                    "safeguard_triggered": True,
                    "message": f"Safeguard: resulting file would be {lines_after} lines (> {safeguard_max_lines}). Set safeguard_confirm=true to apply.",
                })
                continue
            if not dry_run:
                target.parent.mkdir(parents=True, exist_ok=True)
                _atomic_write(target, contents, backup=False)
            added.append(str(target))
            details.append({"path": str(target), "action": "A", "dry_run": dry_run})
        elif kind == "delete":
            path_s = h.get("path")
            target = _ap_resolve_target(base_dir, path_s, policy)
            if not target.exists():
                deleted.append(str(target))
                details.append({"path": str(target), "action": "D", "dry_run": dry_run, "note": "did not exist"})
                continue
            if not target.is_file():
                return {"ok": False, "error": "delete target is not a file"}
            if not dry_run:
                try:
                    target.unlink()
                except Exception as e:
                    return {"ok": False, "error": str(e)}
            deleted.append(str(target))
            details.append({"path": str(target), "action": "D", "dry_run": dry_run})
        elif kind == "update":
            path_s = h.get("path")
            move_to = h.get("move_to")
            src = _ap_resolve_target(base_dir, path_s, policy)
            dst = _ap_resolve_target(base_dir, move_to, policy) if move_to else src
            if not src.exists():
                return {"ok": False, "error": f"source file does not exist: {src}"}
            if not src.is_file():
                return {"ok": False, "error": "source is not a file"}
            _file_size_ok(src, _MAX_EDIT_BYTES)
            before = read_text_auto(src)
            original_lines = before.split("\n")
            if original_lines and original_lines[-1] == "":
                original_lines.pop()
            repls = _ap_compute_replacements(original_lines, h.get("chunks") or [], src)
            after_lines = list(original_lines)
            for start_idx, old_len, new_seg in reversed(repls):
                for _ in range(old_len):
                    if 0 <= start_idx < len(after_lines):
                        after_lines.pop(start_idx)
                for offset, s in enumerate(new_seg):
                    after_lines.insert(start_idx + offset, s)
            if not after_lines or after_lines[-1] != "":
                after_lines.append("")
            after = "\n".join(after_lines)
            lines_after = len(after.splitlines())
            if (lines_after > safeguard_max_lines) and not safeguard_confirm and not dry_run:
                details.append({
                    "path": str(dst),
                    "action": "M",
                    "safeguard_triggered": True,
                    "message": f"Safeguard: resulting file would be {lines_after} lines (> {safeguard_max_lines}). Set safeguard_confirm=true to apply.",
                })
                continue
            if not dry_run:
                dst.parent.mkdir(parents=True, exist_ok=True)
                _atomic_write(dst, after, backup=backup and dst.exists())
                if dst != src:
                    try:
                        src.unlink()
                    except Exception:
                        pass
            modified.append(str(dst))
            details.append({"path": str(dst), "action": "M", "dry_run": dry_run, "moved": (str(dst) if dst != src else None)})
        else:
            return {"ok": False, "error": f"unknown hunk kind '{kind}'"}
    summary = {"added": added, "modified": modified, "deleted": deleted}
    return {"ok": True, "data": {"summary": summary, "details": details, "dry_run": dry_run}}

# ------------------------- string_replace (fallback) -------------------------#
def _glob_files(base_dir: Path, patterns: List[str], exclude: Optional[List[str]]) -> List[Path]:
    files: List[Path] = []
    seen: Set[Path] = set()
    exc: List[str] = [e for e in (exclude or []) if str(e).strip()]
    for pat in patterns or []:
        pat = (pat or "").strip()
        if not pat:
            continue
        for p in base_dir.glob(pat):
            try:
                rp = p.resolve()
            except Exception:
                continue
            if any(rp.match(x) for x in exc):
                continue
            if rp not in seen and rp.is_file():
                seen.add(rp)
                files.append(rp)
    return files


def string_replace(
    pattern: str,
    replacement: str,
    policy: FileToolPolicy,
    *,
    cwd: str | None = ".",
    file_globs: Optional[List[str]] = None,
    exclude_globs: Optional[List[str]] = None,
    is_regex: bool = False,
    expected_total_matches: Optional[int] = None,
    max_replacements_per_file: int = 5,
    max_total_replacements: int = 5,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """
    Minimal, guarded string replacement across files matched by globs.

    Safeguards (intentionally limited):
      - expected_total_matches: abort if planned replacements != expected
      - caps: at most max_replacements_per_file per file, and max_total_replacements overall
      - dry_run: return unified diffs and counts without writing
    """
    pat = str(pattern or "")
    if not pat:
        return {"ok": False, "error": "pattern is required"}
    if file_globs is None or not [g for g in file_globs if str(g).strip()]:
        return {"ok": False, "error": "file_globs is required (non-empty)"}

    base_dir = resolve_path(cwd or ".", policy)
    if base_dir.exists() and base_dir.is_file():
        base_dir = base_dir.parent
    if not base_dir.exists() or not base_dir.is_dir():
        return {"ok": False, "error": "cwd does not exist or is not a directory"}

    # Compile matcher
    try:
        if is_regex:
            rx = re.compile(pat)
        else:
            rx = re.compile(re.escape(pat))
    except re.error as e:
        return {"ok": False, "error": f"invalid regex: {e}"}

    targets = _glob_files(base_dir, [str(g) for g in file_globs], [str(e) for e in (exclude_globs or [])])
    if not targets:
        return {"ok": False, "error": "no files matched globs"}

    total_planned = 0
    total_targets = 0
    details: List[Dict[str, Any]] = []
    changed_files = 0
    write_ops: List[Tuple[Path, str]] = []

    for fp in targets:
        # Enforce policy: path must lie within allowed roots, ext allowlist, size limits
        try:
            # Re-resolve via _ap_resolve_target-like checks by going through resolve_path on relative
            # Compute a path relative to base_dir for verify then back to absolute
            rel = fp.relative_to(base_dir)
            p = _ap_resolve_target(base_dir, str(rel), policy)
        except Exception as e:
            details.append({"path": str(fp), "skipped": True, "reason": str(e)})
            continue
        _file_size_ok(p, policy.max_bytes)

        before = read_text_auto(p)
        matches = list(rx.finditer(before))
        if not matches:
            details.append({"path": str(p), "replacements": 0, "targets": 0, "changed": False})
            continue
        # Count all potential targets in this file (prior to caps)
        total_targets += len(matches)
        # Determine how many we can take in this file without exceeding caps
        remaining_global = max(0, int(max_total_replacements) - total_planned)
        if remaining_global <= 0:
            break
        per_file_cap = int(max_replacements_per_file)
        per_file = min(len(matches), per_file_cap, remaining_global)
        if per_file <= 0:
            details.append({"path": str(p), "replacements": 0, "targets": len(matches), "changed": False, "note": "per-file cap is 0"})
            continue
        # Perform only up to per_file replacements, capturing before/after examples for the ones we applied
        # Build the 'after' string manually so we can compute example pairs accurately
        pieces: List[str] = []
        last_end = 0
        did = 0
        examples: List[Dict[str, str]] = []
        for i, m in enumerate(matches):
            if i >= per_file:
                break
            pieces.append(before[last_end:m.start()])
            try:
                rep = m.expand(replacement)
            except Exception:
                # Fallback: use literal replacement if expansion fails
                rep = replacement
            pieces.append(rep)
            last_end = m.end()
            did += 1
            # Record example mapping for this replacement
            try:
                examples.append({"from": m.group(0), "to": rep})
            except Exception:
                pass
        pieces.append(before[last_end:])
        after = "".join(pieces)
        total_planned += did
        if did > 0:
            changed_files += 1
            diff = "\n".join(
                difflib.unified_diff(
                    before.splitlines(), after.splitlines(),
                    fromfile=str(p), tofile=str(p), lineterm=""
                )
            )
            details.append({
                "path": str(p),
                "replacements": did,
                "targets": len(matches),
                "changed": True,
                "examples": examples,  # caller may ignore when not needed
                "diff": diff if dry_run else None,
            })
            write_ops.append((p, after))
        else:
            details.append({"path": str(p), "replacements": 0, "targets": len(matches), "changed": False})

        # Enforce overall cap
        if total_planned >= int(max_total_replacements):
            break

    if expected_total_matches is not None and int(expected_total_matches) != int(total_planned):
        return {
            "ok": False,
            "error": f"expected_total_matches {expected_total_matches} did not match planned replacements {total_planned}",
            "data": {"summary": {"files_considered": len(targets), "files_changed": changed_files, "total_replacements": total_planned}, "details": details}
        }

    if dry_run:
        return {
            "ok": True,
            "data": {
                "summary": {"files_considered": len(targets), "files_changed": changed_files, "total_replacements": total_planned, "total_targets": total_targets},
                "details": details,
                "dry_run": True,
            },
        }

    # Write changes
    for p, after in write_ops:
        _ensure_size_limit_bytes(after, policy.max_bytes)
        _atomic_write(p, after, backup=False)

    return {
        "ok": True,
        "data": {
            "summary": {"files_considered": len(targets), "files_changed": changed_files, "total_replacements": total_planned, "total_targets": total_targets},
            "details": [{k: v for k, v in d.items() if k != "diff"} for d in details],
            "dry_run": False,
        },
    }
