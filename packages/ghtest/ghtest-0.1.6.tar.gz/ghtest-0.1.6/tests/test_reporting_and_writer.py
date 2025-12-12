import pytest
from unittest.mock import MagicMock, patch, mock_open
from ghtest.analyze_tests import (
    print_scan,
    print_suggestion,
    print_test_summary,
    _load_test_data
)
from ghtest.tests_writer import (
    write_test_modules,
    TestArtifact
)
from ghtest.scanner import FunctionInfo, ParameterInfo
from ghtest.param_suggestor import SuggestedFunctionTests
from ghtest.test_utils import RunTestWithCassette, CaseTestResult

def test_print_scan(capsys):
    # Mock scan results
    func = FunctionInfo(module="m", qualname="f", filepath="f.py", docstring="", parameters=[], lineno=1, returns=None)
    
    print_scan([func])
    captured = capsys.readouterr()
    assert "f" in captured.out

def test_print_suggestion(capsys):
    s = SuggestedFunctionTests(module="m", filepath="f.py", qualname="f", docstring="", param_sets=[{"a": 1}])
    
    print_suggestion([s])
    captured = capsys.readouterr()
    assert "f" in captured.out
    assert "{'a': 1}" in captured.out

def test_print_test_summary(capsys):
    # Pass
    case_pass = CaseTestResult(target="f", params={}, return_value="ok", exception=None, printed="", file_reads=[], file_writes=[], return_summary={}, volatile_return_fields=[])
    tr_pass = RunTestWithCassette(cassette_path="c.yaml", cases=[case_pass])
    
    # Fail
    case_fail = CaseTestResult(target="f", params={}, return_value=None, exception=AssertionError("fail"), printed="", file_reads=[], file_writes=[], return_summary={}, volatile_return_fields=[])
    tr_fail = RunTestWithCassette(cassette_path="c.yaml", cases=[case_fail])
    
    # Mock _load_test_data and get_codes
    with patch("ghtest.analyze_tests._load_test_data") as mock_load, \
         patch("ghtest.analyze_tests.get_codes") as mock_get_codes:
        
        # scs, sps, gts, trs
        mock_load.return_value = ([], [], [], [tr_pass, tr_fail])
        mock_get_codes.return_value = {}
        
        print_test_summary(vb=2) # Need vb > 1 to print details
        
    captured = capsys.readouterr()
    # print_tests prints cassette base name (c), target (f), params ({})
    assert "yaml" in captured.out
    assert "f" in captured.out
    assert "{}" in captured.out

def test_load_test_data():
    with patch("os.path.isfile") as mock_isfile, \
         patch("builtins.open", mock_open()) as mock_file, \
         patch("dill.load") as mock_dill:
        
        mock_isfile.return_value = True
        mock_dill.side_effect = ["scs", "sps", "gts", "trs"]
        
        scs, sps, gts, trs = _load_test_data("dir")
        assert scs == "scs"
        assert trs == "trs"
        
        mock_isfile.return_value = False
        assert _load_test_data("dir") == (None, None, None, None)

def test_write_test_modules(tmp_path):
    # Create artifacts
    s = SuggestedFunctionTests(module="m", filepath="f.py", qualname="f", docstring="", param_sets=[])
    case = CaseTestResult(target="f", params={}, return_value="ok", exception=None, printed="", file_reads=[], file_writes=[], return_summary={}, volatile_return_fields=[])
    tr = RunTestWithCassette(cassette_path="c.yaml", cases=[case])
    artifact = TestArtifact(suggestion=s, run=tr)
    
    output_dir = tmp_path / "tests_out"
    
    # Write
    write_test_modules([artifact], str(output_dir))
    
    # Check file created
    generated_file = output_dir / "test_generated_0.py"
    assert generated_file.exists()
    content = generated_file.read_text()
    assert "def test_f_case_0():" in content
    assert "import_function('m', " in content
