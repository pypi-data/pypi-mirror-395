#!/usr/bin/env python
# coding: utf-8

from __future__ import annotations

import base64
import builtins
import importlib
import importlib.util
import io
import os
import sys
import uuid
import zlib
from collections.abc import Mapping as MappingABC, Sequence as SequenceABC
from contextlib import contextmanager, redirect_stdout
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import re

try:  # pragma: no cover - optional dependency
    from requests import Response as _RequestsResponse
except Exception:  # pragma: no cover - requests not installed
    _RequestsResponse = None


@dataclass
class CaseTestResult:
    target: str
    params: Dict[str, Any]
    return_value: Any
    printed: str
    exception: Optional[BaseException]
    file_reads: List[Tuple[str, str]] = field(default_factory=list)
    file_writes: List[Tuple[str, str]] = field(default_factory=list)
    return_summary: Dict[str, Any] = field(default_factory=dict)
    volatile_return_fields: List[str] = field(default_factory=list)
    cassette_path: Optional[str] = None


@dataclass
class RunTestWithCassette:
    cassette_path: str
    cases: List[CaseTestResult]


def _import_module_from_path(path: str, module_name: Optional[str] = None):
    if module_name is None:
        base = os.path.splitext(os.path.basename(path))[0]
        module_name = f"{base}_{uuid.uuid4().hex}"

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot import module from {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def import_function(
    module: str, filepath: Optional[str], qualname: str
) -> Callable[..., Any]:
    try:
        mod = importlib.import_module(module)
    except Exception:
        if not filepath:
            raise
        mod = _import_module_from_path(filepath)

    obj: Any = mod
    for part in qualname.split("."):
        obj = getattr(obj, part)
    return obj


def call_with_capture(
    func: Callable[..., Any],
    *,
    target: str,
    params: Dict[str, Any],
    volatile_return_fields: Optional[Sequence[str]] = None,
) -> CaseTestResult:
    buf = io.StringIO()
    if volatile_return_fields is None:
        volatile_fields = list(_DEFAULT_VOLATILE_RESPONSE_FIELDS)
    else:
        volatile_fields = list(volatile_return_fields)
    with _capture_file_access() as (reads, writes):
        with redirect_stdout(buf):
            try:
                ret = func(**params)
                exc: Optional[BaseException] = None
            except BaseException as error:  # noqa: BLE001
                ret = None
                exc = error
    return_summary = _summarize_return_value(ret, volatile_fields)
    return CaseTestResult(
        target=target,
        params=params,
        return_value=ret,
        printed=buf.getvalue(),
        exception=exc,
        file_reads=list(reads),
        file_writes=list(writes),
        return_summary=return_summary,
        volatile_return_fields=volatile_fields,
    )


def execute_function(
    module: str,
    filepath: Optional[str],
    qualname: str,
    params: Dict[str, Any],
    *,
    volatile_return_fields: Optional[Sequence[str]] = None,
) -> CaseTestResult:
    func = import_function(module, filepath, qualname)
    return call_with_capture(
        func,
        target=qualname,
        params=params,
        volatile_return_fields=volatile_return_fields,
    )


@contextmanager
def _capture_file_access() -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
    reads: List[Tuple[str, str]] = []
    writes: List[Tuple[str, str]] = []

    original_open = builtins.open
    original_path_open = Path.open

    def _record(path: Optional[str], mode: str) -> None:
        if not path:
            return
        read_flag, write_flag = _classify_mode(mode)
        if read_flag:
            reads.append((path, mode))
        if write_flag:
            writes.append((path, mode))

    def _wrap_open(func):
        def _inner(file, mode="r", *args, **kwargs):
            _record(_normalize_path(file), mode)
            return func(file, mode, *args, **kwargs)

        return _inner

    def _wrap_path_open(func):
        def _inner(self, mode="r", *args, **kwargs):
            _record(str(self), mode)
            return func(self, mode, *args, **kwargs)

        return _inner

    builtins.open = _wrap_open(original_open)
    Path.open = _wrap_path_open(original_path_open)
    try:
        yield reads, writes
    finally:
        builtins.open = original_open
        Path.open = original_path_open


def _classify_mode(mode: str) -> Tuple[bool, bool]:
    if not mode:
        mode = "r"
    read = "r" in mode or "+" in mode
    write = any(flag in mode for flag in ("w", "a", "x", "+"))
    return read, write


def _normalize_path(target: Any) -> Optional[str]:
    if isinstance(target, (str, bytes, os.PathLike)):
        try:
            p = Path(target).resolve()
            # Try to make it relative to CWD
            try:
                return str(p.relative_to(Path.cwd()))
            except ValueError:
                return str(p)
        except Exception:
            return str(target)
    return None


_HEX_PTR_RE = re.compile(r" at 0x[0-9A-Fa-f]+")


def _stable_repr(value: Any) -> str:
    rep = repr(value)
    return _HEX_PTR_RE.sub("", rep)


def _type_name(value: Any) -> str:
    if value is None:
        return "NoneType"
    return f"{value.__class__.__module__}.{value.__class__.__name__}"


def _quick_hash(data: bytes) -> str:
    return format(zlib.adler32(data) & 0xFFFFFFFF, "08x")


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


def _summarize_return_value(
    value: Any, volatile_fields: Sequence[str]
) -> Dict[str, Any]:
    summary: Dict[str, Any] = {
        "type": _type_name(value),
        "repr": _stable_repr(value),
    }
    if _is_literal_value(value):
        summary["value"] = value
        return summary
    if isinstance(value, str):
        summary["text"] = _summarize_blob(value)
        return summary
    if isinstance(value, (bytes, bytearray)):
        summary["bytes"] = _summarize_blob(bytes(value))
        return summary
    if _RequestsResponse is not None and isinstance(value, _RequestsResponse):
        summary["object"] = "requests.Response"
        summary["attributes"] = _collect_response_attributes(value, volatile_fields)
        return summary
    return summary


def _collect_response_attributes(
    response: Any, volatile_fields: Sequence[str]
) -> Dict[str, Dict[str, Any]]:
    attributes: Dict[str, Dict[str, Any]] = {}
    volatile = set(volatile_fields or [])
    candidate_names = {
        name for name in response.__dict__.keys() if not name.startswith("_")
    }
    candidate_names.update(_RESPONSE_EXTRA_ATTRS)
    for name in sorted(candidate_names):
        if name in volatile:
            continue
        try:
            if name == "content":
                value = response.content
            elif name == "text":
                value = response.text
            else:
                value = getattr(response, name)
        except Exception:
            continue
        if callable(value):
            continue
        attributes[name] = _summarize_attribute_value(value)
    return attributes


def _summarize_attribute_value(value: Any) -> Dict[str, Any]:
    summary: Dict[str, Any] = {
        "type": _type_name(value),
        "repr": _stable_repr(value),
    }
    if _is_literal_value(value):
        summary["value"] = value
        return summary
    if isinstance(value, str):
        summary.update(_summarize_blob(value))
        return summary
    if isinstance(value, (bytes, bytearray)):
        summary.update(_summarize_blob(bytes(value)))
        return summary
    if isinstance(value, MappingABC):
        try:
            summary["length"] = len(value)
        except Exception:
            pass
        sample: Dict[str, Any] = {}
        for key, val in list(value.items())[:5]:
            if isinstance(key, str):
                sample[key] = val if _is_literal_value(val) else _stable_repr(val)
        if sample:
            summary["sample"] = sample
        return summary
    if isinstance(value, SequenceABC) and not isinstance(
        value, (str, bytes, bytearray)
    ):
        try:
            summary["length"] = len(value)
        except Exception:
            pass
        preview: List[Any] = []
        for item in list(value)[:5]:
            preview.append(item if _is_literal_value(item) else _stable_repr(item))
        if preview:
            summary["sample"] = preview
        return summary
    return summary


_BLOB_INLINE_LIMIT = 160
_BLOB_PREVIEW_LIMIT = 80
_RESPONSE_EXTRA_ATTRS = {
    "content",
    "elapsed",
    "encoding",
    "headers",
    "history",
    "is_permanent_redirect",
    "is_redirect",
    "ok",
    "reason",
    "status_code",
    "text",
    "url",
}
_DEFAULT_VOLATILE_RESPONSE_FIELDS = ("elapsed", "headers")


def _summarize_blob(value: Union[str, bytes]) -> Dict[str, Any]:
    if isinstance(value, str):
        data = value
        encoded = data.encode("utf-8", errors="replace")
        summary: Dict[str, Any] = {
            "length": len(data),
            "preview": data[:_BLOB_PREVIEW_LIMIT],
            "hash": _quick_hash(encoded),
        }
        if len(data) <= _BLOB_INLINE_LIMIT:
            summary["value"] = data
        return summary
    data_bytes = bytes(value)
    preview_bytes = data_bytes[:_BLOB_PREVIEW_LIMIT]
    summary = {
        "length": len(data_bytes),
        "preview": preview_bytes.decode("utf-8", errors="replace"),
        "preview_b64": base64.b64encode(preview_bytes).decode("ascii"),
        "hash": _quick_hash(data_bytes),
    }
    if len(data_bytes) <= _BLOB_INLINE_LIMIT:
        summary["value_b64"] = base64.b64encode(data_bytes).decode("ascii")
    return summary


def assert_return_summary(
    actual: Optional[Dict[str, Any]],
    expected: Optional[Dict[str, Any]],
    *,
    target: str,
) -> None:
    actual_data = actual or {}
    expected_data = expected or {}
    _compare_summary(actual_data, expected_data, target, path="return")


def _compare_summary(actual: Any, expected: Any, target: str, *, path: str) -> None:
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            _raise_summary_error(target, path, expected, actual)
        for key, exp_val in expected.items():
            if key not in actual:
                _raise_summary_error(target, f"{path}.{key}", exp_val, "<missing>")
            _compare_summary(actual[key], exp_val, target, path=f"{path}.{key}")
        return
    if isinstance(expected, list):
        if not isinstance(actual, list) or len(actual) != len(expected):
            _raise_summary_error(target, path, expected, actual)
        for idx, (act_item, exp_item) in enumerate(zip(actual, expected)):
            _compare_summary(act_item, exp_item, target, path=f"{path}[{idx}]")
        return
    if actual != expected:
        _raise_summary_error(target, path, expected, actual)


def _raise_summary_error(target: str, path: str, expected: Any, actual: Any) -> None:
    raise AssertionError(
        f"{target} return summary mismatch at {path}: expected {expected!r}, got {actual!r}"
    )


__all__ = [
    "CaseTestResult",
    "RunTestWithCassette",
    "call_with_capture",
    "execute_function",
    "import_function",
    "assert_return_summary",
]
