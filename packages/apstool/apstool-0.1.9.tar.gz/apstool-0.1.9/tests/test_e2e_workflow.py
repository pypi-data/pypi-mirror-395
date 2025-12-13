"""
End-to-end integration test for the complete APS CLI workflow.
Tests: init, validate, build, inspect, run, registry (publish/pull)

Registry integration test requires setting environment variable:
    RUN_REGISTRY_TEST=1 pytest tests/test_e2e_workflow.py::test_registry_integration -v
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path
import pytest


def test_full_workflow(tmp_path, monkeypatch):
    """Test complete workflow: init -> validate -> build -> inspect -> run"""
    
    # Change to temp directory
    monkeypatch.chdir(tmp_path)
    
    agent_name = "test-e2e-agent"
    agent_dir = tmp_path / agent_name
    
    # Step 1: Init - Create new agent
    result = subprocess.run(
        [sys.executable, "-m", "aps_cli.app", "init", agent_name],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"init failed: {result.stderr}"
    assert agent_dir.exists()
    assert (agent_dir / "aps" / "agent.yaml").exists()
    assert (agent_dir / "src" / "test_e2e_agent" / "__init__.py").exists()
    assert (agent_dir / "src" / "test_e2e_agent" / "main.py").exists()
    print("✅ Step 1: Init")
    
    # Step 2: Validate - Check manifest is valid
    result = subprocess.run(
        [sys.executable, "-m", "aps_cli.app", "validate", str(agent_dir)],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"validate failed: {result.stderr}"
    output = json.loads(result.stdout.strip())
    assert output["status"] == "ok", f"Validation failed: {output}"
    print("✅ Step 2: Validate")
    
    # Step 3: Build - Package the agent
    result = subprocess.run(
        [sys.executable, "-m", "aps_cli.app", "build", str(agent_dir)],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"build failed: {result.stderr}"
    package_path = agent_dir / "dist" / "dev.test-e2e-agent.aps.tar.gz"
    assert package_path.exists(), f"Package not created at {package_path}"
    print("✅ Step 3: Build")
    
    # Step 4: Inspect - Check package contents
    result = subprocess.run(
        [sys.executable, "-m", "aps_cli.app", "inspect", str(package_path)],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"inspect failed: {result.stderr}"
    manifest = json.loads(result.stdout)
    assert manifest["id"] == "dev.test-e2e-agent"
    assert manifest["aps_version"] == "0.1"
    assert "runtimes" in manifest
    print("✅ Step 4: Inspect")
    
    # Step 5: Run - Execute the agent
    test_input = json.dumps({"text": "hello world"})
    result = subprocess.run(
        [sys.executable, "-m", "aps_cli.app", "run", str(agent_dir)],
        input=test_input,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"run failed: {result.stderr}"
    
    # Parse output (last line should be JSON)
    output_lines = result.stdout.strip().split('\n')
    json_output = json.loads(output_lines[-1])
    
    assert json_output["status"] == "ok", f"Agent run failed: {json_output}"
    assert "outputs" in json_output
    assert json_output["outputs"]["text"] == "HELLO WORLD"
    print("✅ Step 5: Run")
    
    # Step 6: Logs - Verify logs were created
    result = subprocess.run(
        [sys.executable, "-m", "aps_cli.app", "logs", str(agent_dir)],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"logs failed: {result.stderr}"
    assert result.stdout.strip() != "", "No log files found"
    print("✅ Step 6: Logs")
    
    print("\n🎉 All end-to-end tests passed!")


def test_init_with_different_names(tmp_path, monkeypatch):
    """Test init with various agent name formats"""
    monkeypatch.chdir(tmp_path)
    
    test_cases = [
        ("simple-agent", "simple_agent"),
        ("MyAwesomeAgent", "myawesomeagent"),
        ("data-processor-v2", "data_processor_v2"),
    ]
    
    for agent_name, expected_module in test_cases:
        agent_dir = tmp_path / agent_name
        
        result = subprocess.run(
            [sys.executable, "-m", "aps_cli.app", "init", agent_name],
            capture_output=True,
            text=True,
            cwd=tmp_path
        )
        assert result.returncode == 0, f"init failed for {agent_name}: {result.stderr}"
        
        # Check module directory was created with correct name
        module_dir = agent_dir / "src" / expected_module
        assert module_dir.exists(), f"Module dir {module_dir} not found"
        assert (module_dir / "__init__.py").exists()
        assert (module_dir / "main.py").exists()
        
        # Validate the generated agent
        result = subprocess.run(
            [sys.executable, "-m", "aps_cli.app", "validate", str(agent_dir)],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"validate failed for {agent_name}"
        
        print(f"✅ {agent_name} -> {expected_module}")
    
    print("\n🎉 All name format tests passed!")


@pytest.mark.skipif(
    os.environ.get("RUN_REGISTRY_TEST") != "1",
    reason="Registry test requires RUN_REGISTRY_TEST=1 (manual testing only)"
)
def test_registry_integration(tmp_path, monkeypatch):
    """
    Integration test for registry workflow: serve -> publish -> pull
    
    This test is SKIPPED by default because it requires starting a real server.
    
    Prerequisites:
        pip install fastapi uvicorn  # Registry dependencies
    
    To run this test manually:
        RUN_REGISTRY_TEST=1 pytest tests/test_e2e_workflow.py::test_registry_integration -v
    
    Or to run ALL tests including this one:
        RUN_REGISTRY_TEST=1 pytest tests/ -v
    """
    # Check if registry dependencies are available
    try:
        import fastapi
        import uvicorn
    except ImportError as e:
        pytest.skip(f"Registry dependencies not installed: {e}. Run: pip install fastapi uvicorn")
    
    import socket
    
    # Find available port
    with socket.socket() as s:
        s.bind(('', 0))
        port = s.getsockname()[1]
    
    registry_url = f"http://localhost:{port}"
    registry_data = tmp_path / "registry_data"
    registry_data.mkdir()
    
    # Change to temp directory
    monkeypatch.chdir(tmp_path)
    
    # Step 1: Start local registry server in background
    print(f"Starting registry server on port {port}...")
    registry_proc = subprocess.Popen(
        [sys.executable, "-m", "aps_cli.app", "registry", "serve", 
         "--port", str(port), "--root", str(registry_data)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for server to be ready (simple approach: just wait a few seconds)
    time.sleep(3)
    
    if registry_proc.poll() is not None:
        stdout, stderr = registry_proc.communicate()
        pytest.fail(f"Registry server failed to start:\nSTDOUT: {stdout}\nSTDERR: {stderr}")
    
    print(f"✅ Registry server started on port {port}")
    
    try:
        # Step 2: Create and build an agent
        agent_name = "registry-test-agent"
        agent_dir = tmp_path / agent_name
        
        result = subprocess.run(
            [sys.executable, "-m", "aps_cli.app", "init", agent_name],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"init failed: {result.stderr}"
        print("✅ Created agent")
        
        result = subprocess.run(
            [sys.executable, "-m", "aps_cli.app", "build", str(agent_dir)],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"build failed: {result.stderr}"
        package_path = agent_dir / "dist" / "dev.registry-test-agent.aps.tar.gz"
        assert package_path.exists()
        print("✅ Built package")
        
        # Step 3: Publish to local registry
        result = subprocess.run(
            [sys.executable, "-m", "aps_cli.app", "publish", str(package_path),
             "--registry", registry_url],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"publish failed: {result.stderr}"
        print("✅ Published to registry")
        
        # Step 4: Pull from registry to a different location
        pull_dir = tmp_path / "pulled"
        pull_dir.mkdir()
        monkeypatch.chdir(pull_dir)
        
        result = subprocess.run(
            [sys.executable, "-m", "aps_cli.app", "pull", "dev.registry-test-agent",
             "--registry", registry_url],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"pull failed: {result.stderr}"
        print("✅ Pulled from registry")
        
        # Step 5: Verify pulled agent has correct structure
        # Pull creates cache in ~/.aps/cache/<agent-id>/<version>/
        # For this test, we just verify pull succeeded (returncode 0)
        
        print("\n🎉 Registry integration test passed!")
        
    finally:
        # Cleanup: stop registry server
        registry_proc.terminate()
        try:
            registry_proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            registry_proc.kill()
            registry_proc.wait()
        print("✅ Registry server stopped")


# Note: For quick manual testing without pytest:
#   1. aps registry serve --port 8080 --data-dir ./test-registry
#   2. aps publish <package> --registry http://localhost:8080
#   3. aps pull <agent-id> --registry http://localhost:8080


if __name__ == "__main__":
    import tempfile
    import os
    
    class FakeMonkeypatch:
        def chdir(self, path):
            os.chdir(path)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        print("Running end-to-end workflow test...")
        test_full_workflow(Path(tmpdir), FakeMonkeypatch())
        
        print("\nRunning name format tests...")
        with tempfile.TemporaryDirectory() as tmpdir2:
            test_init_with_different_names(Path(tmpdir2), FakeMonkeypatch())
        
        print("\n✅ All e2e tests passed!")
        print("\nNote: Registry workflow tests are in test_registry_resolver.py")
