# cli/tests/test_sign_verify.py
import json
from pathlib import Path
import aps_cli.app as app

def test_keygen_sign_verify_roundtrip(tmp_path, monkeypatch):
    # Sandboxed keystore
    monkeypatch.setattr(app, "KEYS_DIR", tmp_path / "keys")
    monkeypatch.setattr(app, "PUBS_DIR", tmp_path / "keys.pub")
    app.KEYS_DIR.mkdir(parents=True, exist_ok=True)
    app.PUBS_DIR.mkdir(parents=True, exist_ok=True)

    # 1) keygen
    keyname = "testkey"
    rc = app.cmd_keygen(type("NS", (), {"name": keyname})())
    assert rc == 0
    priv = app._key_path(keyname)
    pub  = app._pub_path(keyname)
    assert priv.exists()
    assert pub.exists()

    # 2) fake package
    pkg = tmp_path / "dev.echo.aps.tar.gz"
    pkg.write_bytes(b"hello-world-package")

    # 3) sign
    rc = app.cmd_sign(type("NS", (), {"package": str(pkg), "key": keyname})())
    assert rc == 0
    sig = Path(str(pkg) + ".sig")
    assert sig.exists()

    # 4) verify OK
    rc = app.cmd_verify(type("NS", (), {"package": str(pkg), "signature": str(sig), "pubkey": str(pub)})())
    assert rc == 0

    # 5) verify FAIL (tamper)
    pkg.write_bytes(b"tampered")
    rc = app.cmd_verify(type("NS", (), {"package": str(pkg), "signature": str(sig), "pubkey": str(pub)})())
    assert rc == 1
