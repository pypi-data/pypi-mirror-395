import ast
from typing import List, Optional
from autodg.modules.core.scanner import FrameworkAnalyzer
from autodg.modules.core.models import RouteInfo
from autodg.modules.core.utils import find_files, parse_ast
from autodg.modules.core.ast_parser import ASTParser

class FastAPIAnalyzer(FrameworkAnalyzer):
    def detect(self, project_root: str) -> bool:
        files = find_files(project_root)
        for file in files:
            content = parse_ast(file)
            if not content:
                continue
            for node in ast.walk(content):
                if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        if "fastapi" in alias.name.lower():
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
                if isinstance(node, ast.FunctionDef):
                    route = self._process_function(node, file_path)
                    if route:
                        routes.append(route)
        return routes

    def _process_function(self, node: ast.FunctionDef, file_path: str) -> Optional[RouteInfo]:
        decorators = node.decorator_list
        for decorator in decorators:
            if isinstance(decorator, ast.Call):
                # Handle @app.get('/path'), @router.post('/path') etc.
                if isinstance(decorator.func, ast.Attribute) and decorator.func.attr in ['get', 'post', 'put', 'delete', 'patch', 'options', 'head', 'trace']:
                     if decorator.args:
                        path = decorator.args[0].value if isinstance(decorator.args[0], ast.Constant) else "unknown"
                        method = decorator.func.attr.upper()
                        
                        # Extract extra metadata like tags, summary, response_model
                        extra_meta = {}
                        for keyword in decorator.keywords:
                            if keyword.arg in ['tags', 'summary', 'response_model']:
                                # Simplified extraction, can be expanded
                                extra_meta[keyword.arg] = "extracted" 

                        return RouteInfo(
                            path=self.normalize_path(path),
                            methods=[method],
                            handler_name=node.name,
                            handler_node=node,
                            module=file_path,
                            framework="FastAPI",
                            line_number=node.lineno,
                            source_code=ASTParser.get_function_source(node, open(file_path).read()),
                            docstring=ASTParser.get_docstring(node),
                            parameters=ASTParser.extract_parameters(node),
                            extra_meta=extra_meta
                        )
        return None
