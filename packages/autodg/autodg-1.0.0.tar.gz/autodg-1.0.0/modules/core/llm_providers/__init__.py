from abc import ABC, abstractmethod
from typing import Optional

class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    """
    
    @abstractmethod
    def explain_code(self, source_code: str, context_code: Optional[dict] = None) -> str:
        """
        Generate an explanation for the given source code.
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the provider is available/configured.
        """
        pass
