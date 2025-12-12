import ast
from typing import List, Optional
from modules.core.scanner import FrameworkAnalyzer
from modules.core.models import RouteInfo
from modules.core.utils import find_files, parse_ast
from modules.core.ast_parser import ASTParser

class DRFAnalyzer(FrameworkAnalyzer):
    def detect(self, project_root: str) -> bool:
        files = find_files(project_root)
        for file in files:
            content = parse_ast(file)
            if not content:
                continue
            for node in ast.walk(content):
                if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        if "rest_framework" in alias.name.lower():
                            return True
        return False

    def extract_routes(self, project_root: str) -> List[RouteInfo]:
        routes = []
        files = find_files(project_root)
        for file_path in files:
            tree = parse_ast(file_path)
            if not tree:
                continue
            
            for node in ast.walk(tree):
                # Detect Router registration
                # router.register(r'users', UserViewSet)
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Attribute) and node.func.attr == 'register':
                        if len(node.args) >= 2:
                            prefix = node.args[0].value if isinstance(node.args[0], ast.Constant) else "unknown"
                            viewset_name = node.args[1].id if isinstance(node.args[1], ast.Name) else "unknown"
                            
                            # Expand ViewSet routes
                            routes.extend(self._expand_viewset(prefix, viewset_name, file_path, node))
        return routes

    def _expand_viewset(self, prefix: str, viewset_name: str, file_path: str, node: ast.AST) -> List[RouteInfo]:
        expanded = []
        base_path = self.normalize_path(prefix)
        
        # Standard DRF ViewSet actions
        actions = [
            ("list", "GET", "/"),
            ("create", "POST", "/"),
            ("retrieve", "GET", "/<pk>/"),
            ("update", "PUT", "/<pk>/"),
            ("partial_update", "PATCH", "/<pk>/"),
            ("destroy", "DELETE", "/<pk>/")
        ]
        
        for action, method, suffix in actions:
            expanded.append(RouteInfo(
                path=base_path + suffix if suffix != "/" else base_path,
                methods=[method],
                handler_name=f"{viewset_name}.{action}",
                handler_node=node,
                module=file_path,
                framework="DRF",
                line_number=node.lineno,
                source_code=f"Router registration for {viewset_name}",
                docstring="",
                extra_meta={"viewset": viewset_name, "action": action}
            ))
        return expanded
