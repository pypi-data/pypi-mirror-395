import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from ghtest.tests_writer import _render_scenario_function, _write_scenario_module, ScenarioDefinition, _DataStore
from ghtest.tests_creator import CrudScenario, ScenarioStep, SuggestedFunctionTests

def test_render_scenario_function(tmp_path):
    # Setup
    step = MagicMock(spec=ScenarioStep)
    step.qualname = "func"
    step.module = "mod"
    step.filepath = "mod.py"
    step.params = {"a": 1}
    step.description = "Step 1"
    
    case = MagicMock()
    case.volatile_return_fields = []
    case.exception = None
    case.return_value = "result"
    case.printed = ""
    case.file_reads = []
    case.file_writes = []
    
    scenario = MagicMock(spec=CrudScenario)
    scenario.resource = "User"
    scenario.steps = [step]
    
    suggestion = MagicMock(spec=SuggestedFunctionTests)
    suggestion.scenario = scenario
    suggestion.qualname = "func"
    
    definition = MagicMock(spec=ScenarioDefinition)
    definition.suggestion = suggestion
    definition.cases = [(step, case)]
    
    data_store = MagicMock(spec=_DataStore)
    data_store.literal.side_effect = lambda v, label=None: repr(v)
    data_store.used = False
    
    # Render
    code = _render_scenario_function(
        definition,
        data_store,
        0,
        tmp_path,
        include_return_summary=False,
        exception_assertion="none"
    )
    
    assert "def test_User_scenario_case_0():" in code
    assert "func = import_function('mod', " in code
    assert "params = {'a': 1}" in code
    assert "result = call_with_capture" in code
    assert "assert result.exception is None" in code
    # It uses expected_return variable
    assert "expected_return = 'result'" in code
    assert "assert result.return_value == expected_return" in code

def test_write_scenario_module(tmp_path):
    # Setup similar to above
    step = MagicMock(spec=ScenarioStep)
    step.qualname = "func"
    step.module = "mod"
    step.filepath = "mod.py"
    step.params = {}
    
    case = MagicMock()
    case.volatile_return_fields = []
    case.exception = None
    case.return_value = "result"
    case.printed = ""
    case.file_reads = []
    case.file_writes = []
    
    scenario = MagicMock(spec=CrudScenario)
    scenario.resource = "User"
    
    suggestion = MagicMock(spec=SuggestedFunctionTests)
    suggestion.scenario = scenario
    suggestion.qualname = "func"
    
    definition = MagicMock(spec=ScenarioDefinition)
    definition.suggestion = suggestion
    definition.cases = [(step, case)]
    
    data_store = MagicMock(spec=_DataStore)
    data_store.literal.return_value = None # Use repr
    data_store.used = False
    
    # Write
    with patch("ghtest.tests_writer._render_scenario_function", return_value="    pass"):
        path = _write_scenario_module(
            tmp_path,
            0,
            definition,
            data_store,
            include_return_summary=False,
            exception_assertion="none"
        )
        
    assert path.exists()
    content = path.read_text()
    assert "import vcr" in content
    assert "test_scenario_User_0" in path.name
