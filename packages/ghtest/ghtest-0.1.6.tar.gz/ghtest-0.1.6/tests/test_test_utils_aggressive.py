import pytest
from unittest.mock import MagicMock, patch
from ghtest.test_utils import (
    _summarize_blob,
    _summarize_return_value,
    call_with_capture
)
from ghtest.tests_writer import _DataStore, _literal_or_repr

def test_summarize_blob():
    summary = _summarize_blob(b"short")
    assert summary["length"] == 5
    assert "preview" in summary
    assert "hash" in summary

def test_summarize_return_value():
    ds = MagicMock()
    ds.literal.return_value = "literal"
    
    # It returns a dict
    summary = _summarize_return_value(None, ds)
    assert summary["value"] is None
    assert summary["type"] == "NoneType"
    
    summary = _summarize_return_value(1, ds)
    assert summary["value"] == 1
    # Type name might include module
    assert "int" in summary["type"]

def test_literal_or_repr():
    ds = MagicMock()
    ds.literal.return_value = "literal"
    
    lit, is_repr = _literal_or_repr(1, ds, "name")
    assert lit == "literal"
    assert is_repr is False
    
    ds.literal.return_value = None
    lit, is_repr = _literal_or_repr(object(), ds, "name")
    
    # Debugging
    if lit is None:
        # This should not happen if _stable_repr works
        from ghtest.test_utils import _stable_repr
        print(f"DEBUG: _stable_repr(object()) = {_stable_repr(object())}")
        
    assert isinstance(lit, str)
    # _stable_repr removes the address
    assert "<object object>" in lit or "object object" in lit
    assert is_repr is True
