import ast
from typing import List, Optional, Any
from modules.core.scanner import FrameworkAnalyzer
from modules.core.models import RouteInfo
from modules.core.utils import find_files, parse_ast
from modules.core.ast_parser import ASTParser

class DjangoAnalyzer(FrameworkAnalyzer):
    def detect(self, project_root: str) -> bool:
        files = find_files(project_root)
        for file in files:
            content = parse_ast(file)
            if not content:
                continue
            for node in ast.walk(content):
                if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        if "django" in alias.name.lower():
                            return True
        return False

    def extract_routes(self, project_root: str) -> List[RouteInfo]:
        routes = []
        files = find_files(project_root)
        for file_path in files:
            # Look for urls.py files or files defining urlpatterns
            if "urls.py" in file_path:
                try:
                    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                        source_code = f.read()
                    tree = ast.parse(source_code, filename=file_path)
                except Exception as e:
                    print(f"Error parsing {file_path}: {e}")
                    continue
                
                # Find urlpatterns assignment
                for node in ast.walk(tree):
                    if isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name) and target.id == 'urlpatterns':
                                routes.extend(self._process_urlpatterns(node.value, file_path, "", source_code))
        return routes

    def _process_urlpatterns(self, node: ast.AST, file_path: str, prefix: str, source_code: str) -> List[RouteInfo]:
        routes = []
        if isinstance(node, ast.List):
            for item in node.elts:
                if isinstance(item, ast.Call):
                    # Handle path('route', view, name='name') or re_path(...)
                    func_name = ""
                    if isinstance(item.func, ast.Name):
                        func_name = item.func.id
                    
                    if func_name in ['path', 're_path']:
                        if item.args:
                            route_part = item.args[0].value if isinstance(item.args[0], ast.Constant) else ""
                            full_path = self.normalize_path(prefix + route_part)
                            
                            view_arg = item.args[1]
                            
                            # Check if it's an include()
                            if isinstance(view_arg, ast.Call) and isinstance(view_arg.func, ast.Name) and view_arg.func.id == 'include':
                                # Recursive include resolution would go here
                                # For now, we just note it's an include
                                pass 
                            else:
                                # It's a view
                                handler_name = "unknown"
                                if isinstance(view_arg, ast.Name):
                                    handler_name = view_arg.id
                                elif isinstance(view_arg, ast.Attribute):
                                    handler_name = view_arg.attr
                                elif isinstance(view_arg, ast.Call):
                                    # Handle Class.as_view()
                                    if isinstance(view_arg.func, ast.Attribute) and view_arg.func.attr == 'as_view':
                                        # view_arg.func.value could be Name (MyView) or Attribute (views.MyView)
                                        val = view_arg.func.value
                                        if isinstance(val, ast.Name):
                                            handler_name = val.id
                                        elif isinstance(val, ast.Attribute):
                                            handler_name = val.attr
                                
                                routes.append(RouteInfo(
                                    path=full_path,
                                    methods=["GET", "POST", "PUT", "DELETE", "PATCH"], # Django views handle all by default unless restricted
                                    handler_name=handler_name,
                                    handler_node=item,
                                    module=file_path,
                                    framework="Django",
                                    line_number=item.lineno,
                                    source_code=ast.get_source_segment(source_code, item) or "",
                                    docstring=""
                                ))
        return routes
