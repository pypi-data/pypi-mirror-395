#!/usr/bin/env python
# coding: utf-8

from __future__ import annotations

import os
import pprint
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Sequence, Tuple, Literal

from .tests_creator import ScenarioStep, SuggestedFunctionTests
from .test_utils import CaseTestResult, RunTestWithCassette, _stable_repr


@dataclass
class TestArtifact:
    suggestion: SuggestedFunctionTests
    run: RunTestWithCassette


@dataclass
class TestWriterResult:
    test_modules: List[Path]
    scenario_modules: List[Path]


@dataclass
class ScenarioDefinition:
    suggestion: SuggestedFunctionTests
    cases: List[Tuple[ScenarioStep, CaseTestResult]]


ExceptionAssertionMode = Literal["message", "type", "presence", "none"]
_EXCEPTION_ASSERTION_MODES: Tuple[str, ...] = ("message", "type", "presence", "none")


class _DataStore:
    def __init__(self, base_dir: Path, inline_limit: int = 160) -> None:
        self.base_dir = base_dir
        self.inline_limit = inline_limit
        self.counter = 0
        self.used = False
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def literal(self, value: Any, *, label: str) -> str:
        literal = _format_literal(value)
        if self._should_inline(literal):
            return literal
        filename = self._write_data_file(literal, label=label)
        return f"_load_data({filename!r})"

    def _should_inline(self, literal: str) -> bool:
        if literal is None:
            return True
        return len(literal) <= self.inline_limit

    def _write_data_file(self, literal: str, label: str) -> str:
        self.used = True
        filename = f"{label}_{self.counter}.py"
        self.counter += 1
        path = self.base_dir / filename
        path.write_text(f"DATA = {literal}\n", encoding="utf-8")
        return filename


def write_test_modules(
    artifacts: Sequence[TestArtifact],
    output_dir: str,
    *,
    max_cases_per_module: int = 10,
    inline_char_limit: int = 160,
    include_scenarios: bool = True,
    include_return_summary: bool = True,
    exception_assertion: ExceptionAssertionMode = "type",
) -> TestWriterResult:
    if exception_assertion not in _EXCEPTION_ASSERTION_MODES:
        raise ValueError(
            f"Invalid exception assertion mode {exception_assertion!r}; "
            f"expected one of {', '.join(_EXCEPTION_ASSERTION_MODES)}."
        )
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    data_dir = out_dir / "data"
    data_store = _DataStore(data_dir, inline_limit=inline_char_limit)

    case_defs, scenario_defs = _collect_cases(artifacts)
    if not case_defs and not scenario_defs:
        _cleanup_empty_data_dir(data_dir)
        return TestWriterResult(test_modules=[], scenario_modules=[])

    modules: List[Path] = []
    scenario_modules: List[Path] = []
    module_index = 0
    current_cases: List[str] = []
    for case_def in case_defs:
        test_src = _render_test_function(
            case_def,
            data_store,
            out_dir,
            include_return_summary=include_return_summary,
            exception_assertion=exception_assertion,
        )
        if not test_src:
            continue
        current_cases.append(test_src)
        if len(current_cases) >= max_cases_per_module:
            need_loader = data_store.used
            module_path = _write_module(
                out_dir,
                module_index,
                current_cases,
                data_loader=need_loader,
                include_return_summary=include_return_summary,
            )
            modules.append(module_path)
            current_cases = []
            module_index += 1
            data_store.used = False

    if current_cases:
        need_loader = data_store.used
        module_path = _write_module(
            out_dir,
            module_index,
            current_cases,
            data_loader=need_loader,
            include_return_summary=include_return_summary,
        )
        modules.append(module_path)
        data_store.used = False

    if include_scenarios and scenario_defs:
        scenario_modules = _write_scenario_modules(
            out_dir,
            data_store,
            scenario_defs,
            include_return_summary=include_return_summary,
            exception_assertion=exception_assertion,
        )
        data_store.used = False

    _cleanup_empty_data_dir(data_dir)

    return TestWriterResult(test_modules=modules, scenario_modules=scenario_modules)


def _cleanup_empty_data_dir(data_dir: Path) -> None:
    if not data_dir.exists():
        return
    try:
        if not any(data_dir.iterdir()):
            data_dir.rmdir()
    except OSError:
        pass


def _collect_cases(
    artifacts: Sequence[TestArtifact],
) -> Tuple[
    List[Tuple[SuggestedFunctionTests, CaseTestResult, int]], List[ScenarioDefinition]
]:
    collected: List[Tuple[SuggestedFunctionTests, CaseTestResult, int]] = []
    scenarios: List[ScenarioDefinition] = []

    for artifact in artifacts:
        suggestion = artifact.suggestion
        run_cases = list(artifact.run.cases)

        scenario = suggestion.scenario
        scenario_case_count = len(scenario.steps) if scenario else 0
        scenario_cases: List[CaseTestResult] = []
        if scenario and scenario_case_count and len(run_cases) >= scenario_case_count:
            steps = scenario.steps
            candidate = run_cases[-scenario_case_count:]
            expected_targets = [step.qualname for step in steps]
            actual_targets = [case.target for case in candidate]
            if actual_targets == expected_targets:
                scenario_cases = candidate
                run_cases = run_cases[:-scenario_case_count]
                paired = list(zip(steps, scenario_cases))
                scenarios.append(
                    ScenarioDefinition(suggestion=suggestion, cases=paired)
                )

        main_cases = [case for case in run_cases if case.target == suggestion.qualname]
        for idx, case in enumerate(main_cases):
            collected.append((suggestion, case, idx))

    return collected, scenarios


def _render_test_function(
    item: Tuple[SuggestedFunctionTests, CaseTestResult, int],
    data_store: _DataStore,
    out_dir: Path,
    *,
    include_return_summary: bool,
    exception_assertion: ExceptionAssertionMode,
) -> str:
    suggestion, case, case_idx = item
    func_name = _make_test_name(suggestion.qualname, case_idx)
    lines: List[str] = []
    lines.append(f"def {func_name}():")

    filepath_code = _relativize_path_code(suggestion.filepath, out_dir)
    lines.append(
        f"    func = import_function({suggestion.module!r}, {filepath_code}, {suggestion.qualname!r})"
    )

    params_literal = _format_literal(case.params)
    lines.append(_format_assignment("params", params_literal))
    volatile_literal = _format_literal(case.volatile_return_fields)
    lines.append(_format_assignment("volatile_fields", volatile_literal))
    cassette_path = getattr(case, "cassette_path", None)
    if cassette_path:
        cassette_path_code = _relativize_path_code(cassette_path, out_dir)
        lines.append(f"    cassette_path = {cassette_path_code}")
        lines.append(
            "    vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')"
        )
        lines.append("    with vcr_recorder.use_cassette(cassette_path):")
        lines.append(
            "        result = call_with_capture(func, target={qual!r}, params=params, volatile_return_fields=volatile_fields)".format(
                qual=suggestion.qualname
            )
        )
    else:
        lines.append(
            "    result = call_with_capture(func, target={qual!r}, params=params, volatile_return_fields=volatile_fields)".format(
                qual=suggestion.qualname
            )
        )

    if case.exception is None:
        lines.append("    assert result.exception is None")
        return_literal, is_repr = _literal_or_repr(
            case.return_value, data_store, f"{func_name}_return"
        )
        lines.append(_format_assignment("expected_return", return_literal))
        if is_repr:
            lines.append("    assert repr(result.return_value) == expected_return")
        else:
            lines.append("    assert result.return_value == expected_return")
    else:
        lines.extend(_exception_assertion_lines(case, exception_assertion))

    printed_literal, printed_repr = _literal_or_repr(
        case.printed, data_store, f"{func_name}_stdout"
    )
    lines.append(_format_assignment("expected_output", printed_literal))
    if printed_repr:
        lines.append("    assert repr(result.printed) == expected_output")
    else:
        lines.append("    assert result.printed == expected_output")
    reads_literal = _format_file_access_list(case.file_reads, out_dir)
    lines.append(_format_assignment("expected_reads", reads_literal))
    lines.append("    assert result.file_reads == expected_reads")
    writes_literal = _format_file_access_list(case.file_writes, out_dir)
    lines.append(_format_assignment("expected_writes", writes_literal))
    lines.append("    assert result.file_writes == expected_writes")
    if include_return_summary:
        summary_literal = data_store.literal(
            case.return_summary, label=f"{func_name}_return_summary"
        )
        lines.append(_format_assignment("expected_return_summary", summary_literal))
        lines.append(
            f"    assert_return_summary(result.return_summary, expected_return_summary, target={suggestion.qualname!r})"
        )
    return "\n".join(lines) + "\n"


def _write_module(
    output_dir: Path,
    module_index: int,
    tests: List[str],
    *,
    data_loader: bool,
    include_return_summary: bool,
) -> Path:
    module_name = f"test_generated_{module_index}"
    module_path = output_dir / f"{module_name}.py"
    header_lines = ["import vcr", "from pathlib import Path"]
    if include_return_summary:
        header_lines.append(
            "from ghtest.test_utils import assert_return_summary, call_with_capture, import_function"
        )
    else:
        header_lines.append(
            "from ghtest.test_utils import call_with_capture, import_function"
        )
    header = "\n".join(header_lines).rstrip() + "\n\n"
    if data_loader:
        header += "\n".join(_DATA_LOADER_TEMPLATE).rstrip() + "\n\n"
    body = "\n\n".join(tests).rstrip() + "\n"
    content = header + body
    module_path.write_text(content, encoding="utf-8")
    return module_path


def _write_scenario_modules(
    output_dir: Path,
    data_store: _DataStore,
    scenarios: Sequence[ScenarioDefinition],
    *,
    include_return_summary: bool,
    exception_assertion: ExceptionAssertionMode,
) -> List[Path]:
    modules: List[Path] = []
    scenario_dir = output_dir / "scenarios"
    scenario_dir.mkdir(parents=True, exist_ok=True)
    (scenario_dir / "__init__.py").touch()

    for idx, scenario_def in enumerate(scenarios):
        module_path = _write_scenario_module(
            scenario_dir,
            idx,
            scenario_def,
            data_store,
            include_return_summary=include_return_summary,
            exception_assertion=exception_assertion,
        )
        modules.append(module_path)
        data_store.used = False

    return modules


def _write_scenario_module(
    scenario_dir: Path,
    index: int,
    definition: ScenarioDefinition,
    data_store: _DataStore,
    *,
    include_return_summary: bool,
    exception_assertion: ExceptionAssertionMode,
) -> Path:
    scenario = definition.suggestion.scenario
    resource = None
    if scenario:
        resource = scenario.resource
    safe_resource = "".join(
        ch if ch.isalnum() else "_"
        for ch in (resource or definition.suggestion.qualname)
    )
    safe_resource = safe_resource.strip("_") or "scenario"
    module_name = f"test_scenario_{safe_resource}_{index}"
    module_path = scenario_dir / f"{module_name}.py"

    if include_return_summary:
        header_import = "from ghtest.test_utils import assert_return_summary, call_with_capture, import_function"
    else:
        header_import = (
            "from ghtest.test_utils import call_with_capture, import_function"
        )
    header = textwrap.dedent(
        f"""\
        import os
        import vcr
        from pathlib import Path

        {header_import}

        _SCENARIO_ENV = "GHTEST_RUN_SCENARIOS"
        _SCENARIO_LIVE_ENV = "GHTEST_SCENARIO_LIVE"
        _USE_RECORDED_CASSETTES = os.environ.get(_SCENARIO_LIVE_ENV) != '1'
        """
    )

    if data_store.used:
        data_store.used = False

    needs_loader = False
    body = _render_scenario_function(
        definition,
        data_store,
        index,
        scenario_dir,
        include_return_summary=include_return_summary,
        exception_assertion=exception_assertion,
    )
    needs_loader = data_store.used
    if needs_loader:
        # Scenarios are in a subdir, so data is one level up
        loader_code = "\n".join(_DATA_LOADER_TEMPLATE).replace(
            "Path(__file__).with_name('data')", "Path(__file__).parent.parent / 'data'"
        )
        loader = loader_code.rstrip() + "\n\n"
    else:
        loader = ""
    content = header.rstrip() + "\n\n" + loader + body
    module_path.write_text(content, encoding="utf-8")
    return module_path


def _render_scenario_function(
    definition: ScenarioDefinition,
    data_store: _DataStore,
    scenario_index: int,
    out_dir: Path,
    *,
    include_return_summary: bool,
    exception_assertion: ExceptionAssertionMode,
) -> str:
    scenario = definition.suggestion.scenario
    resource = scenario.resource if scenario else definition.suggestion.qualname
    func_name = _make_test_name(f"{resource}_scenario", scenario_index)
    lines: List[str] = [
        f"def {func_name}():",
        "    # Scenario tests are now enabled by default",
        "    pass",
    ]

    for idx, (step, case) in enumerate(definition.cases):
        comment = step.description or f"Step {idx + 1}: {step.qualname}"
        lines.append(f"    # {comment}")
        filepath_code = _relativize_path_code(step.filepath, out_dir)
        lines.append(
            f"    func = import_function({step.module!r}, {filepath_code}, {step.qualname!r})"
        )
        params_literal = _format_literal(step.params)
        lines.append(_format_assignment("params", params_literal))
        volatile_literal = _format_literal(case.volatile_return_fields)
        lines.append(_format_assignment("volatile_fields", volatile_literal))
        cassette_path = getattr(case, "cassette_path", None)
        call_line = "result = call_with_capture(func, target={qual!r}, params=params, volatile_return_fields=volatile_fields)".format(
            qual=step.qualname
        )
        if cassette_path:
            cassette_path_code = _relativize_path_code(cassette_path, out_dir)
            lines.append(f"    cassette_path = {cassette_path_code}")
            lines.append("    if _USE_RECORDED_CASSETTES:")
            lines.append(
                "        vcr_recorder = vcr.VCR(serializer='yaml', match_on=['uri', 'method', 'body'], record_mode='none')"
            )
            lines.append("        with vcr_recorder.use_cassette(cassette_path):")
            lines.append(f"            {call_line}")
            lines.append("    else:")
            lines.append(f"        {call_line}")
        else:
            lines.append(f"    {call_line}")

        if case.exception is None:
            lines.append("    assert result.exception is None")
            return_literal, return_repr = _literal_or_repr(
                case.return_value,
                data_store,
                f"{func_name}_step_{idx}_return",
            )
            lines.append(_format_assignment("expected_return", return_literal))
            if return_repr:
                lines.append("    assert repr(result.return_value) == expected_return")
            else:
                lines.append("    assert result.return_value == expected_return")
        else:
            lines.extend(_exception_assertion_lines(case, exception_assertion))

        printed_literal, printed_repr = _literal_or_repr(
            case.printed,
            data_store,
            f"{func_name}_step_{idx}_stdout",
        )
        lines.append(_format_assignment("expected_output", printed_literal))
        if printed_repr:
            lines.append("    assert repr(result.printed) == expected_output")
        else:
            lines.append("    assert result.printed == expected_output")
        reads_literal = _format_file_access_list(case.file_reads, out_dir)
        lines.append(_format_assignment("expected_reads", reads_literal))
        lines.append("    assert result.file_reads == expected_reads")
        writes_literal = _format_file_access_list(case.file_writes, out_dir)
        lines.append(_format_assignment("expected_writes", writes_literal))
        lines.append("    assert result.file_writes == expected_writes")
        if include_return_summary:
            summary_literal = data_store.literal(
                case.return_summary, label=f"{func_name}_step_{idx}_return_summary"
            )
            lines.append(_format_assignment("expected_return_summary", summary_literal))
            lines.append(
                f"    assert_return_summary(result.return_summary, expected_return_summary, target={step.qualname!r})"
            )

    return "\n".join(lines) + "\n"


def _make_test_name(qualname: str, idx: int) -> str:
    base = "".join(ch if ch.isalnum() else "_" for ch in qualname)
    base = base.strip("_") or "func"
    return f"test_{base}_case_{idx}"


def _format_literal(value: Any) -> str:
    try:
        return pprint.pformat(value, width=80, sort_dicts=True)
    except Exception:
        return repr(value)


def _format_assignment(name: str, literal: str) -> str:
    if "\n" not in literal:
        return f"    {name} = {literal}"
    lines = literal.splitlines()
    formatted = [f"    {name} = {lines[0]}"]
    formatted.extend(f"    {line}" for line in lines[1:])
    return "\n".join(formatted)


def _literal_or_repr(
    value: Any, data_store: _DataStore, label: str
) -> Tuple[str, bool]:
    literal = data_store.literal(value, label=label)
    if literal is not None:
        return literal, False
    return _stable_repr(value), True


def _exception_assertion_lines(
    case: CaseTestResult,
    mode: ExceptionAssertionMode,
    *,
    indent: str = "    ",
) -> List[str]:
    if case.exception is None:
        return [f"{indent}assert result.exception is None"]

    if mode == "none":
        return []

    lines = [f"{indent}assert result.exception is not None"]
    if mode in ("message", "type"):
        exc_type = (
            f"{case.exception.__class__.__module__}.{case.exception.__class__.__name__}"
        )
        lines.append(
            f"{indent}assert result.exception.__class__.__module__ + '.' + result.exception.__class__.__name__ == {exc_type!r}"
        )
        if mode == "message":
            message = str(case.exception)
            lines.append(f"{indent}assert str(result.exception) == {message!r}")
    return lines


def _is_literal_value(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, (bool, int, float, str)):
        return True
    if isinstance(value, (list, tuple)):
        return all(_is_literal_value(v) for v in value)
    if isinstance(value, dict):
        return all(
            isinstance(k, str) and _is_literal_value(v) for k, v in value.items()
        )
    return False


_DATA_LOADER_TEMPLATE = [
    "import importlib.util",
    "from pathlib import Path",
    "",
    "def _load_data(filename: str):",
    "    data_path = Path(__file__).with_name('data') / filename",
    "    spec = importlib.util.spec_from_file_location(f'{__name__}.{filename}', data_path)",
    "    module = importlib.util.module_from_spec(spec)",
    "    assert spec.loader is not None",
    "    spec.loader.exec_module(module)",
    "    return module.DATA",
    "",
]


def _relativize_path_code(path: str, base_dir: Path) -> str:
    if not path:
        return repr(path)
    try:
        abs_path = Path(path).resolve()
        if not abs_path.is_absolute():
            return repr(path)

        rel_path = os.path.relpath(abs_path, base_dir)
        # Use forward slashes for consistency in generated code
        rel_path = rel_path.replace(os.sep, "/")

        return f"str((Path(__file__).parent / {rel_path!r}).resolve())"
    except Exception:
        return repr(path)


def _format_file_access_list(access_list: List[Tuple[str, str]], out_dir: Path) -> str:
    if not access_list:
        return "[]"
    items = []
    for path, mode in access_list:
        path_code = _relativize_path_code(path, out_dir)
        items.append(f"({path_code}, {mode!r})")
    return "[" + ", ".join(items) + "]"


__all__ = ["TestArtifact", "write_test_modules"]
