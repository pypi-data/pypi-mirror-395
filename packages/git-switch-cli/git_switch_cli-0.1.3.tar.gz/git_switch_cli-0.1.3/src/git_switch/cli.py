#!/usr/bin/env python3
import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

from .ssh_manager import build_ssh_subparser, handle_ssh_command, load_state
from .pat_manager import build_pat_subparser, handle_pat_command
from . import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="git-switch", description="Developer utilities")
    parser.add_argument("--version", action="store_true", help="Print version and exit")
    subparsers = parser.add_subparsers(dest="command", required=False)

    # SSH manager
    build_ssh_subparser(subparsers)

    # PAT manager
    build_pat_subparser(subparsers)

    # Convenience: copy-key (copies public key of a profile or active one)
    p_copy = subparsers.add_parser(
        "copy-key", help="Copy a profile's public SSH key to clipboard (defaults to active)"
    )
    p_copy.add_argument("name", nargs="?", help="Profile name; defaults to active profile")
    p_copy.set_defaults(func=handle_copy_key)

    # Default action prints greeting
    parser.set_defaults(func=lambda _args: (print("Hello from git-switch 👋") or 0))
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if getattr(args, "version", False):
        print(__version__)
        return 0
    if getattr(args, "command", None) == "ssh":
        return handle_ssh_command(args)
    if getattr(args, "command", None) == "pat":
        return handle_pat_command(args)
    func = getattr(args, "func", None)
    if callable(func):
        return int(func(args))
    parser.print_help()
    return 0


def handle_copy_key(args: argparse.Namespace) -> int:
    state = load_state()
    profiles = state.get("profiles", {})  # type: ignore[assignment]
    active = state.get("active_profile")
    name: Optional[str] = args.name or active  # type: ignore[attr-defined]
    if not name:
        print("Error: no profile name provided and no active profile set.", file=sys.stderr)
        return 1
    if name not in profiles:
        print(f"Error: profile '{name}' not found.", file=sys.stderr)
        return 1
    pub_path_str = profiles[name].get("public_key_path")  # type: ignore[index]
    if not pub_path_str:
        print("Error: public_key_path missing for profile.", file=sys.stderr)
        return 1
    pub_path = Path(pub_path_str).expanduser()
    if not pub_path.exists():
        print(f"Error: public key not found at {pub_path}", file=sys.stderr)
        return 1
    key_text = pub_path.read_text(encoding="utf-8")

    def try_run(cmd: List[str]) -> bool:
        try:
            subprocess.run(cmd, input=key_text.encode("utf-8"), check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except Exception:
            return False

    # macOS
    if shutil.which("pbcopy") and try_run(["pbcopy"]):
        print(f"Copied public key for '{name}' to clipboard.")
        return 0
    # Wayland/Linux
    if shutil.which("wl-copy") and try_run(["wl-copy"]):
        print(f"Copied public key for '{name}' to clipboard (wl-copy).")
        return 0
    if shutil.which("xclip") and try_run(["xclip", "-selection", "clipboard"]):
        print(f"Copied public key for '{name}' to clipboard (xclip).")
        return 0
    # Windows
    if shutil.which("clip") and try_run(["clip"]):
        print(f"Copied public key for '{name}' to clipboard (clip).")
        return 0

    # Fallback: print to stdout
    print(key_text, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
