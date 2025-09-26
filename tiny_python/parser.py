import ast
from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class ParsedNode:
    type: str
    value: Any = None
    children: List["ParsedNode"] = None

    def __post_init__(self):
        if self.children is None:
            self.children = []


class TinyPythonParser:
    def __init__(self, allowed_classes=None, allow_dataclass_methods=False,
                 allow_global_functions=False, global_vars=None):
        self.allowed_classes = allowed_classes or []
        self.allow_dataclass_methods = allow_dataclass_methods
        self.allow_global_functions = allow_global_functions
        self.global_vars = global_vars or {}
        self.allowed_node_types = {
            ast.Module,
            ast.Expr,
            ast.Assign,
            ast.AugAssign,
            ast.If,
            ast.For,
            ast.While,
            ast.Compare,
            ast.BoolOp,
            ast.UnaryOp,
            ast.BinOp,
            ast.Call,
            ast.Name,
            ast.Constant,
            ast.List,
            ast.Dict,
            ast.Tuple,
            ast.Subscript,
            ast.Index,
            ast.Slice,
            ast.Attribute,
            ast.keyword,
            ast.Store,
            ast.Load,
            ast.Del,
            ast.Add,
            ast.Sub,
            ast.Mult,
            ast.Div,
            ast.FloorDiv,
            ast.Mod,
            ast.Pow,
            ast.And,
            ast.Or,
            ast.Not,
            ast.Eq,
            ast.NotEq,
            ast.Lt,
            ast.LtE,
            ast.Gt,
            ast.GtE,
            ast.In,
            ast.NotIn,
            ast.Is,
            ast.IsNot,
            ast.USub,
            ast.UAdd,
            ast.Return,
            ast.Break,
            ast.Continue,
            ast.Pass,
        }

    def parse(self, code: str) -> ast.Module:
        try:
            tree = ast.parse(code)
            self._validate_ast(tree)
            return tree
        except SyntaxError as e:
            raise SyntaxError(f"Invalid syntax: {e}")

    def _validate_ast(self, node: ast.AST, parent: Optional[ast.AST] = None):
        if type(node) not in self.allowed_node_types:
            raise ValueError(f"Forbidden node type: {type(node).__name__}")

        if isinstance(node, ast.Call):
            self._validate_call(node)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            self._validate_name_load(node)

        for child in ast.iter_child_nodes(node):
            self._validate_ast(child, node)

    def _validate_call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            allowed_builtins = {
                "len",
                "range",
                "int",
                "float",
                "str",
                "bool",
                "list",
                "dict",
                "tuple",
                "set",
                "abs",
                "min",
                "max",
                "sum",
                "round",
                "sorted",
                "reversed",
                "enumerate",
                "zip",
                "all",
                "any",
                "isinstance",
                "type",
            }
            if node.func.id not in allowed_builtins:
                # Allow global functions if flag is set
                if self.allow_global_functions and node.func.id in self.global_vars:
                    # Check that the global var is callable
                    if callable(self.global_vars[node.func.id]):
                        return  # Allow this function call
                # Allow uppercase names (class constructors)
                if not node.func.id[0].isupper():
                    raise ValueError(f"Function call not allowed: {node.func.id}")
        elif isinstance(node.func, ast.Attribute):
            allowed_methods = {
                "append",
                "extend",
                "insert",
                "remove",
                "pop",
                "clear",
                "index",
                "count",
                "sort",
                "reverse",
                "copy",
                "upper",
                "lower",
                "strip",
                "lstrip",
                "rstrip",
                "split",
                "join",
                "replace",
                "startswith",
                "endswith",
                "find",
                "rfind",
                "format",
                "capitalize",
                "title",
                "isdigit",
                "isalpha",
                "isalnum",
                "isspace",
                "keys",
                "values",
                "items",
                "get",
                "update",
            }
            if node.func.attr not in allowed_methods:
                # If dataclass methods are allowed, permit non-dangerous methods
                if self.allow_dataclass_methods:
                    # Block dangerous methods and private methods
                    dangerous_methods = {
                        "__import__",
                        "__call__",
                        "__getattr__",
                        "__setattr__",
                        "__delattr__",
                        "__getattribute__",
                        "__class__",
                        "__dict__",
                        "__module__",
                        "__code__",
                        "__globals__",
                        "__builtins__",
                        "eval",
                        "exec",
                        "compile",
                    }
                    if node.func.attr in dangerous_methods or node.func.attr.startswith("_"):
                        raise ValueError(f"Method call not allowed: {node.func.attr}")
                    # Otherwise allow the method call - runtime will validate if it's allowed
                else:
                    # Strict mode - only allow explicitly listed methods
                    raise ValueError(f"Method call not allowed: {node.func.attr}")

    def _validate_name_load(self, node: ast.Name):
        forbidden_names = {
            "__import__",
            "eval",
            "exec",
            "compile",
            "open",
            "input",
            "globals",
            "locals",
            "vars",
            "dir",
            "getattr",
            "setattr",
            "delattr",
            "hasattr",
            "__builtins__",
            "__file__",
            "__name__",
        }
        if node.id in forbidden_names:
            raise ValueError(f"Access to '{node.id}' is forbidden")
