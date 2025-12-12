import pytest
from unittest.mock import MagicMock, patch
from ghtest.coverage_analysis import analyze_file_coverage, BranchAnalyzer
import ast

def test_branch_analyzer():
    # Test BranchAnalyzer logic
    # Case 1: If statement, body covered, condition covered
    code = "if True:\n    pass"
    tree = ast.parse(code)
    
    # Line 1 is 'if', Line 2 is 'pass'
    covered = {1, 2}
    missing = set()
    
    analyzer = BranchAnalyzer(covered, missing)
    analyzer.visit(tree)
    
    # Should have no missed branches because we don't know if else was taken?
    # Wait, logic says:
    # if not body_covered: needed=True
    # if orelse and not orelse_covered: needed=False
    # Implicit else is hard.
    assert len(analyzer.missed_branches) == 0

    # Case 2: If statement, body NOT covered
    covered = {1}
    missing = {2}
    analyzer = BranchAnalyzer(covered, missing)
    analyzer.visit(tree)
    
    assert len(analyzer.missed_branches) == 1
    assert analyzer.missed_branches[0]["line"] == 1
    assert analyzer.missed_branches[0]["needed"] is True

    # Case 3: If/Else, else NOT covered
    code = "if True:\n    pass\nelse:\n    pass"
    tree = ast.parse(code)
    # 1: if, 2: pass (body), 4: pass (else)
    covered = {1, 2}
    missing = {4}
    
    analyzer = BranchAnalyzer(covered, missing)
    analyzer.visit(tree)
    
    assert len(analyzer.missed_branches) == 1
    assert analyzer.missed_branches[0]["line"] == 1
    assert analyzer.missed_branches[0]["needed"] is False

def test_analyze_file_coverage_no_file():
    cov = analyze_file_coverage("nonexistent.py", MagicMock())
    assert cov == []
