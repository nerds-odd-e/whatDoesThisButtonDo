from typing import Dict, List
from pathlib import Path
from .testable_sandbox import TestableSandbox

class TestScope():
    """
    Base class for test scope implementations.
    TestScope defines the boundaries and constraints for testing.
    """
    
    def __init__(self):
        """
        Initialize the test scope with configuration.
        
        Args:
            **kwargs: Configuration parameters for the scope
        """
        self.test_oracles: List[Dict[str, str]] = []
        self._testable_sandboxes: List[TestableSandbox] = []
    
    def get_testable_sandboxes(self) -> List[TestableSandbox]:
        """
        Get the list of testable sandboxes.
        
        Returns:
            List of TestableSandbox objects
        """
        return self._testable_sandboxes
    
    def load_test_oracles(self, oracle_dir: str) -> List[Dict[str, str]]:
        """
        Load all test oracle markdown files from the specified directory
        
        Args:
            oracle_dir: Path to the directory containing test oracle files
            
        Returns:
            List of dictionaries containing test oracle name and content
        """
        oracle_path = Path(oracle_dir)
        
        self.test_oracles = []
        for file in oracle_path.glob("*.md"):
            with open(file, 'r') as f:
                self.test_oracles.append({
                    'name': file.name,
                    'content': f.read()
                })
        
        self._testable_sandboxes = []
        
        # Walk through all subdirectories
        for path in oracle_path.rglob("*"):
            # Try to create a TestableSandbox for each potential directory
            if path.is_dir():
                sandbox = TestableSandbox.create_if_valid(path, self)
                if sandbox:
                    self._testable_sandboxes.append(sandbox)
        
        return self.test_oracles