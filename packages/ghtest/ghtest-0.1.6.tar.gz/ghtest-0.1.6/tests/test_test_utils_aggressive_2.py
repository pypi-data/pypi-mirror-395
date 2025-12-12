import pytest
from unittest.mock import MagicMock
from ghtest.test_utils import (
    _summarize_blob,
    _capture_file_access,
    _collect_response_attributes,
    _stable_repr,
    _type_name,
    _is_literal_value
)

def test_summarize_blob():
    # Short blob
    summary = _summarize_blob(b"short")
    assert isinstance(summary, dict)
    assert summary["preview"] == "short"
    assert summary["length"] == 5
    
    # Long blob
    long_blob = b"a" * 100
    summary = _summarize_blob(long_blob)
    assert summary["length"] == 100
    assert "..." in summary["preview"] or len(summary["preview"]) < 100

def test_capture_file_access(tmp_path):
    test_file = tmp_path / "test.txt"
    
    with _capture_file_access() as (reads, writes):
        # Write
        with open(test_file, "w") as f:
            f.write("hello")
        
        # Read
        with open(test_file, "r") as f:
            f.read()
            
    assert any(str(test_file) in str(path) and "w" in mode for path, mode in writes)
    assert any(str(test_file) in str(path) and "r" in mode for path, mode in reads)

def test_collect_response_attributes():
    response = MagicMock()
    response.status_code = 200
    response.headers = {"Content-Type": "application/json"}
    response.json = lambda: {"foo": "bar"}
    response.__dict__ = {"status_code": 200, "headers": {"Content-Type": "application/json"}}
    
    attrs = _collect_response_attributes(response, volatile_fields=[])
    assert "status_code" in attrs
    assert attrs["status_code"]["value"] == 200
    assert "headers" in attrs

def test_stable_repr():
    class Foo:
        pass
    
    f = Foo()
    r = _stable_repr(f)
    assert "Foo object" in r
    assert "at 0x" not in r

def test_type_name():
    assert _type_name(1) == "builtins.int"
    assert _type_name(None) == "NoneType"
    
    class Bar:
        pass
    assert "Bar" in _type_name(Bar())

def test_is_literal_value():
    assert _is_literal_value(1)
    assert _is_literal_value("s")
    assert _is_literal_value([1, "s"])
    assert _is_literal_value({"a": 1})
    assert _is_literal_value(None)
    
    class Baz:
        pass
    assert not _is_literal_value(Baz())
    assert not _is_literal_value([Baz()])
