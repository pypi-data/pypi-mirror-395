import ast
from typing import List

class DBDetector(ast.NodeVisitor):
    def __init__(self):
        self.db_operations = []
        # Common ORM methods
        self.orm_methods = {
            'objects', 'query', 'session', 'execute', 'commit', 'rollback',
            'filter', 'get', 'create', 'update', 'delete', 'save',
            'select', 'insert', 'update', 'delete' # SQLAlchemy core
        }

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            if node.func.attr in self.orm_methods:
                self.db_operations.append(node.func.attr)
        self.generic_visit(node)

    @staticmethod
    def detect(node: ast.AST) -> List[str]:
        """
        Detect potential database operations in an AST node.
        """
        detector = DBDetector()
        detector.visit(node)
        return list(set(detector.db_operations))
