import os
import yaml
from typing import Optional, Dict, Any

class Config:
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "config.yaml"
        self.config_data = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        if not os.path.exists(self.config_path):
            return {}
        
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Could not load config file: {e}")
            return {}
    
    def get_llm_provider(self) -> str:
        return self.config_data.get('llm', {}).get('provider', 'ollama')
    
    def get_llm_config(self) -> Dict[str, Any]:
        return self.config_data.get('llm', {})
