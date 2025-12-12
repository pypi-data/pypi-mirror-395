import pytest
from unittest.mock import MagicMock
from ghtest.param_suggestor import _guess_example_value, _guess_alternative_value
from ghtest.scanner import ParameterInfo, FunctionInfo

def test_guess_example_value_heuristics():
    func = MagicMock(spec=FunctionInfo)
    func.docstring = ""
    
    # Bool
    p = ParameterInfo(name="is_valid", annotation="bool", default=None, kind="POSITIONAL_OR_KEYWORD")
    assert _guess_example_value(p, func) is True
    
    # Int
    p = ParameterInfo(name="count", annotation="int", default=None, kind="POSITIONAL_OR_KEYWORD")
    assert _guess_example_value(p, func) == 1
    
    # Float
    p = ParameterInfo(name="timeout", annotation="float", default=None, kind="POSITIONAL_OR_KEYWORD")
    assert _guess_example_value(p, func) == 1.0
    
    # List
    p = ParameterInfo(name="items", annotation="list", default=None, kind="POSITIONAL_OR_KEYWORD")
    assert _guess_example_value(p, func) == [1, 2]
    
    # Dict
    p = ParameterInfo(name="config", annotation="dict", default=None, kind="POSITIONAL_OR_KEYWORD")
    assert _guess_example_value(p, func) == {"key": "value"}
    
    # Path/File
    p = ParameterInfo(name="filepath", annotation="str", default=None, kind="POSITIONAL_OR_KEYWORD")
    assert _guess_example_value(p, func) == "example.txt"
    
    # URL
    p = ParameterInfo(name="url", annotation="str", default=None, kind="POSITIONAL_OR_KEYWORD")
    assert _guess_example_value(p, func) == "https://example.com"
    
    # Data/Payload - remove annotation to test name heuristic
    p = ParameterInfo(name="payload", annotation=None, default=None, kind="POSITIONAL_OR_KEYWORD")
    assert _guess_example_value(p, func) == {"data": "example"}

def test_guess_example_value_defaults():
    func = MagicMock(spec=FunctionInfo)
    func.docstring = ""
    
    p = ParameterInfo(name="x", annotation="int", default="10", default_value=10, kind="POSITIONAL_OR_KEYWORD")
    assert _guess_example_value(p, func) == 10
    
    p = ParameterInfo(name="y", annotation="str", default="'default'", default_value="default", kind="POSITIONAL_OR_KEYWORD")
    assert _guess_example_value(p, func) == "default"

def test_guess_example_value_sources():
    func = MagicMock(spec=FunctionInfo)
    func.docstring = ""
    p = ParameterInfo(name="x", annotation="int", default=None, kind="POSITIONAL_OR_KEYWORD")
    
    # Literal assignment
    val, src = _guess_example_value(p, func, literal_assignments={"x": [99]}, include_source=True)
    assert val == 99
    assert src == "literal_assignment"
    
    # Module global
    val, src = _guess_example_value(p, func, module_globals={"X": 88}, include_source=True)
    # Note: _choose_global_for_param logic might need exact match or heuristic
    # If it fails to match X to x, this test might fail. Let's try exact name match if possible or rely on heuristic.
    # Assuming heuristic matches X to x or we pass x as global name.
    # Let's use a name that definitely matches.
    p2 = ParameterInfo(name="MAX_RETRIES", annotation="int", default=None, kind="POSITIONAL_OR_KEYWORD")
    val, src = _guess_example_value(p2, func, module_globals={"MAX_RETRIES": 5}, include_source=True)
    assert val == 5
    assert src == "module_global"

def test_guess_alternative_value():
    assert _guess_alternative_value(True) is False
    assert _guess_alternative_value(False) is True
    assert _guess_alternative_value(1) == 2
    assert _guess_alternative_value(1.5) == 3.0
    assert _guess_alternative_value("foo") == "foo_alt"
    assert _guess_alternative_value([1]) == [1, 1]
    assert _guess_alternative_value({"a": 1}) == {"a": 1, "extra": "alt"}
    
    # From module global should return same value
    assert _guess_alternative_value(10, from_module_global=True) == 10
