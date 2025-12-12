import pytest
from unittest.mock import MagicMock, patch, ANY
from ghtest.create_tests_workflow import create_tests, workflow

@pytest.fixture
def mock_components():
    with patch("ghtest.create_tests_workflow.scan") as mock_scan, \
         patch("ghtest.create_tests_workflow.suggest") as mock_suggest, \
         patch("ghtest.create_tests_workflow.make_test") as mock_make_test, \
         patch("ghtest.create_tests_workflow.write_module") as mock_write_module, \
         patch("ghtest.create_tests_workflow._run_tests") as mock_run_tests, \
         patch("ghtest.create_tests_workflow.shutil.rmtree") as mock_rmtree, \
         patch("ghtest.create_tests_workflow.os.makedirs") as mock_makedirs, \
         patch("ghtest.create_tests_workflow.dill.dump") as mock_dill_dump:
        
        yield {
            "scan": mock_scan,
            "suggest": mock_suggest,
            "make_test": mock_make_test,
            "write_module": mock_write_module,
            "run_tests": mock_run_tests,
            "rmtree": mock_rmtree,
            "makedirs": mock_makedirs,
            "dill_dump": mock_dill_dump
        }

def test_create_tests_basic(mock_components):
    # Setup mocks
    mock_func = MagicMock()
    mock_func.qualname = "func"
    mock_func.crud_role = "read"
    mock_func.crud_resource = "res"
    mock_components["scan"].return_value = [mock_func]
    
    mock_suggestion = MagicMock()
    mock_suggestion.qualname = "func"
    mock_suggestion.param_sets = [{"a": 1}]
    mock_suggestion.scenario = None
    mock_components["suggest"].return_value = mock_suggestion
    
    mock_test = MagicMock()
    mock_components["make_test"].return_value = mock_test
    
    mock_result = MagicMock()
    mock_components["run_tests"].return_value = [mock_result]
    
    # Mock coverage to raise ImportError to skip feedback loop
    with patch.dict("sys.modules", {"coverage": None}):
        # Run
        scs, sps, gts, trs = create_tests(
            cassette_dir="cassettes",
            test_dir="tests",
            src_dir="src",
            clean_up=True,
            unsafe=True,
            history=False,
            vb=1
        )
    
    # Verify
    mock_components["scan"].assert_called_with("src")
    mock_components["suggest"].assert_called_with(mock_func, literal_only=False)
    mock_components["make_test"].assert_called_with(suggestion=mock_suggestion, cassette_dir="cassettes")
    mock_components["run_tests"].assert_called()
    mock_components["write_module"].assert_called()
    
    assert len(scs) == 1
    assert len(sps) == 1
    assert len(gts) == 1
    assert len(trs) == 1

def test_create_tests_with_coverage_feedback(mock_components):
    # Setup mocks
    mock_func = MagicMock()
    mock_func.qualname = "func"
    mock_components["scan"].return_value = [mock_func]
    
    mock_suggestion = MagicMock()
    mock_suggestion.param_sets = []
    mock_components["suggest"].return_value = mock_suggestion
    
    # Mock coverage
    mock_cov_module = MagicMock()
    mock_cov_instance = MagicMock()
    mock_cov_module.Coverage.return_value = mock_cov_instance
    
    with patch.dict("sys.modules", {"coverage": mock_cov_module}):
        create_tests(
            cassette_dir="cassettes",
            test_dir="tests",
            src_dir="src",
            vb=1
        )
        
        # Verify coverage was used
        mock_cov_module.Coverage.assert_called()
        mock_cov_instance.start.assert_called()
        mock_cov_instance.stop.assert_called()
        
        # Verify suggest was called twice (initial + targeted)
        assert mock_components["suggest"].call_count == 2
        # Second call should include coverage_data
        args, kwargs = mock_components["suggest"].call_args_list[1]
        assert "coverage_data" in kwargs

def test_workflow(mock_components):
    # Mock create_tests to avoid re-testing its logic
    with patch("ghtest.create_tests_workflow.create_tests") as mock_create_tests, \
         patch("builtins.open", new_callable=MagicMock):
        mock_create_tests.return_value = ([], [], [], [])
        
        workflow("src", "tests", "cassettes")
        
        mock_create_tests.assert_called_with("cassettes", "tests", "src")
        # Verify dill dump was called 4 times (scs, sps, gts, trs)
        assert mock_components["dill_dump"].call_count == 4
