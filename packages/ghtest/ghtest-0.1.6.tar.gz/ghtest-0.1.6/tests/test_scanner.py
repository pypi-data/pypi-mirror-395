import os
from pathlib import Path
from ghtest.scanner import scan_python_functions

def test_scan_python_functions(tmp_path):
    # Create a temporary python file with sample functions
    test_file = tmp_path / "sample.py"
    test_file.write_text("""
def get_commits(name: str, dry_run: bool = False):
    pass

def get_repo_data(name: str):
    pass

def create_repo(name: str):
    pass
""")
    
    functions = scan_python_functions(str(tmp_path))
    
    # Check that we found some functions
    assert len(functions) > 0
    
    # Check for specific functions we know exist in sample.py
    qualnames = [f.qualname for f in functions]
    assert "get_commits" in qualnames
    assert "get_repo_data" in qualnames
    assert "create_repo" in qualnames
    
    # Check details of a specific function
    get_commits = next(f for f in functions if f.qualname == "get_commits")
    assert get_commits.module == "sample"
    param_names = [p.name for p in get_commits.parameters]
    assert "name" in param_names
    assert "dry_run" in param_names
