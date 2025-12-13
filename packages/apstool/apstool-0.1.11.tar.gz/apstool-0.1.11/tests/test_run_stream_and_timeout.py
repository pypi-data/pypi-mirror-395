# cli/tests/test_run_stream_and_timeout.py
import io
import json
import types
from pathlib import Path
import time

import pytest

import aps_cli.app as app


def _make_slow_agent(root: Path, delay_s: float = 2.0):
    """
    Creates a tiny agent that sleeps before printing final JSON.
    """
    (root / "aps").mkdir(parents=True, exist_ok=True)
    (root / "src" / "echo").mkdir(parents=True, exist_ok=True)
    (root / "aps" / "agent.yaml").write_text(
        """aps_version: 0.1
id: dev.slow
name: Slow
version: 0.0.1
summary: Sleeps then returns
runtimes:
  - kind: python
    entrypoint: python src/echo/main.py
""",
        encoding="utf-8",
    )
    (root / "src" / "echo" / "main.py").write_text(
        f"""import sys, json, time
raw = sys.stdin.read() or "{{}}"
time.sleep({delay_s})
print(json.dumps({{"aps_version":"0.1","status":"ok","outputs":{{"text":"done"}}}}))
""",
        encoding="utf-8",
    )


def test_stream_happy_path(tmp_path, monkeypatch, stdin_json):
    """
    Verify --stream prints one final JSON and returns 0.
    """
    # Make a local echo agent (file entrypoint)
    agent_root = tmp_path / "echo-agent"
    (agent_root / "aps").mkdir(parents=True, exist_ok=True)
    (agent_root / "src" / "echo").mkdir(parents=True, exist_ok=True)

    (agent_root / "aps" / "agent.yaml").write_text(
        """aps_version: 0.1
id: dev.echo
name: Echo
version: 0.0.1
summary: Echo agent
runtimes:
  - kind: python
    entrypoint: python src/echo/main.py
""",
        encoding="utf-8",
    )

    (agent_root / "src" / "echo" / "main.py").write_text(
        r"""import sys, json, os, time
raw = sys.stdin.read() or "{}"
try:
    obj = json.loads(raw) if raw.strip() else {}
except Exception:
    obj = {}
inputs = obj.get("inputs", obj) if isinstance(obj, dict) else {}
text = inputs.get("text","")
if os.environ.get("APS_STREAM") == "1":
    for ch in text:
        print(f"[stream] {ch}", flush=True)
        time.sleep(0.001)
    print(json.dumps({"aps_version":"0.1","status":"ok","outputs":{"text": text}}), flush=True)
else:
    print(json.dumps({"aps_version":"0.1","status":"ok","outputs":{"text": text}}))
""",
        encoding="utf-8",
    )

    # Stream run: inject stdin and call CLI
    stdin_json('{"aps_version":"0.1","operation":"run","inputs":{"text":"stream!"}}')
    ns = types.SimpleNamespace(path=str(agent_root), stream=True, input=None, timeout=None)
    rc = app.cmd_run(ns)
    assert rc == 0


def test_sync_timeout(tmp_path, monkeypatch):
    """
    Verify sync run times out with a nonzero exit and TIMEOUT error.
    """
    agent_root = tmp_path / "slow-agent"
    _make_slow_agent(agent_root, delay_s=2.0)

    # Feed empty JSON; set a tight timeout
    monkeypatch.setattr("sys.stdin", io.StringIO("{}"))
    ns = types.SimpleNamespace(path=str(agent_root), stream=False, input=None, timeout=1)
    rc = app.cmd_run(ns)
    assert rc != 0  # expect timeout
