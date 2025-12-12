import argparse
import io

import pytest

from git_switch import pat_manager as pm


def ns(**kwargs):
    return argparse.Namespace(**kwargs)


@pytest.fixture()
def isolate_token_state(isolate_paths, monkeypatch):
    # Reuse the same profiles.json used by ssh_manager.load_state/save_state
    # Ensure a clean token_profiles section for each test
    st = {"profiles": {}, "active_profile": None, "token_profiles": {}, "active_token_profile": None}
    from git_switch import ssh_manager as sm
    sm.save_state(st)
    return sm


def test_cmd_add_requires_username(isolate_token_state, capsys):
    rc = pm.cmd_add(ns(name="p", username="", hosts=None, git_name=None, git_email=None, token=None, token_stdin=False))
    err = capsys.readouterr().err
    assert rc == 1
    assert "--username is required" in err


def test_cmd_add_requires_token(isolate_token_state, capsys):
    rc = pm.cmd_add(ns(name="p", username="u", hosts=None, git_name=None, git_email=None, token=None, token_stdin=False))
    err = capsys.readouterr().err
    assert rc == 1
    assert "provide --token or --token-stdin" in err


def test_cmd_add_success_with_token(monkeypatch, isolate_token_state, capsys):
    calls = {"approve": []}

    def fake_approve(host, username, token):
        calls["approve"].append((host, username, token))

    monkeypatch.setattr(pm, "_git_credential_approve", fake_approve)
    rc = pm.cmd_add(ns(name="p", username="u", hosts="github.com,gitlab.com", git_name=None, git_email=None, token="TKN", token_stdin=False))
    out = capsys.readouterr().out
    assert rc == 0
    assert "Added PAT profile 'p'" in out
    assert calls["approve"] == [("github.com", "u", "TKN"), ("gitlab.com", "u", "TKN")]


def test_cmd_add_reads_token_from_stdin(monkeypatch, isolate_token_state, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("MYTOKEN\n"))
    recorded = []

    def fake_approve(host, username, token):
        recorded.append(token)

    monkeypatch.setattr(pm, "_git_credential_approve", fake_approve)
    rc = pm.cmd_add(ns(name="p2", username="u2", hosts=None, git_name=None, git_email=None, token=None, token_stdin=True))
    out = capsys.readouterr().out
    assert rc == 0
    assert "p2" in out
    assert recorded == ["MYTOKEN"]


def test_cmd_add_existing_profile_errors(isolate_token_state, capsys):
    st = isolate_token_state.load_state()
    st["token_profiles"] = {"p": {"username": "u", "hosts": ["github.com"]}}
    isolate_token_state.save_state(st)
    rc = pm.cmd_add(ns(name="p", username="u", hosts=None, git_name=None, git_email=None, token="T", token_stdin=False))
    err = capsys.readouterr().err
    assert rc == 1
    assert "already exists" in err


def test_cmd_list_empty_is_ok(isolate_token_state, capsys):
    rc = pm.cmd_list(ns())
    out = capsys.readouterr().out
    assert rc == 0
    assert "No PAT profiles" in out


def test_cmd_list_shows_active_and_fields(isolate_token_state, capsys):
    st = isolate_token_state.load_state()
    st["token_profiles"] = {
        "a": {"username": "u1", "hosts": ["h1"], "git_name": None, "git_email": None},
        "b": {"username": "u2", "hosts": ["h2"], "git_name": "N", "git_email": "E"},
    }
    st["active_token_profile"] = "b"
    isolate_token_state.save_state(st)
    rc = pm.cmd_list(ns())
    out = capsys.readouterr().out
    assert rc == 0
    assert "* b" in out and "- a" in out
    assert "username=u2" in out and "hosts=[h2]" in out


def test_cmd_use_profile_not_found(isolate_token_state, capsys):
    rc = pm.cmd_use(ns(name="nope"))
    err = capsys.readouterr().err
    assert rc == 1
    assert "not found" in err


def test_cmd_use_sets_active_and_applies_identity(monkeypatch, isolate_token_state, capsys):
    st = isolate_token_state.load_state()
    st["token_profiles"] = {"p": {"username": "u", "hosts": ["h"], "git_name": "N", "git_email": "E"}}
    isolate_token_state.save_state(st)

    applied = {"calls": 0}

    def fake_apply(name, email):
        applied["calls"] += 1

    monkeypatch.setattr(pm, "_apply_git_identity_globally", fake_apply)
    rc = pm.cmd_use(ns(name="p"))
    out = capsys.readouterr().out
    assert rc == 0
    assert "Switched active PAT profile" in out
    assert applied["calls"] == 1
    assert isolate_token_state.load_state()["active_token_profile"] == "p"


def test_cmd_remove_not_found(isolate_token_state, capsys):
    rc = pm.cmd_remove(ns(name="missing"))
    err = capsys.readouterr().err
    assert rc == 1
    assert "not found" in err


def test_cmd_remove_erases_credentials_and_updates_state(monkeypatch, isolate_token_state, capsys):
    st = isolate_token_state.load_state()
    st["token_profiles"] = {"p": {"username": "u", "hosts": ["h1", "h2"], "git_name": None, "git_email": None}}
    st["active_token_profile"] = "p"
    isolate_token_state.save_state(st)

    erased = []

    def fake_reject(host, username):
        erased.append((host, username))

    monkeypatch.setattr(pm, "_git_credential_reject", fake_reject)
    rc = pm.cmd_remove(ns(name="p"))
    out = capsys.readouterr().out
    assert rc == 0
    assert ("h1", "u") in erased and ("h2", "u") in erased
    lst = isolate_token_state.load_state()
    assert lst.get("token_profiles") == {}
    assert lst.get("active_token_profile") is None


def test_cmd_update_not_found(isolate_token_state, capsys):
    rc = pm.cmd_update(ns(name="missing", git_name=None, git_email=None))
    err = capsys.readouterr().err
    assert rc == 1
    assert "not found" in err


def test_cmd_update_no_changes(isolate_token_state, capsys):
    st = isolate_token_state.load_state()
    st["token_profiles"] = {"p": {"username": "u", "hosts": ["h"], "git_name": None, "git_email": None}}
    isolate_token_state.save_state(st)
    rc = pm.cmd_update(ns(name="p", git_name=None, git_email=None))
    err = capsys.readouterr().err
    assert rc == 1
    assert "nothing to update" in err


def test_cmd_update_success(isolate_token_state, capsys):
    st = isolate_token_state.load_state()
    st["token_profiles"] = {"p": {"username": "u", "hosts": ["h"], "git_name": None, "git_email": None}}
    isolate_token_state.save_state(st)
    rc = pm.cmd_update(ns(name="p", git_name="N", git_email="E"))
    out = capsys.readouterr().out
    assert rc == 0
    assert "Updated PAT profile 'p'" in out


def test_handle_pat_command_no_subcommand(capsys):
    rc = pm.handle_pat_command(ns())
    err = capsys.readouterr().err
    assert rc == 2
    assert "No PAT subcommand" in err


def test_handle_pat_command_delegates():
    called = {"v": 0}

    def f(_args):
        called["v"] += 1
        return 7

    rc = pm.handle_pat_command(ns(func=f))
    assert rc == 7
    assert called["v"] == 1


def test__git_credential_approve_success(monkeypatch):
    recorded = {}

    def fake_run(cmd, **kwargs):
        recorded["cmd"] = cmd
        recorded["input"] = kwargs.get("input", b"")
        class R:
            stdout = b""
            stderr = b""
        return R()

    monkeypatch.setattr(pm.subprocess, "run", fake_run)
    pm._git_credential_approve("github.com", "user", "tok")
    assert recorded["cmd"][:3] == ["git", "credential", "approve"]
    assert b"host=github.com" in recorded["input"] and b"username=user" in recorded["input"] and b"password=tok" in recorded["input"]


def test__git_credential_approve_failure_warns(monkeypatch, capsys):
    class CPE(Exception):
        def __init__(self):
            self.stderr = b"boom"

    def fake_run(cmd, **kwargs):
        raise pm.subprocess.CalledProcessError(1, cmd, stderr=b"boom")

    monkeypatch.setattr(pm.subprocess, "run", fake_run)
    pm._git_credential_approve("host", "u", "t")
    err = capsys.readouterr().err
    assert "failed to store credential" in err


def test__git_credential_reject_success(monkeypatch):
    seen = {}

    def fake_run(cmd, **kwargs):
        seen["cmd"] = cmd
        class R:
            stdout = b""
            stderr = b""
        return R()

    monkeypatch.setattr(pm.subprocess, "run", fake_run)
    pm._git_credential_reject("example.com", "user")
    assert seen["cmd"][:3] == ["git", "credential", "reject"]


def test__git_credential_reject_failure_ignored(monkeypatch):
    def fake_run(cmd, **kwargs):
        raise pm.subprocess.CalledProcessError(1, cmd, stderr=b"x")

    monkeypatch.setattr(pm.subprocess, "run", fake_run)
    # Should not raise
    pm._git_credential_reject("h", "u")


def test__apply_git_identity_globally_sets(monkeypatch, capsys):
    calls = []

    def fake_run(cmd, **kwargs):
        calls.append(cmd)
        class R:
            stdout = b""
            stderr = b""
        return R()

    monkeypatch.setattr(pm.subprocess, "run", fake_run)
    pm._apply_git_identity_globally("Name", "Email")
    out = capsys.readouterr().out
    # Expect two set commands, no unset
    assert calls.count(["git", "config", "--global", "user.name", "Name"]) == 1
    assert calls.count(["git", "config", "--global", "user.email", "Email"]) == 1
    assert "Applied Git identity" in out


def test__apply_git_identity_globally_clears(monkeypatch, capsys):
    calls = []

    def fake_run(cmd, **kwargs):
        calls.append(cmd)
        class R:
            stdout = b""
            stderr = b""
        return R()

    monkeypatch.setattr(pm.subprocess, "run", fake_run)
    pm._apply_git_identity_globally(None, None)
    out = capsys.readouterr().out
    # Expect two unset commands
    assert ["git", "config", "--global", "--unset", "user.name"] in calls
    assert ["git", "config", "--global", "--unset", "user.email"] in calls
    assert "Cleared Git identity" in out

