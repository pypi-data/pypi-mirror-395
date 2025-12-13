# Echo Agent (template)

Minimal APS-compliant agent that echoes `inputs.text`.

Run example via repo root:

```bash
cd cli && pip install -e .
echo '{"operation":"run","inputs":{"text":"hi"}}' | aps run ../examples/echo-agent

