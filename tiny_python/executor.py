import ast
import operator
from dataclasses import fields, is_dataclass
from typing import Any, Dict, List, Optional, Type

from .parser import TinyPythonParser


class ExecutionError(Exception):
    pass


class Executor:
    def __init__(
        self,
        max_iterations: int = 10000,
        max_recursion_depth: int = 100,
        allowed_classes: Optional[List[Type]] = None,
        global_vars: Optional[Dict[str, Any]] = None,
        allow_dataclass_methods: bool = False,
    ):
        self.max_iterations = max_iterations
        self.max_recursion_depth = max_recursion_depth
        self.allowed_classes = allowed_classes or []
        self.global_vars = global_vars or {}
        self.allow_dataclass_methods = allow_dataclass_methods
        self.parser = TinyPythonParser(
            allowed_classes=allowed_classes,
            allow_dataclass_methods=allow_dataclass_methods
        )
        self.iteration_count = 0
        self.recursion_depth = 0
        self.local_scopes = [{}]

        self.binary_ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.FloorDiv: operator.floordiv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow,
        }

        self.compare_ops = {
            ast.Eq: operator.eq,
            ast.NotEq: operator.ne,
            ast.Lt: operator.lt,
            ast.LtE: operator.le,
            ast.Gt: operator.gt,
            ast.GtE: operator.ge,
            ast.Is: operator.is_,
            ast.IsNot: operator.is_not,
            ast.In: lambda x, y: x in y,
            ast.NotIn: lambda x, y: x not in y,
        }

        self.bool_ops = {
            ast.And: lambda values: all(values),
            ast.Or: lambda values: any(values),
        }

        self.unary_ops = {
            ast.UAdd: operator.pos,
            ast.USub: operator.neg,
            ast.Not: operator.not_,
        }

        self.builtin_functions = {
            "len": len,
            "range": range,
            "int": int,
            "float": float,
            "str": str,
            "bool": bool,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "abs": abs,
            "min": min,
            "max": max,
            "sum": sum,
            "round": round,
            "sorted": sorted,
            "reversed": lambda x: list(reversed(x)),
            "enumerate": enumerate,
            "zip": zip,
            "all": all,
            "any": any,
            "isinstance": isinstance,
            "type": type,
        }

    def execute(self, code: str) -> Any:
        self.iteration_count = 0
        self.recursion_depth = 0
        self.local_scopes = [{}]

        tree = self.parser.parse(code)
        result = None
        for node in tree.body:
            result = self._execute_node(node)
            if isinstance(result, ReturnValue):
                return result.value
        return result

    def _check_limits(self):
        self.iteration_count += 1
        if self.iteration_count > self.max_iterations:
            raise ExecutionError(f"Exceeded maximum iterations ({self.max_iterations})")
        if self.recursion_depth > self.max_recursion_depth:
            raise ExecutionError(f"Exceeded maximum recursion depth ({self.max_recursion_depth})")

    def _execute_node(self, node: ast.AST) -> Any:
        self._check_limits()

        if isinstance(node, ast.Expr):
            return self._execute_node(node.value)
        elif isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Name):
            return self._handle_name(node)
        elif isinstance(node, ast.BinOp):
            return self._handle_binop(node)
        elif isinstance(node, ast.UnaryOp):
            return self._handle_unaryop(node)
        elif isinstance(node, ast.Compare):
            return self._handle_compare(node)
        elif isinstance(node, ast.BoolOp):
            return self._handle_boolop(node)
        elif isinstance(node, ast.Assign):
            return self._handle_assign(node)
        elif isinstance(node, ast.AugAssign):
            return self._handle_augassign(node)
        elif isinstance(node, ast.If):
            return self._handle_if(node)
        elif isinstance(node, ast.For):
            return self._handle_for(node)
        elif isinstance(node, ast.While):
            return self._handle_while(node)
        elif isinstance(node, ast.Call):
            return self._handle_call(node)
        elif isinstance(node, ast.List):
            return [self._execute_node(elt) for elt in node.elts]
        elif isinstance(node, ast.Dict):
            return {
                self._execute_node(k): self._execute_node(v) for k, v in zip(node.keys, node.values)
            }
        elif isinstance(node, ast.Tuple):
            return tuple(self._execute_node(elt) for elt in node.elts)
        elif isinstance(node, ast.Subscript):
            return self._handle_subscript(node)
        elif isinstance(node, ast.Slice):
            return slice(
                self._execute_node(node.lower) if node.lower else None,
                self._execute_node(node.upper) if node.upper else None,
                self._execute_node(node.step) if node.step else None,
            )
        elif isinstance(node, ast.Attribute):
            return self._handle_attribute(node)
        elif isinstance(node, ast.Return):
            return ReturnValue(self._execute_node(node.value) if node.value else None)
        elif isinstance(node, ast.Break):
            return BreakLoop()
        elif isinstance(node, ast.Continue):
            return ContinueLoop()
        elif isinstance(node, ast.Pass):
            return None
        else:
            raise ExecutionError(f"Unsupported node type: {type(node).__name__}")

    def _handle_name(self, node: ast.Name):
        if isinstance(node.ctx, ast.Load):
            name = node.id
            for scope in reversed(self.local_scopes):
                if name in scope:
                    return scope[name]
            if name in self.global_vars:
                return self.global_vars[name]
            if name in self.builtin_functions:
                return self.builtin_functions[name]
            for cls in self.allowed_classes:
                if cls.__name__ == name:
                    return cls
            raise NameError(f"Name '{name}' is not defined")
        elif isinstance(node.ctx, ast.Store):
            return node.id
        elif isinstance(node.ctx, ast.Del):
            name = node.id
            for scope in reversed(self.local_scopes):
                if name in scope:
                    del scope[name]
                    return
            raise NameError(f"Name '{name}' is not defined")

    def _handle_binop(self, node: ast.BinOp):
        left = self._execute_node(node.left)
        right = self._execute_node(node.right)
        op_func = self.binary_ops.get(type(node.op))
        if op_func:
            return op_func(left, right)
        raise ExecutionError(f"Unsupported binary operator: {type(node.op).__name__}")

    def _handle_unaryop(self, node: ast.UnaryOp):
        operand = self._execute_node(node.operand)
        op_func = self.unary_ops.get(type(node.op))
        if op_func:
            return op_func(operand)
        raise ExecutionError(f"Unsupported unary operator: {type(node.op).__name__}")

    def _handle_compare(self, node: ast.Compare):
        left = self._execute_node(node.left)
        for op, comparator in zip(node.ops, node.comparators):
            right = self._execute_node(comparator)
            op_func = self.compare_ops.get(type(op))
            if not op_func:
                raise ExecutionError(f"Unsupported comparison operator: {type(op).__name__}")
            if not op_func(left, right):
                return False
            left = right
        return True

    def _handle_boolop(self, node: ast.BoolOp):
        values = []
        for value_node in node.values:
            val = self._execute_node(value_node)
            if isinstance(node.op, ast.And) and not val:
                return False
            elif isinstance(node.op, ast.Or) and val:
                return True
            values.append(val)

        op_func = self.bool_ops.get(type(node.op))
        if op_func:
            return op_func(values)
        raise ExecutionError(f"Unsupported boolean operator: {type(node.op).__name__}")

    def _handle_assign(self, node: ast.Assign):
        value = self._execute_node(node.value)
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.local_scopes[-1][target.id] = value
            elif isinstance(target, ast.Subscript):
                obj = self._execute_node(target.value)
                key = self._execute_node(target.slice)
                obj[key] = value
            elif isinstance(target, ast.Attribute):
                obj = self._execute_node(target.value)
                setattr(obj, target.attr, value)
            elif isinstance(target, (ast.Tuple, ast.List)):
                if not isinstance(value, (tuple, list)):
                    raise TypeError("Cannot unpack non-sequence")
                if len(target.elts) != len(value):
                    raise ValueError(
                        f"Cannot unpack {len(value)} values to {len(target.elts)} targets"
                    )
                for t, v in zip(target.elts, value):
                    if isinstance(t, ast.Name):
                        self.local_scopes[-1][t.id] = v
                    else:
                        raise ExecutionError("Complex unpacking not supported")
        return value

    def _handle_augassign(self, node: ast.AugAssign):
        target = node.target
        if isinstance(target, ast.Name):
            # For augmented assignment, we need to load the current value first
            # even though the target has Store context
            name = target.id

            # Find the current value
            current = None
            for scope in reversed(self.local_scopes):
                if name in scope:
                    current = scope[name]
                    break
            else:
                if name in self.global_vars:
                    current = self.global_vars[name]
                else:
                    raise NameError(f"Name '{name}' is not defined")

            op_func = self.binary_ops.get(type(node.op))
            if not op_func:
                raise ExecutionError(
                    f"Unsupported augmented assignment operator: {type(node.op).__name__}"
                )
            new_value = op_func(current, self._execute_node(node.value))
            self.local_scopes[-1][name] = new_value
            return new_value
        else:
            raise ExecutionError("Augmented assignment only supported for simple names")

    def _handle_if(self, node: ast.If):
        if self._execute_node(node.test):
            for stmt in node.body:
                result = self._execute_node(stmt)
                if isinstance(result, (ReturnValue, BreakLoop, ContinueLoop)):
                    return result
        elif node.orelse:
            for stmt in node.orelse:
                result = self._execute_node(stmt)
                if isinstance(result, (ReturnValue, BreakLoop, ContinueLoop)):
                    return result

    def _handle_for(self, node: ast.For):
        iterable = self._execute_node(node.iter)
        for item in iterable:
            if isinstance(node.target, ast.Name):
                self.local_scopes[-1][node.target.id] = item
            elif isinstance(node.target, (ast.Tuple, ast.List)):
                # Handle tuple unpacking in for loops
                if not isinstance(item, (tuple, list)):
                    raise TypeError("Cannot unpack non-sequence in for loop")
                if len(node.target.elts) != len(item):
                    raise ValueError(f"Too many values to unpack (expected {len(node.target.elts)})")
                for t, v in zip(node.target.elts, item):
                    if isinstance(t, ast.Name):
                        self.local_scopes[-1][t.id] = v
                    else:
                        raise ExecutionError("Complex unpacking in for loop not supported")
            else:
                raise ExecutionError("Complex for loop targets not supported")

            for stmt in node.body:
                result = self._execute_node(stmt)
                if isinstance(result, ReturnValue):
                    return result
                elif isinstance(result, BreakLoop):
                    return None
                elif isinstance(result, ContinueLoop):
                    break
        else:
            if node.orelse:
                for stmt in node.orelse:
                    result = self._execute_node(stmt)
                    if isinstance(result, (ReturnValue, BreakLoop, ContinueLoop)):
                        return result

    def _handle_while(self, node: ast.While):
        while self._execute_node(node.test):
            for stmt in node.body:
                result = self._execute_node(stmt)
                if isinstance(result, ReturnValue):
                    return result
                elif isinstance(result, BreakLoop):
                    return None
                elif isinstance(result, ContinueLoop):
                    break
        else:
            if node.orelse:
                for stmt in node.orelse:
                    result = self._execute_node(stmt)
                    if isinstance(result, (ReturnValue, BreakLoop, ContinueLoop)):
                        return result

    def _handle_call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            func_name = node.func.id

            if func_name in self.builtin_functions:
                func = self.builtin_functions[func_name]
                args = [self._execute_node(arg) for arg in node.args]
                kwargs = {kw.arg: self._execute_node(kw.value) for kw in node.keywords}
                return func(*args, **kwargs)

            for cls in self.allowed_classes:
                if cls.__name__ == func_name:
                    return self._instantiate_class(cls, node)

            func = self._handle_name(node.func)
            if callable(func):
                args = [self._execute_node(arg) for arg in node.args]
                kwargs = {kw.arg: self._execute_node(kw.value) for kw in node.keywords}
                return func(*args, **kwargs)

            raise ExecutionError(f"'{func_name}' is not callable")
        elif isinstance(node.func, ast.Attribute):
            obj = self._execute_node(node.func.value)
            method_name = node.func.attr

            # If dataclass methods are enabled, validate the method is safe
            if self.allow_dataclass_methods:
                # Check if obj is an instance of an allowed dataclass
                obj_class = type(obj)
                is_allowed_instance = False
                for allowed_cls in self.allowed_classes:
                    if isinstance(obj, allowed_cls) and is_dataclass(allowed_cls):
                        is_allowed_instance = True
                        # Verify the method is defined on the class, not acquired elsewhere
                        if not hasattr(allowed_cls, method_name):
                            raise ExecutionError(
                                f"Method '{method_name}' is not defined on dataclass '{allowed_cls.__name__}'"
                            )
                        # Ensure it's not a private method
                        if method_name.startswith('_'):
                            raise ExecutionError(
                                f"Cannot call private method '{method_name}'"
                            )
                        break

                # If it's not a dataclass instance, fall through to normal attribute access
                if not is_allowed_instance:
                    # Still need to handle built-in types like strings, lists, etc.
                    pass

            method = getattr(obj, method_name)
            args = [self._execute_node(arg) for arg in node.args]
            kwargs = {kw.arg: self._execute_node(kw.value) for kw in node.keywords}
            return method(*args, **kwargs)
        else:
            raise ExecutionError("Complex function calls not supported")

    def _instantiate_class(self, cls: Type, node: ast.Call) -> Any:
        if not is_dataclass(cls):
            raise ExecutionError(f"Class '{cls.__name__}' is not a dataclass")

        args = [self._execute_node(arg) for arg in node.args]
        kwargs = {kw.arg: self._execute_node(kw.value) for kw in node.keywords}

        field_names = [f.name for f in fields(cls)]

        if args:
            for i, arg in enumerate(args):
                if i < len(field_names):
                    kwargs[field_names[i]] = arg

        return cls(**kwargs)

    def _handle_subscript(self, node: ast.Subscript):
        obj = self._execute_node(node.value)
        if isinstance(node.slice, ast.Slice):
            slice_obj = self._execute_node(node.slice)
            return obj[slice_obj]
        else:
            key = self._execute_node(node.slice)
            return obj[key]

    def _handle_attribute(self, node: ast.Attribute):
        obj = self._execute_node(node.value)
        return getattr(obj, node.attr)


class ReturnValue:
    def __init__(self, value):
        self.value = value


class BreakLoop:
    pass


class ContinueLoop:
    pass


def safe_exec(
    code: str,
    max_iterations: int = 10000,
    max_recursion_depth: int = 100,
    allowed_classes: Optional[List[Type]] = None,
    global_vars: Optional[Dict[str, Any]] = None,
    allow_dataclass_methods: bool = False,
) -> Any:
    executor = Executor(
        max_iterations=max_iterations,
        max_recursion_depth=max_recursion_depth,
        allowed_classes=allowed_classes,
        global_vars=global_vars,
        allow_dataclass_methods=allow_dataclass_methods,
    )
    return executor.execute(code)
