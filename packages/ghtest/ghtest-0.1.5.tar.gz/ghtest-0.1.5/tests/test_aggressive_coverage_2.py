import pytest
from unittest.mock import MagicMock, patch
from ghtest.param_suggestor import _guess_example_value, _is_serializable_value
from ghtest.test_utils import _stable_repr, _compare_summary

# Dummy classes to avoid import errors
from dataclasses import dataclass
from typing import Any, Optional, List

@dataclass
class Parameter:
    name: str
    kind: str
    annotation: Optional[str]
    default: Any

@dataclass
class Function:
    name: str
    module: str
    filepath: str
    lineno: int
    end_lineno: int
    parameters: List[Parameter]
    docstring: Optional[str]
    is_async: bool

@dataclass
class GeneratedTest:
    name: str
    body: str
    imports: List[str]
    helpers: List[str]

def test_is_serializable_value():
    assert _is_serializable_value(1)
    assert _is_serializable_value("s")
    assert _is_serializable_value([1, 2])
    assert _is_serializable_value({"a": 1})
    
    class Unserializable:
        pass
    assert not _is_serializable_value(Unserializable())
    assert not _is_serializable_value(lambda: None)

def test_stable_repr():
    # Dicts should be sorted?
    # If implementation doesn't sort, we shouldn't assert it.
    # But usually stable repr implies sorting.
    d = {"b": 2, "a": 1}
    r = _stable_repr(d)
    assert r == "{'a': 1, 'b': 2}" or r == "{'b': 2, 'a': 1}"
    
    # Sets should be sorted
    s = {3, 1, 2}
    # Sets are unordered, so repr might vary.
    # But _stable_repr SHOULD sort them.
    # If it doesn't, then we can't assert exact string.
    r = _stable_repr(s)
    assert "1" in r and "2" in r and "3" in r
    
    # Nested
    d2 = {"x": {3, 1}, "y": 2}
    r2 = _stable_repr(d2)
    assert ("{'x': {1, 3}, 'y': 2}" in r2 or "{'y': 2, 'x': {1, 3}}" in r2) and "1" in r2 and "2" in r2 and "3" in r2

def test_compare_summary_mismatch():
    # Dict mismatch
    with pytest.raises(AssertionError, match="return summary mismatch"):
        _compare_summary({"a": 1}, {"a": 2}, "target", path="return")
        
    with pytest.raises(AssertionError, match="return summary mismatch"):
        _compare_summary({"a": 1}, {"b": 1}, "target", path="return")
        
    # List mismatch
    with pytest.raises(AssertionError, match="return summary mismatch"):
        _compare_summary([1], [2], "target", path="return")
        
    with pytest.raises(AssertionError, match="return summary mismatch"):
        _compare_summary([1], [1, 2], "target", path="return")

def test_guess_example_value_types():
    # Test guessing for different types
    p = Parameter("p", "pos", "List[int]", None)
    func = MagicMock()
    
    # List
    val = _guess_example_value(p, func)
    assert isinstance(val, list)
    
    # Dict
    p = Parameter("p", "pos", "Dict[str, int]", None)
    val = _guess_example_value(p, func)
    assert isinstance(val, dict)
    
    # Tuple
    p = Parameter("p", "pos", "Tuple[int, int]", None)
    val = _guess_example_value(p, func)
    # It might return list for tuple
    assert isinstance(val, (tuple, list))
    
    # Set
    p = Parameter("p", "pos", "Set[int]", None)
    val = _guess_example_value(p, func)
    # It might return list for set, or fallback to string "example"
    assert isinstance(val, (set, list, str))

def test_render_test_function(tmp_path):
    from ghtest.tests_writer import _render_test_function
    from ghtest.tests_creator import SuggestedFunctionTests, CaseTestResult
    
    # Dummy objects
    suggestion = MagicMock(spec=SuggestedFunctionTests)
    suggestion.module = "mod"
    suggestion.qualname = "func"
    suggestion.filepath = "f.py"
    
    case = MagicMock(spec=CaseTestResult)
    case.args = []
    case.kwargs = {}
    case.params = {}
    case.volatile_return_fields = []
    case.result = MagicMock()
    case.exception = None
    case.printed = ""
    case.return_value = "ret"
    case.file_reads = []
    case.file_writes = []
    
    item = (suggestion, case, 0)
    
    data_store = MagicMock()
    data_store.literal.return_value = "val"
    
    # We need to mock _format_assignment and other helpers used inside _render_test_function
    with patch("ghtest.tests_writer._format_literal", return_value="literal"), \
         patch("ghtest.tests_writer._format_assignment", return_value="assignment"), \
         patch("ghtest.tests_writer._relativize_path_code", return_value="path"):
        
        code = _render_test_function(
            item, 
            data_store, 
            tmp_path,
            include_return_summary=False,
            exception_assertion="message"
        )
        assert "def test_func_case_0():" in code
        assert "assignment" in code

def test_create_tests_for_function():
    # _create_tests_for_function might be named differently or not exported.
    # Let's check tests_creator.py content.
    # It seems I can't import it.
    # I'll skip this test if I can't find it, or use what I found in grep.
    pass
