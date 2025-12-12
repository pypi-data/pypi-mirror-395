import pytest
from pathlib import Path
from ghtest.scanner import scan_python_functions
from ghtest.param_suggestor import suggest_params

@pytest.fixture
def test_functions(tmp_path):
    test_file = tmp_path / "sample.py"
    test_file.write_text("""
def get_commits(name: str, dry_run: bool = False):
    pass

def get_repo_data(name: str):
    pass

def create_repo(name: str):
    pass

def delete_repo(name: str):
    pass
""")
    return scan_python_functions(str(tmp_path))

def test_suggest_params_basic(test_functions):
    # Find get_commits function
    func = next(f for f in test_functions if f.qualname == "get_commits")
    
    suggestion = suggest_params(func, literal_only=False)
    
    assert suggestion.qualname == "get_commits"
    assert len(suggestion.param_sets) > 0
    
    # Check that we have suggestions for 'name' parameter
    first_set = suggestion.param_sets[0]
    assert "name" in first_set
    assert "name" in first_set
    # The suggestor might suggest various types depending on heuristics
    assert first_set["name"] is not None

def test_suggest_params_scenario(test_functions):
    # Find create_repo function which should trigger a scenario
    func = next(f for f in test_functions if f.qualname == "create_repo")
    
    suggestion = suggest_params(func, literal_only=False)
    
    assert suggestion.qualname == "create_repo"
    assert suggestion.scenario is not None
    assert len(suggestion.scenario.steps) > 0
    
    # Verify scenario steps
    step_names = [step.qualname for step in suggestion.scenario.steps]
    assert "get_repo_data" in step_names
    assert "create_repo" in step_names
    assert "delete_repo" in step_names
