import pytest
import os
from pathlib import Path
from unittest.mock import MagicMock
from ghtest.tests_writer import (
    _format_assignment,
    _make_test_name,
    _exception_assertion_lines,
    _relativize_path_code,
    _format_file_access_list,
    CaseTestResult
)

def test_format_assignment():
    assert _format_assignment("x", "1") == "    x = 1"
    assert _format_assignment("y", "'foo'") == "    y = 'foo'"
    
    multiline = "{\n    'a': 1\n}"
    expected = "    d = {\n        'a': 1\n    }"
    # The function splits lines and prepends indentation
    # Let's verify exact behavior
    res = _format_assignment("d", multiline)
    assert "d = {" in res
    assert "    'a': 1" in res

def test_make_test_name():
    assert _make_test_name("my_func", 0) == "test_my_func_case_0"
    assert _make_test_name("Class.method", 1) == "test_Class_method_case_1"
    assert _make_test_name("___", 2) == "test_func_case_2"

def test_exception_assertion_lines():
    case = MagicMock(spec=CaseTestResult)
    
    # No exception
    case.exception = None
    lines = _exception_assertion_lines(case, "type")
    assert len(lines) == 1
    assert "assert result.exception is None" in lines[0]
    
    # With exception
    case.exception = ValueError("oops")
    
    # Mode: none
    assert _exception_assertion_lines(case, "none") == []
    
    # Mode: type
    lines = _exception_assertion_lines(case, "type")
    assert len(lines) == 2
    assert "assert result.exception is not None" in lines[0]
    assert "builtins.ValueError" in lines[1]
    
    # Mode: message
    lines = _exception_assertion_lines(case, "message")
    assert len(lines) == 3
    assert "assert str(result.exception) == 'oops'" in lines[2]

def test_relativize_path_code(tmp_path):
    base = tmp_path
    
    # Relative path
    p1 = base / "foo.txt"
    code = _relativize_path_code(str(p1), base)
    assert "foo.txt" in code
    assert "Path(__file__).parent" in code
    
    # Absolute path outside
    p2 = Path("/other/path.txt")
    code = _relativize_path_code(str(p2), base)
    assert "/other/path.txt" in code
    
    # Empty
    assert _relativize_path_code("", base) == "''"

def test_format_file_access_list(tmp_path):
    base = tmp_path
    access = [
        (str(base / "foo.txt"), "r"),
        (str(base / "bar.txt"), "w")
    ]
    code = _format_file_access_list(access, base)
    assert "foo.txt" in code
    assert "bar.txt" in code
    assert "'r'" in code
    assert "'w'" in code
    assert code.startswith("[")
    assert code.endswith("]")
