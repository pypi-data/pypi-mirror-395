"""
Entrypoint wrapper for the henosis chat CLI.

Why this exists
- Some earlier wheels accidentally omitted the top-level cli.py module.
- Pointing the console_script at this small wrapper ensures we always
  import lazily and can show a helpful error if the module is missing.

Runtime behavior
- Try to import cli.main (the chat client) and run it.
- If unavailable, print a concise fix hint and exit 1.
"""

from __future__ import annotations

import sys


def main() -> None:  # console entrypoint
    try:
        # Defer heavy imports so the thin wrapper stays fast and robust
        import importlib

        mod = importlib.import_module("cli")
        run = getattr(mod, "main", None)
        if callable(run):
            run()
            return
        # Fallback: try module-level asyncio entry when available
        amain = getattr(mod, "amain", None)
        if callable(amain):
            import asyncio

            try:
                asyncio.run(amain())
            except KeyboardInterrupt:
                print("\nInterrupted.")
            return
        raise ImportError("cli module found but no runnable entry (main/amain)")
    except Exception as e:
        # Friendly self-heal guidance
        msg = (
            "henosis-cli entry module not found. This usually means an older or corrupted install.\n"
            "Fix: upgrade/reinstall the package:\n"
            f"- {sys.executable} -m pip install --no-cache-dir -U henosis-cli\n"
            "- or: pipx reinstall henosis-cli\n\n"
            f"Details: {type(e).__name__}: {e}"
        )
        try:
            sys.stderr.write(msg + "\n")
        except Exception:
            print(msg)
        raise SystemExit(1)
