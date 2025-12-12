from typing import List, Dict

class MermaidGenerator:
    @staticmethod
    def generate_graph(root_node: str, calls: List[str]) -> str:
        """
        Generate a MermaidJS flowchart for a call graph.
        """
        if not calls:
            return ""
        
        lines = ["graph TD"]
        lines.append(f"    {root_node}[{root_node}]")
        
        for call in calls:
            lines.append(f"    {root_node} --> {call}")
            
        return "\n".join(lines)

    @staticmethod
    def generate_db_graph(root_node: str, db_ops: List[str]) -> str:
        """
        Generate a MermaidJS flowchart for DB operations.
        """
        if not db_ops:
            return ""
            
        lines = ["graph TD"]
        lines.append(f"    {root_node}[{root_node}]")
        lines.append(f"    DB[(Database)]")
        
        for op in db_ops:
            lines.append(f"    {root_node} -- {op} --> DB")
            
        return "\n".join(lines)
