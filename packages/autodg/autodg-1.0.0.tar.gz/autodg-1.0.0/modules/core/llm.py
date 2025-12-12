import os
from typing import Optional
from modules.core.config import Config
from modules.core.llm_providers import LLMProvider
from modules.core.llm_providers.ollama import OllamaProvider
from modules.core.llm_providers.openai_provider import OpenAIProvider
from modules.core.llm_providers.claude import ClaudeProvider
from modules.core.llm_providers.gemini import GeminiProvider

class LLMClient:
    def __init__(self, config_path: Optional[str] = None):
        self.provider = self._initialize_provider(config_path)
    
    def _initialize_provider(self, config_path: Optional[str]) -> Optional[LLMProvider]:
        """
        Initialize LLM provider with fallback logic:
        1. Try local Ollama with llama3.1
        2. Check config file for provider selection
        3. Return None if no provider available
        """
        # Try local Ollama first
        ollama = OllamaProvider(model="llama3.1")
        if ollama.is_available():
            print("Using Ollama (llama3.1) locally")
            return ollama
        
        # Load config
        config = Config(config_path)
        provider_name = config.get_llm_provider()
        llm_config = config.get_llm_config()
        
        # Initialize based on config
        if provider_name == 'ollama':
            cfg = llm_config.get('ollama', {})
            provider = OllamaProvider(
                model=cfg.get('model', 'llama3.1'),
                host=cfg.get('host', 'http://localhost:11434')
            )
            if provider.is_available():
                print(f"Using Ollama ({cfg.get('model', 'llama3.1')}) at {cfg.get('host')}")
                return provider
        
        elif provider_name == 'openai':
            cfg = llm_config.get('openai', {})
            api_key = cfg.get('api_key') or os.getenv('OPENAI_API_KEY')
            if api_key:
                provider = OpenAIProvider(api_key=api_key, model=cfg.get('model', 'gpt-4'))
                print(f"Using OpenAI ({cfg.get('model', 'gpt-4')})")
                return provider
        
        elif provider_name == 'claude':
            cfg = llm_config.get('claude', {})
            api_key = cfg.get('api_key') or os.getenv('ANTHROPIC_API_KEY')
            if api_key:
                provider = ClaudeProvider(api_key=api_key, model=cfg.get('model', 'claude-3-5-sonnet-20241022'))
                print(f"Using Claude ({cfg.get('model', 'claude-3-5-sonnet-20241022')})")
                return provider
        
        elif provider_name == 'gemini':
            cfg = llm_config.get('gemini', {})
            api_key = cfg.get('api_key') or os.getenv('GOOGLE_API_KEY')
            if api_key:
                provider = GeminiProvider(api_key=api_key, model=cfg.get('model', 'gemini-1.5-flash'))
                print(f"Using Gemini ({cfg.get('model', 'gemini-1.5-flash')})")
                return provider
        
        print("Warning: No LLM provider available. AI explanations will be disabled.")
        return None
    
    def explain_code(self, source_code: str, context_code: Optional[dict] = None) -> str:
        if not self.provider:
            return "LLM provider not available."
        return self.provider.explain_code(source_code, context_code)
    
    def is_available(self) -> bool:
        return self.provider is not None
