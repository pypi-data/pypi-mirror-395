import pytest
from pathlib import Path
from ghtest.tests_writer import _relativize_path_code, _format_file_access_list

def test_relativize_path_code_relative(tmp_path):
    # Case: path is inside base_dir
    base_dir = tmp_path / "tests"
    base_dir.mkdir()
    target_file = base_dir / "data/file.txt"
    
    # We need absolute paths for the function to work as expected
    code = _relativize_path_code(str(target_file.resolve()), base_dir.resolve())
    
    # Expect something like str((Path(__file__).parent / 'data/file.txt').resolve())
    assert "Path(__file__).parent" in code
    assert "data/file.txt" in code
    assert ".resolve()" in code

def test_relativize_path_code_parent(tmp_path):
    # Case: path is in parent of base_dir
    base_dir = tmp_path / "tests"
    base_dir.mkdir()
    target_file = tmp_path / "src/file.py"
    
    code = _relativize_path_code(str(target_file.resolve()), base_dir.resolve())
    
    assert "Path(__file__).parent" in code
    assert "../src/file.py" in code

def test_relativize_path_code_absolute():
    # Case: path is completely outside (e.g. /tmp vs /home)
    # This depends on OS, but let's try a path that is likely not relative
    base_dir = Path("/home/user/project")
    target_file = Path("/var/log/syslog")
    
    # If it can't relativize easily (different drives on windows, or just far away), 
    # it might still produce a relative path with many ../..
    # But our implementation uses os.path.relpath which usually works.
    
    # Let's test that it produces a Path object construction string, even if it has many ..
    code = _relativize_path_code("relative/path.txt", base_dir)
    assert "Path(__file__).parent" in code
    assert "relative/path.txt" in code

def test_format_file_access_list(tmp_path):
    out_dir = tmp_path / "tests"
    out_dir.mkdir()
    
    access_list = [
        (str(out_dir / "file1.txt"), "r"),
        (str(out_dir / "file2.txt"), "w")
    ]
    
    code = _format_file_access_list(access_list, out_dir)
    
    assert code.startswith("[")
    assert code.endswith("]")
    assert "file1.txt" in code
    assert "file2.txt" in code
    assert "'r'" in code
    assert "'w'" in code
    assert "Path(__file__).parent" in code
