import ast
from typing import Dict, List, Any, Set

class CallGraphBuilder(ast.NodeVisitor):
    def __init__(self):
        self.calls = []
        self.current_function = None

    def visit_FunctionDef(self, node):
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = None

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.calls.append(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            self.calls.append(node.func.attr)
        self.generic_visit(node)

    @staticmethod
    def build_graph(node: ast.AST) -> List[str]:
        """
        Build a flat list of called functions/methods from an AST node.
        """
        builder = CallGraphBuilder()
        builder.visit(node)
        return list(set(builder.calls)) # Return unique calls
