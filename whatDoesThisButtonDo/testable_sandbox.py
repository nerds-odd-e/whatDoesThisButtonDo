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