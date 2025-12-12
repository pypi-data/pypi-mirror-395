import os
import json
from pathlib import Path
import argparse

import pytest

from git_switch import ssh_manager as sm


def test_load_state_default_when_missing(isolate_paths):
    state = sm.load_state()
    assert state["profiles"] == {}
    assert state["active_profile"] is None


def test_load_state_invalid_json(isolate_paths):
    sm.PROFILES_FILE.write_text("{invalid", encoding="utf-8")
    state = sm.load_state()
    assert state["profiles"] == {}


def test_load_state_missing_keys(isolate_paths):
    sm.PROFILES_FILE.write_text(json.dumps({"profiles": {}}), encoding="utf-8")
    state = sm.load_state()
    assert "active_profile" in state
    sm.PROFILES_FILE.write_text(json.dumps({"active_profile": None}), encoding="utf-8")
    state = sm.load_state()
    assert state["profiles"] == {}


def test_save_state_roundtrip(isolate_paths):
    data = {"profiles": {"a": {"key_path": "/k", "public_key_path": "/k.pub", "hosts": ["h"]}}, "active_profile": "a"}
    sm.save_state(data)
    loaded = sm.load_state()
    assert loaded == data


def test_profile_serialize_deserialize(isolate_paths):
    p = sm.Profile(name="work", key_path="/k", public_key_path="/k.pub", email="e@x", hosts=["h1", "h2"], git_name="N", git_email="E")
    d = sm.dict_from_profile(p)
    p2 = sm.profile_from_dict("work", d)
    assert p2.name == "work"
    assert p2.key_path == "/k"
    assert p2.public_key_path == "/k.pub"
    assert p2.git_email == "E"


def test_ensure_include_in_ssh_config_inserts_once(isolate_paths):
    # Pre-populate config with some content without include
    sm.SSH_CONFIG_FILE.write_text("Host something\n  User test\n", encoding="utf-8")
    sm.ensure_include_in_ssh_config()
    sm.ensure_include_in_ssh_config()
    content = sm.SSH_CONFIG_FILE.read_text(encoding="utf-8")
    assert content.splitlines()[0].startswith("Include ")
    # Ensure only one include
    assert content.count("Include ") == 1


def test_write_include_for_profile_writes_hosts(isolate_paths):
    p = sm.Profile(name="p", key_path="/k", public_key_path="/k.pub", email=None, hosts=["github.com", "gitlab.com"])
    sm.write_include_for_profile(p)
    text = sm.INCLUDE_FILE.read_text(encoding="utf-8")
    assert "BEGIN git-switch managed block" in text
    assert "END git-switch managed block" in text
    assert "Host github.com" in text and "Host gitlab.com" in text
    assert "IdentityFile /k" in text


def test__chmod_secure_swallows_permissionerror(isolate_paths, monkeypatch, tmp_path):
    f = tmp_path / "x"
    f.write_text("x", encoding="utf-8")

    def fake_chmod(path, mode):
        raise PermissionError("nope")

    monkeypatch.setattr(os, "chmod", fake_chmod)
    sm._chmod_secure(f, 0o600)


def test_generate_ed25519_key_success(isolate_paths, monkeypatch, tmp_path):
    # Simulate ssh-keygen success
    def fake_run(cmd, **kwargs):
        class R:
            stdout = b""
            stderr = b""
        return R()

    monkeypatch.setattr(sm.subprocess, "run", fake_run)

    key_path = tmp_path / "id_ed25519"
    # Pretend ssh-keygen created the files
    key_path.write_text("priv", encoding="utf-8")
    (tmp_path / "id_ed25519.pub").write_text("pub", encoding="utf-8")

    priv, pub = sm.generate_ed25519_key(key_path, "comment")
    assert priv == key_path
    assert pub == key_path.with_suffix(".pub")


def test_generate_ed25519_key_missing_ssh_keygen(isolate_paths, monkeypatch, capsys, tmp_path):
    def fake_run(cmd, **kwargs):
        raise FileNotFoundError()

    monkeypatch.setattr(sm.subprocess, "run", fake_run)
    with pytest.raises(SystemExit) as se:
        sm.generate_ed25519_key(tmp_path / "id_ed25519", "c")
    assert se.value.code == 1
    err = capsys.readouterr().err
    assert "ssh-keygen not found" in err


def test_generate_ed25519_key_calledprocesserror(isolate_paths, monkeypatch, capsys, tmp_path):
    class CPE(Exception):
        pass

    def fake_run(cmd, **kwargs):
        raise sm.subprocess.CalledProcessError(returncode=1, cmd=cmd, output=b"", stderr=b"bad")

    monkeypatch.setattr(sm.subprocess, "run", fake_run)
    with pytest.raises(SystemExit) as se:
        sm.generate_ed25519_key(tmp_path / "id_ed25519", "c")
    assert se.value.code == 1
    err = capsys.readouterr().err
    assert "Error generating key" in err

