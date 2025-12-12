"""
Unit tests for utils.py
"""

from aimon.utils import format_response

def test_format_response():
    assert format_response("  hello   world  ") == "hello world"
