import ast
import pytest
from unittest.mock import MagicMock, patch
from ghtest.tests_creator import (
    _FunctionFinder,
    _DestructiveCallVisitor,
    _is_destructive_call,
    _looks_destructive_name,
    make_test_function,
    SuggestedFunctionTests,
    ScenarioStep,
    CrudScenario,
)

def test_function_finder():
    code = """
class MyClass:
    def my_method(self):
        pass

def my_function():
    pass

async def my_async_function():
    pass
"""
    finder = _FunctionFinder("my_function")
    finder.visit(ast.parse(code))
    assert finder.found is not None
    assert isinstance(finder.found, ast.FunctionDef)
    assert finder.found.name == "my_function"

    finder = _FunctionFinder("MyClass.my_method")
    finder.visit(ast.parse(code))
    assert finder.found is not None
    assert isinstance(finder.found, ast.FunctionDef)
    assert finder.found.name == "my_method"
    
    finder = _FunctionFinder("my_async_function")
    finder.visit(ast.parse(code))
    assert finder.found is not None
    assert isinstance(finder.found, ast.AsyncFunctionDef)

def test_destructive_call_visitor():
    code = """
def safe():
    print("hello")

def unsafe():
    os.remove("file")
    
def unsafe_rmtree():
    shutil.rmtree("dir")
"""
    visitor = _DestructiveCallVisitor()
    visitor.visit(ast.parse(code).body[0]) # safe
    assert not visitor.found
    
    visitor = _DestructiveCallVisitor()
    visitor.visit(ast.parse(code).body[1]) # unsafe
    assert visitor.found

    visitor = _DestructiveCallVisitor()
    visitor.visit(ast.parse(code).body[2]) # unsafe_rmtree
    assert visitor.found

def test_is_destructive_call():
    # Mock AST nodes for calls
    # os.remove
    node = ast.Call(
        func=ast.Attribute(
            value=ast.Name(id="os", ctx=ast.Load()),
            attr="remove",
            ctx=ast.Load()
        ),
        args=[], keywords=[]
    )
    assert _is_destructive_call(node)

    # remove()
    node = ast.Call(
        func=ast.Name(id="remove", ctx=ast.Load()),
        args=[], keywords=[]
    )
    assert _is_destructive_call(node)
    
    # print()
    node = ast.Call(
        func=ast.Name(id="print", ctx=ast.Load()),
        args=[], keywords=[]
    )
    assert not _is_destructive_call(node)

def test_looks_destructive_name():
    assert _looks_destructive_name("delete_repo")
    assert _looks_destructive_name("remove_file")
    assert _looks_destructive_name("rm_dir")
    assert not _looks_destructive_name("get_repo")
    assert not _looks_destructive_name("create_repo")

def test_make_test_function(tmp_path):
    # Setup suggestion
    suggestion = SuggestedFunctionTests(
        module="mod",
        filepath="f.py",
        qualname="func",
        docstring=None,
        param_sets=[{"a": 1}],
        scenario=None
    )
    
    cassette_dir = str(tmp_path / "cassettes")
    
    with patch("ghtest.tests_creator.import_function") as mock_import:
        mock_func = MagicMock()
        mock_import.return_value = mock_func
        
        result_obj = make_test_function(suggestion, cassette_dir)
        
        # Run the generated test function
        # make_test_function returns a GeneratedTest object, which has a test_callable field
        
        result = result_obj.test_callable()
        
        # Verify it called the function
        mock_func.assert_called_with(a=1)
        assert result.cassette_path.startswith(cassette_dir)

def test_run_crud_scenario(tmp_path):
    from ghtest.tests_creator import _run_crud_scenario, CrudScenario, ScenarioStep, CaseTestResult
    
        # Mock import_function and call_with_capture
    with patch("ghtest.tests_creator.import_function") as mock_import, \
         patch("ghtest.tests_creator.call_with_capture") as mock_call:
        
        mock_func = MagicMock()
        mock_import.return_value = mock_func
        
        def side_effect(func, target, params, volatile_return_fields):
            return CaseTestResult(target=target, params=params, return_value="ok", exception=None, printed="", file_reads=[], file_writes=[], return_summary={}, volatile_return_fields=[])
            
        mock_call.side_effect = side_effect
        
        scenario = CrudScenario(
            resource="res",
            identifier="id",
            steps=[
                ScenarioStep(module="mod", filepath="f.py", qualname="create", params={}),
                ScenarioStep(module="mod", filepath="f.py", qualname="delete", params={}, cleanup=True)
            ]
        )
        
        # Run with assume safe to avoid prompt
        with patch.dict("os.environ", {"GHTEST_ASSUME_SAFE": "1"}):
            results = _run_crud_scenario(scenario, interactive=False)
            
        assert len(results) == 2
        # Check cleanup executed
        assert results[1].target == "delete"
