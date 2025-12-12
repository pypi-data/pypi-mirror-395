import os
import ast
from typing import Optional, List

def read_file(file_path: str) -> str:
    """
    Read file content safely, replacing invalid characters.
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def parse_ast(file_path: str) -> Optional[ast.AST]:
    """
    Parse a Python file into an AST.
    """
    content = read_file(file_path)
    if not content:
        return None
    try:
        return ast.parse(content, filename=file_path)
    except SyntaxError as e:
        print(f"Syntax error in {file_path}: {e}")
        return None

def find_files(root_dir: str, extension: str = ".py", exclude_dirs: Optional[List[str]] = None) -> List[str]:
    """
    Recursively find all files with a specific extension, skipping excluded directories.
    """
    if exclude_dirs is None:
        exclude_dirs = ["env", "venv", ".env", ".venv", "node_modules", "site-packages", "__pycache__", ".git","media","uploads","static","templates",]

    matches = []
    for root, dirs, files in os.walk(root_dir):
        # Modify dirs in-place to skip excluded directories
        # We filter out directories that match any of the exclude patterns
        # strict match or starts with for env/venv variants if desired, but usually exact match is safer for things like 'node_modules'.
        # For 'env' and 'venv', users often have variations like 'venv3', 'env_proj'. 
        # Given the user request "starting from env/, venv...", I will use startswith for those specific ones if they are just "env" or "venv" in the list, 
        # but to be safe and standard, I'll stick to the list provided + common ones.
        # Actually, let's implement a smarter filter: if d in exclude_dirs or d.startswith('.')
        
        # User request: "exclude the folders where forlder starting from env/, venv, .env/, .venv/,node_modules, sitepackages"
        # I will implement logic to check if directory name starts with any of the excluded prefixes.
        
        dirs[:] = [d for d in dirs if not any(d.startswith(ex) for ex in exclude_dirs) and "site-packages" not in d]
        
        for file in files:
            if file.endswith(extension):
                matches.append(os.path.join(root, file))
    return matches
