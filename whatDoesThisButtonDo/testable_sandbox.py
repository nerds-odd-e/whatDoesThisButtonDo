from pathlib import Path
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .test_scope import TestScope

class TestableSandbox:
    """
    Represents a sandbox directory that contains testability features.
    """
    def __init__(self, path: Path, test_scope: 'TestScope'):
        """
        Initialize a testable sandbox.
        
        Args:
            path: Path to the sandbox directory
            test_scope: Reference to the parent TestScope
        """
        self.path = path
        self.test_scope = test_scope
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
    def create_if_valid(
        cls, 
        path: Path, 
        test_scope: 'TestScope'
    ) -> Optional['TestableSandbox']:
        """
        Factory method to create a TestableSandbox if the path is valid.
        
        Args:
            path: Path to check and create sandbox from
            test_scope: Reference to the parent TestScope
            
        Returns:
            TestableSandbox instance if valid, None otherwise
        """
        sandbox = cls(path, test_scope)
        return sandbox if sandbox.is_valid else None 