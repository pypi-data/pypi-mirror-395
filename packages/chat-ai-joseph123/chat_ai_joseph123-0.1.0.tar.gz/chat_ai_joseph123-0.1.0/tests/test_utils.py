import pytest
from CHAT_AI import format_response

def test_format_response():
    raw = " Hello   world   \n\n\nThis is   a test. "
    out = format_response(raw)
    assert out.startswith("Hello world")
    assert "\n\n" in out
