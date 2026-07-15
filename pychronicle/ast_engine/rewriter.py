"""
rewriter.py

AST Rewriter for PyChronicle.

Transforms Python source code by inserting tracing calls after every
variable assignment. The transformed code can then be executed while
recording the history of variables.

Example

x = 10

becomes

x = 10
__pychronicle_trace__("x", x, 1)

"""

import ast
from typing import Optional


TRACE_FUNCTION = "__pychronicle_trace__"


class AssignmentRewriter(ast.NodeTransformer):
    """
    Inserts tracing calls after assignments.
    """

    def visit_Assign(self, node: ast.Assign):
        self.generic_visit(node)

        new_nodes = [node]

        for target in node.targets:
            new_nodes.extend(self._create_trace_nodes(target, node.lineno))

        return new_nodes

    def visit_AnnAssign(self, node: ast.AnnAssign):
        self.generic_visit(node)

        new_nodes = [node]
        new_nodes.extend(
            self._create_trace_nodes(node.target, node.lineno)
        )

        return new_nodes

    def visit_AugAssign(self, node: ast.AugAssign):
        self.generic_visit(node)

        new_nodes = [node]
        new_nodes.extend(
            self._create_trace_nodes(node.target, node.lineno)
        )

        return new_nodes

    def _create_trace_nodes(self, target, lineno):
        """
        Creates trace function calls for each assigned variable.
        """

        nodes = []

        if isinstance(target, ast.Name):

            trace_call = ast.Expr(
                value=ast.Call(
                    func=ast.Name(
                        id=TRACE_FUNCTION,
                        ctx=ast.Load(),
                    ),
                    args=[
                        ast.Constant(target.id),
                        ast.Name(
                            id=target.id,
                            ctx=ast.Load(),
                        ),
                        ast.Constant(lineno),
                    ],
                    keywords=[],
                )
            )

            nodes.append(trace_call)

        elif isinstance(target, (ast.Tuple, ast.List)):

            for element in target.elts:
                nodes.extend(
                    self._create_trace_nodes(
                        element,
                        lineno,
                    )
                )

        return nodes


def rewrite_source(source: str) -> str:
    """
    Rewrite Python source code by inserting trace calls.
    """

    tree = ast.parse(source)

    transformer = AssignmentRewriter()

    tree = transformer.visit(tree)

    ast.fix_missing_locations(tree)

    return ast.unparse(tree)


def rewrite_file(input_file: str,
                 output_file: Optional[str] = None):
    """
    Rewrite a Python file.

    If output_file is None,
    overwrite the original file.
    """

    with open(input_file, "r", encoding="utf-8") as f:
        source = f.read()

    rewritten = rewrite_source(source)

    if output_file is None:
        output_file = input_file

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(rewritten)


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(
        description="Rewrite Python source for tracing."
    )

    parser.add_argument(
        "input",
        help="Input Python file",
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output file",
    )

    args = parser.parse_args()

    rewrite_file(
        args.input,
        args.output,
    )

    print("Source successfully rewritten.")