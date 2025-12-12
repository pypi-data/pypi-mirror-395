"""
Unit tests for ai.py
"""

from aimon.ai import get_response, summarize_text

def test_get_response():
    assert "AI Response" in get_response("hello")


def test_summarize_text():
    text = "Hello world. This is a test. More sentences."
    result = summarize_text(text)
    assert result.startswith("Hello world.")
