import pytest
from unittest.mock import MagicMock, patch
from ghtest.cassette_sanitizer import (
    sanitize_cassette_data,
    _sanitize_node,
    _sanitize_primitive,
    _mask_auth_value,
    _mask_token,
    _mask_string,
    _mask_int,
    _looks_like_secret
)

def test_sanitize_cassette_data():
    data = {
        "interactions": [
            {
                "request": {
                    "headers": {"Authorization": ["Bearer secret"]},
                    "body": {"string": '{"token": "secret"}'}
                },
                "response": {
                    "body": {"string": '{"key": "value"}'}
                }
            }
        ]
    }
    changed = sanitize_cassette_data(data)
    assert changed
    assert data["interactions"][0]["request"]["headers"]["Authorization"] == ["Bearer xxxxxx"]
    assert "secret" not in data["interactions"][0]["request"]["body"]["string"]

def test_sanitize_node():
    # Test dropping keys
    data = {"url": "http://example.com", "keep": "me"}
    sanitized, changed = _sanitize_node(data, None)
    assert changed
    assert "url" not in sanitized
    assert "keep" in sanitized
    
    # Test masking string keys
    data = {"password": "secret"}
    sanitized, changed = _sanitize_node(data, None)
    assert changed
    assert sanitized["password"] != "secret"

def test_sanitize_primitive():
    # Test auth keys
    val, changed = _sanitize_primitive("Bearer secret", "authorization")
    assert changed
    assert val == "Bearer xxxxxx"
    
    # Test sensitive keys
    val, changed = _sanitize_primitive("secret", "x-api-key")
    assert changed
    assert val != "secret"
    
    # Test looks like secret
    val, changed = _sanitize_primitive("Bearer secret", "other")
    assert changed
    assert val != "Bearer secret"

def test_mask_auth_value():
    assert _mask_auth_value("Bearer secret") == "Bearer xxxxxx"
    assert _mask_auth_value("Token secret") == "Token xxxxxx"
    assert _mask_auth_value("Basic secret") == "Basic xxxxxx"
    assert _mask_auth_value("user:password") == "user:xxxxxxxx"

def test_mask_token():
    assert _mask_token("secret") == "xxxxxx"
    assert _mask_token("123") == "xxx"
    assert _mask_token("") == ""

def test_mask_string():
    assert _mask_string("secret") != "secret"
    assert len(_mask_string("secret")) == len("secret")

def test_mask_int():
    assert _mask_int(12345) != 12345
    assert isinstance(_mask_int(12345), int)

def test_looks_like_secret():
    assert _looks_like_secret("Bearer secret")
    assert _looks_like_secret("Token secret")
    assert not _looks_like_secret("hello world")
