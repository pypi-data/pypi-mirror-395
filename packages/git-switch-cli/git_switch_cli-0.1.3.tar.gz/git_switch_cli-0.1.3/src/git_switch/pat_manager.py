import argparse
import os
import subprocess
import sys
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional

# We intentionally reuse the generic state helpers from the SSH manager
from .ssh_manager import load_state, save_state


@dataclass
class TokenProfile:
    name: str
    username: str
    hosts: List[str]
    git_name: Optional[str] = None
    git_email: Optional[str] = None


def _profile_from_dict(name: str, data: Dict[str, object]) -> TokenProfile:
    return TokenProfile(
        name=name,
        username=str(data.get("username", "")),
        hosts=list(data.get("hosts", ["github.com"])) if isinstance(data.get("hosts"), list) else ["github.com"],
        git_name=data.get("git_name") if isinstance(data.get("git_name"), str) else None,
        git_email=data.get("git_email") if isinstance(data.get("git_email"), str) else None,
    )


def _dict_from_profile(profile: TokenProfile) -> Dict[str, object]:
    d = asdict(profile)
    d.pop("name", None)
    return d


def _git_credential_approve(host: str, username: str, token: str) -> None:
    """Store credentials via the configured Git credential helper.

    This writes to the helper (osxkeychain/libsecret/manager-core/etc) without
    adding any runtime dependency.
    """
    payload = f"protocol=https\nhost={host}\nusername={username}\npassword={token}\n\n".encode("utf-8")
    try:
        subprocess.run(["git", "credential", "approve"], input=payload, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        detail = (e.stderr.decode().strip() if e.stderr else "").strip()
        print(f"Warning: failed to store credential for {host}: {detail}", file=sys.stderr)


def _git_credential_reject(host: str, username: str) -> None:
    payload = f"protocol=https\nhost={host}\nusername={username}\n\n".encode("utf-8")
    try:
        subprocess.run(["git", "credential", "reject"], input=payload, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        # Best-effort erase
        pass


def _apply_git_identity_globally(git_name: Optional[str], git_email: Optional[str]) -> None:
    set_pairs: List[tuple[str, str]] = []
    if git_name:
        set_pairs.append(("user.name", git_name))
    if git_email:
        set_pairs.append(("user.email", git_email))
    unset_keys: List[str] = []
    if not git_name:
        unset_keys.append("user.name")
    if not git_email:
        unset_keys.append("user.email")
    for key, value in set_pairs:
        try:
            subprocess.run(["git", "config", "--global", key, value], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(f"Warning: failed to set git {key}: {e.stderr.decode().strip()}")
    for key in unset_keys:
        try:
            subprocess.run(["git", "config", "--global", "--unset", key], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            pass
    if set_pairs:
        print("Applied Git identity in global config.")
    elif unset_keys:
        print("Cleared Git identity in global config.")
    else:
        print("Note: profile has no git_name/git_email; nothing applied.")


def cmd_add(args: argparse.Namespace) -> int:
    state = load_state()
    token_profiles: Dict[str, Dict[str, object]] = state.get("token_profiles", {})  # type: ignore[assignment]

    name: str = args.name
    username: str = args.username
    hosts: List[str] = [h.strip() for h in (args.hosts or "github.com").split(",") if h.strip()]
    git_name: Optional[str] = getattr(args, "git_name", None)
    git_email: Optional[str] = getattr(args, "git_email", None)

    if not username:
        print("Error: --username is required", file=sys.stderr)
        return 1

    if name in token_profiles:
        print(f"Error: profile '{name}' already exists", file=sys.stderr)
        return 1

    token: Optional[str] = getattr(args, "token", None)
    if getattr(args, "token_stdin", False):
        # Read token from stdin safely
        token = sys.stdin.read().strip()
    if not token:
        print("Error: provide --token or --token-stdin", file=sys.stderr)
        return 1

    # Store credentials for each host
    for host in hosts:
        _git_credential_approve(host, username, token)

    profile = TokenProfile(name=name, username=username, hosts=hosts, git_name=git_name, git_email=git_email)
    token_profiles[name] = _dict_from_profile(profile)
    state["token_profiles"] = token_profiles
    save_state(state)
    print(f"Added PAT profile '{name}'. Stored credentials for hosts: {', '.join(hosts)}")
    return 0


def cmd_list(_: argparse.Namespace) -> int:
    state = load_state()
    token_profiles: Dict[str, Dict[str, object]] = state.get("token_profiles", {})  # type: ignore[assignment]
    active = state.get("active_token_profile")
    if not token_profiles:
        print("No PAT profiles found. Use 'git-switch pat add --name <name> --username <u> --token-stdin' to create one.")
        return 0
    for name, pdata in token_profiles.items():
        p = _profile_from_dict(name, pdata)
        star = "*" if name == active else "-"
        hosts = ",".join(p.hosts)
        print(f"{star} {name}  username={p.username}  hosts=[{hosts}]  git_name={p.git_name or '-'} git_email={p.git_email or '-'}")
    return 0


def cmd_use(args: argparse.Namespace) -> int:
    state = load_state()
    token_profiles: Dict[str, Dict[str, object]] = state.get("token_profiles", {})  # type: ignore[assignment]
    name: str = args.name
    if name not in token_profiles:
        print(f"Error: profile '{name}' not found", file=sys.stderr)
        return 1
    profile = _profile_from_dict(name, token_profiles[name])

    state["active_token_profile"] = name
    save_state(state)
    print(f"Switched active PAT profile to '{name}'.")

    _apply_git_identity_globally(profile.git_name, profile.git_email)

    print("Note: PAT authentication works with HTTPS remotes. If your remotes use SSH, convert them, e.g.:\n  git remote set-url origin https://<host>/<owner>/<repo>.git")
    return 0


def cmd_remove(args: argparse.Namespace) -> int:
    state = load_state()
    token_profiles: Dict[str, Dict[str, object]] = state.get("token_profiles", {})  # type: ignore[assignment]
    name: str = args.name
    if name not in token_profiles:
        print(f"Error: profile '{name}' not found", file=sys.stderr)
        return 1

    pdata = token_profiles.pop(name)
    profile = _profile_from_dict(name, pdata)
    # Erase stored credentials
    for host in profile.hosts:
        _git_credential_reject(host, profile.username)

    # Update state
    state["token_profiles"] = token_profiles
    if state.get("active_token_profile") == name:
        state["active_token_profile"] = None
    save_state(state)
    print(f"Removed PAT profile '{name}'.")
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    state = load_state()
    token_profiles: Dict[str, Dict[str, object]] = state.get("token_profiles", {})  # type: ignore[assignment]
    name: str = args.name
    if name not in token_profiles:
        print(f"Error: profile '{name}' not found", file=sys.stderr)
        return 1
    profile = _profile_from_dict(name, token_profiles[name])

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

    token_profiles[name] = _dict_from_profile(profile)
    state["token_profiles"] = token_profiles
    save_state(state)
    print(f"Updated PAT profile '{name}'. git_name={profile.git_name or '-'} git_email={profile.git_email or '-'}")
    return 0


def build_pat_subparser(subparsers: argparse._SubParsersAction) -> None:
    pat_parser = subparsers.add_parser("pat", help="Manage Git HTTPS (PAT) profiles")
    pat_sub = pat_parser.add_subparsers(dest="pat_cmd", required=True)

    p_add = pat_sub.add_parser("add", help="Add a PAT profile and store credentials via Git helper")
    p_add.add_argument("--name", required=True, help="Profile name (e.g., work, personal)")
    p_add.add_argument("--username", required=True, help="Username for HTTPS auth (e.g., GitHub username)")
    p_add.add_argument("--hosts", required=False, help="Comma-separated hosts (default: github.com)")
    p_add.add_argument("--git-name", dest="git_name", required=False, help="Git user.name for this profile")
    p_add.add_argument("--git-email", dest="git_email", required=False, help="Git user.email for this profile")
    group = p_add.add_mutually_exclusive_group(required=True)
    group.add_argument("--token", help="Personal access token (NOT RECOMMENDED: shows in process list)")
    group.add_argument("--token-stdin", action="store_true", help="Read token from stdin for safety")
    p_add.set_defaults(func=cmd_add)

    p_list = pat_sub.add_parser("list", help="List PAT profiles and show active")
    p_list.set_defaults(func=cmd_list)

    p_use = pat_sub.add_parser("use", help="Activate a PAT profile and apply Git identity")
    p_use.add_argument("--name", required=True, help="Profile name to activate")
    p_use.set_defaults(func=cmd_use)

    p_update = pat_sub.add_parser("update", help="Update a PAT profile's Git identity")
    p_update.add_argument("--name", required=True, help="Profile name to update")
    p_update.add_argument("--git-name", dest="git_name", required=False, help="New Git user.name for this profile")
    p_update.add_argument("--git-email", dest="git_email", required=False, help="New Git user.email for this profile")
    p_update.set_defaults(func=cmd_update)

    p_rm = pat_sub.add_parser("remove", help="Remove a PAT profile and erase stored credentials")
    p_rm.add_argument("--name", required=True, help="Profile name to remove")
    p_rm.set_defaults(func=cmd_remove)


def handle_pat_command(args: argparse.Namespace) -> int:
    if hasattr(args, "func"):
        return args.func(args)
    print("No PAT subcommand provided. See --help.", file=sys.stderr)
    return 2

