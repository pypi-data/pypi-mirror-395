import pytest
from ghtest.cassette_sanitizer import (
    sanitize_cassette_data,
    _mask_token,
    _mask_auth_value,
    _mask_string,
    _mask_int,
)

def test_mask_token():
    assert _mask_token("secret123") == "xxxxxxxxx"
    assert _mask_token("") == ""
    assert _mask_token("abc-def") == "xxx-xxx"

def test_mask_auth_value():
    assert _mask_auth_value("Bearer secret") == "Bearer xxxxxx"
    assert _mask_auth_value("token mytoken") == "token xxxxxxx"
    assert _mask_auth_value("Basic user:pass") == "Basic xxxx:xxxx"
    assert _mask_auth_value("just-a-token") == "xxxx-x-xxxxx"

def test_mask_string():
    original = "sensitive data"
    masked = _mask_string(original)
    assert masked != original
    assert len(masked) == len(original)
    # Should be deterministic
    assert _mask_string(original) == masked

def test_mask_int():
    original = 12345
    masked = _mask_int(original)
    assert masked != original
    assert isinstance(masked, int)
    # Should be deterministic
    assert _mask_int(original) == masked

def test_sanitize_cassette_data_dict():
    data = {
        "interactions": [
            {
                "request": {
                    "headers": {"Authorization": ["Bearer secret"]},
                    "body": {"string": '{"token": "mytoken"}'}
                },
                "response": {
                    "body": {"string": '{"access_token": "hidden"}'}
                }
            }
        ]
    }
    changed = sanitize_cassette_data(data)
    assert changed
    
    # Check headers
    auth_header = data["interactions"][0]["request"]["headers"]["Authorization"][0]
    assert auth_header == "Bearer xxxxxx"
    
    # Check request body
    req_body = data["interactions"][0]["request"]["body"]["string"]
    assert "mytoken" not in req_body
    
    # Check response body
    res_body = data["interactions"][0]["response"]["body"]["string"]
    assert "hidden" not in res_body

def test_sanitize_cassette_data_no_change():
    data = {"interactions": [{"request": {}, "response": {}}]}
    changed = sanitize_cassette_data(data)
    assert not changed
