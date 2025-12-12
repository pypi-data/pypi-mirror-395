#!/usr/bin/env python
# coding: utf-8

# In[1]:


import ast
import os
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set, Tuple


# In[2]:


@dataclass
class ParameterInfo:
    name: str
    kind: str  # "positional_only", "positional_or_keyword", "var_positional", "keyword_only", "var_keyword"
    annotation: Optional[str]
    default: Optional[str]
    default_value: Optional[Any] = None


@dataclass
class FunctionInfo:
    module: str  # e.g. "pkg.sub.module"
    qualname: str  # e.g. "func", "Class.method", "Class.Inner.method"
    filepath: str  # path to the .py file
    lineno: int  # line number in source
    parameters: List[ParameterInfo]
    returns: Optional[str]  # return annotation as string, if any
    docstring: Optional[str]
    module_globals: Dict[str, Any] = field(default_factory=dict)
    sample_calls: List[Dict[str, Any]] = field(default_factory=list)
    module_call_values: List[Dict[str, Any]] = field(default_factory=list)
    module_param_values: Dict[str, List[Any]] = field(default_factory=dict)
    crud_role: Optional[str] = None
    crud_resource: Optional[str] = None
    parameter_usage_values: Dict[str, List[Any]] = field(default_factory=dict)
    unused_parameters: Set[str] = field(default_factory=set)
    module_functions: List["FunctionInfo"] = field(default_factory=list, repr=False)

    def import_object(self) -> Callable[..., Any]:
        """
        Import and return the actual function object using module + qualname.
        """
        import importlib

        mod = importlib.import_module(self.module)
        obj: Any = mod
        for part in self.qualname.split("."):
            obj = getattr(obj, part)
        return obj


def _annotation_to_str(node: Optional[ast.expr]) -> Optional[str]:
    if node is None:
        return None
    # Use ast.unparse when available (Python 3.9+); fall back to ast.dump.
    unparse = getattr(ast, "unparse", None)
    if unparse is not None:
        try:
            return unparse(node)
        except Exception:
            pass
    return ast.dump(node)


def _expr_to_str(node: Optional[ast.expr]) -> Optional[str]:
    if node is None:
        return None
    unparse = getattr(ast, "unparse", None)
    if unparse is not None:
        try:
            return unparse(node)
        except Exception:
            pass
    return ast.dump(node)


def _literal_eval_with_flag(node: Optional[ast.expr]) -> Tuple[bool, Optional[Any]]:
    if node is None:
        return True, None
    try:
        return True, ast.literal_eval(node)
    except Exception:
        return False, None


def _literal_eval_node(node: Optional[ast.expr]) -> Optional[Any]:
    success, value = _literal_eval_with_flag(node)
    if success:
        return value
    return None


def _is_dunder_main_guard(test: ast.expr) -> bool:
    if not isinstance(test, ast.Compare):
        return False
    if len(test.ops) != 1 or not isinstance(test.ops[0], ast.Eq):
        return False
    if len(test.comparators) != 1:
        return False

    left = test.left
    right = test.comparators[0]

    def _is_name(node: ast.AST) -> bool:
        return isinstance(node, ast.Name) and node.id == "__name__"

    def _is_main_literal(node: ast.AST) -> bool:
        return isinstance(node, ast.Constant) and node.value == "__main__"

    return (_is_name(left) and _is_main_literal(right)) or (
        _is_name(right) and _is_main_literal(left)
    )


class _MainBlockCallCollector(ast.NodeVisitor):
    def __init__(self) -> None:
        self.calls: List[ast.Call] = []

    def visit_Call(self, node: ast.Call) -> None:
        self.calls.append(node)
        self.generic_visit(node)


def _call_target_name(node: ast.AST) -> Optional[str]:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
        # Handle direct ClassName.method references
        return f"{node.value.id}.{node.attr}"
    return None


def _detect_crud_role_and_resource(
    qualname: str,
) -> Tuple[Optional[str], Optional[str]]:
    name = qualname.split(".")[-1].lower()
    tokens = name.split("_")
    if not tokens:
        return None, None
    verb = tokens[0]
    resource_tokens = tokens[1:] or []

    create_verbs = {"create", "add", "make", "insert", "new", "build"}
    delete_verbs = {"delete", "remove", "destroy", "drop"}
    read_verbs = {"get", "fetch", "read", "show"}
    list_verbs = {"list", "ls"}
    update_verbs = {"update", "set", "put"}

    role = None
    if verb in create_verbs:
        role = "create"
    elif verb in delete_verbs:
        role = "delete"
    elif verb in read_verbs:
        role = "read"
    elif verb in list_verbs:
        role = "list"
    elif verb in update_verbs:
        role = "update"

    if not role:
        return None, None

    skip_words = {"data", "info", "details", "item", "items"}
    resource_tokens = [tok for tok in resource_tokens if tok and tok not in skip_words]
    resource = "_".join(resource_tokens) if resource_tokens else None

    if resource and resource.endswith("s") and not resource.endswith("ss"):
        resource = resource[:-1]

    return role, resource


def _ordered_parameter_names(params: List[ParameterInfo]) -> List[str]:
    names: List[str] = []
    for p in params:
        if p.kind in {"var_positional", "var_keyword"}:
            continue
        names.append(p.name)
    return names


def _call_kwargs_from_literal_call(
    call: ast.Call,
    params: List[ParameterInfo],
) -> Optional[Dict[str, Any]]:
    ordered = _ordered_parameter_names(params)
    kwargs: Dict[str, Any] = {}
    pos_index = 0

    for arg in call.args:
        success, value = _literal_eval_with_flag(arg)
        if not success:
            return None
        while pos_index < len(ordered) and ordered[pos_index] in kwargs:
            pos_index += 1
        if pos_index >= len(ordered):
            return None
        kwargs[ordered[pos_index]] = value
        pos_index += 1

    for kw in call.keywords:
        if kw.arg is None:
            return None
        success, value = _literal_eval_with_flag(kw.value)
        if not success:
            return None
        kwargs[kw.arg] = value

    return kwargs


def _extract_sample_calls(
    tree: ast.Module,
    functions: List[FunctionInfo],
) -> Dict[str, List[Dict[str, Any]]]:
    if not functions:
        return {}

    top_level_funcs = {
        func.qualname: func for func in functions if "." not in func.qualname
    }
    if not top_level_funcs:
        return {}

    calls: List[ast.Call] = []
    for node in tree.body:
        if isinstance(node, ast.If) and _is_dunder_main_guard(node.test):
            collector = _MainBlockCallCollector()
            for stmt in node.body:
                collector.visit(stmt)
            calls.extend(collector.calls)

    sample_map: Dict[str, List[Dict[str, Any]]] = {}
    if not calls:
        return sample_map

    for call in calls:
        target_name = _call_target_name(call.func)
        if not target_name:
            continue
        func = top_level_funcs.get(target_name)
        if func is None:
            continue
        kwargs = _call_kwargs_from_literal_call(call, func.parameters)
        if kwargs is None:
            continue
        sample_map.setdefault(func.qualname, []).append(kwargs)

    return sample_map


class _InModuleCallCollector(ast.NodeVisitor):
    def __init__(self, function_lookup: Dict[str, List[FunctionInfo]]) -> None:
        self.function_lookup = function_lookup
        self.calls: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    def visit_Call(self, node: ast.Call) -> None:
        target_name = _call_target_name(node.func)
        if target_name:
            candidates = self._resolve_candidates(target_name)
            if candidates:
                func = candidates
                kwargs = _call_kwargs_from_literal_call(node, func.parameters)
                if kwargs:
                    self.calls[func.qualname].append(kwargs)
        self.generic_visit(node)

    def _resolve_candidates(self, target_name: str) -> Optional[FunctionInfo]:
        # Prefer exact qualname match, e.g., Class.method
        direct = self.function_lookup.get(target_name)
        if direct and len(direct) == 1:
            return direct[0]

        simple_name = target_name.split(".")[-1]
        candidates = self.function_lookup.get(simple_name)
        if candidates and len(candidates) == 1:
            return candidates[0]
        return None


def _build_function_lookup(
    functions: List[FunctionInfo],
) -> Dict[str, List[FunctionInfo]]:
    lookup: Dict[str, List[FunctionInfo]] = defaultdict(list)
    for func in functions:
        lookup[func.qualname].append(func)
        simple = func.qualname.split(".")[-1]
        if simple != func.qualname:
            lookup[simple].append(func)
    return lookup


def _extract_internal_call_map(
    tree: ast.Module,
    functions: List[FunctionInfo],
) -> Dict[str, List[Dict[str, Any]]]:
    if not functions:
        return {}
    lookup = _build_function_lookup(functions)
    collector = _InModuleCallCollector(lookup)
    collector.visit(tree)
    return collector.calls


def _extract_module_globals(tree: ast.Module) -> Dict[str, Any]:
    """
    Collect module-level assignments that look like constants, i.e. the section
    between the last import and the first function/class definition.
    """
    body = tree.body
    last_import_idx = -1
    first_def_idx = len(body)

    for idx, node in enumerate(body):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            last_import_idx = idx
        elif isinstance(
            node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
        ) and first_def_idx == len(body):
            first_def_idx = idx

    start = last_import_idx + 1
    end = first_def_idx

    globals_dict: Dict[str, Any] = {}

    for node in body[start:end]:
        if isinstance(node, ast.Assign):
            targets = node.targets
            value_node = node.value
        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]
            value_node = node.value
        else:
            continue

        if value_node is None:
            continue

        try:
            value = ast.literal_eval(value_node)
        except Exception:
            continue

        for target in targets:
            if isinstance(target, ast.Name):
                globals_dict[target.id] = value

    return globals_dict


class _ParamUsageVisitor(ast.NodeVisitor):
    def __init__(self, param_info: Dict[str, ParameterInfo]) -> None:
        self.param_info = param_info
        self.param_names = set(param_info.keys())
        self.used_params: Set[str] = set()
        self.literal_hints: Dict[str, List[Any]] = defaultdict(list)

    def _record_value(self, name: str, value: Any) -> None:
        if name not in self.param_names:
            return
        self.used_params.add(name)
        if value is None:
            bucket = self.literal_hints[name]
            if None not in bucket:
                bucket.append(None)
            return
        bucket = self.literal_hints[name]
        if value not in bucket:
            bucket.append(value)

    def _record_dict_hint(self, name: str) -> None:
        example = {"key": "value"}
        self._record_value(name, example)

    def _record_list_hint(self, name: str) -> None:
        self._record_value(name, ["value"])

    def _looks_boolean_param(self, name: str) -> bool:
        info = self.param_info.get(name)
        if not info:
            return False
        annotation = (info.annotation or "").lower() if info.annotation else ""
        default_value = getattr(info, "default_value", None)
        if isinstance(default_value, bool):
            return True
        if "bool" in annotation:
            return True
        lowered = name.lower()
        bool_prefixes = (
            "is_",
            "has_",
            "should_",
            "enable_",
            "allow_",
            "use_",
            "can_",
            "needs_",
        )
        if lowered.endswith("_flag") or lowered.startswith(bool_prefixes):
            return True
        return False

    def _ensure_bool_values(self, name: str) -> None:
        self.used_params.add(name)
        info = self.param_info.get(name)
        annotation = (info.annotation or "").lower() if info and info.annotation else ""
        default_value = getattr(info, "default_value", None) if info else None
        if not self._looks_boolean_param(name):
            # numeric parameters occasionally appear in truthy checks; give small ints if annotated
            if isinstance(default_value, (int, float)) and not isinstance(
                default_value, bool
            ):
                self._record_value(name, 0)
                self._record_value(name, 1)
            elif "int" in annotation or "float" in annotation:
                self._record_value(name, 0)
                self._record_value(name, 1)
            return

        if isinstance(default_value, (int, float)) and not isinstance(
            default_value, bool
        ):
            self._record_value(name, 0)
            self._record_value(name, 1)
            return
        if "int" in annotation or "float" in annotation:
            self._record_value(name, 0)
            self._record_value(name, 1)
            return
        self._record_value(name, False)
        self._record_value(name, True)

    def _extract_param_name(self, node: ast.AST) -> Optional[str]:
        if isinstance(node, ast.Name) and node.id in self.param_names:
            return node.id
        return None

    def _literal_eval(self, node: ast.AST) -> Optional[Any]:
        try:
            return ast.literal_eval(node)
        except Exception:
            return None

    def _record_threshold_values(self, name: str, value: Any) -> None:
        if isinstance(value, bool):
            self._ensure_bool_values(name)
            return
        if isinstance(value, int):
            for candidate in (value - 1, value, value + 1):
                self._record_value(name, candidate)
        elif isinstance(value, float):
            for candidate in (value, value + 1.0):
                self._record_value(name, candidate)

    def _handle_comparison(self, name: str, op: ast.cmpop, other: ast.AST) -> None:
        literal = self._literal_eval(other)
        if literal is None and isinstance(other, (ast.List, ast.Tuple, ast.Set)):
            literal = self._literal_eval(other)
        if isinstance(op, (ast.In, ast.NotIn)) and isinstance(
            literal, (list, tuple, set)
        ):
            for item in literal:
                self._record_value(name, item)
            return
        if literal is None:
            return
        if isinstance(op, (ast.Eq, ast.Is, ast.NotEq, ast.IsNot)):
            self._record_value(name, literal)
        elif isinstance(op, (ast.Gt, ast.GtE, ast.Lt, ast.LtE)):
            self._record_threshold_values(name, literal)

    def _reverse_compare_op(self, op: ast.cmpop) -> ast.cmpop:
        mapping = {
            ast.Gt: ast.Lt,
            ast.GtE: ast.LtE,
            ast.Lt: ast.Gt,
            ast.LtE: ast.GtE,
        }
        for original, reversed_cls in mapping.items():
            if isinstance(op, original):
                return reversed_cls()
        return op

    def _analyze_compare(self, node: ast.Compare) -> None:
        left = node.left
        for op, comparator in zip(node.ops, node.comparators):
            left_name = self._extract_param_name(left)
            right_name = self._extract_param_name(comparator)
            if left_name:
                self.used_params.add(left_name)
                self._handle_comparison(left_name, op, comparator)
            elif right_name:
                reversed_op = self._reverse_compare_op(op)
                self.used_params.add(right_name)
                self._handle_comparison(right_name, reversed_op, left)
            left = comparator

    def _analyze_condition(self, expr: ast.AST) -> None:
        if isinstance(expr, ast.Name):
            name = self._extract_param_name(expr)
            if name:
                self._ensure_bool_values(name)
            return
        if isinstance(expr, ast.UnaryOp) and isinstance(expr.op, ast.Not):
            operand = expr.operand
            if isinstance(operand, ast.Name):
                name = self._extract_param_name(operand)
                if name:
                    self._ensure_bool_values(name)
            else:
                self._analyze_condition(expr.operand)
            return
        if isinstance(expr, ast.BoolOp):
            for value in expr.values:
                self._analyze_condition(value)
            return
        if isinstance(expr, ast.Compare):
            self._analyze_compare(expr)
            return
        self.visit(expr)

    def visit_Name(self, node: ast.Name) -> None:
        if node.id in self.param_names:
            self.used_params.add(node.id)
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        base = node.value
        if isinstance(base, ast.Name) and base.id in self.param_names:
            self.used_params.add(base.id)
            attr = node.attr
            if attr in {
                "items",
                "keys",
                "values",
                "get",
                "update",
                "pop",
                "setdefault",
            }:
                self._record_dict_hint(base.id)
            elif attr in {"append", "extend", "insert", "pop", "remove", "clear"}:
                self._record_list_hint(base.id)
        self.generic_visit(node)

    def visit_Subscript(self, node: ast.Subscript) -> None:
        base = node.value
        if isinstance(base, ast.Name) and base.id in self.param_names:
            self.used_params.add(base.id)
            self._record_dict_hint(base.id)
        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:
        self._analyze_condition(node.test)
        for stmt in node.body:
            self.visit(stmt)
        for stmt in node.orelse:
            self.visit(stmt)

    def visit_While(self, node: ast.While) -> None:
        self._analyze_condition(node.test)
        for stmt in node.body:
            self.visit(stmt)
        for stmt in node.orelse:
            self.visit(stmt)


def _collect_parameter_usage(
    func_def: ast.AST, params: List[ParameterInfo]
) -> Tuple[Dict[str, List[Any]], Set[str]]:
    param_map = {p.name: p for p in params if p.name not in {"self", "cls"}}
    visitor = _ParamUsageVisitor(param_map)
    visitor.visit(func_def)
    usage_values = dict(visitor.literal_hints)
    used = visitor.used_params
    optional_unused = {
        p.name
        for p in params
        if p.name in param_map and p.default is not None and p.name not in used
    }
    return usage_values, optional_unused


def _collect_module_param_values(
    functions: List[FunctionInfo],
    sample_calls: Dict[str, List[Dict[str, Any]]],
    call_map: Dict[str, List[Dict[str, Any]]],
) -> Dict[str, List[Any]]:
    hints: Dict[str, List[Any]] = defaultdict(list)

    def _add_value(name: str, value: Any) -> None:
        if name is None:
            return
        bucket = hints[name]
        if value not in bucket:
            bucket.append(value)

    for func in functions:
        for call in call_map.get(func.qualname, []):
            for pname, value in call.items():
                _add_value(pname, value)

        for sample in sample_calls.get(func.qualname, []):
            for pname, value in sample.items():
                _add_value(pname, value)

        for param in func.parameters:
            if param.default_value is not None:
                _add_value(param.name, param.default_value)

    return hints


def _collect_parameters(args: ast.arguments) -> List[ParameterInfo]:
    params: List[ParameterInfo] = []

    # Positional-only args (Python 3.8+)
    posonly = getattr(args, "posonlyargs", [])
    for i, arg in enumerate(posonly):
        default_node = None
        if args.defaults:
            # defaults apply to last N positional args (posonly + normal)
            total_pos = len(posonly) + len(args.args)
            offset = total_pos - len(args.defaults)
            idx = i
            if idx >= offset:
                default_node = args.defaults[idx - offset]
        params.append(
            ParameterInfo(
                name=arg.arg,
                kind="positional_only",
                annotation=_annotation_to_str(arg.annotation),
                default=_expr_to_str(default_node),
                default_value=_literal_eval_node(default_node),
            )
        )

    # Regular positional-or-keyword args
    total_pos = len(posonly) + len(args.args)
    for i, arg in enumerate(args.args):
        default_node = None
        if args.defaults:
            offset = total_pos - len(args.defaults)
            idx = len(posonly) + i
            if idx >= offset:
                default_node = args.defaults[idx - offset]
        params.append(
            ParameterInfo(
                name=arg.arg,
                kind="positional_or_keyword",
                annotation=_annotation_to_str(arg.annotation),
                default=_expr_to_str(default_node),
                default_value=_literal_eval_node(default_node),
            )
        )

    # *args
    if args.vararg is not None:
        params.append(
            ParameterInfo(
                name=args.vararg.arg,
                kind="var_positional",
                annotation=_annotation_to_str(args.vararg.annotation),
                default=None,
            )
        )

    # keyword-only args
    for arg, default_node in zip(args.kwonlyargs, args.kw_defaults):
        params.append(
            ParameterInfo(
                name=arg.arg,
                kind="keyword_only",
                annotation=_annotation_to_str(arg.annotation),
                default=_expr_to_str(default_node),
                default_value=_literal_eval_node(default_node),
            )
        )

    # **kwargs
    if args.kwarg is not None:
        params.append(
            ParameterInfo(
                name=args.kwarg.arg,
                kind="var_keyword",
                annotation=_annotation_to_str(args.kwarg.annotation),
                default=None,
            )
        )

    return params


def _module_name_from_path(root: str, filepath: str) -> str:
    rel = os.path.relpath(filepath, root)
    rel_no_ext = os.path.splitext(rel)[0]
    parts = rel_no_ext.split(os.sep)
    module = ".".join(parts)
    if module.endswith(".__init__"):
        module = module[: -len(".__init__")]
    return module or "__main__"


def scan_python_functions(root: str) -> List[FunctionInfo]:
    """
    Recursively scan a folder for Python functions (including methods in classes).

    Returns a list of FunctionInfo objects with module name, qualified name,
    source file path, parameters, return annotation, and docstring.
    """
    results: List[FunctionInfo] = []

    ignored_dirs = {
        ".ipynb_checkpoints",
        ".git",
        ".venv",
        ".uv-cache",
        "__pycache__",
        "tests",
        "testdata_tests",
        "testdata_tests_repro",
        "node_modules",
        "site-packages",
        "dist",
        "build",
    }

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d
            for d in dirnames
            if d not in ignored_dirs and not d.endswith("-checkpoint")
        ]
        for filename in filenames:
            if not filename.endswith(".py"):
                continue
            if filename.endswith("-checkpoint.py"):
                continue

            filepath = os.path.join(dirpath, filename)

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    source = f.read()
            except (OSError, UnicodeDecodeError):
                continue

            try:
                tree = ast.parse(source, filename=filepath)
            except SyntaxError:
                # In normal circumstances, if importing works under this Python
                # version, ast.parse should also work; this guards against
                # mismatched versions, partial files, or similar issues.
                continue

            module_name = _module_name_from_path(root, filepath)
            module_globals = _extract_module_globals(tree)
            start_idx = len(results)

            class QualnameVisitor(ast.NodeVisitor):
                def __init__(self) -> None:
                    self.class_stack: List[str] = []
                    self.function_depth: int = 0

                def visit_ClassDef(self, node: ast.ClassDef) -> None:
                    # If we are inside a function, this is a local class. Skip it.
                    if self.function_depth > 0:
                        self.generic_visit(node)
                        return

                    self.class_stack.append(node.name)
                    self.generic_visit(node)
                    self.class_stack.pop()

                def _handle_function(self, node: ast.AST) -> None:
                    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        return

                    # If we are already inside a function, this is a nested function. Skip collecting it.
                    # But we still need to visit it to find nested classes/functions (though we skip those too).
                    if self.function_depth > 0:
                        return

                    if self.class_stack:
                        qualname = ".".join(self.class_stack + [node.name])
                    else:
                        qualname = node.name

                    func_def = node  # type: ignore[assignment]
                    params = _collect_parameters(func_def.args)  # type: ignore[arg-type]
                    returns = _annotation_to_str(func_def.returns)  # type: ignore[arg-type]
                    docstring = ast.get_docstring(node)

                    crud_role, crud_resource = _detect_crud_role_and_resource(qualname)
                    usage_values, unused_optional = _collect_parameter_usage(
                        func_def, params
                    )

                    results.append(
                        FunctionInfo(
                            module=module_name,
                            qualname=qualname,
                            filepath=filepath,
                            lineno=node.lineno,
                            parameters=params,
                            returns=returns,
                            docstring=docstring,
                            module_globals=module_globals,
                            crud_role=crud_role,
                            crud_resource=crud_resource,
                            parameter_usage_values=usage_values,
                            unused_parameters=unused_optional,
                        )
                    )

                def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
                    self._handle_function(node)
                    self.function_depth += 1
                    self.generic_visit(node)
                    self.function_depth -= 1

                def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
                    self._handle_function(node)
                    self.function_depth += 1
                    self.generic_visit(node)
                    self.function_depth -= 1

            QualnameVisitor().visit(tree)

            module_functions = results[start_idx:]
            sample_call_map = _extract_sample_calls(tree, module_functions)
            internal_call_map = _extract_internal_call_map(tree, module_functions)
            module_param_values = _collect_module_param_values(
                module_functions, sample_call_map, internal_call_map
            )

            for func in module_functions:
                func.module_functions = module_functions
            for func in module_functions:
                func.sample_calls = (
                    sample_call_map.get(func.qualname, []) if sample_call_map else []
                )
                func.module_param_values = module_param_values
                func.module_call_values = internal_call_map.get(func.qualname, [])

    return results


# In[ ]:


# In[ ]:
