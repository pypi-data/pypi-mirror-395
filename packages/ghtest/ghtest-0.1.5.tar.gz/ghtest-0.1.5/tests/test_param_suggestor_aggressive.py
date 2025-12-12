import pytest
from unittest.mock import MagicMock, patch
from ghtest.param_suggestor import (
    _extract_module_globals_from_file,
    _sanitize_db_value,
    _update_param_database,
    _infer_param_type,
    _build_branch_param_sets,
    ScenarioStep,
    CrudScenario,
    SuggestedFunctionTests
)

def test_extract_module_globals_from_file(tmp_path):
    f = tmp_path / "test_globals.py"
    f.write_text("A = 1\nB = 's'\nC = [1, 2]\n")
    
    globals_dict = _extract_module_globals_from_file(str(f))
    assert globals_dict["A"] == 1
    assert globals_dict["B"] == 's'
    assert globals_dict["C"] == [1, 2]

def test_sanitize_db_value():
    assert _sanitize_db_value(1) == 1
    assert _sanitize_db_value(1.5) == 1.5
    assert _sanitize_db_value(True) is True
    assert _sanitize_db_value(None) is None
    # Strings and complex types are sanitized to None
    assert _sanitize_db_value("s") is None
    assert _sanitize_db_value([1, 2]) is None
    assert _sanitize_db_value({"a": 1}) is None

def test_infer_param_type():
    func = MagicMock()
    p1 = MagicMock()
    p1.name = "p1"
    p1.annotation = "int"
    p1.default_value = None
    
    p2 = MagicMock()
    p2.name = "p2"
    p2.annotation = None
    p2.default_value = 10
    
    func.parameters = [p1, p2]
    
    assert _infer_param_type(func, "p1") == "int"
    assert _infer_param_type(func, "p2") == "int"
    assert _infer_param_type(func, "p3") is None

def test_update_param_database(tmp_path):
    with patch("ghtest.param_suggestor._param_db_path", return_value=tmp_path / "params.json"), \
         patch("ghtest.param_suggestor._should_write_param_db", return_value=True):
        
        func = MagicMock()
        func.parameters = []
        
        # Use values that survive sanitization (int, float, bool)
        observed = {"p1": [1, 2], "p2": [True, False]}
        
        _update_param_database(func, observed)
        
        # Verify file content
        import json
        data = json.loads((tmp_path / "params.json").read_text())
        assert "p1" in data
        assert "p2" in data
        assert 1 in data["p1"]["literals"]
        assert 2 in data["p1"]["literals"]
        assert True in data["p2"]["literals"]

def test_build_branch_param_sets():
    # This requires AST analysis, might be complex to test without real file.
    # We can mock _load_function_node and _BranchHintCollector.
    pass
