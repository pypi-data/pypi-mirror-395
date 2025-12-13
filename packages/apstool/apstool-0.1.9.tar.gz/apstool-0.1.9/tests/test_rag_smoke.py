# cli/tests/test_rag_smoke.py
import io, types, json
from pathlib import Path
import aps_cli.app as app

def test_rag_local(tmp_path, monkeypatch):
    # examples/ is in parent directory relative to cli/
    root = Path(__file__).parent.parent.parent / "examples" / "rag-agent"
    assert (root / "aps" / "agent.yaml").exists(), f"Expected {root / 'aps' / 'agent.yaml'} to exist"
    req = '{"aps_version":"0.1","operation":"run","inputs":{"query":"APS","top_k":1}}'
    monkeypatch.setattr("sys.stdin", io.StringIO(req))
    # Increase timeout to 30s for sklearn initialization (especially on slower systems)
    ns = types.SimpleNamespace(path=str(root), stream=False, input=None, timeout=30)
    rc = app.cmd_run(ns)
    assert rc == 0
