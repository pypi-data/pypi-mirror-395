import ast
import pytest
from pathlib import Path
from ghtest.param_suggestor import (
    _extract_module_globals_from_file,
    _extract_literal_assignments_from_file,
    _looks_like_env_placeholder,
    _strip_numeric_suffix,
    _select_preferred_hint,
    _guess_example_value,
    _build_minimal_kwargs,
    _guess_alternative_value,
)
from ghtest.scanner import FunctionInfo, ParameterInfo

def test_extract_module_globals(tmp_path):
    p = tmp_path / "test_globals.py"
    p.write_text("""
import os
CONST_INT = 42
CONST_STR = "hello"
CONST_LIST = [1, 2, 3]
CONST_DICT = {"a": 1}
def foo():
    pass
NOT_A_CONST = "after def"
""")
    globals_dict = _extract_module_globals_from_file(str(p))
    assert globals_dict["CONST_INT"] == 42
    assert globals_dict["CONST_STR"] == "hello"
    assert globals_dict["CONST_LIST"] == [1, 2, 3]
    assert globals_dict["CONST_DICT"] == {"a": 1}
    assert "NOT_A_CONST" not in globals_dict

def test_extract_literal_assignments(tmp_path):
    p = tmp_path / "test_literals.py"
    p.write_text("""
def foo(x):
    y = 10
    z: int = 20
    name = "alice"
    
async def bar():
    val = 3.14
""")
    # The collector skips function bodies to avoid local assignments.
    # We need module-level assignments for this test to work as written, 
    # or we need to understand that _extract_literal_assignments_from_file *only* looks at module level?
    # Let's check implementation: visit_FunctionDef returns early.
    # So it ONLY collects module level assignments.
    # Let's rewrite the test case to use module level assignments.
    
    p.write_text("""
y = 10
z: int = 20
name = "alice"
val = 3.14
""")
    literals = _extract_literal_assignments_from_file(str(p))
    assert 10 in literals["y"]
    assert 20 in literals["z"]
    assert "alice" in literals["name"]
    assert 3.14 in literals["val"]

def test_looks_like_env_placeholder():
    # The function expects tokens to be lowercased (as they come from gname.lower())
    assert _looks_like_env_placeholder(["my", "secret"], "password")
    assert not _looks_like_env_placeholder(["api", "key"], "api_key")

def test_strip_numeric_suffix():
    assert _strip_numeric_suffix("item_1") == "item"
    assert _strip_numeric_suffix("user2") == "user"
    assert _strip_numeric_suffix("name") == "name"

def test_select_preferred_hint():
    assert _select_preferred_hint(None) is None
    assert _select_preferred_hint([]) is None
    assert _select_preferred_hint([1, 2, 3]) == 1
    # It returns the first non-None value.
    assert _select_preferred_hint(["", "foo"]) == ""
    assert _select_preferred_hint([None, "foo"]) == "foo"

def test_guess_example_value_basic():
    # Mock ParameterInfo
    param = ParameterInfo(name="count", annotation="int", default=None, kind="POSITIONAL_OR_KEYWORD")
    # FunctionInfo needs 'returns' argument
    func = FunctionInfo(module="mod", qualname="func", filepath="f.py", docstring=None, parameters=[param], lineno=1, returns=None)
    
    val = _guess_example_value(param, func)
    assert isinstance(val, int)

    param_str = ParameterInfo(name="name", annotation="str", default=None, kind="POSITIONAL_OR_KEYWORD")
    val_str = _guess_example_value(param_str, func)
    assert isinstance(val_str, str)

def test_guess_example_value_with_globals():
    param = ParameterInfo(name="limit", annotation="int", default=None, kind="POSITIONAL_OR_KEYWORD")
    func = FunctionInfo(module="mod", qualname="func", filepath="f.py", docstring=None, parameters=[param], lineno=1, returns=None)
    
    module_globals = {"DEFAULT_LIMIT": 100}
    val = _guess_example_value(param, func, module_globals=module_globals)
    assert val == 100

def test_dedupe_param_sets():
    from ghtest.param_suggestor import _dedupe_param_sets
    
    sets = [
        {"a": 1, "b": 2},
        {"a": 1, "b": 2},
        {"b": 2, "a": 1},
        {"a": 2, "b": 3}
    ]
    deduped = _dedupe_param_sets(sets)
    assert len(deduped) == 2
    assert {"a": 1, "b": 2} in deduped
    assert {"a": 2, "b": 3} in deduped

def test_extract_test_param_sets_for_func(tmp_path):
    from ghtest.param_suggestor import _extract_test_param_sets_for_func
    
    # Create a dummy test file
    p = tmp_path / "test_sample.py"
    p.write_text("""
def test_func():
    func(a=1, b=2)
    func(a=3, b=4)
    other_func(a=5)
""")
    
    # Mock FunctionInfo objects
    func = FunctionInfo(module="mod", qualname="func", filepath="f.py", docstring=None, parameters=[
        ParameterInfo("a", "POSITIONAL_OR_KEYWORD", "int", None),
        ParameterInfo("b", "POSITIONAL_OR_KEYWORD", "int", None)
    ], lineno=1, returns=None)
    
    test_func = FunctionInfo(module="tests.test_sample", qualname="test_func", filepath=str(p), docstring=None, parameters=[], lineno=1, returns=None)
    
    param_sets = _extract_test_param_sets_for_func(func, [test_func])
    
    assert len(param_sets) == 2
    assert {"a": 1, "b": 2} in param_sets
    assert {"a": 3, "b": 4} in param_sets

def test_suggest_params_integration(tmp_path):
    from ghtest.param_suggestor import suggest_params
    
    # Mock FunctionInfo
    param = ParameterInfo(name="x", annotation="int", default=None, kind="POSITIONAL_OR_KEYWORD")
    func = FunctionInfo(module="mod", qualname="func", filepath="f.py", docstring=None, parameters=[param], lineno=1, returns=None)
    
    # Test with no existing tests
    suggestion = suggest_params(func, test_functions=[])
    assert len(suggestion.param_sets) > 0
    assert "x" in suggestion.param_sets[0]
    assert isinstance(suggestion.param_sets[0]["x"], int)

def test_guess_alternative_value():
    assert _guess_alternative_value(True) is False
    assert _guess_alternative_value(False) is True
    assert _guess_alternative_value(10) != 10
    assert isinstance(_guess_alternative_value(10), int)
    assert _guess_alternative_value("foo") != "foo"
    assert isinstance(_guess_alternative_value("foo"), str)
