import ast
import os
from typing import Dict
from modules.core.utils import find_files, parse_ast
from modules.core.ast_parser import ASTParser

class FunctionIndexer:
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.function_map: Dict[str, str] = {} # name -> source_code

    def build_index(self):
        """
        Scan the project and index all functions.
        """
        print("Indexing functions for context...")
        files = find_files(self.project_root)
        for file_path in files:
            # Skip site-packages explicitly if not already handled by find_files
            if "site-packages" in file_path or "node_modules" in file_path:
                continue
                
            tree = parse_ast(file_path)
            if not tree:
                continue
            
            try:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    source_code = f.read()
            except:
                continue

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef):
                    # We store by simple name for now. 
                    # Collision handling: last one wins or we could store list.
                    # For simplicity in this iteration, we store the last one found.
                    code = ASTParser.get_function_source(node, source_code)
                    if code:
                        self.function_map[node.name] = code
    
    def get_source(self, function_name: str) -> str:
        return self.function_map.get(function_name, "")
