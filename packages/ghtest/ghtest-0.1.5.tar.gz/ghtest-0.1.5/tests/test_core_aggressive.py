import pytest
from unittest.mock import MagicMock, patch
from ghtest.core import create_tests

def test_create_tests(tmp_path):
    # Mock dependencies
    with patch("ghtest.core.scan") as mock_scan, \
         patch("ghtest.core.suggest") as mock_suggest, \
         patch("ghtest.core.make_test") as mock_make_test, \
         patch("ghtest.core._run_tests") as mock_run_tests, \
         patch("ghtest.core.write_module") as mock_write_module, \
         patch("shutil.rmtree") as mock_rmtree:
        
        # Setup mocks
        func = MagicMock()
        func.qualname = "foo"
        mock_scan.return_value = [func]
        
        sp = MagicMock()
        sp.param_sets = [{}]
        sp.qualname = "foo"
        mock_suggest.return_value = sp
        
        gt = MagicMock()
        mock_make_test.return_value = gt
        
        tr = MagicMock()
        mock_run_tests.return_value = [tr]
        
        # Run create_tests
        cassette_dir = str(tmp_path / "cassettes")
        test_dir = str(tmp_path / "tests")
        src_dir = str(tmp_path / "src")
        
        scs, sps, gts, trs = create_tests(
            cassette_dir=cassette_dir,
            test_dir=test_dir,
            src_dir=src_dir,
            clean_up=True,
            unsafe=True,
            history=False,
            vb=2
        )
        
        # Verify interactions
        mock_scan.assert_called_with(src_dir)
        mock_suggest.assert_called()
        mock_make_test.assert_called()
        mock_run_tests.assert_called()
        mock_write_module.assert_called()
        
        assert len(scs) == 1
        assert len(sps) == 1
        assert len(gts) == 1
        assert len(trs) == 1
