from abc import ABC, abstractmethod
from typing import List, Optional
from .models import RouteInfo

class FrameworkAnalyzer(ABC):
    """
    Abstract Base Class for all Framework Analyzers.
    """

    @abstractmethod
    def detect(self, project_root: str) -> bool:
        """
        Detect if the project uses this framework.
        """
        pass

    @abstractmethod
    def extract_routes(self, project_root: str) -> List[RouteInfo]:
        """
        Extract all routes from the project.
        """
        pass

    def normalize_path(self, path: str) -> str:
        """
        Normalize route paths to a common format.
        """
        if not path.startswith("/"):
            path = "/" + path
        return path
