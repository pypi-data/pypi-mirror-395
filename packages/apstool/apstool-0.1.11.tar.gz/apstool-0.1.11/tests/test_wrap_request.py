# cli/tests/test_wrap_request.py
import json
import aps_cli.app as app


def test_wrap_request_with_valid_json_object():
    """Test that valid JSON objects are passed as inputs, not wrapped as text."""
    input_json = '{"resume_text": "John Doe...", "job_description": "Python developer"}'
    result = app._wrap_request(input_json, single_input=None)
    
    parsed = json.loads(result)
    assert parsed["aps_version"] == "0.1"
    assert parsed["operation"] == "run"
    assert "inputs" in parsed
    assert parsed["inputs"]["resume_text"] == "John Doe..."
    assert parsed["inputs"]["job_description"] == "Python developer"
    # Should NOT wrap as {"text": "..."}
    assert "text" not in parsed["inputs"] or parsed["inputs"].get("text") != input_json


def test_wrap_request_with_full_envelope():
    """Test that full APS envelopes are passed through unchanged."""
    envelope = '{"aps_version":"0.1","operation":"run","inputs":{"query":"test"}}'
    result = app._wrap_request(envelope, single_input=None)
    
    parsed = json.loads(result)
    assert parsed["aps_version"] == "0.1"
    assert parsed["operation"] == "run"
    assert parsed["inputs"]["query"] == "test"


def test_wrap_request_with_plain_text():
    """Test that plain text is wrapped as inputs.text."""
    plain_text = "Hello world"
    result = app._wrap_request(plain_text, single_input=None)
    
    parsed = json.loads(result)
    assert parsed["inputs"]["text"] == plain_text


def test_wrap_request_with_single_input_flag():
    """Test --input flag wraps content under specified key."""
    content = '{"nested": "data"}'
    result = app._wrap_request(content, single_input="resume")
    
    parsed = json.loads(result)
    assert "resume" in parsed["inputs"]
    # The nested object should be preserved
    assert parsed["inputs"]["resume"]["nested"] == "data"


def test_wrap_request_with_json_array():
    """Test that JSON arrays are wrapped as text (not a dict)."""
    json_array = '[1, 2, 3]'
    result = app._wrap_request(json_array, single_input=None)
    
    parsed = json.loads(result)
    assert "text" in parsed["inputs"]
    assert "[1, 2, 3]" in parsed["inputs"]["text"]
