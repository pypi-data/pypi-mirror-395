import pytest
from pathlib import Path
from unittest.mock import MagicMock
from ghtest.tests_writer import (
    _DataStore,
    _format_assignment,
    _format_literal,
    _is_literal_value,
    TestArtifact,
    write_test_modules,
)
from ghtest.tests_creator import SuggestedFunctionTests
from ghtest.test_utils import RunTestWithCassette, CaseTestResult

def test_data_store(tmp_path):
    ds = _DataStore(tmp_path / "data", inline_limit=10)
    
    # Small literal should be inlined
    # _should_inline returns True if len(literal) <= inline_limit
    assert ds._should_inline("short")
    
    val_short = "short"
    lit_short = ds.literal(val_short, label="short")
    assert lit_short == "'short'"
    
    val_long = "long" * 10
    lit_long = ds.literal(val_long, label="long")
    assert "load_data" in lit_long
    # The DataStore creates files in base_dir.
    # We need to check if any file was created or if the specific file exists.
    # The filename is hash based or label based?
    # _write_data_file uses label + hash if needed?
    # Let's check if *any* file exists in data dir.
    assert any((tmp_path / "data").iterdir())

def test_format_assignment():
    # _format_assignment adds 4 spaces indentation
    assert _format_assignment("x", "10").strip() == "x = 10"
    assert _format_assignment("y", "'s'").strip() == "y = 's'"

def test_format_literal():
    assert _format_literal(10) == "10"
    assert _format_literal("s") == "'s'"
    assert _format_literal(None) == "None"
    assert _format_literal(True) == "True"

def test_is_literal_value():
    assert _is_literal_value(1)
    assert _is_literal_value("s")
    assert _is_literal_value([1, 2])
    assert _is_literal_value({"a": 1})
    
    class Foo: pass
    assert not _is_literal_value(Foo())

def test_write_test_modules(tmp_path):
    # Create dummy artifacts
    suggestion = SuggestedFunctionTests(
        module="mod",
        filepath="f.py",
        qualname="func",
        docstring=None,
        param_sets=[{"a": 1}],
        scenario=None
    )
    
    run_result = RunTestWithCassette(
        cassette_path="c.yaml",
        cases=[CaseTestResult(target="func", params={"a": 1}, return_value=2, exception=None, printed="", file_reads=[], file_writes=[], return_summary={}, volatile_return_fields=[])]
    )
    
    artifact = TestArtifact(suggestion=suggestion, run=run_result)
    
    out_dir = tmp_path / "tests"
    write_test_modules([artifact], str(out_dir))
    
    assert out_dir.exists()
    test_files = list(out_dir.glob("test_*.py"))
    assert len(test_files) > 0
    
    content = test_files[0].read_text()
    assert "def test_func" in content
    # The writer uses assert_return_summary for validation
    assert "assert_return_summary(result.return_summary" in content
