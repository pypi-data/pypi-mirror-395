import argparse
import json
from pathlib import Path

import pytest

from git_switch import ssh_manager as sm


def ns(**kwargs):
    return argparse.Namespace(**kwargs)


def test_cmd_init_creates_include(isolate_paths, capsys):
    rc = sm.cmd_init(ns())
    out = capsys.readouterr().out
    assert rc == 0
    assert sm.INCLUDE_FILE.exists()
    assert "Initialized SSH config include" in out


def test_cmd_add_existing_profile_errors(isolate_paths, capsys):
    state = {"profiles": {"p": {"key_path": "/k", "public_key_path": "/k.pub", "hosts": ["h"]}}, "active_profile": None}
    sm.save_state(state)
    rc = sm.cmd_add(ns(name="p", email=None, git_name=None, git_email=None, hosts=None, key_path=None, generate=False, force=False))
    err = capsys.readouterr().err
    assert rc == 1
    assert "already exists" in err


def test_cmd_add_with_key_path_success(isolate_paths, capsys, tmp_path):
    priv = tmp_path / "id_ed25519"
    pub = tmp_path / "id_ed25519.pub"
    priv.write_text("priv", encoding="utf-8")
    pub.write_text("pub", encoding="utf-8")
    sm.save_state({"profiles": {}, "active_profile": None})
    rc = sm.cmd_add(ns(name="p", email=None, git_name=None, git_email=None, hosts="github.com", key_path=str(priv), generate=False, force=False))
    out = capsys.readouterr().out
    assert rc == 0
    st = sm.load_state()
    assert "p" in st["profiles"]
    assert "Public key:" in out


def test_cmd_add_generate_key_exists_without_force(isolate_paths, capsys, monkeypatch):
    sm.save_state({"profiles": {}, "active_profile": None})
    # Pre-create files to trigger exists branch
    key = sm.MANAGED_DIR / "p" / "id_ed25519"
    key.parent.mkdir(parents=True, exist_ok=True)
    key.write_text("x", encoding="utf-8")
    key.with_suffix(".pub").write_text("x", encoding="utf-8")
    rc = sm.cmd_add(ns(name="p", email=None, git_name=None, git_email=None, hosts=None, key_path=None, generate=True, force=False))
    err = capsys.readouterr().err
    assert rc == 1
    assert "Use --force to overwrite" in err


def test_cmd_add_generate_key_with_force_removes_and_generates(isolate_paths, capsys, monkeypatch):
    sm.save_state({"profiles": {}, "active_profile": None})
    key = sm.MANAGED_DIR / "p" / "id_ed25519"
    key.parent.mkdir(parents=True, exist_ok=True)
    key.write_text("x", encoding="utf-8")
    key.with_suffix(".pub").write_text("x", encoding="utf-8")

    def fake_gen(dst, comment):
        return dst, dst.with_suffix(".pub")

    monkeypatch.setattr(sm, "generate_ed25519_key", fake_gen)
    rc = sm.cmd_add(ns(name="p", email="e@x", git_name=None, git_email=None, hosts="github.com", key_path=None, generate=True, force=True))
    out = capsys.readouterr().out
    assert rc == 0
    st = sm.load_state()
    assert "p" in st["profiles"]
    assert "Added profile" in out


def test_cmd_list_empty(isolate_paths, capsys):
    sm.save_state({"profiles": {}, "active_profile": None})
    rc = sm.cmd_list(ns())
    out = capsys.readouterr().out
    assert rc == 0
    assert "No profiles found" in out


def test_cmd_list_non_empty_with_active(isolate_paths, capsys):
    st = {"profiles": {"a": {"key_path": "/k", "public_key_path": "/k.pub", "hosts": ["h"], "email": None},
                         "b": {"key_path": "/k2", "public_key_path": "/k2.pub", "hosts": ["h2"], "email": None}},
          "active_profile": "b"}
    sm.save_state(st)
    rc = sm.cmd_list(ns())
    out = capsys.readouterr().out
    assert rc == 0
    assert "* b" in out
    assert "- a" in out


def test_cmd_use_profile_not_found(isolate_paths, capsys):
    sm.save_state({"profiles": {}, "active_profile": None})
    rc = sm.cmd_use(ns(name="missing", apply_global=False))
    err = capsys.readouterr().err
    assert rc == 1
    assert "not found" in err


def test_cmd_use_applies_identity_and_writes_include(isolate_paths, monkeypatch, capsys):
    st = {"profiles": {"p": {"key_path": "/k", "public_key_path": "/k.pub", "hosts": ["h"], "git_name": "N", "git_email": "E"}}, "active_profile": None}
    sm.save_state(st)

    calls = {"ensure": 0, "write": 0, "git": 0}

    def fake_ensure():
        calls["ensure"] += 1

    def fake_write(profile):
        calls["write"] += 1

    def fake_run(cmd, **kwargs):
        calls["git"] += 1
        class R:
            stdout = b""
            stderr = b""
        return R()

    monkeypatch.setattr(sm, "ensure_include_in_ssh_config", fake_ensure)
    monkeypatch.setattr(sm, "write_include_for_profile", fake_write)
    monkeypatch.setattr(sm.subprocess, "run", fake_run)

    rc = sm.cmd_use(ns(name="p", apply_global=True))
    out = capsys.readouterr().out
    assert rc == 0
    assert "Applied Git identity" in out
    assert calls["ensure"] == 1 and calls["write"] == 1 and calls["git"] >= 2
    assert sm.load_state()["active_profile"] == "p"


def test_cmd_use_clears_identity_when_none(isolate_paths, monkeypatch, capsys):
    st = {"profiles": {"p": {"key_path": "/k", "public_key_path": "/k.pub", "hosts": ["h"]}}, "active_profile": None}
    sm.save_state(st)

    def fake_run(cmd, **kwargs):
        class R:
            stdout = b""
            stderr = b""
        return R()

    monkeypatch.setattr(sm.subprocess, "run", fake_run)
    rc = sm.cmd_use(ns(name="p", apply_global=False))
    out = capsys.readouterr().out
    assert rc == 0
    assert "Cleared Git identity" in out


def test_cmd_use_inside_repo_unsets_local(isolate_paths, monkeypatch, capsys):
    st = {"profiles": {"p": {"key_path": "/k", "public_key_path": "/k.pub", "hosts": ["h"], "git_name": "N", "git_email": "E"}}, "active_profile": None}
    sm.save_state(st)

    def fake_run(cmd, **kwargs):
        if cmd[:3] == ["git", "rev-parse", "--is-inside-work-tree"]:
            class R:
                stdout = b"true"
                stderr = b""
            return R()
        class R:
            stdout = b""
            stderr = b""
        return R()

    monkeypatch.setattr(sm.subprocess, "run", fake_run)
    rc = sm.cmd_use(ns(name="p", apply_global=True))
    assert rc == 0


def test_cmd_remove_not_found(isolate_paths, capsys):
    sm.save_state({"profiles": {}, "active_profile": None})
    rc = sm.cmd_remove(ns(name="p", force=False, delete_keys=False))
    err = capsys.readouterr().err
    assert rc == 1
    assert "not found" in err


def test_cmd_remove_active_without_force(isolate_paths, capsys):
    st = {"profiles": {"p": {"key_path": "/k", "public_key_path": "/k.pub", "hosts": ["h"]}}, "active_profile": "p"}
    sm.save_state(st)
    rc = sm.cmd_remove(ns(name="p", force=False, delete_keys=False))
    err = capsys.readouterr().err
    assert rc == 1
    assert "Use --force" in err


def test_cmd_remove_delete_keys_managed(isolate_paths, capsys):
    key = sm.MANAGED_DIR / "p" / "id_ed25519"
    key.parent.mkdir(parents=True, exist_ok=True)
    key.write_text("x", encoding="utf-8")
    key.with_suffix(".pub").write_text("y", encoding="utf-8")
    st = {"profiles": {"p": {"key_path": str(key), "public_key_path": str(key.with_suffix(".pub")), "hosts": ["h"]}}, "active_profile": None}
    sm.save_state(st)
    rc = sm.cmd_remove(ns(name="p", force=True, delete_keys=True))
    out = capsys.readouterr().out
    assert rc == 0
    assert "Deleted managed key files" in out
    assert not key.exists()
    assert "p" not in sm.load_state()["profiles"]


def test_cmd_remove_skip_delete_not_managed(isolate_paths, capsys, tmp_path):
    key = tmp_path / "id_ed25519"
    key.write_text("x", encoding="utf-8")
    key.with_suffix(".pub").write_text("y", encoding="utf-8")
    st = {"profiles": {"p": {"key_path": str(key), "public_key_path": str(key.with_suffix(".pub")), "hosts": ["h"]}}, "active_profile": None}
    sm.save_state(st)
    rc = sm.cmd_remove(ns(name="p", force=True, delete_keys=True))
    out = capsys.readouterr().out
    assert rc == 0
    assert "Skipped deleting keys" in out
    assert key.exists()


def test_cmd_remove_delete_keys_error_warnings(isolate_paths, capsys, monkeypatch):
    key = sm.MANAGED_DIR / "p" / "id_ed25519"
    key.parent.mkdir(parents=True, exist_ok=True)
    key.write_text("x", encoding="utf-8")
    key.with_suffix(".pub").write_text("y", encoding="utf-8")
    st = {"profiles": {"p": {"key_path": str(key), "public_key_path": str(key.with_suffix(".pub")), "hosts": ["h"]}}, "active_profile": None}
    sm.save_state(st)

    class Boom(Exception):
        pass

    def boom_unlink(self):
        raise Boom("boom")

    monkeypatch.setattr(Path, "unlink", boom_unlink, raising=False)
    rc = sm.cmd_remove(ns(name="p", force=True, delete_keys=True))
    out = capsys.readouterr().out
    assert rc == 0
    assert "failed to delete key files" in out


def test_cmd_update_not_found(isolate_paths, capsys):
    sm.save_state({"profiles": {}, "active_profile": None})
    rc = sm.cmd_update(ns(name="p", git_name=None, git_email=None))
    err = capsys.readouterr().err
    assert rc == 1
    assert "not found" in err


def test_cmd_update_no_changes(isolate_paths, capsys):
    st = {"profiles": {"p": {"key_path": "/k", "public_key_path": "/k.pub", "hosts": ["h"], "git_name": None, "git_email": None}}, "active_profile": None}
    sm.save_state(st)
    rc = sm.cmd_update(ns(name="p", git_name=None, git_email=None))
    err = capsys.readouterr().err
    assert rc == 1
    assert "nothing to update" in err


def test_cmd_update_success(isolate_paths, capsys):
    st = {"profiles": {"p": {"key_path": "/k", "public_key_path": "/k.pub", "hosts": ["h"], "git_name": None, "git_email": None}}, "active_profile": None}
    sm.save_state(st)
    rc = sm.cmd_update(ns(name="p", git_name="N", git_email="E"))
    out = capsys.readouterr().out
    assert rc == 0
    assert "Updated profile 'p'" in out


def test_handle_ssh_command_no_subcommand(capsys):
    rc = sm.handle_ssh_command(ns())
    err = capsys.readouterr().err
    assert rc == 2
    assert "No SSH subcommand" in err

