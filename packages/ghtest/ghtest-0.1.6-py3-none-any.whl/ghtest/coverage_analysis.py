import ast
from typing import Any, Dict, List, Set

try:
    import coverage
except ImportError:
    coverage = None


class BranchAnalyzer(ast.NodeVisitor):
    def __init__(self, covered_lines: Set[int], missing_lines: Set[int]) -> None:
        self.covered_lines = covered_lines
        self.missing_lines = missing_lines
        self.missed_branches: List[Dict[str, Any]] = []

    def visit_If(self, node: ast.If) -> None:
        self.check_branch(node)
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:
        self.check_branch(node)
        self.generic_visit(node)

    def check_branch(self, node: ast.AST) -> None:
        # The line of the 'if' or 'while' statement
        start_line = node.lineno

        # If the condition itself wasn't executed, we can't do anything yet (unreachable)
        if start_line not in self.covered_lines:
            return

        # Check body coverage
        body_covered = self.is_block_covered(node.body)

        # Check orelse coverage
        orelse_covered = False
        if node.orelse:
            orelse_covered = self.is_block_covered(node.orelse)

        # We can't easily detect implicit else without CFG, but if body wasn't covered,
        # we definitely took the else path (or crashed).
        # If body WAS covered, we might have missed the else path.

        if not body_covered:
            self.missed_branches.append(
                {"line": start_line, "condition": node.test, "needed": True}
            )

        if node.orelse and not orelse_covered:
            self.missed_branches.append(
                {"line": start_line, "condition": node.test, "needed": False}
            )

    def is_block_covered(self, nodes: List[ast.AST]) -> bool:
        """Check if any line in the block was executed."""
        for node in nodes:
            if hasattr(node, "lineno"):
                if node.lineno in self.covered_lines:
                    return True
        return False


def analyze_file_coverage(filepath: str, cov_data: Any) -> List[Dict[str, Any]]:
    """
    Analyze a single file to find missed branches using coverage data.
    Returns a list of missed branch hints.
    """
    if coverage is None:
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
    except OSError:
        return []

    try:
        tree = ast.parse(source, filename=filepath)
    except SyntaxError:
        return []

    try:
        # analysis() returns (filename, statements, excluded, missing, missing_formatted)
        analysis = cov_data.analysis(filepath)
    except coverage.misc.CoverageException:
        return []

    executable_lines = set(analysis[1])
    missing_lines = set(analysis[2])  # Index 2 is missing lines
    covered_lines = executable_lines - missing_lines

    analyzer = BranchAnalyzer(covered_lines, missing_lines)
    analyzer.visit(tree)

    return analyzer.missed_branches
