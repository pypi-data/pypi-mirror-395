import os
from ai_helpers import format_response, summarize_text, get_response

def test_format_response_basic():
    s = "  Hello\n\n\nWorld  "
    out = format_response(s)
    assert "Hello" in out and "World" in out
    assert "\n\n\n" not in out

def test_get_response_mock():
    # Force mock provider
    os.environ["AI_PROVIDER"] = "mock"
    res = get_response("Hello world", provider="mock")
    assert "you asked" in res
