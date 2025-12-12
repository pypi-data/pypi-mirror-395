import os
import shutil
from pathlib import Path
import pytest
from ghtest.core import create_tests

def test_create_tests_integration(tmp_path):
    # Setup paths
    # Setup paths
    testdata_dir = tmp_path / "src"
    testdata_dir.mkdir()
    (testdata_dir / "sample.py").write_text("""
def get_commits(name: str, dry_run: bool = False):
    pass
""")
    cassette_dir = tmp_path / "cassettes"
    test_out_dir = tmp_path / "tests"
    
    # Run create_tests
    # We use unsafe=True to avoid interactive prompts (though we shouldn't have destructive ops in this subset if we are careful, 
    # but testdata has delete_repo. However, create_tests runs them. 
    # Wait, create_tests executes the functions. If we run it on testdata, it will try to create/delete repos.
    # We should probably mock the actual execution or use a safer subset.
    # But for integration test, maybe we just want to see if it generates tests.
    
    # Actually, create_tests *runs* the generated tests to record cassettes.
    # If we run it on testdata/gh_api.py, it will try to hit GitHub API if we don't mock it.
    # But wait, testdata/gh_api.py has a dry_run parameter.
    # The suggestor should suggest dry_run=True.
    
    # However, to be safe and fast, maybe we should mock `_run_tests` inside core.py?
    # Or just let it run but expect it might fail if no creds?
    # But we want to test the *generation* logic.
    
    # Let's mock `_run_tests` to avoid actual execution during the integration test.
    # We just want to verify that it scans, suggests, and generates test objects.
    
    from unittest.mock import patch
    
    # Patch coverage.Coverage to avoid "No data was collected" warning
    # because we are mocking the actual execution (_run_tests)
    with patch("ghtest.core._run_tests") as mock_run, \
         patch("coverage.Coverage"):
        # Mock return value of _run_tests (list of TestResult)
        # It returns a list of CaseTestResult or None
        mock_run.return_value = [None] * 5 # Dummy return
        
        scs, sps, gts, trs = create_tests(
            cassette_dir=str(cassette_dir),
            test_dir=str(test_out_dir),
            src_dir=str(testdata_dir),
            clean_up=True,
            unsafe=True, # To avoid interactive prompt logic in core
            vb=0
        )
        
        # Verify results
        assert len(scs) > 0 # Should find functions
        assert len(sps) > 0 # Should suggest params
        assert len(gts) > 0 # Should generate tests
        
        # Verify output directory was created
        assert test_out_dir.exists()
        
        # Verify that write_module was called (which writes files)
        # Since we mocked _run_tests, trs contains Nones, so write_module might skip writing if it checks for valid results.
        # core.py: if tr is not None: artifacts.append(...)
        # So if we return None, nothing is written.
        
        # Let's verify that it *tried* to run tests
        mock_run.assert_called()

def test_create_tests_no_cleanup(tmp_path):
    # Test with clean_up=False
    testdata_dir = tmp_path / "src"
    testdata_dir.mkdir()
    (testdata_dir / "sample.py").write_text("def foo(): pass")
    cassette_dir = tmp_path / "cassettes"
    test_out_dir = tmp_path / "tests"
    
    cassette_dir.mkdir()
    test_out_dir.mkdir()
    (test_out_dir / "existing.txt").write_text("keep me")
    
    from unittest.mock import patch
    with patch("ghtest.core._run_tests") as mock_run, \
         patch("coverage.Coverage"):
        mock_run.return_value = []
        create_tests(
            cassette_dir=str(cassette_dir),
            test_dir=str(test_out_dir),
            src_dir=str(testdata_dir),
            clean_up=False,
            unsafe=True
        )
        
    assert (test_out_dir / "existing.txt").exists()
