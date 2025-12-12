import argparse
import json
import os
import shlex
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# Paths and constants
HOME_DIR = Path.home()
CONFIG_DIR = HOME_DIR / ".config" / "git-switch"
PROFILES_FILE = CONFIG_DIR / "profiles.json"
SSH_DIR = HOME_DIR / ".ssh"
MANAGED_DIR = SSH_DIR / "git-switch"
INCLUDE_FILE = SSH_DIR / "git-switch-managed.conf"
SSH_CONFIG_FILE = SSH_DIR / "config"
MANAGED_HEADER = (
    "# ----- BEGIN git-switch managed block -----\n"
    "# This file is auto-generated. Do not edit manually.\n"
    "# Use `git-switch ssh use <profile>` to switch keys.\n"
)
MANAGED_FOOTER = "# ----- END git-switch managed block -----\n"


@dataclass
class Profile:
    name: str
    key_path: str
    public_key_path: str
    email: Optional[str]
    hosts: List[str]
    git_name: Optional[str] = None
    git_email: Optional[str] = None


def ensure_directories() -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    SSH_DIR.mkdir(parents=True, exist_ok=True)
    MANAGED_DIR.mkdir(parents=True, exist_ok=True)


def _chmod_secure(file_path: Path, mode: int) -> None:
    try:
        os.chmod(file_path, mode)
    except PermissionError:
        pass


def load_state() -> Dict[str, object]:
    ensure_directories()
    if not PROFILES_FILE.exists():
        return {"profiles": {}, "active_profile": None}
    try:
        with PROFILES_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return {"profiles": {}, "active_profile": None}
    if "profiles" not in data or not isinstance(data["profiles"], dict):
        data["profiles"] = {}
    if "active_profile" not in data:
        data["active_profile"] = None
    return data


def save_state(state: Dict[str, object]) -> None:
    ensure_directories()
    tmp_path = PROFILES_FILE.with_suffix(".tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
    tmp_path.replace(PROFILES_FILE)


def profile_from_dict(name: str, data: Dict[str, object]) -> Profile:
    return Profile(
        name=name,
        key_path=str(data.get("key_path", "")),
        public_key_path=str(data.get("public_key_path", "")),
        email=data.get("email") if isinstance(data.get("email"), str) else None,
        hosts=list(data.get("hosts", ["github.com"])) if isinstance(data.get("hosts"), list) else ["github.com"],
        git_name=data.get("git_name") if isinstance(data.get("git_name"), str) else None,
        git_email=(data.get("git_email") if isinstance(data.get("git_email"), str) else None)
        or (data.get("email") if isinstance(data.get("email"), str) else None),
    )


def dict_from_profile(profile: Profile) -> Dict[str, object]:
    d = asdict(profile)
    # Persist fields except name (used as key)
    d.pop("name", None)
    return d


def generate_ed25519_key(key_path: Path, comment: str) -> Tuple[Path, Path]:
    ensure_directories()
    key_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ssh-keygen",
        "-t",
        "ed25519",
        "-C",
        comment,
        "-f",
        str(key_path),
        "-N",
        "",
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("Error: ssh-keygen not found. Please install OpenSSH tools.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        stderr = (e.stderr.decode().strip() if e.stderr else "").strip()
        stdout = (e.stdout.decode().strip() if e.stdout else "").strip()
        detail = stderr or stdout or "ssh-keygen failed"
        print(f"Error generating key: {detail}", file=sys.stderr)
        print("Hint: If the key file already exists, use --force or remove it.", file=sys.stderr)
        sys.exit(1)
    priv = key_path
    pub = key_path.with_suffix(".pub")
    _chmod_secure(priv, 0o600)
    if pub.exists():
        _chmod_secure(pub, 0o644)
    return priv, pub


def ensure_include_in_ssh_config() -> None:
    ensure_directories()
    if not SSH_CONFIG_FILE.exists():
        SSH_CONFIG_FILE.touch()
        _chmod_secure(SSH_CONFIG_FILE, 0o600)
    # Ensure Include line exists
    include_line = f"Include {INCLUDE_FILE}\n"
    try:
        with SSH_CONFIG_FILE.open("r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []
    normalized = [l.strip() for l in lines]
    if any(l.lower().startswith("include ") and INCLUDE_FILE.name in l for l in normalized):
        return
    # Prepend include at the top for precedence
    new_lines = [include_line]
    new_lines.extend(lines)
    with SSH_CONFIG_FILE.open("w", encoding="utf-8") as f:
        f.writelines(new_lines)


def write_include_for_profile(profile: Profile) -> None:
    ensure_directories()
    lines: List[str] = []
    lines.append(MANAGED_HEADER)
    key_path = Path(profile.key_path)
    for host in profile.hosts:
        lines.append(f"Host {host}\n")
        lines.append(f"    HostName {host}\n")
        lines.append("    User git\n")
        lines.append(f"    IdentityFile {key_path}\n")
        lines.append("    IdentitiesOnly yes\n\n")
    lines.append(MANAGED_FOOTER)
    with INCLUDE_FILE.open("w", encoding="utf-8") as f:
        f.writelines(lines)
    _chmod_secure(INCLUDE_FILE, 0o600)


def cmd_init(_: argparse.Namespace) -> int:
    ensure_directories()
    ensure_include_in_ssh_config()
    if not INCLUDE_FILE.exists():
        with INCLUDE_FILE.open("w", encoding="utf-8") as f:
            f.write(MANAGED_HEADER + MANAGED_FOOTER)
        _chmod_secure(INCLUDE_FILE, 0o600)
    print(f"Initialized SSH config include at: {INCLUDE_FILE}")
    print(f"Profiles store: {PROFILES_FILE}")
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    state = load_state()
    profiles: Dict[str, Dict[str, object]] = state["profiles"]  # type: ignore[assignment]
    name: str = args.name
    email: Optional[str] = args.email
    git_name: Optional[str] = getattr(args, "git_name", None)
    git_email: Optional[str] = getattr(args, "git_email", None)
    hosts: List[str] = [h.strip() for h in (args.hosts or "github.com").split(",") if h.strip()]

    if name in profiles:
        print(f"Error: profile '{name}' already exists", file=sys.stderr)
        return 1

    if args.key_path:
        key_path = Path(os.path.expanduser(args.key_path))
        pub_path = key_path.with_suffix(".pub")
        if not key_path.exists():
            print(f"Error: key path does not exist: {key_path}", file=sys.stderr)
            return 1
        if not pub_path.exists():
            print(f"Error: public key not found next to private key: {pub_path}", file=sys.stderr)
            return 1
    else:
        default_key_dir = MANAGED_DIR / name
        key_path = default_key_dir / "id_ed25519"
        comment = email or name
        # Handle existing files
        if key_path.exists() or key_path.with_suffix(".pub").exists():
            if getattr(args, "force", False):
                try:
                    if key_path.exists():
                        key_path.unlink()
                    pub_existing = key_path.with_suffix(".pub")
                    if pub_existing.exists():
                        pub_existing.unlink()
                except Exception as e:
                    print(f"Error: failed to remove existing key files: {e}", file=sys.stderr)
                    return 1
            else:
                print(f"Error: key already exists at {key_path}. Use --force to overwrite.", file=sys.stderr)
                return 1
        print(f"Generating ed25519 key at: {key_path}")
        priv, pub_path = generate_ed25519_key(key_path, comment)
        key_path = priv

    profile = Profile(
        name=name,
        key_path=str(key_path),
        public_key_path=str(key_path.with_suffix(".pub")),
        email=email,
        hosts=hosts,
        git_name=git_name,
        git_email=git_email or email,
    )
    profiles[name] = dict_from_profile(profile)
    save_state(state)
    print(f"Added profile '{name}'.")
    print(f"Public key: {profile.public_key_path}")
    return 0


def cmd_list(_: argparse.Namespace) -> int:
    state = load_state()
    profiles: Dict[str, Dict[str, object]] = state["profiles"]  # type: ignore[assignment]
    active = state.get("active_profile")
    if not profiles:
        print("No profiles found. Use 'git-switch ssh add --name <name> --generate' to create one.")
        return 0
    for name, pdata in profiles.items():
        p = profile_from_dict(name, pdata)
        star = "*" if name == active else "-"
        hosts = ",".join(p.hosts)
        print(f"{star} {name}  key={p.key_path}  hosts=[{hosts}]  email={p.email or '-'}")
    return 0


def cmd_use(args: argparse.Namespace) -> int:
    state = load_state()
    profiles: Dict[str, Dict[str, object]] = state["profiles"]  # type: ignore[assignment]
    name: str = args.name
    if name not in profiles:
        print(f"Error: profile '{name}' not found", file=sys.stderr)
        return 1
    profile = profile_from_dict(name, profiles[name])
    ensure_include_in_ssh_config()
    write_include_for_profile(profile)
    state["active_profile"] = name
    save_state(state)
    print(f"Switched active profile to '{name}'.")
    print(f"Updated include file: {INCLUDE_FILE}")

    # Always apply Git identity globally (deprecated: --apply-git/--global are ignored if provided)
    scope_args: List[str] = ["--global"]
    cwd = None
    set_pairs = []
    if profile.git_name:
        set_pairs.append(("user.name", profile.git_name))
    if profile.git_email:
        set_pairs.append(("user.email", profile.git_email))
    # Unset keys that are not specified on this profile to avoid stale values
    unset_keys: List[str] = []
    if not profile.git_name:
        unset_keys.append("user.name")
    if not profile.git_email:
        unset_keys.append("user.email")
    for key, value in set_pairs:
        cmd = ["git", "config"] + scope_args + [key, value]
        try:
            subprocess.run(cmd, check=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(f"Warning: failed to set git {key}: {e.stderr.decode().strip()}")
    # Attempt to clear unspecified keys; ignore errors if they weren't set
    for key in unset_keys:
        cmd = ["git", "config", "--global", "--unset", key]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            pass
    if set_pairs:
        print("Applied Git identity in global config.")
    elif unset_keys:
        print("Cleared Git identity in global config.")
    else:
        print("Note: profile has no git_name/git_email; nothing applied.")  # pragma: no cover

    # Also clear any local repo overrides so global values take effect
    try:
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        pass
    else:
        for key in ["user.name", "user.email"]:
            try:
                subprocess.run(["git", "config", "--unset", key], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError:
                pass
    return 0


def cmd_remove(args: argparse.Namespace) -> int:
    state = load_state()
    profiles: Dict[str, Dict[str, object]] = state["profiles"]  # type: ignore[assignment]
    name: str = args.name
    if name not in profiles:
        print(f"Error: profile '{name}' not found", file=sys.stderr)
        return 1
    # Prevent removing active without confirmation flag
    if state.get("active_profile") == name and not args.force:
        print("Error: profile is active. Use --force to remove.", file=sys.stderr)
        return 1
    # Optionally remove generated key files if they live under MANAGED_DIR
    pdata = profiles.pop(name)
    save_state(state)
    if args.delete_keys:
        key_path = Path(str(pdata.get("key_path", "")))
        if str(key_path).startswith(str(MANAGED_DIR)):
            try:
                if key_path.exists():
                    key_path.unlink()
                pub_path = key_path.with_suffix(".pub")
                if pub_path.exists():
                    pub_path.unlink()
                # Remove parent dir if empty
                try:
                    key_path.parent.rmdir()
                except OSError:
                    pass
                print("Deleted managed key files.")
            except Exception as e:
                print(f"Warning: failed to delete key files: {e}")
        else:
            print("Skipped deleting keys (not under managed directory).")
    if state.get("active_profile") == name:
        state["active_profile"] = None
        save_state(state)
    print(f"Removed profile '{name}'.")
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    state = load_state()
    profiles: Dict[str, Dict[str, object]] = state["profiles"]  # type: ignore[assignment]
    name: str = args.name
    if name not in profiles:
        print(f"Error: profile '{name}' not found", file=sys.stderr)
        return 1
    profile = profile_from_dict(name, profiles[name])

    changed = False
    if getattr(args, "git_name", None) is not None:
        profile.git_name = args.git_name
        changed = True
    if getattr(args, "git_email", None) is not None:
        profile.git_email = args.git_email
        changed = True

    if not changed:
        print("Error: nothing to update. Provide --git-name and/or --git-email.", file=sys.stderr)
        return 1

    profiles[name] = dict_from_profile(profile)
    save_state(state)
    print(f"Updated profile '{name}'. git_name={profile.git_name or '-'} git_email={profile.git_email or '-'}")
    return 0


def build_ssh_subparser(subparsers: argparse._SubParsersAction) -> None:
    ssh_parser = subparsers.add_parser("ssh", help="Manage Git SSH profiles")
    ssh_sub = ssh_parser.add_subparsers(dest="ssh_cmd", required=True)

    p_init = ssh_sub.add_parser("init", help="Initialize managed SSH include and config store")
    p_init.set_defaults(func=cmd_init)

    p_add = ssh_sub.add_parser("add", help="Add a profile (optionally generate an ed25519 key)")
    p_add.add_argument("--name", required=True, help="Profile name (e.g., work, personal)")
    p_add.add_argument("--email", required=False, help="Email/comment for the key")
    p_add.add_argument("--hosts", required=False, help="Comma-separated hosts (default: github.com)")
    p_add.add_argument("--git-name", dest="git_name", required=False, help="Git user.name for this profile")
    p_add.add_argument("--git-email", dest="git_email", required=False, help="Git user.email for this profile")
    p_add.add_argument("--force", action="store_true", help="Overwrite existing key files if present (when --generate)")
    group = p_add.add_mutually_exclusive_group(required=False)
    group.add_argument("--generate", action="store_true", help="Generate a new ed25519 key")
    group.add_argument("--key-path", help="Path to an existing private key to use")
    p_add.set_defaults(func=cmd_add)

    p_list = ssh_sub.add_parser("list", help="List profiles and show active")
    p_list.set_defaults(func=cmd_list)

    p_use = ssh_sub.add_parser("use", help="Activate a profile, update SSH include, and apply Git identity")
    p_use.add_argument("--name", required=True, help="Profile name to activate")
    # --apply-git is deprecated; kept for backward compatibility as a no-op
    p_use.add_argument("--apply-git", action="store_true", help=argparse.SUPPRESS)
    # --global is deprecated; always applied globally now
    p_use.add_argument("--global", dest="apply_global", action="store_true", help=argparse.SUPPRESS)
    p_use.set_defaults(func=cmd_use)

    p_update = ssh_sub.add_parser("update", help="Update a profile's Git identity")
    p_update.add_argument("--name", required=True, help="Profile name to update")
    p_update.add_argument("--git-name", dest="git_name", required=False, help="New Git user.name for this profile")
    p_update.add_argument("--git-email", dest="git_email", required=False, help="New Git user.email for this profile")
    p_update.set_defaults(func=cmd_update)

    p_rm = ssh_sub.add_parser("remove", help="Remove a profile")
    p_rm.add_argument("--name", required=True, help="Profile name to remove")
    p_rm.add_argument("--force", action="store_true", help="Allow removing the active profile")
    p_rm.add_argument("--delete-keys", action="store_true", help="Also delete managed key files if owned")
    p_rm.set_defaults(func=cmd_remove)


def handle_ssh_command(args: argparse.Namespace) -> int:
    if hasattr(args, "func"):
        return args.func(args)
    print("No SSH subcommand provided. See --help.", file=sys.stderr)
    return 2
