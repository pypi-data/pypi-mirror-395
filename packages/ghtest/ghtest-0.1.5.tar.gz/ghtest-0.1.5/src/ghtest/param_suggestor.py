#!/usr/bin/env python
# coding: utf-8

import ast
import json
import os
import random
import string
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from .coverage_analysis import analyze_file_coverage

VERBOSITY_PARAM_TOKENS = ("verbose", "verbosity", "vb", "print", "show")
_PARAM_HISTORY_ENV = "GHTEST_PARAM_HISTORY"
_PARAM_DB_ENV = "GHTEST_PARAM_DB"
_PARAM_DB_DISABLE_ENV = "GHTEST_DISABLE_PARAM_DB_WRITE"
_PARAM_HISTORY_CACHE: Optional[Dict[str, List[Any]]] = None
_PARAM_DB_CACHE: Optional[Dict[str, Dict[str, Any]]] = None
_LITERAL_ASSIGNMENTS_CACHE: Dict[str, Dict[str, List[Any]]] = {}
VB = 0


@dataclass
class ScenarioStep:
    module: str
    filepath: str
    qualname: str
    params: Dict[str, Any]
    expect: Optional[str] = None  # "truthy" | "falsy" | None
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
    module: str  # import path, e.g. "pkg.sub.module"
    filepath: str
    qualname: str  # "func", "Class.method", ...
    docstring: Optional[str]
    param_sets: List[Dict[str, Any]]  # each dict is kwargs for a call
    scenario: Optional[CrudScenario] = None


def _extract_module_globals_from_file(filepath: str) -> Dict[str, Any]:
    """
    Parse the module source and extract top-level assignments that are likely
    to be constants (between the last import and the first def/class).
    """
    try:
        if VB:
            print(f"_extract_module_globals: reading {filepath}")  # noqa: E701
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
    except OSError:
        return {}

    try:
        tree = ast.parse(source, filename=filepath)
    except SyntaxError:
        return {}

    body = tree.body
    last_import_idx = -1
    first_def_idx = len(body)

    for i, node in enumerate(body):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            last_import_idx = i
        elif isinstance(
            node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
        ) and first_def_idx == len(body):
            first_def_idx = i

    start = last_import_idx + 1
    end = first_def_idx

    globals_dict: Dict[str, Any] = {}

    for node in body[start:end]:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            value_node = node.value
            if value_node is None:
                continue
            try:
                value = ast.literal_eval(value_node)
            except Exception:
                continue

            if isinstance(node, ast.Assign):
                targets = node.targets
            else:
                targets = [node.target]

            for target in targets:
                if isinstance(target, ast.Name):
                    globals_dict[target.id] = value

    return globals_dict


def _literal_eval_assign(node: ast.AST) -> Tuple[bool, Optional[Any]]:
    try:
        return True, ast.literal_eval(node)
    except Exception:
        return False, None


def _iter_assignment_names(target: ast.AST):
    if isinstance(target, ast.Name):
        yield target.id.lower()
    elif isinstance(target, (ast.Tuple, ast.List)):
        for elt in target.elts:
            yield from _iter_assignment_names(elt)


class _LiteralAssignmentCollector(ast.NodeVisitor):
    def __init__(self) -> None:
        self.values: Dict[str, List[Any]] = defaultdict(list)

    def _add(self, name: str, value: Any) -> None:
        bucket = self.values[name]
        if value not in bucket:
            bucket.append(value)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        # Skip function bodies to avoid picking up local assignments.
        return

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        return

    def visit_Assign(self, node: ast.Assign) -> None:
        success, value = _literal_eval_assign(node.value)
        if not success:
            return
        for target in node.targets:
            for name in _iter_assignment_names(target):
                self._add(name, value)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if node.value is None:
            return
        success, value = _literal_eval_assign(node.value)
        if not success:
            return
        target = node.target
        for name in _iter_assignment_names(target):
            self._add(name, value)


def _extract_literal_assignments_from_file(
    filepath: Optional[str],
) -> Dict[str, List[Any]]:
    if not filepath:
        return {}
    cached = _LITERAL_ASSIGNMENTS_CACHE.get(filepath)
    if cached is not None:
        return cached
    try:
        if VB:
            print(f"_extract_literal: reading {filepath}")  # noqa: E701
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
    except OSError:
        _LITERAL_ASSIGNMENTS_CACHE[filepath] = {}
        return {}
    try:
        tree = ast.parse(source, filename=filepath)
    except SyntaxError:
        _LITERAL_ASSIGNMENTS_CACHE[filepath] = {}
        return {}

    collector = _LiteralAssignmentCollector()
    collector.visit(tree)
    result = dict(collector.values)
    _LITERAL_ASSIGNMENTS_CACHE[filepath] = result
    return result


def _strip_numeric_suffix(name: str) -> str:
    stripped = name.rstrip("0123456789")
    if stripped.endswith("_"):
        stripped = stripped.rstrip("_")
    return stripped


_ENV_PLACEHOLDER_SUFFIXES = {"term", "key", "token", "secret", "env", "var"}


def _looks_like_env_placeholder(tokens: List[str], pname: str) -> bool:
    if not tokens:
        return False
    last = tokens[-1]
    if last not in _ENV_PLACEHOLDER_SUFFIXES:
        return False
    if last in pname:
        return False
    return True


def _choose_global_for_param(
    param: "ParameterInfo",  # noqa: F821
    module_globals: Dict[str, Any],
) -> Optional[Any]:
    """
    Try to find a suitable module-level constant for this parameter, based on
    name similarity and (optionally) annotation / value type.
    """
    if not module_globals:
        return None

    pname = param.name.lower()
    ann = (param.annotation or "").lower()

    best_score = 0
    best_value: Any = None

    for gname, gval in module_globals.items():
        gname_lower = gname.lower()
        stripped = _strip_numeric_suffix(gname_lower)
        tokens = [tok for tok in stripped.split("_") if tok]
        score = 0

        if stripped == pname or gname_lower == pname:
            score = 5
        elif stripped.endswith("_" + pname):
            score = 4
        elif pname in tokens:
            score = 3
        elif stripped.endswith(pname):
            score = 2
        elif pname in gname_lower:
            score = 1

        if score == 0:
            continue

        if _looks_like_env_placeholder(tokens, pname):
            continue

        if ann:
            if "str" in ann and not isinstance(gval, str):
                continue
            if ("int" in ann or "integer" in ann) and not isinstance(gval, int):
                continue
            if "float" in ann and not isinstance(gval, float):
                continue
            if "bool" in ann and not isinstance(gval, bool):
                continue

        if score > best_score:
            best_score = score
            best_value = gval

    return best_value


def _select_preferred_hint(values: Optional[List[Any]]) -> Optional[Any]:
    if not values:
        return None
    for value in values:
        if value is not None:
            return value
    return values[0]


def _guess_example_value(
    param: "ParameterInfo",  # noqa: F821
    func: "FunctionInfo",  # noqa: F821
    module_globals: Optional[Dict[str, Any]] = None,
    module_param_values: Optional[Dict[str, List[Any]]] = None,
    literal_assignments: Optional[Dict[str, List[Any]]] = None,
    parameter_usage_values: Optional[Dict[str, List[Any]]] = None,
    param_db_values: Optional[Dict[str, Dict[str, Any]]] = None,
    history_values: Optional[Dict[str, List[Any]]] = None,
    include_source: bool = False,
) -> Any:
    """
    Heuristic guess of a reasonable example value for a parameter,
    considering module-level constants in the function's module.
    """
    source = "heuristic"
    default_value = getattr(param, "default_value", None)

    def _finish(val: Any) -> Any:
        return (val, source) if include_source else val

    if literal_assignments:
        literal = _select_preferred_hint(literal_assignments.get(param.name.lower()))
        if literal is not None:
            if include_source:
                return literal, "literal_assignment"
            return literal

    if parameter_usage_values:
        usage_hint = _select_preferred_hint(parameter_usage_values.get(param.name))
        if usage_hint is not None:
            if include_source:
                return usage_hint, "usage"
            return usage_hint

    if module_globals:
        global_match = _choose_global_for_param(param, module_globals)
        if global_match is not None:
            if include_source:
                return global_match, "module_global"
            return global_match

    if module_param_values:
        hints = _select_preferred_hint(module_param_values.get(param.name))
        if hints is not None:
            if include_source:
                return hints, "module_param"
            return hints

    if param_db_values:
        db_entry = param_db_values.get(param.name.lower())
        if db_entry:
            literals = db_entry.get("literals")
            value = _select_preferred_hint(literals)
            if value is not None:
                if include_source:
                    return value, "database"
                return value

    if history_values:
        history = _select_preferred_hint(history_values.get(param.name.lower()))
        if history is not None:
            if include_source:
                return history, "history"
            return history

    name = param.name.lower()
    ann = (param.annotation or "").lower()
    if not ann and default_value is not None:
        ann = type(default_value).__name__.lower()
    doc = (func.docstring or "").lower()

    if (
        ann in {"bool", "builtins.bool", "typing.bool"}
        or name.startswith("is_")
        or name.startswith("has_")
        or name.endswith("_flag")
    ):
        value = default_value if isinstance(default_value, bool) else True
        return _finish(value)

    if "path" in name or "file" in name or "filename" in name:
        value = "example.txt"
        return _finish(value)
    if "dir" in name or "folder" in name:
        value = "example_dir"
        return _finish(value)

    if "url" in name or "uri" in name:
        value = "https://example.com"
        return _finish(value)

    if (
        ann in {"int", "builtins.int"}
        or any(k in name for k in ["count", "num", "size", "length", "index", "max"])
        or name in {"n", "i", "j", "k"}
    ):
        value = default_value if isinstance(default_value, int) else 1
        return _finish(value)

    if ann in {"float", "builtins.float"} or "timeout" in name or "seconds" in name:
        value = default_value if isinstance(default_value, float) else 1.0
        return _finish(value)

    if ("list" in ann or "sequence" in ann or "tuple" in ann) or name.endswith("s"):
        value = default_value if isinstance(default_value, (list, tuple)) else [1, 2]
        return _finish(value)

    if "dict" in ann or "mapping" in ann or "map" in name:
        value = default_value if isinstance(default_value, dict) else {"key": "value"}
        return _finish(value)

    if "data" in name or "payload" in name or "json" in name:
        value = (
            default_value if isinstance(default_value, dict) else {"data": "example"}
        )
        return _finish(value)

    if (
        ann in {"str", "builtins.str"}
        or "name" in name
        or "label" in name
        or "key" in name
    ):
        value = default_value if isinstance(default_value, str) else "example"
        return _finish(value)

    if "path" in doc and ("file" in name or "path" in name):
        value = "example.txt"
        return _finish(value)

    if default_value is not None:
        return _finish(default_value)

    value = "example"
    return _finish(value)


def _build_minimal_kwargs(
    func: "FunctionInfo",  # noqa: F821
    module_globals: Dict[str, Any],
    module_param_values: Dict[str, List[Any]],
    literal_assignments: Dict[str, List[Any]],
    parameter_usage_values: Dict[str, List[Any]],
    param_db_values: Dict[str, Dict[str, Any]],
    history_values: Dict[str, List[Any]],
) -> Dict[str, Any]:
    required: List["ParameterInfo"] = []  # noqa: F821

    is_method = "." in func.qualname
    for idx, p in enumerate(func.parameters):
        if is_method and idx == 0 and p.name in {"self", "cls"}:
            continue
        if p.kind in {"var_positional", "var_keyword"}:
            continue
        if p.default is None:
            required.append(p)

    kwargs: Dict[str, Any] = {}
    for p in required:
        kwargs[p.name] = _guess_example_value(
            p,
            func,
            module_globals=module_globals,
            module_param_values=module_param_values,
            literal_assignments=literal_assignments,
            parameter_usage_values=parameter_usage_values,
            param_db_values=param_db_values,
            history_values=history_values,
        )
    return kwargs


def _apply_resource_identifier(
    kwargs: Dict[str, Any], func: "FunctionInfo", identifier: str  # noqa: F821
) -> None:
    candidate_names = {"name", "slug", "repo", "item", "resource", "id"}
    resource_lower = (func.crud_resource or "").lower()
    for p in func.parameters:
        pname = p.name
        lower = pname.lower()
        if pname in kwargs:
            continue
        if any(
            pname.startswith(prefix) for prefix in ("max_", "min_", "num_", "count_")
        ):
            continue
        if lower in candidate_names or (resource_lower and resource_lower in lower):
            kwargs[pname] = identifier
    for key in list(kwargs.keys()):
        lower = key.lower()
        if lower in candidate_names or (resource_lower and resource_lower in lower):
            kwargs[key] = identifier


def _build_crud_scenario(
    func: "FunctionInfo",  # noqa: F821
    module_globals: Dict[str, Any],
    module_param_values: Dict[str, List[Any]],
    literal_assignments: Dict[str, List[Any]],
    param_db_values: Dict[str, Dict[str, Any]],
    history_values: Dict[str, List[Any]],
) -> Optional[CrudScenario]:
    if getattr(func, "crud_role", None) != "create":
        return None

    resource = func.crud_resource or func.qualname.split(".")[-1]
    peers = [f for f in getattr(func, "module_functions", []) if f is not func]
    delete_func = next(
        (
            f
            for f in peers
            if f.crud_resource == func.crud_resource and f.crud_role == "delete"
        ),
        None,
    )
    read_func = next(
        (
            f
            for f in peers
            if f.crud_resource == func.crud_resource and f.crud_role == "read"
        ),
        None,
    )
    if not read_func:
        read_func = next(
            (
                f
                for f in peers
                if f.crud_resource == func.crud_resource and f.crud_role == "list"
            ),
            None,
        )
    if not delete_func or not read_func:
        return None

    identifier = _generate_resource_identifier(resource)

    def build_kwargs(
        target: "FunctionInfo", overrides: Optional[Dict[str, Any]] = None  # noqa: F821
    ) -> Dict[str, Any]:
        target_globals = getattr(target, "module_globals", None) or module_globals
        target_module_params = (
            getattr(target, "module_param_values", None) or module_param_values
        )
        target_literals = _extract_literal_assignments_from_file(
            getattr(target, "filepath", None)
        )
        target_usage = getattr(target, "parameter_usage_values", None) or {}
        kwargs = _build_minimal_kwargs(
            target,
            target_globals,
            target_module_params,
            target_literals,
            target_usage,
            param_db_values,
            history_values,
        )
        if overrides:
            for key, value in overrides.items():
                if any(p.name == key for p in target.parameters):
                    kwargs[key] = value
        _apply_resource_identifier(kwargs, target, identifier)
        return kwargs

    steps: List[ScenarioStep] = []

    pre_get = build_kwargs(read_func, {"dry_run": False})
    steps.append(
        ScenarioStep(
            module=read_func.module,
            filepath=read_func.filepath,
            qualname=read_func.qualname,
            params=pre_get,
            expect="falsy",
            description="Ensure resource does not exist before creation.",
        )
    )

    create_kwargs = build_kwargs(func, {"dry_run": False})
    steps.append(
        ScenarioStep(
            module=func.module,
            filepath=func.filepath,
            qualname=func.qualname,
            params=create_kwargs,
            expect="truthy",
            description="Create resource instance.",
        )
    )

    post_get = build_kwargs(read_func, {"dry_run": False})
    steps.append(
        ScenarioStep(
            module=read_func.module,
            filepath=read_func.filepath,
            qualname=read_func.qualname,
            params=post_get,
            expect="truthy",
            description="Validate resource exists after creation.",
        )
    )

    delete_kwargs = build_kwargs(delete_func, {"dry_run": False, "force": True})
    steps.append(
        ScenarioStep(
            module=delete_func.module,
            filepath=delete_func.filepath,
            qualname=delete_func.qualname,
            params=delete_kwargs,
            expect="truthy",
            cleanup=True,
            description="Delete the resource to leave no residue.",
        )
    )

    final_get = build_kwargs(read_func, {"dry_run": False})
    steps.append(
        ScenarioStep(
            module=read_func.module,
            filepath=read_func.filepath,
            qualname=read_func.qualname,
            params=final_get,
            expect="falsy",
            description="Ensure resource is gone after deletion.",
        )
    )

    note = (
        "Set GHTEST_ASSUME_SAFE=1 to skip confirmations before running this scenario."
    )

    return CrudScenario(
        resource=resource or "resource",
        identifier=identifier,
        steps=steps,
        note=note,
    )


def _guess_alternative_value(value: Any, *, from_module_global: bool = False) -> Any:
    """
    Given a baseline example value, produce a different one for
    tests that override defaults.
    """
    if from_module_global:
        return value
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, float):
        return value * 2 or 1.0
    if isinstance(value, str):
        return value + "_alt"
    if isinstance(value, list):
        return value + value
    if isinstance(value, dict):
        new = dict(value)
        new["extra"] = "alt"
        return new
    return (value, "alt")


def _safe_literal_eval(node: ast.AST) -> Any:
    """
    Best-effort literal_eval wrapper for arguments in test calls.
    Returns a Python value or raises if not evaluable.
    """
    return ast.literal_eval(node)


def _is_call_to_target(call: ast.Call, target_name: str) -> bool:
    fn = call.func
    if isinstance(fn, ast.Name):
        return fn.id == target_name
    if isinstance(fn, ast.Attribute):
        return fn.attr == target_name
    return False


def _extract_param_sets_from_test_function(
    func: "FunctionInfo",  # noqa: F821
    test_func: "FunctionInfo",  # noqa: F821
) -> List[Dict[str, Any]]:
    """
    From a single test function, extract argument sets for calls to the
    function under test, based on literal arguments.
    """
    target_name = func.qualname.split(".")[-1]
    test_name = test_func.qualname.split(".")[-1]
    if not test_name.startswith("test_"):
        return []

    try:
        if VB:
            print(f"_extract_param_sets: reading {test_func.filepath}")  # noqa: E701
        with open(test_func.filepath, "r", encoding="utf-8") as f:
            source = f.read()
    except OSError:
        return []

    try:
        tree = ast.parse(source, filename=test_func.filepath)
    except SyntaxError:
        return []

    desired_test_def: Optional[ast.FunctionDef] = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == test_name:
            desired_test_def = node
            break

    if desired_test_def is None:
        return []

    params = func.parameters
    if not params:
        return []

    is_method = "." in func.qualname and params[0].name in {"self", "cls"}
    start_index = 1 if is_method else 0

    param_sets: List[Dict[str, Any]] = []

    sample_calls = getattr(func, "sample_calls", None) or []
    for sample in sample_calls:
        param_sets.append(dict(sample))

    for node in ast.walk(desired_test_def):
        if not isinstance(node, ast.Call):
            continue
        if not _is_call_to_target(node, target_name):
            continue

        kwargs: Dict[str, Any] = {}
        ok = True

        try:
            for i, arg_node in enumerate(node.args):
                param_index = start_index + i
                if param_index >= len(params):
                    break
                pname = params[param_index].name  # noqa: F821
                value = _safe_literal_eval(arg_node)
                kwargs[pname] = value

            for kw in node.keywords:
                if kw.arg is None:
                    continue
                value = _safe_literal_eval(kw.value)
                kwargs[kw.arg] = value
        except Exception:
            ok = False

        if ok and kwargs:
            param_sets.append(kwargs)

    return param_sets


def _extract_test_param_sets_for_func(
    func: "FunctionInfo",  # noqa: F821
    test_funcs: List["FunctionInfo"],  # noqa: F821
) -> List[Dict[str, Any]]:
    """
    Look through all test functions and collect param sets for calls to func.
    Test functions are identified by name test_{function_under_test} and
    the call must actually appear inside the test body.
    """
    if not test_funcs:
        return []

    target_name = func.qualname.split(".")[-1]
    expected_test_name = f"test_{target_name}"

    matching_tests = [
        tf for tf in test_funcs if tf.qualname.split(".")[-1] == expected_test_name
    ]

    all_param_sets: List[Dict[str, Any]] = []
    for tf in matching_tests:
        all_param_sets.extend(_extract_param_sets_from_test_function(func, tf))

    return all_param_sets


def _dedupe_param_sets(param_sets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    def _freeze(value: Any) -> Any:
        if isinstance(value, (list, tuple)):
            return tuple(_freeze(v) for v in value)
        if isinstance(value, dict):
            return tuple(sorted((k, _freeze(v)) for k, v in value.items()))
        if isinstance(value, set):
            return tuple(sorted(_freeze(v) for v in value))
        return value

    seen = set()
    result: List[Dict[str, Any]] = []
    for ps in param_sets:
        try:
            key = tuple(sorted((k, _freeze(v)) for k, v in ps.items()))
        except TypeError:
            key = tuple(sorted((k, repr(v)) for k, v in ps.items()))
        if key in seen:
            continue
        seen.add(key)
        result.append(ps)
    return result


def suggest_params(
    func: "FunctionInfo",  # noqa: F821
    test_functions: Optional[List["FunctionInfo"]] = None,  # noqa: F821
    *,
    literal_only: bool = False,
    coverage_data: Optional[Any] = None,
) -> SuggestedFunctionTests:
    """
    Suggest parameter sets for tests of a single FunctionInfo.

    Uses three sources, in order of preference:
    1) Existing test functions (from a tests folder) that call the function.
    2) A minimal set using only required parameters (skipping self/cls).
    3) Additional sets where defaulted parameters are given alternative values.

    test_functions should be the scanner results from the tests directory.
    """
    required: List["ParameterInfo"] = []  # noqa: F821
    optional: List["ParameterInfo"] = []  # noqa: F821
    unused_parameters = set(getattr(func, "unused_parameters", None) or [])

    is_method = "." in func.qualname

    for idx, p in enumerate(func.parameters):
        if is_method and idx == 0 and p.name in {"self", "cls"}:
            continue

        if p.kind in {"var_positional", "var_keyword"}:
            continue

        is_required = p.default is None
        if is_required:
            required.append(p)
        else:
            optional.append(p)

    if unused_parameters:
        optional = [p for p in optional if p.name not in unused_parameters]

    module_globals = getattr(func, "module_globals", None) or {}
    if not module_globals:
        filepath = getattr(func, "filepath", None)
        if isinstance(filepath, str):
            module_globals = _extract_module_globals_from_file(filepath)
    module_param_values = getattr(func, "module_param_values", None) or {}
    filepath = getattr(func, "filepath", None)
    literal_assignments = _extract_literal_assignments_from_file(filepath)
    parameter_usage_values = getattr(func, "parameter_usage_values", None) or {}
    history_values = _load_param_history()
    param_db_values = _load_param_database()

    param_sets: List[Dict[str, Any]] = []
    observed_values: Dict[str, List[Any]] = defaultdict(list)

    def _record(call_kwargs: Dict[str, Any]) -> None:
        for name, value in call_kwargs.items():
            if not _is_serializable_value(value):
                continue
            bucket = observed_values.setdefault(name, [])
            if value not in bucket:
                bucket.append(value)

    for name, values in module_param_values.items():
        for value in values:
            if not _is_serializable_value(value):
                continue
            bucket = observed_values.setdefault(name, [])
            if value not in bucket:
                bucket.append(value)

    module_call_values = getattr(func, "module_call_values", None) or []
    for call in module_call_values:
        call_copy = dict(call)
        param_sets.append(call_copy)
        _record(call_copy)

    sample_calls = getattr(func, "sample_calls", None) or []
    for sample in sample_calls:
        sample_copy = dict(sample)
        param_sets.append(sample_copy)
        _record(sample_copy)

    if test_functions:
        test_param_sets = _extract_test_param_sets_for_func(func, test_functions)
        param_sets.extend(test_param_sets)
        for call_kwargs in test_param_sets:
            _record(call_kwargs)

    minimal: Dict[str, Any] = {}
    for p in required:
        minimal[p.name] = _guess_example_value(
            p,
            func,
            module_globals=module_globals,
            module_param_values=module_param_values,
            literal_assignments=literal_assignments,
            parameter_usage_values=parameter_usage_values,
            param_db_values=param_db_values,
            history_values=history_values,
        )

    param_sets.append(minimal)
    _record(minimal)

    for opt in optional:
        usage_candidates = (
            parameter_usage_values.get(opt.name) if parameter_usage_values else None
        )
        if usage_candidates:
            for candidate in usage_candidates:
                call_kwargs = dict(minimal)
                call_kwargs[opt.name] = candidate
                param_sets.append(call_kwargs)
                _record(call_kwargs)
            continue

        baseline, source = _guess_example_value(
            opt,
            func,
            module_globals=module_globals,
            module_param_values=module_param_values,
            literal_assignments=literal_assignments,
            parameter_usage_values=parameter_usage_values,
            param_db_values=param_db_values,
            history_values=history_values,
            include_source=True,
        )
        baseline_kwargs = dict(minimal)
        if baseline is not None:
            baseline_kwargs[opt.name] = baseline
            param_sets.append(baseline_kwargs)
            _record(baseline_kwargs)

        if not literal_only:
            alt = _guess_alternative_value(
                baseline,
                from_module_global=(source == "module_global"),
            )
            if alt != baseline:
                alt_kwargs = dict(minimal)
                alt_kwargs[opt.name] = alt
                param_sets.append(alt_kwargs)
                _record(alt_kwargs)

    if not literal_only:
        verbosity_params = required + optional
        for p in verbosity_params:
            candidate_values = _verbosity_candidate_values(p)
            if not candidate_values:
                continue
            for value in candidate_values:
                call_kwargs = dict(minimal)
                call_kwargs[p.name] = value
                param_sets.append(call_kwargs)
                _record(call_kwargs)

    if not literal_only:
        branch_calls = _build_branch_param_sets(
            func, minimal, coverage_data=coverage_data
        )
        for call_kwargs in branch_calls:
            param_sets.append(call_kwargs)
            _record(call_kwargs)

    param_sets = _dedupe_param_sets(param_sets)
    _update_param_history(observed_values)
    _update_param_database(func, observed_values)

    scenario = None
    if getattr(func, "crud_role", None) == "create":
        scenario = _build_crud_scenario(
            func,
            module_globals,
            module_param_values,
            literal_assignments,
            param_db_values,
            history_values,
        )

    return SuggestedFunctionTests(
        module=func.module,
        filepath=func.filepath,
        qualname=func.qualname,
        docstring=func.docstring,
        param_sets=param_sets,
        scenario=scenario,
    )


def _is_verbosity_param(name: str) -> bool:
    lname = name.lower()
    for token in VERBOSITY_PARAM_TOKENS:
        if token == "vb":
            if lname == "vb" or lname.startswith("vb_") or lname.endswith("_vb"):
                return True
        if token in lname:
            return True
    return False


def _verbosity_candidate_values(
    param: "ParameterInfo",  # noqa: F821
) -> Optional[List[Any]]:
    if not _is_verbosity_param(param.name):
        return None

    ann = (param.annotation or "").lower()
    default_value = getattr(param, "default_value", None)

    if "bool" in ann or isinstance(default_value, bool):
        base = [False, True]
    elif "int" in ann or (
        isinstance(default_value, int) and not isinstance(default_value, bool)
    ):
        base = [0, 1, 2, 3]
    else:
        base = [False, True]

    if default_value is not None and default_value not in base:
        base.append(default_value)

    seen = set()
    ordered: List[Any] = []
    for value in base:
        if value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered


def _history_path() -> Path:
    env = os.environ.get(_PARAM_HISTORY_ENV)
    if env:
        return Path(env)
    state_home = os.environ.get("XDG_STATE_HOME")
    if state_home:
        base = Path(state_home)
    else:
        base = Path.home() / ".local" / "state"
    return base / "ghtest" / "param_history.json"


def _is_serializable_value(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, (bool, int, float, str)):
        return True
    if isinstance(value, list):
        return all(_is_serializable_value(v) for v in value)
    if isinstance(value, dict):
        return all(
            isinstance(k, str) and _is_serializable_value(v) for k, v in value.items()
        )
    return False


def _load_param_history() -> Dict[str, List[Any]]:
    global _PARAM_HISTORY_CACHE
    if _PARAM_HISTORY_CACHE is not None:
        return _PARAM_HISTORY_CACHE

    path = _history_path()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            _PARAM_HISTORY_CACHE = {str(k).lower(): list(v) for k, v in data.items()}
        else:
            _PARAM_HISTORY_CACHE = {}
    except FileNotFoundError:
        _PARAM_HISTORY_CACHE = {}
    except json.JSONDecodeError:
        _PARAM_HISTORY_CACHE = {}
    return _PARAM_HISTORY_CACHE


def _save_param_history(history: Dict[str, List[Any]]) -> None:
    path = _history_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")


def _history_values_for(name: str) -> List[Any]:
    history = _load_param_history()
    return history.get(name.lower(), [])


def _update_param_history(observed: Dict[str, List[Any]]) -> None:
    if not observed:
        return
    history = _load_param_history()
    changed = False
    for name, values in observed.items():
        key = name.lower()
        bucket = history.setdefault(key, [])
        for value in values:
            if not _is_serializable_value(value):
                continue
            if value not in bucket:
                bucket.append(value)
                changed = True
    if changed:
        _save_param_history(history)


_SAFE_STRING_LITERALS = {
    "max",
    "min",
    "all",
    "none",
    "auto",
    "default",
    "first",
    "last",
}


def _is_truthy_env(value: Optional[str]) -> bool:
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _param_seed_path() -> Path:
    return Path(__file__).resolve().parent / "data" / "param_seed.json"


def _param_db_path() -> Path:
    env = os.environ.get(_PARAM_DB_ENV)
    if env:
        return Path(env)
    state_home = os.environ.get("XDG_STATE_HOME")
    base = Path(state_home) if state_home else Path.home() / ".local" / "state"
    return base / "ghtest" / "param_db.json"


def _should_write_param_db(path: Path) -> bool:
    disable = _is_truthy_env(os.environ.get(_PARAM_DB_DISABLE_ENV))
    if not disable:
        return True
    # Allow writes if user explicitly set a project-specific DB path.
    return bool(os.environ.get(_PARAM_DB_ENV))


def _sanitize_db_value(value: Any) -> Optional[Any]:
    if isinstance(value, bool):
        return value
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, float):
        return value
    if isinstance(value, str):
        cleaned = value.strip()
        if cleaned.lower() in _SAFE_STRING_LITERALS:
            return cleaned
        return None
    return None


def _normalize_db_entry(entry: Any) -> Optional[Dict[str, Any]]:
    if not isinstance(entry, dict):
        return None
    normalized: Dict[str, Any] = {}
    entry_type = entry.get("type")
    if isinstance(entry_type, str) and entry_type:
        normalized["type"] = entry_type
    literals: List[Any] = []
    for value in (
        entry.get("literals", []) if isinstance(entry.get("literals"), list) else []
    ):
        sanitized = _sanitize_db_value(value)
        if sanitized is None:
            continue
        if sanitized not in literals:
            literals.append(sanitized)
    normalized["literals"] = literals
    return normalized


def _merge_db_entries(existing: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
    merged = {
        "type": existing.get("type") or new.get("type"),
        "literals": list(existing.get("literals", [])),
    }
    for value in new.get("literals", []):
        if value not in merged["literals"]:
            merged["literals"].append(value)
    return merged


def _read_param_file(path: Path) -> Dict[str, Dict[str, Any]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}
    if not isinstance(data, dict):
        return {}
    result: Dict[str, Dict[str, Any]] = {}
    for key, entry in data.items():
        normalized = _normalize_db_entry(entry)
        if not normalized:
            continue
        result[key.lower()] = normalized
    return result


def _load_param_database() -> Dict[str, Dict[str, Any]]:
    global _PARAM_DB_CACHE
    if _PARAM_DB_CACHE is not None:
        return _PARAM_DB_CACHE
    combined: Dict[str, Dict[str, Any]] = {}
    seed = _read_param_file(_param_seed_path())
    combined.update(seed)
    local = _read_param_file(_param_db_path())
    for key, entry in local.items():
        if key in combined:
            combined[key] = _merge_db_entries(combined[key], entry)
        else:
            combined[key] = entry
    _PARAM_DB_CACHE = combined
    return combined


def _save_param_db(entries: Dict[str, Dict[str, Any]]) -> bool:
    path = _param_db_path()
    if not _should_write_param_db(path):
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    serializable = {
        key: {"type": value.get("type"), "literals": value.get("literals", [])}
        for key, value in sorted(entries.items())
        if value.get("literals")
    }
    path.write_text(
        json.dumps(serializable, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return True


def _infer_param_type(func: "FunctionInfo", name: str) -> Optional[str]:  # noqa: F821
    for param in getattr(func, "parameters", []):
        if param.name != name:
            continue
        if param.annotation:
            return param.annotation
        default_value = getattr(param, "default_value", None)
        if default_value is not None:
            return type(default_value).__name__
        break
    return None


def _update_param_database(
    func: "FunctionInfo", observed: Dict[str, List[Any]]  # noqa: F821
) -> None:
    if not observed:
        return
    local_entries = _read_param_file(_param_db_path())
    changed = False
    for name, values in observed.items():
        sanitized_values = []
        for value in values:
            sanitized = _sanitize_db_value(value)
            if sanitized is None:
                continue
            sanitized_values.append(sanitized)
        if not sanitized_values:
            continue
        key = name.lower()
        entry = local_entries.setdefault(key, {"type": None, "literals": []})
        if not entry.get("type"):
            inferred = _infer_param_type(func, name)
            if inferred:
                entry["type"] = inferred
        for val in sanitized_values:
            if val not in entry["literals"]:
                entry["literals"].append(val)
                changed = True
    if changed:
        wrote = _save_param_db(local_entries)
        if wrote:
            global _PARAM_DB_CACHE
            _PARAM_DB_CACHE = None


_AST_MODULE_CACHE: Dict[str, Optional[ast.Module]] = {}


@dataclass
class _BranchHint:
    param: str
    kind: str
    value: Any


def _build_branch_param_sets(
    func: "FunctionInfo",  # noqa: F821
    base_kwargs: Dict[str, Any],
    coverage_data: Optional[Any] = None,
) -> List[Dict[str, Any]]:
    node = _load_function_node(func.filepath, func.qualname)
    if node is None:
        return []
    param_names = {p.name for p in func.parameters}
    if not param_names:
        return []
    param_map = {p.name: p for p in func.parameters}
    collector = _BranchHintCollector(param_names, root=node)
    collector.visit(node)

    missed_branches = []
    if coverage_data and func.filepath:
        missed_branches = analyze_file_coverage(func.filepath, coverage_data)

    branch_calls: List[Dict[str, Any]] = []

    # Process coverage-based hints first if available
    if missed_branches:
        for missed in missed_branches:
            # Find hints that match the missed condition
            # This is a bit tricky because we need to map the AST condition back to parameters.
            # We can reuse _BranchHintCollector logic on the specific condition node.
            condition_collector = _BranchHintCollector(
                param_names, root=missed["condition"]
            )
            # We need to visit the condition expression, not the whole function
            condition_collector._analyze_expr(missed["condition"])

            for hint in condition_collector.hints:
                # Filter hints to match the 'needed' outcome (True/False)
                # If needed is True, we want values that make the condition True.
                # If needed is False, we want values that make the condition False.

                # _branch_hint_candidate_values returns values for specific kinds (truthy, falsy, eq, etc.)
                # We need to align the hint kind with the needed outcome.

                # If hint.kind is 'truthy' and needed is True -> use truthy values
                # If hint.kind is 'truthy' and needed is False -> use falsy values (which are NOT returned by _branch_hint_candidate_values for 'truthy' kind directly?)
                # Wait, _branch_hint_candidate_values returns [True, False] for truthy kind.
                # So we just need to pick the right one.

                values = _branch_hint_candidate_values(hint, param_map)

                # Filter values based on 'needed'
                targeted_values = []
                for val in values:
                    # This is a heuristic check. Ideally we'd evaluate the condition with the value.
                    # But we can assume:
                    # - if needed=True, we want the "primary" value for the hint kind
                    # - if needed=False, we want the "alternative" value

                    # Actually, let's just add all of them. The goal is to cover the branch.
                    # If we missed the branch, it means we probably didn't have a test case that exercised it.
                    # So adding *both* truthy and falsy values for the condition is a good strategy.
                    targeted_values.append(val)

                for candidate in targeted_values:
                    if candidate is _MISSING_LITERAL:
                        continue
                    kwargs = dict(base_kwargs)
                    kwargs[hint.param] = candidate
                    branch_calls.append(kwargs)

    # Always include static analysis of all branches to ensure baseline coverage
    # (Targeted hints are added above)
    for hint in collector.hints:
        values = _branch_hint_candidate_values(hint, param_map)
        for candidate in values:
            if candidate is _MISSING_LITERAL:
                continue
            kwargs = dict(base_kwargs)
            kwargs[hint.param] = candidate
            branch_calls.append(kwargs)
    return branch_calls


def _load_function_node(filepath: Optional[str], qualname: str) -> Optional[ast.AST]:
    if not filepath or not qualname:
        return None
    module = _load_ast_module(filepath)
    if module is None:
        return None
    finder = _TargetFunctionFinder(qualname)
    finder.visit(module)
    return finder.found


def _load_ast_module(filepath: str) -> Optional[ast.Module]:
    if filepath in _AST_MODULE_CACHE:
        return _AST_MODULE_CACHE[filepath]
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
    except OSError:
        _AST_MODULE_CACHE[filepath] = None
        return None
    try:
        tree = ast.parse(source, filename=filepath)
    except SyntaxError:
        tree = None
    _AST_MODULE_CACHE[filepath] = tree
    return tree


class _TargetFunctionFinder(ast.NodeVisitor):
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


_MISSING_LITERAL = object()


def _literal_or_missing(node: ast.AST) -> Any:
    try:
        return ast.literal_eval(node)
    except Exception:
        return _MISSING_LITERAL


class _BranchHintCollector(ast.NodeVisitor):
    def __init__(self, param_names: Set[str], *, root: ast.AST) -> None:
        self.param_names = param_names
        self.root = root
        self.hints: List[_BranchHint] = []
        self._seen: Set[Tuple[str, str, Any]] = set()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if node is self.root:
            self.generic_visit(node)
        # Skip nested function bodies.
        return

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        if node is self.root:
            self.generic_visit(node)
        return

    def visit_If(self, node: ast.If) -> None:
        self._analyze_expr(node.test)
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:
        self._analyze_expr(node.test)
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        for value in node.values:
            self._analyze_expr(value)

    def _analyze_expr(self, expr: ast.AST) -> None:
        if isinstance(expr, ast.BoolOp):
            for value in expr.values:
                self._analyze_expr(value)
            return
        if isinstance(expr, ast.UnaryOp) and isinstance(expr.op, ast.Not):
            name = self._param_from_node(expr.operand)
            if name:
                self._record_hint(name, "falsy", None)
            return
        if isinstance(expr, ast.Name):
            name = self._param_from_node(expr)
            if name:
                self._record_hint(name, "truthy", None)
            return
        if isinstance(expr, ast.Compare):
            self._handle_compare(expr)

    def _handle_compare(self, node: ast.Compare) -> None:
        if len(node.ops) != 1 or len(node.comparators) != 1:
            return
        op = node.ops[0]
        right = node.comparators[0]
        left_name = self._param_from_node(node.left)
        right_name = self._param_from_node(right)
        right_value = _literal_or_missing(right)
        left_value = _literal_or_missing(node.left)
        if left_name and right_value is not _MISSING_LITERAL:
            kind = _compare_op_kind(op, flipped=False)
            if kind:
                self._record_hint(left_name, kind, right_value)
            return
        if right_name and left_value is not _MISSING_LITERAL:
            kind = _compare_op_kind(op, flipped=True)
            if kind:
                self._record_hint(right_name, kind, left_value)
            return

    def _param_from_node(self, node: ast.AST) -> Optional[str]:
        if isinstance(node, ast.Name) and node.id in self.param_names:
            return node.id
        return None

    def _record_hint(self, param: str, kind: str, value: Any) -> None:
        hashable = _hashable_value(value)
        key = (param, kind, hashable)
        if key in self._seen:
            return
        self._seen.add(key)
        self.hints.append(_BranchHint(param=param, kind=kind, value=value))


def _compare_op_kind(op: ast.cmpop, *, flipped: bool) -> Optional[str]:
    mapping = {
        ast.Eq: "eq",
        ast.NotEq: "ne",
        ast.Is: "eq",
        ast.IsNot: "ne",
        ast.Gt: "gt",
        ast.GtE: "ge",
        ast.Lt: "lt",
        ast.LtE: "le",
        ast.In: "in",
        ast.NotIn: "not_in",
    }
    for node_type, label in mapping.items():
        if isinstance(op, node_type):
            kind = label
            break
    else:
        return None
    if flipped and kind in {"gt", "ge", "lt", "le"}:
        swap = {"gt": "lt", "ge": "le", "lt": "gt", "le": "ge"}
        kind = swap[kind]
    # "in" comparisons are only supported when parameter is on the left side.
    if flipped and kind in {"in", "not_in"}:
        return None
    return kind


def _hashable_value(value: Any) -> Any:
    if isinstance(value, list):
        return tuple(_hashable_value(v) for v in value)
    if isinstance(value, dict):
        return tuple(sorted((k, _hashable_value(v)) for k, v in value.items()))
    if isinstance(value, set):
        return tuple(sorted(_hashable_value(v) for v in value))
    return value


def _branch_hint_candidate_values(
    hint: _BranchHint, param_map: Dict[str, Any]
) -> List[Any]:
    param_info = param_map.get(hint.param)
    is_bool = False
    truthy_value = "example"
    falsy_value = None

    if param_info:
        name = param_info.name.lower()
        ann = (param_info.annotation or "").lower()
        default_value = getattr(param_info, "default_value", None)

        if (
            ann in {"bool", "builtins.bool", "typing.bool"}
            or name.startswith("is_")
            or name.startswith("has_")
            or name.endswith("_flag")
            or isinstance(default_value, bool)
        ):
            is_bool = True

        if not is_bool:
            if ann in {"int", "builtins.int"}:
                truthy_value = 1
                falsy_value = 0
            elif ann in {"float", "builtins.float"}:
                truthy_value = 1.0
                falsy_value = 0.0
            elif ann in {"list", "builtins.list", "typing.list"}:
                truthy_value = ["example"]
                falsy_value = []
            elif ann in {"dict", "builtins.dict", "typing.dict"}:
                truthy_value = {"key": "value"}
                falsy_value = {}

    if hint.kind == "truthy":
        if is_bool:
            return [True, False]
        return [truthy_value]
    if hint.kind == "falsy":
        if is_bool:
            return [False, True]
        return [falsy_value]
    if hint.kind == "eq":
        alt = _branch_alt_value(hint.value)
        values = [hint.value]
        if alt is not None:
            values.append(alt)
        return values
    if hint.kind == "ne":
        alt = _branch_alt_value(hint.value)
        return [alt] if alt is not None else []
    if hint.kind in {"gt", "ge", "lt", "le"}:
        return _numeric_branch_values(hint.value, hint.kind)
    if hint.kind == "in":
        options = list(hint.value) if isinstance(hint.value, (list, tuple, set)) else []
        if not options:
            return []
        alt = _branch_alt_value(options[0])
        result = [options[0]]
        if alt is not None:
            result.append(alt)
        return result
    if hint.kind == "not_in":
        options = list(hint.value) if isinstance(hint.value, (list, tuple, set)) else []
        if not options:
            return []
        alt = _branch_alt_value(options[0])
        if alt is None:
            return []
        while alt in options:
            alt = _branch_alt_value(alt)
            if alt is None:
                break
        return [alt] if alt is not None else []
    return []


def _numeric_branch_values(value: Any, kind: str) -> List[Any]:
    if isinstance(value, bool):
        value = int(value)
    if not isinstance(value, (int, float)):
        return []
    step = 1 if isinstance(value, int) else 0.5
    if kind == "gt":
        return [value + step, value]
    if kind == "ge":
        return [value, value - step]
    if kind == "lt":
        return [value - step, value]
    if kind == "le":
        return [value, value + step]
    return []


def _branch_alt_value(value: Any) -> Optional[Any]:
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, float):
        return value + 1.0
    if value is None:
        return True
    if isinstance(value, str):
        return value + "_alt"
    if isinstance(value, (list, tuple, set)):
        return (
            next(iter(value), None)
            if isinstance(value, set)
            else (value[0] if value else None)
        )
    return None


def _generate_resource_identifier(resource: Optional[str]) -> str:
    prefix = "".join(ch for ch in (resource or "") if ch.isalpha()).lower() or "item"
    prefix = prefix[:3] if prefix else "itm"
    if not prefix[0].isalpha():
        prefix = "a" + prefix[1:]
    suffix = "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(6)
    )
    return f"{prefix}{suffix}"
