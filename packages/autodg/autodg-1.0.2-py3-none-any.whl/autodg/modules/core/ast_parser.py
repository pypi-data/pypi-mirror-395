import ast
from typing import Optional, List, Dict, Any

class ASTParser:
    """
    Helper class for AST traversal and extraction.
    """

    @staticmethod
    def get_decorators(node: ast.FunctionDef) -> List[str]:
        """
        Extract decorator names from a function definition.
        """
        decorators = []
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name):
                decorators.append(decorator.id)
            elif isinstance(decorator, ast.Call):
                if isinstance(decorator.func, ast.Name):
                    decorators.append(decorator.func.id)
                elif isinstance(decorator.func, ast.Attribute):
                    decorators.append(decorator.func.attr)
        return decorators

    @staticmethod
    def get_docstring(node: ast.AST) -> str:
        """
        Extract docstring from an AST node.
        """
        return ast.get_docstring(node) or ""

    @staticmethod
    def get_function_source(node: ast.FunctionDef, source_code: str) -> str:
        """
        Extract the source code of a function from the file source.
        """
        return ast.get_source_segment(source_code, node) or ""

    @staticmethod
    def extract_parameters(node: ast.FunctionDef) -> List[Dict[str, Any]]:
        """
        Extract parameters from a function definition.
        """
        params = []
        for arg in node.args.args:
            params.append({
                "name": arg.arg,
                "type": ASTParser._get_annotation(arg.annotation)
            })
        return params

    @staticmethod
    def _get_annotation(node: Optional[ast.AST]) -> str:
        if node is None:
            return "Any"
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return node.attr
        return "ComplexType"
