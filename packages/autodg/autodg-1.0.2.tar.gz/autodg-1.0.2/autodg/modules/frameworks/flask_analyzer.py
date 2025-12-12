import ast
from typing import List, Optional
from autodg.modules.core.scanner import FrameworkAnalyzer
from autodg.modules.core.models import RouteInfo
from autodg.modules.core.utils import find_files, parse_ast
from autodg.modules.core.ast_parser import ASTParser

class FlaskAnalyzer(FrameworkAnalyzer):
    def detect(self, project_root: str) -> bool:
        files = find_files(project_root)
        for file in files:
            content = parse_ast(file)
            if not content:
                continue
            for node in ast.walk(content):
                if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        if "flask" in alias.name.lower():
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
                # Handle @app.route('/path') or @bp.route('/path')
                if isinstance(decorator.func, ast.Attribute) and decorator.func.attr == 'route':
                    if decorator.args:
                        path = decorator.args[0].value if isinstance(decorator.args[0], ast.Constant) else "unknown"
                        methods = ["GET"] # Default
                        
                        # Extract methods from keywords
                        for keyword in decorator.keywords:
                            if keyword.arg == 'methods' and isinstance(keyword.value, ast.List):
                                methods = [elt.value for elt in keyword.value.elts if isinstance(elt, ast.Constant)]
                        
                        return RouteInfo(
                            path=self.normalize_path(path),
                            methods=methods,
                            handler_name=node.name,
                            handler_node=node,
                            module=file_path,
                            framework="Flask",
                            line_number=node.lineno,
                            source_code=ASTParser.get_function_source(node, open(file_path).read()),
                            docstring=ASTParser.get_docstring(node),
                            parameters=ASTParser.extract_parameters(node)
                        )
                
                # Handle @app.get('/path'), @app.post('/path') etc.
                elif isinstance(decorator.func, ast.Attribute) and decorator.func.attr in ['get', 'post', 'put', 'delete', 'patch']:
                     if decorator.args:
                        path = decorator.args[0].value if isinstance(decorator.args[0], ast.Constant) else "unknown"
                        method = decorator.func.attr.upper()
                        return RouteInfo(
                            path=self.normalize_path(path),
                            methods=[method],
                            handler_name=node.name,
                            handler_node=node,
                            module=file_path,
                            framework="Flask",
                            line_number=node.lineno,
                            source_code=ASTParser.get_function_source(node, open(file_path).read()),
                            docstring=ASTParser.get_docstring(node),
                            parameters=ASTParser.extract_parameters(node)
                        )
        return None
