import argparse
from pathlib import Path

import pytest

from git_switch import cli


def test_main_default_greeting(capsys):
    rc = cli.main([])
    out = capsys.readouterr().out
    assert rc == 0
    assert "Hello from git-switch" in out


def test_main_delegates_to_ssh(monkeypatch):
    called = {}

    def fake_handle(args: argparse.Namespace) -> int:
        called["args"] = args
        return 123

    monkeypatch.setattr(cli, "handle_ssh_command", fake_handle)
    rc = cli.main(["ssh", "list"])  # subcommand delegated
    assert rc == 123
    assert called["args"].ssh_cmd == "list"


def test_version_flag_prints_version(capsys):
    rc = cli.main(["--version"])
    out = capsys.readouterr().out.strip()
    assert rc == 0
    # Version should match __version__
    from git_switch import __version__
    assert out == __version__


def test_handle_copy_key_no_name_and_no_active(isolate_paths, write_state, capsys):
    write_state({}, None)
    ns = argparse.Namespace(name=None)
    rc = cli.handle_copy_key(ns)
    err = capsys.readouterr().err
    assert rc == 1
    assert "no profile name" in err


def test_handle_copy_key_profile_not_found(isolate_paths, write_state, capsys):
    write_state({}, None)
    ns = argparse.Namespace(name="missing")
    rc = cli.handle_copy_key(ns)
    err = capsys.readouterr().err
    assert rc == 1
    assert "not found" in err


def test_handle_copy_key_missing_public_key_path_in_state(isolate_paths, write_state, capsys):
    write_state({"p": {"key_path": "/x/y", "hosts": ["github.com"]}}, "p")
    ns = argparse.Namespace(name="p")
    rc = cli.handle_copy_key(ns)
    err = capsys.readouterr().err
    assert rc == 1
    assert "public_key_path missing" in err


def test_handle_copy_key_pub_file_missing(isolate_paths, write_state, capsys, tmp_path):
    pub_path = tmp_path / "id_ed25519.pub"
    write_state({"p": {"public_key_path": str(pub_path)}}, "p")
    ns = argparse.Namespace(name="p")
    rc = cli.handle_copy_key(ns)
    err = capsys.readouterr().err
    assert rc == 1
    assert "public key not found" in err


def test_handle_copy_key_clipboard_pbcopy_success(isolate_paths, write_state, monkeypatch, capsys, tmp_path):
    pub_path = tmp_path / "id_ed25519.pub"
    pub_path.write_text("ssh-ed25519 AAAAB3NzaC1yc2EAAA key\n", encoding="utf-8")
    write_state({"p": {"public_key_path": str(pub_path)}}, "p")

    def fake_which(name):
        return "/usr/bin/pbcopy" if name == "pbcopy" else None

    calls = {"run": 0}

    def fake_run(cmd, **kwargs):
        calls["run"] += 1
        class R:
            stdout = b""
            stderr = b""
        return R()

    monkeypatch.setattr(cli.shutil, "which", fake_which)
    monkeypatch.setattr(cli.subprocess, "run", fake_run)

    rc = cli.handle_copy_key(argparse.Namespace(name="p"))
    out = capsys.readouterr().out
    assert rc == 0
    assert "Copied public key" in out
    assert calls["run"] == 1


def test_handle_copy_key_clipboard_wl_copy_after_pbcopy_failure(isolate_paths, write_state, monkeypatch, capsys, tmp_path):
    pub_path = tmp_path / "id_ed25519.pub"
    pub_path.write_text("ssh-ed25519 AAAA key\n", encoding="utf-8")
    write_state({"p": {"public_key_path": str(pub_path)}}, "p")

    def fake_which(name):
        return "/usr/bin/" + name

    def fake_run(cmd, **kwargs):
        if cmd[0].endswith("pbcopy"):
            raise Exception("pbcopy failed")
        class R:
            stdout = b""
            stderr = b""
        return R()

    monkeypatch.setattr(cli.shutil, "which", fake_which)
    monkeypatch.setattr(cli.subprocess, "run", fake_run)

    rc = cli.handle_copy_key(argparse.Namespace(name="p"))
    out = capsys.readouterr().out
    assert rc == 0
    assert "wl-copy" in out


def test_handle_copy_key_fallback_prints_key(isolate_paths, write_state, monkeypatch, capsys, tmp_path):
    pub_path = tmp_path / "id_ed25519.pub"
    content = "ssh-ed25519 AAAAB3NzaC1yc2EAAA test\n"
    pub_path.write_text(content, encoding="utf-8")
    write_state({"p": {"public_key_path": str(pub_path)}}, "p")

    def fake_which(name):
        return None

    monkeypatch.setattr(cli.shutil, "which", fake_which)

    rc = cli.handle_copy_key(argparse.Namespace(name="p"))
    io = capsys.readouterr()
    assert rc == 0
    assert content == io.out


def test_handle_copy_key_clipboard_xclip_success(isolate_paths, write_state, monkeypatch, capsys, tmp_path):
    pub_path = tmp_path / "id_ed25519.pub"
    pub_path.write_text("ssh-ed25519 AAAA key\n", encoding="utf-8")
    write_state({"p": {"public_key_path": str(pub_path)}}, "p")

    def fake_which(name):
        return "/usr/bin/xclip" if name == "xclip" else None

    def fake_run(cmd, **kwargs):
        class R:
            stdout = b""
            stderr = b""
        return R()

    monkeypatch.setattr(cli.shutil, "which", fake_which)
    monkeypatch.setattr(cli.subprocess, "run", fake_run)

    rc = cli.handle_copy_key(argparse.Namespace(name="p"))
    out = capsys.readouterr().out
    assert rc == 0
    assert "xclip" in out


def test_handle_copy_key_clipboard_clip_success(isolate_paths, write_state, monkeypatch, capsys, tmp_path):
    pub_path = tmp_path / "id_ed25519.pub"
    pub_path.write_text("ssh-ed25519 AAAA key\n", encoding="utf-8")
    write_state({"p": {"public_key_path": str(pub_path)}}, "p")

    def fake_which(name):
        return "/Windows/System32/clip.exe" if name == "clip" else None

    def fake_run(cmd, **kwargs):
        class R:
            stdout = b""
            stderr = b""
        return R()

    monkeypatch.setattr(cli.shutil, "which", fake_which)
    monkeypatch.setattr(cli.subprocess, "run", fake_run)

    rc = cli.handle_copy_key(argparse.Namespace(name="p"))
    out = capsys.readouterr().out
    assert rc == 0
    assert "clip)." in out


def test_main_when_no_callable_func_prints_help(monkeypatch, capsys):
    class DummyParser:
        def parse_args(self, argv=None):
            class A:
                pass
            return A()

        def print_help(self):
            print("HELP")

    def fake_build():
        return DummyParser()

    monkeypatch.setattr(cli, "build_parser", fake_build)
    rc = cli.main([])
    io = capsys.readouterr()
    assert rc == 0
    assert "HELP" in io.out

