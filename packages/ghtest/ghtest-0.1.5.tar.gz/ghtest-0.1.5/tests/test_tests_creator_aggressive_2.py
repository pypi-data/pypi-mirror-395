import pytest
import ast
from unittest.mock import MagicMock, patch
from ghtest.tests_creator import (
    _looks_destructive_name,
    _is_destructive_call,
    _function_body_has_destructive_calls,
    _format_step_summary,
    ScenarioStep,
    _should_confirm_execution,
    _prompt_user_confirmation
)

def test_looks_destructive_name():
    assert _looks_destructive_name("remove_user")
    assert _looks_destructive_name("delete_file")
    assert _looks_destructive_name("destroy_world")
    assert _looks_destructive_name("drop_table")
    assert _looks_destructive_name("rm_rf")
    assert not _looks_destructive_name("get_user")
    assert not _looks_destructive_name("create_file")

def test_is_destructive_call():
    # os.remove("file")
    call = ast.Call(
        func=ast.Attribute(
            value=ast.Name(id="os", ctx=ast.Load()),
            attr="remove",
            ctx=ast.Load()
        ),
        args=[], keywords=[]
    )
    assert _is_destructive_call(call)
    
    # shutil.rmtree("dir")
    call = ast.Call(
        func=ast.Attribute(
            value=ast.Name(id="shutil", ctx=ast.Load()),
            attr="rmtree",
            ctx=ast.Load()
        ),
        args=[], keywords=[]
    )
    assert _is_destructive_call(call)
    
    # remove("file")
    call = ast.Call(
        func=ast.Name(id="remove", ctx=ast.Load()),
        args=[], keywords=[]
    )
    assert _is_destructive_call(call)
    
    # print("hello")
    call = ast.Call(
        func=ast.Name(id="print", ctx=ast.Load()),
        args=[], keywords=[]
    )
    assert not _is_destructive_call(call)

def test_function_body_has_destructive_calls(tmp_path):
    # Destructive function
    dest_file = tmp_path / "destructive.py"
    dest_file.write_text("""
import os
def dangerous():
    os.remove("foo")
""")
    assert _function_body_has_destructive_calls(str(dest_file), "dangerous")
    
    # Safe function
    safe_file = tmp_path / "safe.py"
    safe_file.write_text("""
def safe():
    print("hello")
""")
    assert not _function_body_has_destructive_calls(str(safe_file), "safe")
    
    # Non-existent file
    assert not _function_body_has_destructive_calls(str(tmp_path / "missing.py"), "func")

def test_format_step_summary():
    step = ScenarioStep(
        module="mod",
        filepath="file.py",
        qualname="my_func",
        params={"a": 1, "b": "test"}
    )
    summary = _format_step_summary(step)
    assert "my_func" in summary
    assert "a=1" in summary
    assert "b='test'" in summary

def test_should_confirm_execution():
    # Destructive name
    s1 = MagicMock()
    s1.qualname = "delete_user"
    assert _should_confirm_execution(s1)
    
    # Destructive body
    s2 = MagicMock()
    s2.qualname = "clean_up"
    s2.filepath = "file.py"
    with patch("ghtest.tests_creator._function_body_has_destructive_calls", return_value=True):
        assert _should_confirm_execution(s2)
        
    # Safe
    s3 = MagicMock()
    s3.qualname = "get_user"
    s3.filepath = "file.py"
    with patch("ghtest.tests_creator._function_body_has_destructive_calls", return_value=False):
        assert not _should_confirm_execution(s3)

def test_prompt_user_confirmation():
    s = MagicMock()
    s.qualname = "delete_user"
    s.filepath = "file.py"
    
    with patch("builtins.input", return_value="y"):
        _prompt_user_confirmation(s)
        
    with patch("builtins.input", return_value="n"):
        with pytest.raises(RuntimeError):
            _prompt_user_confirmation(s)
