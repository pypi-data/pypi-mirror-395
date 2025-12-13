# cli/src/aps_cli/app.py
# APS CLI – clean baseline
# ------------------------------------------------------------
# Features:
# - validate | build | publish | pull | run (sync/--stream) | logs | inspect | registry serve
# - Self-healing registry:// resolver with cache verification
# - Robust streaming (write->flush->close stdin BEFORE reading)
# - Sync path merges stderr->stdout to avoid 3.13 pipe race
# - Log persistence under ~/.aps/logs
# - Clear stderr logging for all non-JSON chatter
# ------------------------------------------------------------

from __future__ import annotations
import os, sys, json, argparse, tarfile, shutil, subprocess, threading, time, shlex
from pathlib import Path
from typing import Any, Dict, Optional
from pathlib import Path
import base64

# Optional cryptography imports - only needed for sign/verify
try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives import serialization, hashes
    from cryptography.hazmat.backends import default_backend
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False



# 3rd party (ensure installed in venv for CLI usage)
import requests
try:
    import yaml
except ImportError:
    print("[init] ERROR: PyYAML not installed. pip install pyyaml", file=sys.stderr)
    raise

# ------------------------------ Constants / Paths

HOME = Path.home()
class _EnvPath:
    """Lightweight path-like object that resolves an env var on each access.

    This keeps module-level references (e.g. `app.CACHE_DIR / id / ver`) working
    while still allowing tests to change `APS_CACHE_DIR` at runtime via
    environment monkeypatching.
    """
    def __init__(self, envvar: str, fallback: Path):
        self.envvar = envvar
        self.fallback = fallback

    def _path(self) -> Path:
        return Path(os.environ.get(self.envvar, str(self.fallback)))

    def __truediv__(self, other):
        return self._path() / other

    def __str__(self):
        return str(self._path())

    def __fspath__(self):
        return str(self._path())

    def exists(self):
        return self._path().exists()

    def mkdir(self, *args, **kwargs):
        return self._path().mkdir(*args, **kwargs)


CACHE_DIR = _EnvPath("APS_CACHE_DIR", HOME / ".aps" / "cache")
LOGS_DIR = _EnvPath("APS_LOGS_DIR", HOME / ".aps" / "logs")
DEFAULT_REGISTRY = os.environ.get("APS_REGISTRY", "http://localhost:8080")
KEYS_DIR = Path.home() / ".aps" / "keys"
PUBS_DIR  = Path.home() / ".aps" / "keys.pub"
KEYS_DIR.mkdir(parents=True, exist_ok=True)
PUBS_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------ Helpers
def _key_path(name: str) -> Path:
    return KEYS_DIR / f"{name}.priv"

def _pub_path(name: str) -> Path:
    return PUBS_DIR / f"{name}.pub"

def _fingerprint_pubkey(pub_bytes: bytes) -> str:
    # simple SHA256 fingerprint (base64)
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(pub_bytes)
    return base64.urlsafe_b64encode(digest.finalize()).decode("utf-8").rstrip("=")

def _load_private_key(path: Path):
    data = path.read_bytes()
    return serialization.load_pem_private_key(data, password=None, backend=default_backend())

def _load_public_key(path: Path):
    data = path.read_bytes()
    return serialization.load_pem_public_key(data, backend=default_backend())

def _write_private_key(path: Path, key):
    pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    path.write_bytes(pem)
    os.chmod(path, 0o600)

def _write_public_key(path: Path, key):
    pem = key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    path.write_bytes(pem)
    return pem

def _sign_bytes(priv_key, payload: bytes) -> bytes:
    return priv_key.sign(payload)

def _verify_sig(pub_key, payload: bytes, sig: bytes) -> bool:
    try:
        pub_key.verify(sig, payload)
        return True
    except Exception:
        return False
    
def _http_get_bytes(url: str, timeout=30) -> bytes | None:
    try:
        r = requests.get(url, timeout=timeout, stream=True)
        if r.status_code != 200:
            return None
        buf = bytearray()
        for chunk in r.iter_content(chunk_size=65536):
            if chunk:
                buf.extend(chunk)
        return bytes(buf)
    except Exception:
        return None

def _download_package(reg: str, agent_id: str, ver: str) -> Path:
    """Download the tarball to a temp file and return its path (caller extracts/cleans)."""
    urls = [
        f"{reg}/v1/pull/{agent_id}/{ver}",
        f"{reg}/v1/pull?id={agent_id}&version={ver}",
        f"{reg}/v1/pull?id={agent_id}",  # legacy
    ]
    last_err = None
    for url in urls:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".aps.tar.gz") as tmp:
                tmp_path = Path(tmp.name)
                with requests.get(url, stream=True, timeout=30) as r:
                    r.raise_for_status()
                    for chunk in r.iter_content(chunk_size=65536):
                        if chunk:
                            tmp.write(chunk)
            return tmp_path
        except Exception as e:
            last_err = e
    raise RuntimeError(f"failed to download {agent_id}@{ver}: {last_err}")


def eprint(*a, **k):
    print(*a, file=sys.stderr, **k)

def _now_ts() -> str:
    return time.strftime("%Y-%m-%dT%H-%M-%SZ", time.gmtime())

def _logs_dir_for(agent_id: str, version: str) -> Path:
    return LOGS_DIR / agent_id / version

def _write_log(agent_root: Path, manifest: Dict[str, Any], stderr_lines: list[str], final_json: Optional[dict]):
    """Persist a run log. Enabled when APS_SAVE_LOGS in {"1","true"} (default: on)."""
    if os.environ.get("APS_SAVE_LOGS", "1") not in ("1", "true", "True"):
        return
    agent_id = manifest.get("id", "unknown")
    version  = manifest.get("version", "unknown")
    d = _logs_dir_for(agent_id, version)
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{_now_ts()}.log"
    with p.open("w", encoding="utf-8") as f:
        f.write(f"# APS LOG\nid: {agent_id}\nversion: {version}\n")
        f.write(f"time: {_now_ts()}\n\n")
        f.write("## STDERR/LOGS\n")
        for line in stderr_lines:
            f.write(line.rstrip("\n") + "\n")
        f.write("\n## RESULT\n")
        f.write(json.dumps(final_json if final_json else {
            "status":"error","error":{"code":"NO_FINAL_RESPONSE","message":"Agent exited without valid JSON"}
        }))
    eprint(f"[logs] wrote {p}")

def agent_root(p: str | Path) -> Path:
    """Return the agent root Path (dir containing aps/agent.yaml)."""
    p = Path(p).resolve()  # Resolve to absolute path
    if p.is_file() and p.suffixes[-2:] == [".tar", ".gz"]:
        # tarball is treated in inspect/build/publish paths; run expects a dir
        raise FileNotFoundError(f"Run expects directory, got tar: {p}")
    if (p / "aps" / "agent.yaml").exists():
        return p
    raise FileNotFoundError(f"Missing manifest: {p}/aps/agent.yaml")

def load_manifest(root: Path) -> Dict[str, Any]:
    with (root / "aps" / "agent.yaml").open("r", encoding="utf-8") as f:
        return yaml.safe_load(f.read())

def _get_python_entrypoint(manifest: Dict[str, Any]) -> Optional[list[str]]:
    """Extract Python entrypoint from manifest, supporting both old and new formats.
    
    New format (APS v0.1 spec):
      runtime: python3
      entrypoint: src/module/main.py
    
    Old format:
      runtimes:
        - kind: python
          entrypoint: ["python", "-m", "module.main"]
    """
    # Try new format first (flat runtime + entrypoint)
    if "runtime" in manifest and "entrypoint" in manifest:
        runtime = manifest["runtime"]
        if runtime and ("python" in runtime.lower() or runtime == "python3"):
            entry = manifest["entrypoint"]
            if isinstance(entry, str):
                # Convert path to python command
                if entry.endswith(".py"):
                    return ["python", entry]
                else:
                    return shlex.split(entry)
            elif isinstance(entry, list):
                return entry
    
    # Fall back to old format (runtimes array)
    rt = next((r for r in manifest.get("runtimes", []) 
               if r.get("kind") == "python" and r.get("entrypoint")), None)
    if rt:
        entry = rt["entrypoint"]
        if isinstance(entry, str):
            entry_list = shlex.split(entry)
        elif isinstance(entry, list):
            entry_list = list(entry)
        else:
            return None
        
        # Replace 'python' with sys.executable for consistent Python environment
        if entry_list and entry_list[0] in ("python", "python3"):
            entry_list[0] = sys.executable
        return entry_list
    
    return None

def cached_agent_dir(agent_id: str, version: str) -> Path:
    return CACHE_DIR / agent_id / version

def _is_json_status_line(line: str) -> Optional[dict]:
    """Heuristic: parse if dict and has 'status' key."""
    if not line or line[0] != "{" or line[-1] != "}":
        return None
    try:
        obj = json.loads(line)
        if isinstance(obj, dict) and "status" in obj:
            return obj
    except Exception:
        return None
    return None

def _emit_implicit_error() -> int:
    print(json.dumps({"status":"error","error":{"code":"NO_FINAL_RESPONSE","message":"Agent produced no final JSON"}}))
    return 1

def _wrap_request(stdin_raw: str, single_input: Optional[str]) -> str:
    """
    Accepts either:
      - Full envelope: {"aps_version": "...", "operation": "run", "inputs": {...}}
      - Raw inputs object or a primitive under --input key.
    Always returns a full envelope string.
    """
    # If user passed raw, but also provided --input key, wrap as {"inputs": {key: raw}}
    if single_input:
        try:
            raw = json.loads(stdin_raw) if stdin_raw.strip() else None
        except Exception:
            raw = stdin_raw if stdin_raw.strip() else None
        payload = {"aps_version":"0.1","operation":"run","inputs":{single_input: raw}}
        return json.dumps(payload)

    # Try parsing as JSON first
    try:
        obj = json.loads(stdin_raw) if stdin_raw.strip() else {}
    except Exception:
        # Not valid JSON - wrap as text
        env = {"aps_version":"0.1","operation":"run","inputs": {"text": stdin_raw}}
        return json.dumps(env)

    # If already a full APS envelope, pass through
    if isinstance(obj, dict) and "inputs" in obj and "operation" in obj:
        return json.dumps(obj)

    # If it's a valid JSON object, treat it as the inputs
    if isinstance(obj, dict):
        env = {"aps_version":"0.1","operation":"run","inputs": obj}
        return json.dumps(env)
    
    # For other JSON types (arrays, primitives), wrap as text
    env = {"aps_version":"0.1","operation":"run","inputs": {"text": str(obj)}}
    return json.dumps(env)

# ------------------------------ Tar extraction (flatten if nested)

def _extract_agent_pkg(pkg_path: str, target: Path):
    """
    Extract tar.gz into `target`. Supports both:
      - Flat tars: aps/..., src/...
      - Nested tars: <name>/aps/..., <name>/src/...
    """
    import tempfile
    target.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmpd:
        with tarfile.open(pkg_path, "r:gz") as tf:
            # NOTE: For demo/dev we trust packages; add safe_member checks if needed
            tf.extractall(path=tmpd)

        tmp_root = Path(tmpd)
        # Case A: flat
        if (tmp_root / "aps" / "agent.yaml").exists():
            for item in tmp_root.iterdir():
                shutil.move(str(item), str(target / item.name))
            return

        # Case B: nested – find directory that contains aps/agent.yaml
        cand = None
        for p in tmp_root.rglob("aps/agent.yaml"):
            cand = p.parent.parent  # .../<cand>/aps/agent.yaml
            break
        if cand:
            for item in cand.iterdir():
                shutil.move(str(item), str(target / item.name))
            return

    raise FileNotFoundError("package missing aps/agent.yaml")

# ------------------------------ Registry resolution / Pull

def _resolve_registry_path_if_needed(path: str) -> str:
    """Resolve registry://ID to local cache path (and self-heal incomplete cache)."""
    if not path.startswith("registry://"):
        return path

    agent_id = path.replace("registry://", "")
    reg = DEFAULT_REGISTRY

    # Get metadata (latest version)
    r = requests.get(f"{reg}/v1/agents/{agent_id}", timeout=10)
    if r.status_code != 200:
        raise RuntimeError(f"failed to resolve {agent_id}: HTTP {r.status_code}")
    meta = r.json()
    version = meta["version"]
    target = cached_agent_dir(agent_id, version)

    # Self-heal if cache is missing
    if not (target / "aps" / "agent.yaml").exists():
        eprint(f"[run] cache incomplete for {agent_id}@{version}; pulling…")
        ns = argparse.Namespace(agent=agent_id, registry=reg, version=version)
        rc = cmd_pull(ns)
        if rc != 0 or not (target / "aps" / "agent.yaml").exists():
            raise FileNotFoundError(f"Missing manifest after pull: {target}/aps/agent.yaml")

    eprint(f"[run] resolved registry://{agent_id} -> {target}")
    return str(target)

# ------------------------------ Commands

def cmd_validate(args):
    root = agent_root(args.path)
    mf = load_manifest(root)
    required = ["aps_version","id","name","version","runtimes"]
    missing = [k for k in required if k not in mf]
    if missing:
        print(json.dumps({"status":"error","error":{"code":"MISSING_KEYS","missing":missing}}))
        return 1
    print(json.dumps({"status":"ok"}))
    return 0

def cmd_build(args):
    root = Path(args.path).resolve()
    dist_dir = Path(args.dist or (root / "dist"))
    dist_dir.mkdir(parents=True, exist_ok=True)

    mf = load_manifest(root)
    agent_id = mf["id"]; version = mf["version"]
    out_path = dist_dir / f"{agent_id}.aps.tar.gz"

    eprint(f"[build] packaging {agent_id}@{version} -> {out_path}")
    with tarfile.open(out_path, "w:gz") as tf:
        # Add select paths at top-level; avoid nesting (no arcname=root.name)
        for rel in ["aps", "src", "README.md", "assets","LICENSE"]:
            p = root / rel
            if p.exists():
                tf.add(p, arcname=rel)
    print(str(out_path))
    return 0




def cmd_init(args):
    tgt = Path(args.path).resolve()
    if tgt.exists() and any(tgt.iterdir()):
        print("[init] ERROR: target not empty", file=sys.stderr); return 2
    
    # Derive agent name from path (sanitize for Python module name)
    agent_name = tgt.name.replace("-", "_").replace(" ", "_").lower()
    # Ensure it's a valid Python identifier
    if not agent_name.isidentifier():
        agent_name = "agent"
    agent_id = f"dev.{tgt.name.lower().replace('_', '.')}"
    
    # Create directory structure
    (tgt/"aps").mkdir(parents=True, exist_ok=True)
    (tgt/"src"/agent_name).mkdir(parents=True, exist_ok=True)
    
    # Load template from package
    template_path = Path(__file__).parent / "templates" / "echo_agent" / "aps" / "agent.yaml"
    if template_path.exists():
        template = template_path.read_text(encoding="utf-8")
        # Customize template with agent-specific values
        template = template.replace("dev.echo", agent_id)
        template = template.replace('name: "Echo"', f'name: "{tgt.name}"')
        template = template.replace("Echoes the input text.", f"Agent: {tgt.name}")
        template = template.replace("echo.main", f"{agent_name}.main")
        (tgt/"aps"/"agent.yaml").write_text(template, encoding="utf-8")
    else:
        # Fallback to inline template if file not found
        (tgt/"aps"/"agent.yaml").write_text(
            'aps_version: "0.1"\n'
            f'id: "{agent_id}"\n'
            f'name: "{tgt.name}"\n'
            'version: "0.1.0"\n'
            f'summary: "Agent: {tgt.name}"\n'
            'runtimes:\n'
            '  - kind: "python"\n'
            f'    entrypoint: ["python", "-m", "{agent_name}.main"]\n'
            'capabilities:\n'
            '  inputs:\n'
            '    schema:\n'
            '      type: object\n'
            '      properties:\n'
            '        text: { type: string }\n'
            '      required: ["text"]\n'
            '  outputs:\n'
            '    schema:\n'
            '      type: object\n'
            '      properties:\n'
            '        text: { type: string }\n'
            '      required: ["text"]\n'
            '  tools: []\n'
            'policies:\n'
            '  network: { egress: [] }\n'
        , encoding="utf-8")
    
    # Create agent implementation
    (tgt/"src"/agent_name/"__init__.py").write_text("", encoding="utf-8")
    (tgt/"src"/agent_name/"main.py").write_text(
        "import sys, json\nraw=sys.stdin.read()\nreq=json.loads(raw)\ntext=(req.get('inputs') or {}).get('text','')\n"
        "print(json.dumps({'status':'ok','outputs':{'text':text.upper()}}))\n", encoding="utf-8")
    (tgt/"AGENT_CARD.md").write_text(f"# {tgt.name}\n\nAgent description goes here.\n", encoding="utf-8")
    print(f"[init] Created {tgt}"); return 0

def cmd_publish(args):
    pkg = Path(args.package).resolve()
    reg = args.registry or DEFAULT_REGISTRY
    files = {"file": open(pkg, "rb")}
    eprint(f"[publish] -> {reg} ({pkg.name})")
    r = requests.post(f"{reg}/v1/publish", files=files, timeout=60)
    if r.status_code >= 400:
        eprint(f"[publish] ERROR {r.status_code}: {r.text}")
        r.raise_for_status()
    print(json.dumps(r.json()))
    return 0

def cmd_sig_validate(args, agent_id: str, ver: str, tmp_pkg: Path):
    # --- Optional signature verification ---
    if getattr(args, "verify", False):
        # Try to fetch a detached signature from common endpoints
        sig_candidates = [
            f"{reg}/v1/signature/{agent_id}/{ver}",
            f"{reg}/v1/signature?id={agent_id}&version={ver}",
            f"{reg}/v1/pull/{agent_id}/{ver}.sig",
            f"{reg}/v1/pull?id={agent_id}&version={ver}&sig=1",
        ]
        sig_bytes = None
        for url in sig_candidates:
            sig_bytes = _http_get_bytes(url)
            if sig_bytes:
                print(f"[pull] Retrieved signature from {url}")
                break

        if sig_bytes is None:
            if getattr(args, "require_signature", False):
                print("[pull] ERROR: signature not available and --require-signature set", file=sys.stderr)
                try: tmp_pkg.unlink(missing_ok=True)
                except Exception: pass
                return 2
            else:
                print("[pull] WARN: no signature found; skipping verification", file=sys.stderr)
        else:
            # Determine pubkey path
            pub_path = None
            if getattr(args, "pubkey", None):
                pub_path = Path(args.pubkey).expanduser().resolve()
            else:
                # If no pubkey provided, look for a conventional name:
                # ~/.aps/keys.pub/<agent_id>.pub  OR ~/.aps/keys.pub/default.pub
                candidate1 = PUBS_DIR / f"{agent_id}.pub"
                candidate2 = PUBS_DIR / "default.pub"
                pub_path = candidate1 if candidate1.exists() else (candidate2 if candidate2.exists() else None)

            if not pub_path or not pub_path.exists():
                if getattr(args, "require_signature", False):
                    print("[pull] ERROR: no public key available for verification", file=sys.stderr)
                    try: tmp_pkg.unlink(missing_ok=True)
                    except Exception: pass
                    return 2
                else:
                    print("[pull] WARN: no public key provided; skipping verification", file=sys.stderr)
            else:
                # Write signature to temp file and verify using existing verify logic
                tmp_sig = Path(str(tmp_pkg) + ".sig")
                tmp_sig.write_bytes(sig_bytes)
                rc = cmd_verify(argparse.Namespace(package=str(tmp_pkg), signature=str(tmp_sig), pubkey=str(pub_path)))
                try: tmp_sig.unlink(missing_ok=True)
                except Exception: pass
                if rc != 0 and getattr(args, "require_signature", False):
                    # Hard fail if required
                    try: tmp_pkg.unlink(missing_ok=True)
                    except Exception: pass
                    return rc
                elif rc != 0:
                    print("[pull] WARN: signature verification failed; continuing (no --require-signature)", file=sys.stderr)


def cmd_pull(args):
    agent_id = args.agent
    reg = args.registry or DEFAULT_REGISTRY

    # Resolve version
    r = requests.get(f"{reg}/v1/agents/{agent_id}", timeout=10)
    r.raise_for_status()
    meta = r.json()
    version = args.version if getattr(args, "version", None) and args.version != "latest" else meta["version"]

    # Download
    url = f"{reg}/v1/agents/{agent_id}/download?version={version}"
    eprint(f"[pull] GET {url}")
    rd = requests.get(url, stream=True, timeout=60)
    rd.raise_for_status()

    target = cached_agent_dir(agent_id, version)
    target.mkdir(parents=True, exist_ok=True)
    tmp_pkg = target.parent / f"{agent_id}-{version}.tmp.tar.gz"
    with open(tmp_pkg, "wb") as f:
        for chunk in rd.iter_content(8192):
            if chunk:
                f.write(chunk)

    # Optional signature validation
    cmd_sig_validate(args, agent_id, version, tmp_pkg)

    # Extract (flatten if needed)
    _extract_agent_pkg(str(tmp_pkg), target)
    tmp_pkg.unlink(missing_ok=True)
    eprint(f"[pull] ready: {target}")
    return 0

def helper_run_agent(path: str, req: str, timeout_s=None) -> int:
    """
    SYNC path:
      - Merge stderr -> stdout to avoid Python 3.13 dual-pipe races.
      - Only print final JSON line to stdout.
      - Persist logs separate from final JSON.
    """
    root = agent_root(path)
    mf = load_manifest(root)

    env = os.environ.copy()
    src_dir = root / "src"
    if src_dir.exists():
        env["PYTHONPATH"] = str(src_dir) + os.pathsep + env.get("PYTHONPATH", "")
    env.setdefault("PYTHONUNBUFFERED", "1")
    env["APS_AGENT_ROOT"] = str(root)

    # Select python runtime (supports both old and new manifest formats)
    entry = _get_python_entrypoint(mf)
    if not entry:
        eprint("[run] ERROR: no python runtime found in manifest")
        return 2

    proc = subprocess.Popen(
        entry,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,  # merged to avoid 3.13 EBADF race
        text=True,
        env=env,
        cwd=str(root)
    )

    try:
        out, _ = proc.communicate(input=req, timeout=timeout_s)
    except subprocess.TimeoutExpired:
        proc.kill()
        try:
            out, _ = proc.communicate(timeout=1)
        except Exception:
            out = out or ""
        err_obj = {"status":"error","error":{"code":"TIMEOUT","message":f"Agent exceeded timeout ({timeout_s}s)"}}
        _write_log(root, mf, (out.splitlines() if out else []), err_obj)
        print(json.dumps(err_obj))
        return 124

    lines = out.splitlines() if out else []
    final_json, final_idx = None, -1
    for i, line in enumerate(lines):
        obj = _is_json_status_line(line)
        if obj:
            final_json, final_idx = obj, i

    logs_lines = lines[:final_idx] + lines[final_idx+1:] if final_idx >= 0 else lines
    _write_log(root, mf, logs_lines, final_json)

    if final_json:
        print(json.dumps(final_json))
        return 0 if final_json.get("status") == "ok" else 1
    return _emit_implicit_error()

def cmd_run_stream(args):
    """
    STREAM path:
      - Set APS_STREAM=1 for agent behavior switch
      - Write -> flush -> close stdin BEFORE reading any output
      - Drain stderr concurrently; mirror non-JSON stdout lines to stderr
      - Persist logs; print final JSON once to stdout
    """
    root = agent_root(args.path)
    mf = load_manifest(root)

    env = os.environ.copy()
    src_dir = root / "src"
    if src_dir.exists():
        env["PYTHONPATH"] = str(src_dir) + os.pathsep + env.get("PYTHONPATH", "")
    env.setdefault("PYTHONUNBUFFERED", "1")
    env["APS_STREAM"] = "1"
    env["APS_AGENT_ROOT"] = str(root)
    
    # Select python runtime (supports both old and new manifest formats)
    entry = _get_python_entrypoint(mf)
    if not entry:
        eprint("[run] ERROR: no python runtime found in manifest")
        return 2

    # Read + wrap user stdin first
    raw = sys.stdin.read() or ""
    req = _wrap_request(raw, getattr(args, "input", None))

    proc = subprocess.Popen(
        entry, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, env=env, cwd=str(root), bufsize=1
    )

    # Strict ordering: write->flush->close BEFORE reads
    try:
        to_send = req if req.endswith("\n") else req + "\n"
        proc.stdin.write(to_send)
        proc.stdin.flush()
    except BrokenPipeError:
        pass
    finally:
        try: proc.stdin.close()
        except Exception: pass

    collected_stderr: list[str] = []

    def _drain_err(pipe):
        for line in iter(pipe.readline, ''):
            if not line:
                break
            collected_stderr.append(line)
            eprint(line.rstrip("\n"))
        try: pipe.close()
        except Exception: pass

    t = threading.Thread(target=_drain_err, args=(proc.stderr,), daemon=True)
    t.start()

    final_json = None
    for line in iter(proc.stdout.readline, ''):
        s = line.rstrip("\n")
        if not s:
            continue
        obj = _is_json_status_line(s)
        if obj:
            final_json = obj
            if obj.get("status") == "error":
                break
        else:
            # Non-JSON stdout is treated as log; mirror to stderr
            eprint(s)

    try: proc.stdout.close()
    except Exception: pass
    proc.wait()

    _write_log(root, mf, collected_stderr, final_json)
    if final_json:
        print(json.dumps(final_json))
        return 0 if final_json.get("status") == "ok" else 1
    return _emit_implicit_error()

def cmd_run(args):
    path = _resolve_registry_path_if_needed(args.path)
    if getattr(args, "stream", False):
        # stream mode uses its own runner (already reads stdin internally)
        args.path = path
        return cmd_run_stream(args)
    else:
        # sync mode reads stdin here then calls helper
        raw = sys.stdin.read() or ""
        req = _wrap_request(raw, getattr(args, "input", None))
        args.path = path
        return helper_run_agent(args.path, req, timeout_s=args.timeout)

def cmd_logs(args):
    resolved = _resolve_registry_path_if_needed(args.path)
    root = agent_root(resolved)
    mf = load_manifest(root)
    d = _logs_dir_for(mf.get("id","unknown"), mf.get("version","unknown"))
    if not d.exists():
        eprint(f"[logs] no logs for {mf.get('id')}@{mf.get('version')} in {d}")
        return 1
    files = sorted(d.glob("*.log"))
    if not files:
        eprint(f"[logs] no log files found in {d}")
        return 1
    if args.latest:
        print(files[-1].read_text(encoding="utf-8"), end="")
        return 0
    for f in files:
        print(f.name)
    return 0

def cmd_inspect(args):
    p = Path(args.path)
    if p.is_file() and p.suffixes[-2:] == [".tar", ".gz"]:
        try:
            with tarfile.open(p, "r:gz") as tf:
                m = tf.getmember("aps/agent.yaml")
                with tf.extractfile(m) as f:
                    manifest = yaml.safe_load(f.read().decode("utf-8"))
        except Exception as e:
            eprint(f"[inspect] ERROR: {e}")
            return 1
    else:
        manifest = load_manifest(agent_root(p))
    print(json.dumps(manifest, indent=2))
    return 0

    # --- Signing
def cmd_keygen(args):
    name = args.name
    priv_path = _key_path(name)
    pub_path  = _pub_path(name)

    if priv_path.exists() or pub_path.exists():
        print(f"[keygen] ERROR: key '{name}' already exists", file=sys.stderr)
        return 2

    priv = ed25519.Ed25519PrivateKey.generate()
    pub  = priv.public_key()

    _write_private_key(priv_path, priv)
    pub_pem = _write_public_key(pub_path, pub)
    fp = _fingerprint_pubkey(pub_pem)

    print(json.dumps({
        "status": "ok",
        "key": name,
        "private": str(priv_path),
        "public": str(pub_path),
        "fingerprint": fp
    }))
    return 0

def cmd_sign(args):
    if not HAS_CRYPTO:
        print("[sign] ERROR: cryptography library not installed. Install with: pip install apstool[dev]", file=sys.stderr)
        return 2
    
    pkg = Path(args.package).resolve()
    if not pkg.exists():
        print(f"[sign] ERROR: package not found: {pkg}", file=sys.stderr)
        return 2

    keyname = args.key
    priv = _load_private_key(_key_path(keyname))

    payload = pkg.read_bytes()
    sig = _sign_bytes(priv, payload)

    sig_path = pkg.with_suffix(pkg.suffix + ".sig") if pkg.suffix else Path(str(pkg) + ".sig")
    sig_path.write_bytes(sig)

    # also print pubkey fingerprint for convenience
    pub_pem = priv.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    fp = _fingerprint_pubkey(pub_pem)

    print(json.dumps({
        "status": "ok",
        "package": str(pkg),
        "signature": str(sig_path),
        "key": keyname,
        "fingerprint": fp
    }))
    return 0

def cmd_verify(args):
    if not HAS_CRYPTO:
        print("[verify] ERROR: cryptography library not installed. Install with: pip install apstool[dev]", file=sys.stderr)
        return 2
    
    pkg = Path(args.package).resolve()
    sig_path = Path(args.signature).resolve() if args.signature else pkg.with_suffix(pkg.suffix + ".sig")
    pubfile = Path(args.pubkey).resolve()

    if not pkg.exists():
        print(f"[verify] ERROR: package not found: {pkg}", file=sys.stderr)
        return 2
    if not sig_path.exists():
        print(f"[verify] ERROR: signature not found: {sig_path}", file=sys.stderr)
        return 2
    if not pubfile.exists():
        print(f"[verify] ERROR: pubkey not found: {pubfile}", file=sys.stderr)
        return 2

    payload = pkg.read_bytes()
    sig = sig_path.read_bytes()
    pub = _load_public_key(pubfile)

    ok = _verify_sig(pub, payload, sig)
    if ok:
        print(json.dumps({"status":"ok","verified":True,"package":str(pkg),"signature":str(sig_path)}))
        return 0
    else:
        print(json.dumps({"status":"error","error":{"code":"BAD_SIGNATURE","message":"Signature does not match"}}))
        return 1



def cmd_registry_serve(args):
    # Launch FastAPI registry in-process
    import uvicorn
    from aps_registry.server import create_app
    app = create_app(args.root)
    eprint(f"[registry] serving at 0.0.0.0:{args.port} (root={args.root})")
    uvicorn.run(app, host="0.0.0.0", port=int(args.port), log_level="info")

# ------------------------------ Argparse / Main

def main(argv=None):
    parser = argparse.ArgumentParser(prog="aps", add_help=True)
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    sub = parser.add_subparsers(dest="cmd")

    p = sub.add_parser("validate", help="Validate an agent manifest")
    p.add_argument("path")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("build", help="Build an APS package (.aps.tar.gz)")
    p.add_argument("path")
    p.add_argument("--dist", default=None)
    p.set_defaults(func=cmd_build)

    #
    # init
    #
    s = sub.add_parser("init", help="Create a new APS agent scaffold")
    s.add_argument("path")
    s.set_defaults(func=cmd_init)
    
    p = sub.add_parser("publish", help="Publish a built package to a registry")
    p.add_argument("package")
    p.add_argument("--registry", default=DEFAULT_REGISTRY)
    p.set_defaults(func=cmd_publish)

    p = sub.add_parser("pull", help="Pull an agent from registry into local cache")
    p.add_argument("agent")
    p.add_argument("--version", default="latest")
    p.add_argument("--registry", default=DEFAULT_REGISTRY)
    p.add_argument("--verify", action="store_true", help="Verify package signature after download")
    p.add_argument("--pubkey", help="Path to public key PEM for verification")
    p.add_argument(
        "--require-signature",
        action="store_true",
        help="Fail if signature is missing or invalid when --verify is set",
    )
    p.set_defaults(func=cmd_pull)

    p = sub.add_parser("run", help="Run an agent (dir or registry://id)")
    p.add_argument("path")
    p.add_argument("--stream", action="store_true", help="Enable streaming mode")
    p.add_argument("--input", default=None, help="When raw input, wrap under inputs.{key}")
    p.add_argument("--timeout", type=int, default=None, help="Timeout seconds (sync only)")
    p.set_defaults(func=cmd_run)

    p = sub.add_parser("logs", help="Show saved logs for an agent")
    p.add_argument("path")
    p.add_argument("--latest", action="store_true")
    p.set_defaults(func=cmd_logs)

    p = sub.add_parser("inspect", help="Inspect manifest from dir or tarball")
    p.add_argument("path")
    p.set_defaults(func=cmd_inspect)

    #
    # signing
    #
        # keys
    s = sub.add_parser("keygen", help="Generate a new Ed25519 keypair into ~/.aps/keys")
    s.add_argument("name", help="Key name (e.g., 'default')")
    s.set_defaults(func=cmd_keygen)

    s = sub.add_parser("sign", help="Sign an .aps.tar.gz file with a private key")
    s.add_argument("package", help="Path to .aps.tar.gz")
    s.add_argument("--key", default="default", help="Key name (default: 'default')")
    s.set_defaults(func=cmd_sign)

    s = sub.add_parser("verify", help="Verify a package signature with a public key")
    s.add_argument("package", help="Path to .aps.tar.gz")
    s.add_argument("--signature", help="Path to detached signature (defaults to <pkg>.sig)")
    s.add_argument("--pubkey", required=True, help="Path to public key PEM (e.g., ~/.aps/keys.pub/default.pub)")
    s.set_defaults(func=cmd_verify)

    #
    # registry serve
    #

    p = sub.add_parser("registry", help="Registry commands")
    s = p.add_subparsers(dest="subcmd")
    r = s.add_parser("serve", help="Start a local APS registry")
    r.add_argument("--root", default="registry_data")
    r.add_argument("--port", type=int, default=8080)
    r.set_defaults(func=cmd_registry_serve)

    args = parser.parse_args(argv)

    # Show version
    if getattr(args, "version", False) and args.cmd is None:
        print("apstool 0.1.11")
        return 0
    
    if not hasattr(args, "func"):
        parser.print_help()
        return 1
    return args.func(args)

if __name__ == "__main__":
    sys.exit(main())
