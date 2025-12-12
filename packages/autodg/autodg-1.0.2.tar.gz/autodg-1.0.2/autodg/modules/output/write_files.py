import os
from typing import List
from autodg.modules.core.models import RouteInfo
from autodg.modules.core.mermaid import MermaidGenerator
from autodg.modules.core.llm import LLMClient
from autodg.modules.core.utils import find_files, read_file
from autodg.modules.core.progress import ProgressTracker

class MarkdownGenerator:
    def __init__(self, output_dir: str, use_llm: bool = False):
        self.output_dir = output_dir
        self.use_llm = use_llm
        self.llm_client = LLMClient() if use_llm else None
        
        # Ensure output directories exist
        os.makedirs(os.path.join(output_dir, "files"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "request_docs"), exist_ok=True)

    def generate_route_docs(self, routes: List[RouteInfo]):
        """
        Generate documentation for each route.
        """
        print(f"Generating documentation for {len(routes)} routes...")
        tracker = ProgressTracker(len(routes), prefix="Routes")
        
        for i, route in enumerate(routes):
            # Improved filename: index_METHOD__handler__path
            safe_path = route.path.replace('/', '_').strip('_')
            if len(safe_path) > 50:
                safe_path = safe_path[:50] + "..."
            
            filename = f"{i}_{route.methods[0]}__{route.handler_name}__{safe_path}.md"
            # Sanitize filename
            filename = filename.replace("<", "").replace(">", "").replace(":", "")
            
            filepath = os.path.join(self.output_dir, "request_docs", filename)
            
            content = self._build_route_markdown(route)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            
            tracker.update()
        tracker.finish()

    def generate_file_docs(self, project_root: str):
        """
        Generate documentation for each Python file in the project.
        """
        if not self.use_llm:
            print("Skipping file-wise documentation (LLM disabled).")
            return

        print("Generating file-wise documentation...")
        files = find_files(project_root)
        
        # Filter out site-packages/node_modules before count
        target_files = [f for f in files if "site-packages" not in f and "node_modules" not in f]
        
        tracker = ProgressTracker(len(target_files), prefix="Files")
        
        for file_path in target_files:
            content = read_file(file_path)
            if not content:
                tracker.update()
                continue
                
            relative_path = os.path.relpath(file_path, project_root)
            safe_name = relative_path.replace("/", "_").replace("\\", "_").replace(".py", "")
            output_path = os.path.join(self.output_dir, "files", f"{safe_name}.md")
            
            explanation = self.llm_client.explain_code(content)
            
            md = f"# File: {relative_path}\n\n"
            md += "## AI Overview\n"
            md += explanation
            md += "\n\n## Source Code\n"
            md += "```python\n"
            md += content
            md += "\n```\n"
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(md)
            
            tracker.update()
        tracker.finish()

    def _build_route_markdown(self, route: RouteInfo) -> str:
        md = []
        md.append(f"# {route.methods[0]} {route.path}")
        md.append(f"**Framework**: {route.framework}")
        md.append(f"**Module**: `{route.module}`")
        md.append(f"**Handler**: `{route.handler_name}`")
        
        md.append("## Parameters")
        if route.parameters:
            for param in route.parameters:
                md.append(f"- `{param['name']}`: {param['type']}")
        else:
            md.append("No parameters.")
            
        md.append("## Source Code")
        md.append("```python")
        md.append(route.source_code)
        md.append("```")
        
        if route.db_operations:
            md.append("## Database Operations")
            for op in route.db_operations:
                md.append(f"- `{op}`")
            
            md.append("### DB Diagram")
            md.append("```mermaid")
            md.append(MermaidGenerator.generate_db_graph(route.handler_name, route.db_operations))
            md.append("```")

        if route.call_graph and route.call_graph.get("direct_calls"):
            md.append("## Call Graph")
            md.append("```mermaid")
            md.append(MermaidGenerator.generate_graph(route.handler_name, route.call_graph["direct_calls"]))
            md.append("```")

        if self.use_llm and self.llm_client and self.llm_client.is_available():
            md.append("## AI Explanation")
            # Pass context_code to LLM
            explanation = self.llm_client.explain_code(route.source_code, route.context_code)
            md.append(explanation)
            
        return "\n\n".join(md)
