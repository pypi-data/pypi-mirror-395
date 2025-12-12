from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import ast

@dataclass
class RouteInfo:
    path: str
    methods: List[str]
    handler_name: str
    handler_node: Optional[ast.AST] = None
    module: str = ""
    framework: str = ""
    line_number: int = 0
    source_code: str = ""
    docstring: str = ""
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    return_type: str = "Any"
    db_operations: List[str] = field(default_factory=list)
    call_graph: Dict[str, Any] = field(default_factory=dict)
    context_code: Dict[str, str] = field(default_factory=dict) # function_name -> source_code
    extra_meta: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FileInfo:
    filename: str
    module_path: str
    classes: List[str]
    functions: List[str]
    imports: List[str]
    source_code: str
