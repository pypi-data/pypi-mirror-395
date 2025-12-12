#!/usr/bin/env python
# coding: utf-8

# In[2]:


import ast
import glob
import os
import sys
import textwrap
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Sequence

import vcr

try:  # pragma: no cover - fallback for direct script usage
    from .test_utils import (
        CaseTestResult,
        RunTestWithCassette,
        call_with_capture,
        # execute_function,
        import_function,
    )
except ImportError:  # pragma: no cover
    current_dir = os.path.dirname(__file__)
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    from test_utils import (  # type: ignore
        CaseTestResult,
        RunTestWithCassette,
        call_with_capture,
        import_function,
    )


# In[5]:


@dataclass
class ScenarioStep:
    module: str
    filepath: str
    qualname: str
    params: Dict[str, Any]
    expect: Optional[str] = None
    cleanup: bool = False
    description: Optional[str] = None


@dataclass
class CrudScenario:
    resource: str
    identifier: str
    steps: List[ScenarioStep]
    note: Optional[str] = None


@dataclass
class SuggestedFunctionTests:
    module: str
    filepath: str
    qualname: str
    docstring: Optional[str]
    param_sets: List[Dict[str, Any]]  # each dict is kwargs for a call
    scenario: Optional[CrudScenario] = None


@dataclass
class GeneratedTest:
    test_callable: Callable[[], RunTestWithCassette]
    cassette_path: str
    source: str  # Python source code of an equivalent test function


_DESTRUCTIVE_NAME_HINTS = (
    "remove",
    "delete",
    "destroy",
    "drop",
    "del_",
    "rm_",
    "rmdir",
)

_DESTRUCTIVE_ATTR_HINTS = {
    ("os", "remove"),
    ("os", "rmdir"),
    ("os", "unlink"),
    ("shutil", "rmtree"),
}

_DESTRUCTIVE_SIMPLE_CALLS = {
    "remove",
    "unlink",
    "rmdir",
    "rmtree",
    "delete",
    "del",
    "rmtree",
}


def _looks_destructive_name(qualname: str) -> bool:
    lname = qualname.lower()
    return any(token in lname for token in _DESTRUCTIVE_NAME_HINTS)


def _load_function_ast(filepath: str) -> Optional[ast.Module]:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
    except OSError:
        return None

    try:
        return ast.parse(source, filename=filepath)
    except SyntaxError:
        return None


class _FunctionFinder(ast.NodeVisitor):
    def __init__(self, target: str) -> None:
        self.target = target
        self.stack: List[str] = []
        self.found: Optional[ast.AST] = None

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        if self.found:
            return
        self.stack.append(node.name)
        self.generic_visit(node)
        self.stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if self.found:
            return
        current = ".".join(self.stack + [node.name])
        if current == self.target:
            self.found = node
            return
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.visit_FunctionDef(node)  # type: ignore[arg-type]


class _DestructiveCallVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.found = False

    def visit_Call(self, node: ast.Call) -> None:
        if self.found:
            return
        if _is_destructive_call(node):
            self.found = True
            return
        self.generic_visit(node)


def _is_destructive_call(node: ast.Call) -> bool:
    func = node.func
    if isinstance(func, ast.Attribute):
        attr = func.attr.lower()
        base = func.value
        if isinstance(base, ast.Name):
            base_name = base.id.lower()
            if (base_name, attr) in _DESTRUCTIVE_ATTR_HINTS:
                return True
        if attr in _DESTRUCTIVE_SIMPLE_CALLS:
            return True
    elif isinstance(func, ast.Name):
        if func.id.lower() in _DESTRUCTIVE_SIMPLE_CALLS:
            return True
    return False


def _function_body_has_destructive_calls(filepath: str, qualname: str) -> bool:
    tree = _load_function_ast(filepath)
    if tree is None:
        return False
    finder = _FunctionFinder(qualname)
    finder.visit(tree)
    if finder.found is None:
        return False
    visitor = _DestructiveCallVisitor()
    visitor.visit(finder.found)  # type: ignore[arg-type]
    return visitor.found


def _should_confirm_execution(suggestion: SuggestedFunctionTests) -> bool:
    if _looks_destructive_name(suggestion.qualname):
        return True
    return _function_body_has_destructive_calls(
        suggestion.filepath, suggestion.qualname
    )


def _prompt_user_confirmation(suggestion: SuggestedFunctionTests) -> None:
    prompt = (
        f"Function {suggestion.qualname} in {suggestion.filepath} may perform destructive actions.\n"
        "Proceed with executing auto-generated tests? [y/N]: "
    )
    response = input(prompt)
    if response.strip().lower() not in {"y", "yes"}:
        raise RuntimeError("Aborted executing potentially destructive test target.")


def _format_step_summary(step: ScenarioStep) -> str:
    param_display = ", ".join(f"{k}={v!r}" for k, v in step.params.items())
    return f"{step.qualname}({param_display})"


def _confirm_crud_scenario(scenario: CrudScenario, interactive=True) -> None:
    if not interactive:
        return
    lines = [
        f"Planned CRUD scenario for resource '{scenario.resource}' as '{scenario.identifier}':",
    ]
    for step in scenario.steps:
        lines.append(f"  - {_format_step_summary(step)}")
    if scenario.note:
        lines.append(f"Note: {scenario.note}")
    lines.append("Proceed with the full sequence? [y/N]: ")
    response = input("\n".join(lines))
    if response.strip().lower() not in {"y", "yes"}:
        print("Aborted CRUD scenario execution.")
        return
    return True


def _execute_scenario_step(
    step: ScenarioStep,
    *,
    record: bool = True,
    cassette_dir: Optional[str] = None,
    cassette_name: Optional[str] = None,
    record_mode: str = "once",
) -> CaseTestResult:
    func = import_function(step.module, step.filepath, step.qualname)
    params = dict(step.params)
    recorder = None
    if record and cassette_dir and cassette_name:
        recorder = vcr.VCR(
            serializer="yaml",
            cassette_library_dir=cassette_dir,
            record_mode=record_mode,
            match_on=["uri", "method", "body"],
        )
    if recorder and record:
        with recorder.use_cassette(cassette_name):
            result = call_with_capture(
                func,
                target=step.qualname,
                params=params,
                volatile_return_fields=None,
            )
        if cassette_dir and cassette_name:
            cassette_file = os.path.join(cassette_dir, cassette_name)
            result.cassette_path = cassette_file
            if not os.path.exists(cassette_file):
                try:
                    with open(cassette_file, "w", encoding="utf-8") as fh:
                        fh.write("interactions: []\nversion: 1\n")
                except OSError:
                    pass
    else:
        result = call_with_capture(
            func,
            target=step.qualname,
            params=params,
            volatile_return_fields=None,
        )
    ret = result.return_value
    exc = result.exception
    if step.expect == "truthy" and not ret and exc is None:
        msg = f"Expected truthy result for {step.qualname}, got {ret!r}"
        print(f"SCENARIO FAILURE: {msg}")
        result.exception = AssertionError(msg)
    if step.expect == "falsy" and ret and exc is None:
        msg = f"Expected falsy result for {step.qualname}, got {ret!r}"
        print(f"SCENARIO FAILURE: {msg}")
        result.exception = AssertionError(msg)
    if exc:
        print(f"SCENARIO EXCEPTION in {step.qualname}: {exc}")
    return result


def _run_crud_scenario(
    scenario: CrudScenario,
    interactive=True,
    *,
    cassette_dir: Optional[str] = None,
    cassette_base: Optional[str] = None,
    record_mode: str = "once",
) -> List[CaseTestResult]:
    assume_safe = os.environ.get("GHTEST_ASSUME_SAFE") == "1"
    if assume_safe:
        confirmed = True
    else:
        confirmed = _confirm_crud_scenario(scenario, interactive=interactive)
    results: List[CaseTestResult] = []
    if not assume_safe and not confirmed:
        return results
    cleanup_step = next((s for s in scenario.steps if s.cleanup), None)
    cleanup_executed = False
    pending_error: Optional[BaseException] = None

    try:
        cassette_base_value = cassette_base
        for idx, step in enumerate(scenario.steps):
            cassette_name = None
            if cassette_dir and cassette_base_value is not None:
                suffix = "cleanup" if step.cleanup else f"step_{idx}"
                cassette_name = f"{cassette_base_value}.{suffix}.yaml"
            result = _execute_scenario_step(
                step,
                cassette_dir=cassette_dir,
                cassette_name=cassette_name,
                record_mode=record_mode,
            )
            results.append(result)
            if step.cleanup and result.exception is None:
                cleanup_executed = True
            if result.exception is not None:
                # Stop execution on failure, but pad results for remaining steps
                remaining_steps = scenario.steps[idx + 1 :]
                for skipped_step in remaining_steps:
                    skipped_result = CaseTestResult(
                        target=skipped_step.qualname,
                        params=skipped_step.params,
                        return_value=None,
                        printed="",
                        exception=RuntimeError("Skipped due to previous step failure"),
                        return_summary={},
                        volatile_return_fields=[],
                    )
                    results.append(skipped_result)
                break
    except BaseException as exc:  # noqa: BLE001
        pending_error = exc  # noqa: F841
        # If we crashed outside the loop or during setup, we might need more padding,
        # but the break above handles the common case of step failure.
    finally:
        if cleanup_step and not cleanup_executed:
            try:
                cassette_name = None
                if cassette_dir and cassette_base_value is not None:
                    cassette_name = f"{cassette_base_value}.cleanup.yaml"
                _execute_scenario_step(
                    cleanup_step,
                    record=False,
                    cassette_dir=cassette_dir,
                    cassette_name=cassette_name,
                    record_mode=record_mode,
                )
            except Exception:
                pass
    # if pending_error:
    #    raise pending_error
    return results


def make_test_function(
    suggestion: SuggestedFunctionTests,
    cassette_dir: str,
    record_mode: str = "once",
    volatile_response_fields: Optional[Sequence[str]] = None,
) -> GeneratedTest:
    os.makedirs(cassette_dir, exist_ok=True)

    func_name = f"test_{suggestion.qualname.replace('.', '_')}"
    requested_base = f"{suggestion.module}.{suggestion.qualname}".replace(":", "_")
    cassette_base = _ensure_unique_cassette_base(cassette_dir, requested_base)
    if cassette_base != requested_base:
        print(
            f"Existing cassette detected for {requested_base}; "
            f"recording new interactions under {cassette_base}."
        )
    cassette_path = os.path.join(cassette_dir, f"{cassette_base}.yaml")
    scenario_cassette_base: Optional[str] = None
    if suggestion.scenario:
        requested_scenario_base = f"{cassette_base}.scenario"
        scenario_cassette_base = _ensure_unique_cassette_base(
            cassette_dir, requested_scenario_base
        )

    if volatile_response_fields is None:
        volatile_fields: Optional[List[str]] = None
    else:
        volatile_fields = list(volatile_response_fields)

    def test(interactive=True) -> RunTestWithCassette:
        if _should_confirm_execution(suggestion):
            if not os.environ.get("GHTEST_ASSUME_SAFE") == "1":
                if interactive:
                    _prompt_user_confirmation(suggestion)
                else:
                    raise RuntimeError(
                        "aborted executing potentially destructive test target."
                    )
        func = import_function(
            suggestion.module, suggestion.filepath, suggestion.qualname
        )
        results: List[CaseTestResult] = []

        for idx, params in enumerate(suggestion.param_sets):
            case_cassette = f"{cassette_base}.case_{idx}.yaml"
            recorder = vcr.VCR(
                serializer="yaml",
                cassette_library_dir=cassette_dir,
                record_mode=record_mode,
                match_on=["uri", "method", "body"],
            )
            try:
                with recorder.use_cassette(case_cassette):
                    result = call_with_capture(
                        func,
                        target=suggestion.qualname,
                        params=dict(params),
                        volatile_return_fields=volatile_fields,
                    )
            except Exception as exc:  # noqa: BLE001
                if _is_vcr_overwrite_error(exc):
                    _reraise_with_vcr_guidance(
                        exc, os.path.join(cassette_dir, case_cassette)
                    )
                # Create a failed result
                result = CaseTestResult(
                    target=suggestion.qualname,
                    params=dict(params),
                    exception=exc,
                    return_value=None,
                    printed="",
                    file_reads=[],
                    file_writes=[],
                    return_summary={},
                    volatile_return_fields=volatile_fields,
                )

            result.cassette_path = os.path.join(cassette_dir, case_cassette)
            results.append(result)

        if suggestion.scenario:
            scenario_results = _run_crud_scenario(
                suggestion.scenario,
                interactive=interactive,
                cassette_dir=cassette_dir,
                cassette_base=scenario_cassette_base,
                record_mode=record_mode,
            )
            results.extend(scenario_results)

        return RunTestWithCassette(
            cassette_path=cassette_path,
            cases=results,
        )

    test.__name__ = func_name
    if suggestion.docstring:
        test.__doc__ = f"Auto-generated test for {suggestion.qualname} with VCR.\n\n{suggestion.docstring}"

    param_sets_repr = repr(suggestion.param_sets)
    volatile_repr = repr(volatile_fields)

    source = textwrap.dedent(
        f"""import os
from typing import List

import vcr

from ghtest.test_utils import (
    CaseTestResult,
    RunTestWithCassette,
    call_with_capture,
    import_function,
)


def {func_name}() -> RunTestWithCassette:
    module = {suggestion.module!r}
    filepath = {suggestion.filepath!r}
    qualname = {suggestion.qualname!r}
    cassette_dir = {cassette_dir!r}
    cassette_base = {cassette_base!r}
    cassette_path = os.path.join(cassette_dir, f"{{cassette_base}}.yaml")
    param_sets = {param_sets_repr}
    volatile_fields = {volatile_repr}

    os.makedirs(cassette_dir, exist_ok=True)

    func = import_function(module, filepath, qualname)
    results: List[CaseTestResult] = []

    for idx, params in enumerate(param_sets):
        recorder = vcr.VCR(
            serializer="yaml",
            cassette_library_dir=cassette_dir,
            record_mode={record_mode!r},
            match_on=["uri", "method", "body"],
        )
        cassette_name = f"{cassette_base}.case_{{idx}}.yaml"
        with recorder.use_cassette(cassette_name):
            result = call_with_capture(func, target=qualname, params=params, volatile_return_fields=volatile_fields)
        result.cassette_path = os.path.join(cassette_dir, cassette_name)
        results.append(result)

    return RunTestWithCassette(cassette_path=os.path.join(cassette_dir, f"{cassette_base}.yaml"), cases=results)
        """
    )

    return GeneratedTest(
        test_callable=test,
        cassette_path=cassette_path,
        source=source,
    )


def _ensure_unique_cassette_base(cassette_dir: str, base: str) -> str:
    candidate = base
    suffix = 1
    while _cassette_artifacts_exist(cassette_dir, candidate):
        candidate = f"{base}__{suffix}"
        suffix += 1
    return candidate


def _cassette_artifacts_exist(cassette_dir: str, base: str) -> bool:
    cassette_file = os.path.join(cassette_dir, f"{base}.yaml")
    if os.path.exists(cassette_file):
        return True
    pattern = os.path.join(cassette_dir, f"{base}.case_*.yaml")
    return any(glob.glob(pattern))


def _reraise_with_vcr_guidance(exc: Exception, cassette_file: str) -> None:
    if _is_vcr_overwrite_error(exc):
        raise RuntimeError(
            (
                "VCR refused to overwrite existing cassette "
                f"{cassette_file}. Delete the cassette, set remove_cassettes=True, "
                "or rerun after cleaning up the conflicting files."
            )
        ) from exc


def _is_vcr_overwrite_error(exc: BaseException) -> bool:
    errors_mod = getattr(vcr, "errors", None)
    if errors_mod is None:
        return False
    error_cls = getattr(errors_mod, "CannotOverwriteExistingCassetteException", None)
    if error_cls is None:
        return False
    try:
        return isinstance(exc, error_cls)
    except Exception:
        return False


# In[ ]:


def _run_tests(gts, interactive=True, vb=0):
    trs = []
    for gt in gts:
        try:
            tr = gt.test_callable(interactive=interactive)
            trs.append(tr)
        except Exception as e:
            if vb:
                print(str(e))
            # if tests fail, we append None so the number of items remains in sync with eg result or suggest lists
            trs.append(None)
    return trs
