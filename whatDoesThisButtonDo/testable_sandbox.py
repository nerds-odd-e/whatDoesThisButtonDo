from pathlib import Path
from typing import Optional

class TestableSandbox:
    """
    Represents a sandbox directory that contains testability features.
    """
    def __init__(self, path: Path):
        """
        Initialize a testable sandbox.
        
        Args:
            path: Path to the sandbox directory
        """
        self.path = path
        self.testability_dir = path / "testability"

    @property
    def name(self) -> str:
        """Get the name of the sandbox directory."""
        return self.path.name

    @property
    def is_valid(self) -> bool:
        """Check if this is a valid testable sandbox."""
        return self.testability_dir.is_dir()

    def start(self) -> dict:
        """
        Loads and executes the start function from the testability directory.
        
        Returns:
            A dictionary mapping function names to their documentation
        """
        import importlib.util
        import sys
        
        # Load the start.py module from testability directory
        start_path = self.testability_dir / "start.py"
        if not start_path.is_file():
            raise FileNotFoundError("start.py not found in testability directory")
            
        spec = importlib.util.spec_from_file_location("start", start_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["start"] = module
        spec.loader.exec_module(module)
        
        if not hasattr(module, "start"):
            raise AttributeError("start function not found in start.py")
            
        result = module.start()
        
        # Process the actions list into a dictionary of function documentation
        if not isinstance(result, dict) or 'actions' not in result:
            raise ValueError("start() must return a dict with 'actions' field")
            
        return {
            func.__name__: {'description': func.__doc__ or ''} 
            for func in result['actions']
        }

    @classmethod
    def create_if_valid(cls, path: Path) -> Optional['TestableSandbox']:
        """
        Factory method to create a TestableSandbox if the path is valid.
        
        Args:
            path: Path to check and create sandbox from
            
        Returns:
            TestableSandbox instance if valid, None otherwise
        """
        sandbox = cls(path)
        return sandbox if sandbox.is_valid else None 