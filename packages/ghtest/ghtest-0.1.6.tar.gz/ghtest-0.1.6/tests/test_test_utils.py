import os
from pathlib import Path
import pytest
from ghtest.test_utils import (
    call_with_capture,
    import_function,
    _normalize_path,
    CaseTestResult
)

def dummy_function(x, y=1):
    print(f"x={x}, y={y}")
    return x + y

def dummy_file_access(path, mode='r'):
    with open(path, mode) as f:
        return f.read()

def test_call_with_capture_basic():
    result = call_with_capture(
        dummy_function,
        target="dummy_function",
        params={"x": 10, "y": 20}
    )
    assert result.return_value == 30
    assert result.printed == "x=10, y=20\n"
    assert result.exception is None

def test_call_with_capture_exception():
    def failing_function():
        raise ValueError("oops")
        
    result = call_with_capture(
        failing_function,
        target="failing_function",
        params={}
    )
    assert result.return_value is None
    assert isinstance(result.exception, ValueError)

def test_normalize_path_relative():
    # Test that paths inside CWD are relativized
    cwd = Path.cwd()
    abs_path = cwd / "foo/bar.txt"
    normalized = _normalize_path(str(abs_path))
    assert normalized == "foo/bar.txt"

def test_normalize_path_absolute():
    # Test that paths outside CWD remain absolute (or at least valid)
    # On unix, /tmp is usually outside user CWD
    abs_path = Path("/tmp/foo.txt")
    normalized = _normalize_path(str(abs_path))
    assert normalized == str(abs_path.resolve())

def test_capture_file_access(tmp_path):
    # Create a dummy file
    test_file = tmp_path / "test.txt"
    test_file.write_text("hello")
    
    # We need to change CWD to tmp_path for relative path test to work reliably
    # or just check that it captures *some* path
    
    # Let's use a file in current directory for relative path check
    local_file = Path("test_capture.txt")
    local_file.write_text("content")
    
    try:
        result = call_with_capture(
            dummy_file_access,
            target="dummy_file_access",
            params={"path": str(local_file)}
        )
        assert result.exception is None
        # Check that read was captured
        assert len(result.file_reads) > 0
        path, mode = result.file_reads[0]
        assert path == "test_capture.txt"
        assert "r" in mode
    finally:
        if local_file.exists():
            local_file.unlink()
