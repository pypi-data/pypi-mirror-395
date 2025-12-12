import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from ghtest.cassette_sanitizer import (
    sanitize_file,
    sanitize_paths,
    _iter_cassette_paths,
    _should_drop_key,
    _sanitize_http_body
)

def test_sanitize_file(tmp_path):
    f = tmp_path / "test.yaml"
    f.write_text("interactions: []")
    
    # No change
    assert not sanitize_file(f)
    
    # Change
    f.write_text("interactions:\n- request:\n    headers:\n      authorization: ['Bearer secret123']")
    
    assert sanitize_file(f)
    content = f.read_text()
    assert "secret123" not in content

def test_sanitize_http_body():
    # JSON body in VCR format
    body = {"string": '{"key": "value"}'}
    assert not _sanitize_http_body(body)
    
    # Sensitive
    original = '{"password": "secret123"}'
    body_sensitive = {"string": original}
    assert _sanitize_http_body(body_sensitive)
    assert body_sensitive["string"] != original
    
    # Non-JSON
    body_text = {"string": "text"}
    assert not _sanitize_http_body(body_text)

def test_sanitize_paths(tmp_path):
    d = tmp_path / "cassettes"
    d.mkdir()
    f1 = d / "c1.yaml"
    f1.write_text("interactions: []")
    
    # Pass file directly
    # Returns (changed, total)
    assert sanitize_paths([f1]) == (0, 1)
    
    # Pass directory Path object
    # assert sanitize_paths([d]) == (0, 1)
    pass
