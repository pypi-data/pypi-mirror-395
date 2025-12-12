import pytest
import sys
import json
from unittest.mock import MagicMock, patch
from ghtest.scanner import ParameterInfo, FunctionInfo

# Dynamic access to the module
param_suggestor = sys.modules["ghtest.param_suggestor"]

def test_param_database_functions(tmp_path):
    # Test _load_param_database and _update_param_database
    db_path = tmp_path / "params.json"
    
    with patch("ghtest.param_suggestor._PARAM_DB_CACHE", None), \
         patch.dict("os.environ", {"GHTEST_PARAM_DB": str(db_path)}), \
         patch("ghtest.param_suggestor._PARAM_DB_DISABLE_ENV", "GHTEST_DISABLE_PARAM_DB_WRITE_TEST"):
        
        # Initial load (might not be empty due to defaults)
        db = param_suggestor._load_param_database()
        assert isinstance(db, dict)
        
        # Update
        func = MagicMock()
        func.qualname = "test_func_unique_name"
        observed = {"a": [1]}
        param_suggestor._update_param_database(func, observed)
        
        # Verify save
        assert db_path.exists()
        content = json.loads(db_path.read_text())
        assert "a" in content
        assert content["a"]["literals"] == [1]

def test_infer_type():
    # Verify function existence first
    if hasattr(param_suggestor, "_infer_type"):
        assert param_suggestor._infer_type(1) == "int"
        assert param_suggestor._infer_type("s") == "str"
        assert param_suggestor._infer_type(True) == "bool"
        assert param_suggestor._infer_type(1.0) == "float"
        assert param_suggestor._infer_type([]) == "list"
        assert param_suggestor._infer_type({}) == "dict"
        assert param_suggestor._infer_type(None) == "NoneType"

def test_generate_values_for_type():
    # Verify function existence first
    if hasattr(param_suggestor, "_generate_values_for_type"):
        # Int
        vals = param_suggestor._generate_values_for_type("int")
        assert all(isinstance(x, int) for x in vals)
        
        # Str
        vals = param_suggestor._generate_values_for_type("str")
        assert all(isinstance(x, str) for x in vals)

def test_suggest_params(tmp_path):
    func = MagicMock(spec=FunctionInfo)
    func.qualname = "my_func"
    func.module = "mod"
    func.filepath = "file.py"
    func.docstring = None
    func.parameters = [
        ParameterInfo(name="x", annotation="int", default=None, kind="POSITIONAL_OR_KEYWORD")
    ]
    
    # Mock dependencies
    with patch("ghtest.param_suggestor._load_param_history", return_value={}), \
         patch("ghtest.param_suggestor._load_param_database", return_value={}):
        
        suggestion = param_suggestor.suggest_params(func)
        assert len(suggestion.param_sets) > 0
        assert "x" in suggestion.param_sets[0]

def test_suggest_params_with_literals(tmp_path):
    func = MagicMock(spec=FunctionInfo)
    func.qualname = "my_func"
    func.module = "mod"
    func.filepath = "file.py"
    func.docstring = None
    func.parameters = [
        ParameterInfo(name="limit", annotation="int", default=None, kind="POSITIONAL_OR_KEYWORD")
    ]
    
    # Mock literal assignments extraction
    with patch("ghtest.param_suggestor._extract_literal_assignments_from_file", return_value={"limit": [10, 20]}), \
         patch("ghtest.param_suggestor._load_param_history", return_value={}), \
         patch("ghtest.param_suggestor._load_param_database", return_value={}):
        
        suggestion = param_suggestor.suggest_params(func)
        # Should suggest literal values
        values = [ps["limit"] for ps in suggestion.param_sets if "limit" in ps]
        assert 10 in values or 20 in values

def test_suggest_params_with_globals(tmp_path):
    func = MagicMock(spec=FunctionInfo)
    func.qualname = "my_func"
    func.module = "mod"
    func.filepath = "file.py"
    func.docstring = None
    func.parameters = [
        ParameterInfo(name="timeout", annotation="int", default=None, kind="POSITIONAL_OR_KEYWORD")
    ]
    func.module_globals = {"DEFAULT_TIMEOUT": 30}
    
    with patch("ghtest.param_suggestor._extract_literal_assignments_from_file", return_value={}), \
         patch("ghtest.param_suggestor._load_param_history", return_value={}), \
         patch("ghtest.param_suggestor._load_param_database", return_value={}):
        
        suggestion = param_suggestor.suggest_params(func)
        values = [ps["timeout"] for ps in suggestion.param_sets if "timeout" in ps]
        assert 30 in values


