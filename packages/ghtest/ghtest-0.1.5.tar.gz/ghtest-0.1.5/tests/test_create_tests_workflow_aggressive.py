import pytest
from unittest.mock import MagicMock, patch
from ghtest.create_tests_workflow import _run_tests, create_tests

def test_run_tests():
    # Success case
    gt1 = MagicMock()
    gt1.test_callable.return_value = "result1"
    
    gt2 = MagicMock()
    gt2.test_callable.return_value = "result2"
    
    results = _run_tests([gt1, gt2], interactive=False, vb=0)
    assert results == ["result1", "result2"]
    
    # Failure case
    gt3 = MagicMock()
    gt3.test_callable.side_effect = Exception("oops")
    
    results = _run_tests([gt3], interactive=False, vb=1)
    assert results == [None]

def test_create_tests_flow(tmp_path):
    # Mock dependencies
    with patch("ghtest.create_tests_workflow.scan") as mock_scan, \
         patch("ghtest.create_tests_workflow.suggest") as mock_suggest, \
         patch("ghtest.create_tests_workflow.make_test") as mock_make_test, \
         patch("ghtest.create_tests_workflow.write_module") as mock_write, \
         patch("ghtest.create_tests_workflow._run_tests") as mock_run:
         
        mock_scan.return_value = [MagicMock(qualname="func1", crud_role=None)]
        mock_suggest.return_value = MagicMock(param_sets=[{}])
        mock_make_test.return_value = MagicMock()
        mock_run.return_value = ["result"]
        
        cassette_dir = str(tmp_path / "cassettes")
        test_dir = str(tmp_path / "tests")
        src_dir = str(tmp_path / "src")
        
        scs, sps, gts, trs = create_tests(
            cassette_dir, test_dir, src_dir,
            clean_up=True, unsafe=True, history=False, vb=1
        )
        
        assert len(scs) == 1
        assert len(sps) == 1
        assert len(gts) == 1
        assert len(trs) == 1
        
        mock_scan.assert_called_once()
        assert mock_suggest.call_count >= 1
        assert mock_make_test.call_count >= 1
        assert mock_run.call_count >= 1
        mock_write.assert_called_once()
