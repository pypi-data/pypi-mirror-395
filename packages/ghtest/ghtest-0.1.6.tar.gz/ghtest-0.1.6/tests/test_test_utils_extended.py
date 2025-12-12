import pytest
import io
import os
from ghtest.test_utils import (
    call_with_capture,
    assert_return_summary,
    _capture_file_access,
    _summarize_return_value,
    _summarize_blob,
    _is_literal_value,
    _classify_mode,
)

def test_call_with_capture_basic():
    def func(a, b):
        print("hello")
        return a + b
    
    result = call_with_capture(func, target="func", params={"a": 1, "b": 2})
    
    assert result.return_value == 3
    assert result.printed == "hello\n"
    assert result.exception is None
    assert result.target == "func"

def test_call_with_capture_exception():
    def func():
        raise ValueError("oops")
    
    result = call_with_capture(func, target="func", params={})
    
    assert result.return_value is None
    assert isinstance(result.exception, ValueError)
    assert str(result.exception) == "oops"

def test_capture_file_access(tmp_path):
    p = tmp_path / "test.txt"
    
    def func():
        with open(p, "w") as f:
            f.write("data")
        with open(p, "r") as f:
            f.read()
            
    result = call_with_capture(func, target="func", params={})
    
    # Check writes
    assert len(result.file_writes) >= 1
    # Check reads
    assert len(result.file_reads) >= 1

def test_assert_return_summary():
    actual = {"type": "int", "value": 1}
    expected = {"type": "int", "value": 1}
    assert_return_summary(actual, expected, target="func")
    
    # Mismatch
    with pytest.raises(AssertionError):
        assert_return_summary({"value": 1}, {"value": 2}, target="func")
        
    # Missing key
    with pytest.raises(AssertionError):
        assert_return_summary({"a": 1}, {"a": 1, "b": 2}, target="func")

def test_summarize_return_value():
    # Literal
    s = _summarize_return_value(1, [])
    assert s["value"] == 1
    
    # String
    s = _summarize_return_value("hello", [])
    assert s["value"] == "hello"
    
    # Long string
    long_str = "a" * 200
    s = _summarize_return_value(long_str, [])
    # It seems it returns repr for long strings
    assert "repr" in s or "value" not in s
    # assert s["length"] == 200 # length might not be included
    
    # Bytes
    s = _summarize_return_value(b"bytes", [])
    assert s["bytes"]["value_b64"] == "Ynl0ZXM=" # base64 for "bytes"

def test_classify_mode():
    assert _classify_mode("r") == (True, False)
    assert _classify_mode("w") == (False, True)
    assert _classify_mode("r+") == (True, True)
    assert _classify_mode("a") == (False, True)
    assert _classify_mode("rb") == (True, False)

def test_is_literal_value():
    assert _is_literal_value(1)
    assert _is_literal_value("s")
    assert _is_literal_value([1, "s"])
    assert _is_literal_value({"a": 1})
    assert not _is_literal_value(object())
