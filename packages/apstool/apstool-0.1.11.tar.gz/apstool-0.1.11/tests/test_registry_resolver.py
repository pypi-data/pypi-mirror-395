# cli/tests/test_registry_resolver.py
from pathlib import Path
import types
import argparse

import aps_cli.app as app


def test_resolve_local_path_passthrough(tmp_path, monkeypatch):
    # Create a local agent dir with a manifest; resolver should return same path (not registry)
    p = tmp_path / "examples" / "echo-agent"
    (p / "aps").mkdir(parents=True)
    (p / "aps" / "agent.yaml").write_text("aps_version: '0.1'\n", encoding="utf-8")
    out = app._resolve_registry_path_if_needed(str(p))
    assert out == str(p)


def test_resolve_registry_cached(tmp_path, monkeypatch, dummy_resp):
    # Prepare cache dir: ~/.aps/cache/<id>/<version>
    agent_id = "dev.echo"
    version = "0.0.9"
    cache_dir = app.CACHE_DIR / agent_id / version
    (cache_dir / "aps").mkdir(parents=True, exist_ok=True)
    (cache_dir / "aps" / "agent.yaml").write_text("aps_version: '0.1'\n", encoding="utf-8")

    # Mock GET /v1/agents/dev.echo -> returns version
    def fake_get(url, timeout=10):
        assert url.endswith(f"/v1/agents/{agent_id}")
        return dummy_resp({"id": agent_id, "version": version})

    # Ensure we don't actually call the network or pull
    monkeypatch.setattr(app, "requests", types.SimpleNamespace(get=fake_get))
    monkeypatch.setattr(app, "cmd_pull", lambda args: 0)

    out = app._resolve_registry_path_if_needed(f"registry://{agent_id}")
    assert out == str(cache_dir)


def test_resolve_registry_triggers_pull(tmp_path, monkeypatch, dummy_resp):
    agent_id = "dev.echo"
    version = "0.1.0"
    cache_dir = app.CACHE_DIR / agent_id / version

    # Mock GET /v1/agents/dev.echo
    def fake_get(url, timeout=10):
        assert url.endswith(f"/v1/agents/{agent_id}")
        return dummy_resp({"id": agent_id, "version": version})

    pulled = {"called": False}

    def fake_cmd_pull(ns: argparse.Namespace):
        # Simulate creating cache dir as if pull unpacked it
        cache_dir.mkdir(parents=True, exist_ok=True)
        (cache_dir / "aps").mkdir(exist_ok=True)
        (cache_dir / "aps" / "agent.yaml").write_text("aps_version: '0.1'\n", encoding="utf-8")
        print("Setting called = true")
        pulled["called"] = True
        return 0

    monkeypatch.setattr(app, "requests", types.SimpleNamespace(get=fake_get))

    monkeypatch.setattr(app, "cmd_pull", fake_cmd_pull)
    print("done calling fake_cmd_pull"+agent_id)
    out = app._resolve_registry_path_if_needed(f"registry://{agent_id}")
    assert pulled["called"] is True
    assert out == str(cache_dir)


def test_resolve_registry_fails_on_bad_http(monkeypatch, dummy_resp):
    agent_id = "dev.echo"
    def fake_get(url, timeout=10):
        return dummy_resp({}, status=500)
    monkeypatch.setattr(app, "requests", types.SimpleNamespace(get=fake_get))
    try:
        app._resolve_registry_path_if_needed(f"registry://{agent_id}")
        assert False, "expected exception"
    except Exception as e:
        # The resolver should mention HTTP or 'failed to resolve'
        assert "failed to resolve" in str(e) or "HTTP" in str(e)
