from typing import List, Type
from autodg.modules.core.scanner import FrameworkAnalyzer
from autodg.modules.core.models import RouteInfo
from autodg.modules.frameworks.flask_analyzer import FlaskAnalyzer
from autodg.modules.frameworks.fastapi_analyzer import FastAPIAnalyzer
from autodg.modules.frameworks.django_analyzer import DjangoAnalyzer
from autodg.modules.frameworks.drf_analyzer import DRFAnalyzer

class Dispatcher:
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.analyzers: List[Type[FrameworkAnalyzer]] = [
            FlaskAnalyzer,
            FastAPIAnalyzer,
            DjangoAnalyzer,
            DRFAnalyzer
        ]
        self.active_analyzers: List[FrameworkAnalyzer] = []

    def detect_frameworks(self):
        """
        Detect which frameworks are used in the project.
        """
        print(f"Scanning {self.project_root} for frameworks...")
        for analyzer_cls in self.analyzers:
            analyzer = analyzer_cls()
            if analyzer.detect(self.project_root):
                print(f"Detected: {analyzer.__class__.__name__}")
                self.active_analyzers.append(analyzer)

    def run(self) -> List[RouteInfo]:
        """
        Run all active analyzers and aggregate routes.
        """
        all_routes = []
        if not self.active_analyzers:
            print("No supported frameworks detected.")
            return []

        for analyzer in self.active_analyzers:
            try:
                routes = analyzer.extract_routes(self.project_root)
                all_routes.extend(routes)
            except Exception as e:
                print(f"Error running {analyzer.__class__.__name__}: {e}")
        
        return all_routes
