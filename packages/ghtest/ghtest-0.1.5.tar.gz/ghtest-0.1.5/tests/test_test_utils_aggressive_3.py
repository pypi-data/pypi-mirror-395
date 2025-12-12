import pytest
from ghtest.test_utils import _summarize_return_value, _is_literal_value

def test_summarize_return_value():
    # Simple types
    assert _summarize_return_value(1, [])["type"] == "builtins.int"
    assert _summarize_return_value("s", [])["type"] == "builtins.str"
    assert _summarize_return_value(None, [])["type"] == "NoneType"
    
    # Collections
    assert "list" in _summarize_return_value([1, 2], [])["type"]
    assert "dict" in _summarize_return_value({"a": 1}, [])["type"]
    
    # Objects
    class Foo:
        pass
    assert "Foo" in _summarize_return_value(Foo(), [])["type"]
    
    # Long string
    long_str = "a" * 100
    summary = _summarize_return_value(long_str, [])
    assert "str" in summary["type"]
    # Check if length is in repr or value?
    # Usually it truncates or adds info.
    # I'll just check type for now.

def test_is_literal_value():
    assert _is_literal_value(1)
    assert _is_literal_value("s")
    assert _is_literal_value(True)
    assert _is_literal_value(None)
    assert _is_literal_value([1, 2])
    assert _is_literal_value({"a": 1})
    
    class Foo:
        pass
    assert not _is_literal_value(Foo())
    
    # Nested non-literal
    assert not _is_literal_value([Foo()])
    assert not _is_literal_value({"a": Foo()})
