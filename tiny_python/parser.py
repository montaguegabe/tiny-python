import ast
from dataclasses import dataclass
from typing import Any, List, Optional

from .constants import ALLOWED_BUILTINS, ALLOWED_METHODS


@dataclass
class ParsedNode:
    type: str
    value: Any = None
    children: List["ParsedNode"] = None

    def __post_init__(self):
        if self.children is None:
            self.children = []


class TinyPythonParser:
    def __init__(
        self,
        allowed_classes=None,
        global_vars=None,
        allowed_functions=None,
    ):
        self.allowed_classes = allowed_classes or []
        self.global_vars = global_vars or {}
        self.allowed_functions = allowed_functions or []
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
            if node.func.id not in ALLOWED_BUILTINS:
                # Allow global functions if flag is set
                if node.func.id in self.global_vars:
                    # Check that the global var is callable
                    if callable(self.global_vars[node.func.id]):
                        return  # Allow this function call
                # Check if function is in allowed_functions list
                # We check by name since we don't have the actual function object here
                for func in self.allowed_functions:
                    if hasattr(func, "__name__") and func.__name__ == node.func.id:
                        return  # Allow this function call
                # Allow uppercase names (class constructors)
                if not node.func.id[0].isupper():
                    raise ValueError(f"Function call not allowed: {node.func.id}")
        elif isinstance(node.func, ast.Attribute):
            # Check if this is an allowed method call
            # We'll validate at runtime what type the object is
            method_name = node.func.attr

            # Check if method is in any of the allowed lists
            is_allowed = False
            for type_name, allowed_methods in ALLOWED_METHODS.items():
                if method_name in allowed_methods:
                    is_allowed = True
                    break

            if not is_allowed:
                raise ValueError(f"Method '{method_name}' is not allowed")

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
