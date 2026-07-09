"""
AST Parsing Engine for PyChronicle.

Reads a target Python file, parses its Abstract Syntax Tree, and
identifies every variable assignment in it: simple assignments,
annotated assignments, augmented assignments (+=, -=, ...), and
tuple/list unpacking.
"""

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Union


@dataclass
class VariableAssignment:
    """A single variable assignment found in the source file."""
    name: str
    line_number: int
    col_offset: int
    value_expr: str            # source text of the right-hand side
    annotation: Optional[str] = None
    scope: str = "module"      # "module", or the enclosing function/class name
    is_augmented: bool = False


class AssignmentVisitor(ast.NodeVisitor):
    """Walks an AST tree and collects every variable assignment."""

    def __init__(self):
        self.assignments: List[VariableAssignment] = []
        self._scope_stack: List[str] = ["module"]

    # ---- scope tracking -------------------------------------------------
    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._scope_stack.append(node.name)
        self.generic_visit(node)
        self._scope_stack.pop()

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node: ast.ClassDef):
        self._scope_stack.append(node.name)
        self.generic_visit(node)
        self._scope_stack.pop()

    # ---- assignment handling ---------------------------------------------
    def visit_Assign(self, node: ast.Assign):
        value_expr = self._unparse(node.value)
        for target in node.targets:
            self._record_target(target, node.lineno, node.col_offset, value_expr)
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign):
        value_expr = self._unparse(node.value) if node.value else ""
        annotation = self._unparse(node.annotation)
        self._record_target(node.target, node.lineno, node.col_offset,
                             value_expr, annotation=annotation)
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign):
        value_expr = self._unparse(node.value)
        self._record_target(node.target, node.lineno, node.col_offset,
                             value_expr, is_augmented=True)
        self.generic_visit(node)

    # ---- helpers ----------------------------------------------------------
    def _record_target(self, target, lineno, col_offset, value_expr,
                        annotation=None, is_augmented=False):
        if isinstance(target, ast.Name):
            name = target.id
        elif isinstance(target, (ast.Attribute, ast.Subscript)):
            name = self._unparse(target)
        elif isinstance(target, (ast.Tuple, ast.List)):
            for elt in target.elts:
                self._record_target(elt, lineno, col_offset, value_expr,
                                     is_augmented=is_augmented)
            return
        else:
            return

        self.assignments.append(VariableAssignment(
            name=name,
            line_number=lineno,
            col_offset=col_offset,
            value_expr=value_expr,
            annotation=annotation,
            scope=self._scope_stack[-1],
            is_augmented=is_augmented,
        ))

    @staticmethod
    def _unparse(node) -> str:
        if node is None:
            return ""
        try:
            return ast.unparse(node)
        except Exception:
            return "<unparsable>"


def parse_file(path: Union[str, Path]) -> List[VariableAssignment]:
    """Parse the Python file at `path` and return all assignments found."""
    path = Path(path)
    source = path.read_text(encoding="utf-8")
    return parse_source(source, filename=str(path))


def parse_source(source: str, filename: str = "<string>") -> List[VariableAssignment]:
    """Parse a raw source string and return all assignments found."""
    tree = ast.parse(source, filename=filename)
    visitor = AssignmentVisitor()
    visitor.visit(tree)
    return visitor.assignments


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python parser.py <target_file.py>")
        sys.exit(1)

    for a in parse_file(sys.argv[1]):
        ann = f"  # {a.annotation}" if a.annotation else ""
        op = "+=" if a.is_augmented else "="
        print(f"L{a.line_number:<5} [{a.scope}] {a.name} {op} {a.value_expr}{ann}")