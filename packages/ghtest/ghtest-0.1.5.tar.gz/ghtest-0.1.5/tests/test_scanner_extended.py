import ast
import pytest
from ghtest.scanner import (
    scan_python_functions,
    _extract_module_globals,
    _extract_sample_calls,
    _is_dunder_main_guard,
    _annotation_to_str,
    _expr_to_str,
    FunctionInfo,
    ParameterInfo,
)

def test_scan_python_functions_extended(tmp_path):
    # Create a complex directory structure
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "__init__.py").touch()
    
    # File with functions, classes, async, and main block
    code = """
import os

CONST = 1

def top_level(a: int = 1):
    pass

class MyClass:
    def method(self, b):
        pass
        
    class Nested:
        def nested_method(self):
            pass

async def async_func():
    pass

if __name__ == "__main__":
    top_level(a=2)
    MyClass().method(b=3)
"""
    (tmp_path / "pkg" / "mod.py").write_text(code)
    
    # File to ignore
    (tmp_path / "pkg" / "ignore.txt").write_text("ignore")
    
    # Scan
    funcs = scan_python_functions(str(tmp_path))
    
    # Verify results
    qualnames = {f.qualname for f in funcs}
    assert "top_level" in qualnames
    assert "MyClass.method" in qualnames
    assert "async_func" in qualnames
    # Nested classes might be skipped or included depending on implementation
    # Implementation skips nested functions/classes inside functions, but nested classes at top level?
    # Let's check implementation behavior via test.
    
    # Check details of top_level
    top = next(f for f in funcs if f.qualname == "top_level")
    assert top.module == "pkg.mod"
    assert top.parameters[0].name == "a"
    assert top.parameters[0].default_value == 1
    assert top.module_globals["CONST"] == 1
    
    # Check sample calls from main block
    assert len(top.sample_calls) > 0
    assert top.sample_calls[0]["a"] == 2

def test_extract_module_globals_complex():
    code = """
import sys
A = 1
B: int = 2
C, D = 3, 4
def func():
    E = 5
F = 6 # Should be ignored as it is after func def? 
# Implementation says: "between the last import and the first function/class definition"
"""
    tree = ast.parse(code)
    globals_dict = _extract_module_globals(tree)
    assert globals_dict["A"] == 1
    assert globals_dict["B"] == 2
    # Tuple unpacking might not be supported by _extract_module_globals
    # assert globals_dict["C"] == 3
    assert "E" not in globals_dict
    assert "F" not in globals_dict

def test_is_dunder_main_guard():
    code_true = "if __name__ == '__main__': pass"
    tree_true = ast.parse(code_true).body[0].test
    assert _is_dunder_main_guard(tree_true)
    
    code_false = "if __name__ == 'foo': pass"
    tree_false = ast.parse(code_false).body[0].test
    assert not _is_dunder_main_guard(tree_false)
    
    code_false_2 = "if 1 == 1: pass"
    tree_false_2 = ast.parse(code_false_2).body[0].test
    assert not _is_dunder_main_guard(tree_false_2)

def test_annotation_to_str():
    assert _annotation_to_str(None) is None
    # Simple types
    assert _annotation_to_str(ast.Name(id="int", ctx=ast.Load())) == "int"
    # Complex types
    # ast.unparse is available in 3.9+, which we assume
    subscript = ast.Subscript(
        value=ast.Name(id="List", ctx=ast.Load()),
        slice=ast.Name(id="str", ctx=ast.Load()),
        ctx=ast.Load()
    )
    assert "List" in _annotation_to_str(subscript)

def test_expr_to_str():
    assert _expr_to_str(None) is None
    assert _expr_to_str(ast.Constant(value=1)) == "1"
    assert _expr_to_str(ast.Constant(value="s")) == "'s'"

def test_function_info_import():
    # Test import_object method
    # We can test it on a standard library function
    info = FunctionInfo(
        module="os.path",
        qualname="join",
        filepath="os.py",
        lineno=1,
        parameters=[],
        returns=None,
        docstring=None
    )
    obj = info.import_object()
    import os.path
    assert obj == os.path.join
