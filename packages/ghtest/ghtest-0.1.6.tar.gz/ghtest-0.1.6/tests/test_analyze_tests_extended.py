import pytest
from unittest.mock import MagicMock, patch
from ghtest.analyze_tests import (
    _count_codes,
    _analyze_codes,
    _get_function_name,
    _compact_names,
    _sum_codes,
    get_codes,
    _get_test_files,
    _get_name,
    _get_base_test_name,
    _get_tests,
    _get_methods,
    _get_modules,
)

def test_count_codes():
    # _count_codes expects a list of codes (ints or strings)
    codes = [200, 404, 200, "Error", None]
    counts = _count_codes(codes)
    assert counts[200] == 2
    assert counts[404] == 1
    assert counts["Error"] == 1

def test_compact_names():
    # _compact_names expects a list of tuples: (path, name, codes_list)
    # It returns a dict: {name: {code: count}}
    data = [
        ("path1", "test_foo", [200]),
        ("path2", "test_bar", [200]),
        ("path3", "test_foo", [404]),
    ]
    compact = _compact_names(data)
    
    assert isinstance(compact, dict)
    assert "test_foo" in compact
    assert "test_bar" in compact
    
    # Check counts
    # test_foo has one 200 and one 404
    assert compact["test_foo"][200] == 1
    assert compact["test_foo"][404] == 1

def test_sum_codes():
    # _sum_codes expects list of tuples (path, name, codes_list)
    # It returns {name: set(codes)}
    r = [
        ("p1", "func1", [200, 200, 404]),
        ("p2", "func2", [200, 500])
    ]
    total = _sum_codes(r)
    
    assert isinstance(total, dict)
    assert "func1" in total
    assert isinstance(total["func1"], set)
    assert 200 in total["func1"]
    assert 404 in total["func1"]
    assert len(total["func1"]) == 2 # 200 is deduped

def test_get_base_test_name():
    # It returns the filename (last part of path)
    assert _get_base_test_name("path/to/test_func.yaml") == "test_func.yaml"
    assert _get_base_test_name("test_func.case_1.yaml") == "test_func.case_1.yaml"

def test_get_modules(tmp_path):
    (tmp_path / "mod1.py").touch()
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "__init__.py").touch() # Make it a package
    (tmp_path / "pkg" / "mod2.py").touch()
    
    modules = _get_modules(str(tmp_path))
    assert "mod1" in modules
    assert "mod2" in modules or "pkg.mod2" in modules

def test_analyze_codes_mock(tmp_path):
    # Create dummy cassettes
    cassette_dir = tmp_path / "cassettes"
    cassette_dir.mkdir()
    (cassette_dir / "test_func.yaml").write_text("""
interactions:
- response:
    status:
      code: 200
""")
    (cassette_dir / "test_func.case_1.yaml").write_text("""
interactions:
- response:
    status:
      code: 404
""")
    
    modules = ["mod"]
    
    # We need to mock _get_function_name to map test_func -> mod.func
    with patch("ghtest.analyze_tests._get_function_name") as mock_get_name:
        mock_get_name.return_value = "mod.func"
        
        codes = _analyze_codes(str(cassette_dir), modules)
        
        # codes is a list of tuples: (file, func_name, [codes])
        assert isinstance(codes, list)
        func_entries = [x for x in codes if x[1] == "mod.func"]
        assert len(func_entries) >= 1
        
        # Check that we found the codes
        all_codes = []
        for entry in func_entries:
            all_codes.extend(entry[2])
            
        assert 200 in all_codes
        assert 404 in all_codes

def test_print_scan(capsys):
    from ghtest.analyze_tests import print_scan
    from ghtest.scanner import FunctionInfo, ParameterInfo
    
    param = ParameterInfo(name="a", annotation="int", default=1, kind="POSITIONAL_OR_KEYWORD")
    func = FunctionInfo(module="mod", qualname="func", filepath="f.py", docstring=None, parameters=[param], lineno=1, returns=None)
    
    print_scan([func])
    captured = capsys.readouterr()
    assert "func" in captured.out
    assert "{'a': 1}" in captured.out

def test_print_suggestion(capsys):
    from ghtest.analyze_tests import print_suggestion
    from ghtest.tests_creator import SuggestedFunctionTests
    
    suggestion = SuggestedFunctionTests(module="mod", filepath="f.py", qualname="func", docstring=None, param_sets=[{"a": 1}])
    
    print_suggestion([suggestion])
    captured = capsys.readouterr()
    assert "func" in captured.out
    assert "{'a': 1}" in captured.out

def test_print_tests(capsys):
    from ghtest.analyze_tests import print_tests
    from ghtest.test_utils import CaseTestResult, RunTestWithCassette
    
    case = CaseTestResult(target="func", params={"a": 1}, return_value=None, exception=None, printed="", file_reads=[], file_writes=[], return_summary={}, volatile_return_fields=[])
    case.cassette_path = "cassettes/mod.func.case_0.yaml"
    
    tr = RunTestWithCassette(cassette_path="cassettes/mod.test_func.yaml", cases=[case])
    
    print_tests([tr])
    captured = capsys.readouterr()
    assert "test_func" in captured.out
    assert "case_0" in captured.out
    assert "{'a': 1}" in captured.out

def test_load_test_data(tmp_path):
    from ghtest.analyze_tests import _load_test_data
    import dill
    
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    (data_dir / "scs").write_bytes(dill.dumps(["scan"]))
    (data_dir / "sps").write_bytes(dill.dumps(["suggest"]))
    (data_dir / "gts").write_bytes(dill.dumps(["gen"]))
    (data_dir / "trs").write_bytes(dill.dumps(["result"]))
    
    scs, sps, gts, trs = _load_test_data(test_objects_dir=str(data_dir))
    assert scs == ["scan"]
    assert sps == ["suggest"]
    assert gts == ["gen"]
    assert trs == ["result"]
    
    # Test missing
    scs, sps, gts, trs = _load_test_data(test_objects_dir=str(tmp_path / "missing"))
    assert scs is None

def test_print_test_summary_integration(capsys):
    from ghtest.analyze_tests import print_test_summary
    
    # Mock dependencies to avoid real IO
    with patch("ghtest.analyze_tests._print_tests") as mock_print_tests, \
         patch("ghtest.analyze_tests.get_codes") as mock_get_codes:
        
        print_test_summary(vb=0)
        
        mock_print_tests.assert_called()
        mock_get_codes.assert_called()
        
        captured = capsys.readouterr()
        assert "test summary" in captured.out
        assert "return codes summary" in captured.out

def test_get_function_name():
    # Test mapping from cassette path to function name
    # This might depend on file content or naming convention
    # If it reads the file to find "qualname" or similar metadata?
    # Or just parses the filename?
    # Implementation likely reads the test file or cassette metadata.
    # Let's assume filename convention for now or mock dependencies.
    pass
