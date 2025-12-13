
---

## `cli/README.md`

```markdown
# APS CLI

**Command-line tool for the Agent Packaging Standard (APS)**

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.10+-blue)]()
[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](https://github.com/vedahegde60/agent-packaging-standard/blob/main/LICENSE)

The APS CLI enables developers to build, validate, sign, publish, and run portable AI agents following the [Agent Packaging Standard](https://agentpackaging.org).

---

## 🚀 Installation

### From PyPI (Recommended)

```bash
pip install apstool
```

For optional features (signing, RAG examples):

```bash
pip install apstool[dev]
```

### From Source (For Development)

```bash
git clone https://github.com/vedahegde60/agent-packaging-standard.git
cd agent-packaging-standard/cli
pip install -e .
```

---

## 📖 Quick Start

### Initialize a New Agent

Create a new agent from the APS template:

```bash
aps init my-agent
cd my-agent
```

This scaffolds a complete agent structure with:
- `aps/agent.yaml` — Manifest with metadata, runtime, dependencies
- `src/main.py` — Example Python entrypoint
- `requirements.txt` — Python dependencies

### Validate Your Agent

Check that your manifest is correctly structured:

```bash
aps validate my-agent
```

### Run Your Agent

Execute the agent locally with JSON input/output:

```bash
echo '{"text": "hello world"}' | aps run my-agent
```

Or use the `--input` flag:

```bash
aps run my-agent --input '{"text": "hello world"}'
```

### Build a Package

Create a distributable `.aps.tar.gz` package:

```bash
aps build my-agent
```

This produces `my-agent.aps.tar.gz` containing the manifest, code, and metadata.

### Sign Your Package

Sign the package for verification and provenance:

```bash
aps sign my-agent.aps.tar.gz --key path/to/cosign.key
```

### Verify a Package

Verify the signature and integrity:

```bash
aps verify my-agent.aps.tar.gz
```

### Publish to a Registry

Push your agent to a registry:

```bash
aps publish my-agent --registry registry://local
```

### Pull from a Registry

Download an agent from a registry:

```bash
aps pull dev.echo --registry registry://local
```

---

## 🧰 Command Reference

| Command | Description |
|---------|-------------|
| `aps init <path>` | Scaffold a new agent from template |
| `aps validate <path>` | Validate agent manifest structure |
| `aps run <path>` | Execute agent locally (stdin/stdout JSON) |
| `aps build <path>` | Package agent into `.aps.tar.gz` |
| `aps sign <package>` | Sign package with Cosign |
| `aps verify <package>` | Verify package signature |
| `aps publish <path>` | Push agent to registry |
| `aps pull <name>` | Pull agent from registry |
| `aps inspect <package>` | Show package metadata |

For full details, see the [CLI Reference](https://agentpackaging.org/cli/reference/).

---

## 🧪 Running Tests

```bash
cd cli
pytest -q
```

All tests run in isolated environments to avoid contaminating user data.

---

## 📚 Learn More

- **Documentation**: [agentpackaging.org](https://agentpackaging.org)
- **Specification**: [APS v0.1](../docs/specs/APS-v0.1.md)
- **Examples**: [examples/](../examples/)
- **Contributing**: [CONTRIBUTING.md](../CONTRIBUTING.md)

---

## 🛠️ Development

### Setup

```bash
cd cli
pip install -e .
```

### Run Tests

```bash
pytest -q
```

### Build Distribution

```bash
python -m build
```

---

## 📄 License

Apache License 2.0 — See [LICENSE](../LICENSE) for details.

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

> **Note**: The `aps run` command is a minimal reference implementation for local testing.  
> For production workloads, use a full-featured runtime that supports APS agents.

