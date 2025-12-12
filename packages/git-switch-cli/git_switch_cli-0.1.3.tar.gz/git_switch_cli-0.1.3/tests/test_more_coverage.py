import argparse
import runpy
from pathlib import Path

import pytest

from git_switch import ssh_manager as sm
from pathlib import Path as _Path


def test_cli_main_module_executes():
    # Ensure __main__ branch in cli.py is executed without crashing
    with pytest.raises(SystemExit):
        runpy.run_module("git_switch.cli", run_name="__main__")


def test_ensure_include_in_ssh_config_file_open_error(isolate_paths, monkeypatch):
    # Force Path.open to raise FileNotFoundError only for SSH_CONFIG_FILE
    original_open = _Path.open

    def guarded_open(self, *args, **kwargs):
        mode = args[0] if args else kwargs.get("mode", "r")
        if self == sm.SSH_CONFIG_FILE and "r" in mode:
            raise FileNotFoundError()
        return original_open(self, *args, **kwargs)

    monkeypatch.setattr(_Path, "open", guarded_open, raising=True)
    sm.ensure_include_in_ssh_config()


def test_cmd_add_key_path_missing(isolate_paths, capsys, tmp_path):
    sm.save_state({"profiles": {}, "active_profile": None})
    rc = sm.cmd_add(argparse.Namespace(name="p", email=None, git_name=None, git_email=None, hosts=None, key_path=str(tmp_path/"nope"), generate=False, force=False))
    err = capsys.readouterr().err
    assert rc == 1
    assert "key path does not exist" in err


def test_cmd_add_pub_missing(isolate_paths, capsys, tmp_path):
    sm.save_state({"profiles": {}, "active_profile": None})
    priv = tmp_path / "id_ed25519"
    priv.write_text("priv", encoding="utf-8")
    rc = sm.cmd_add(argparse.Namespace(name="p", email=None, git_name=None, git_email=None, hosts=None, key_path=str(priv), generate=False, force=False))
    err = capsys.readouterr().err
    assert rc == 1
    assert "public key not found" in err


def test_cmd_add_force_remove_existing_files_error(isolate_paths, capsys, monkeypatch):
    sm.save_state({"profiles": {}, "active_profile": None})
    key = sm.MANAGED_DIR / "p" / "id_ed25519"
    key.parent.mkdir(parents=True, exist_ok=True)
    key.write_text("x", encoding="utf-8")
    key.with_suffix(".pub").write_text("y", encoding="utf-8")

    def boom_unlink(self):
        raise RuntimeError("boom")

    monkeypatch.setattr(Path, "unlink", boom_unlink, raising=False)
    rc = sm.cmd_add(argparse.Namespace(name="p", email=None, git_name=None, git_email=None, hosts=None, key_path=None, generate=True, force=True))
    err = capsys.readouterr().err
    assert rc == 1
    assert "failed to remove existing key files" in err


def test_cmd_use_warn_on_set_git_failure(isolate_paths, capsys, monkeypatch):
    st = {"profiles": {"p": {"key_path": "/k", "public_key_path": "/k.pub", "hosts": ["h"], "git_name": "N", "git_email": "E"}}, "active_profile": None}
    sm.save_state(st)

    def fake_run(cmd, **kwargs):
        if cmd[:2] == ["git", "config"] and len(cmd) > 3 and cmd[-2] in {"user.name", "user.email"}:
            raise sm.subprocess.CalledProcessError(returncode=1, cmd=cmd, output=b"", stderr=b"bad")
        class R:
            stdout = b""
            stderr = b""
        return R()

    monkeypatch.setattr(sm.subprocess, "run", fake_run)
    rc = sm.cmd_use(argparse.Namespace(name="p", apply_global=True))
    out = capsys.readouterr().out
    assert rc == 0
    assert "Warning: failed to set git" in out


def test_cmd_use_unset_keys_ignores_errors(isolate_paths, capsys, monkeypatch):
    st = {"profiles": {"p": {"key_path": "/k", "public_key_path": "/k.pub", "hosts": ["h"]}}, "active_profile": None}
    sm.save_state(st)

    def fake_run(cmd, **kwargs):
        if cmd[:4] == ["git", "config", "--global", "--unset"]:
            raise sm.subprocess.CalledProcessError(returncode=1, cmd=cmd, output=b"", stderr=b"")
        class R:
            stdout = b""
            stderr = b""
        return R()

    monkeypatch.setattr(sm.subprocess, "run", fake_run)
    rc = sm.cmd_use(argparse.Namespace(name="p", apply_global=False))
    assert rc == 0
    # Ensure message for no identity when no set/unset performed
    st = {"profiles": {"q": {"key_path": "/k", "public_key_path": "/k.pub", "hosts": ["h"], "git_name": None, "git_email": None}}, "active_profile": None}
    sm.save_state(st)

    def fake_run2(cmd, **kwargs):
        # Simulate not inside a repo to hit try/except path later too
        if cmd[:3] == ["git", "rev-parse", "--is-inside-work-tree"]:
            raise sm.subprocess.CalledProcessError(returncode=1, cmd=cmd, output=b"", stderr=b"")
        class R:
            stdout = b""
            stderr = b""
        return R()

    monkeypatch.setattr(sm.subprocess, "run", fake_run2)
    capsys.readouterr()
    rc = sm.cmd_use(argparse.Namespace(name="q", apply_global=False))
    io = capsys.readouterr()
    assert rc == 0
    assert "Cleared Git identity in global config." in io.out


def test_cmd_use_rev_parse_failure_path(isolate_paths, monkeypatch):
    st = {"profiles": {"p": {"key_path": "/k", "public_key_path": "/k.pub", "hosts": ["h"], "git_name": "N", "git_email": "E"}}, "active_profile": None}
    sm.save_state(st)

    def fake_run(cmd, **kwargs):
        if cmd[:3] == ["git", "rev-parse", "--is-inside-work-tree"]:
            raise sm.subprocess.CalledProcessError(returncode=1, cmd=cmd, output=b"", stderr=b"")
        class R:
            stdout = b""
            stderr = b""
        return R()

    monkeypatch.setattr(sm.subprocess, "run", fake_run)
    rc = sm.cmd_use(argparse.Namespace(name="p", apply_global=True))
    assert rc == 0


def test_cmd_use_inside_repo_unset_local_errors_are_ignored(isolate_paths, monkeypatch):
    st = {"profiles": {"p": {"key_path": "/k", "public_key_path": "/k.pub", "hosts": ["h"], "git_name": "N", "git_email": "E"}}, "active_profile": None}
    sm.save_state(st)

    def fake_run(cmd, **kwargs):
        if cmd[:3] == ["git", "rev-parse", "--is-inside-work-tree"]:
            class R:
                stdout = b"true"
                stderr = b""
            return R()
        if cmd[:3] == ["git", "config", "--unset"]:
            raise sm.subprocess.CalledProcessError(returncode=1, cmd=cmd, output=b"", stderr=b"")
        class R:
            stdout = b""
            stderr = b""
        return R()

    monkeypatch.setattr(sm.subprocess, "run", fake_run)
    rc = sm.cmd_use(argparse.Namespace(name="p", apply_global=True))
    assert rc == 0


def test_cmd_remove_rmdir_ignores_oserror(isolate_paths, capsys, monkeypatch):
    key = sm.MANAGED_DIR / "p" / "id_ed25519"
    key.parent.mkdir(parents=True, exist_ok=True)
    key.write_text("x", encoding="utf-8")
    key.with_suffix(".pub").write_text("y", encoding="utf-8")
    st = {"profiles": {"p": {"key_path": str(key), "public_key_path": str(key.with_suffix(".pub")), "hosts": ["h"]}}, "active_profile": None}
    sm.save_state(st)

    def boom_rmdir(self):
        raise OSError("busy")

    monkeypatch.setattr(Path, "rmdir", boom_rmdir, raising=False)
    rc = sm.cmd_remove(argparse.Namespace(name="p", force=True, delete_keys=True))
    out = capsys.readouterr().out
    assert rc == 0
    assert "Deleted managed key files" in out


def test_cmd_remove_active_with_force_updates_state(isolate_paths, capsys):
    key = sm.MANAGED_DIR / "p" / "id_ed25519"
    key.parent.mkdir(parents=True, exist_ok=True)
    key.write_text("x", encoding="utf-8")
    key.with_suffix(".pub").write_text("y", encoding="utf-8")
    st = {"profiles": {"p": {"key_path": str(key), "public_key_path": str(key.with_suffix(".pub")), "hosts": ["h"]}}, "active_profile": "p"}
    sm.save_state(st)
    rc = sm.cmd_remove(argparse.Namespace(name="p", force=True, delete_keys=False))
    assert rc == 0
    assert sm.load_state()["active_profile"] is None


def test_handle_ssh_command_calls_func():
    called = {}
    def f(args):
        called["x"] = True
        return 42
    rc = sm.handle_ssh_command(argparse.Namespace(func=f))
    assert rc == 42
    assert called.get("x") is True

