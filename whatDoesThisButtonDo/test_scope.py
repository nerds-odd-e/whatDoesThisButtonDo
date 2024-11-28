from typing import List
from pathlib import Path
from .testable_sandbox import TestableSandbox
from .test_oracles import TestOracles

class TestScope():
    """
    Base class for test scope implementations.
    TestScope defines the boundaries and constraints for testing.
    """
    
    def __init__(self):
        """
        Initialize the test scope with configuration.
        """
        self.test_oracles = TestOracles()
        self._testable_sandboxes: List[TestableSandbox] = []
    
    def get_testable_sandboxes(self) -> List[TestableSandbox]:
        """
        Get the list of testable sandboxes.
        
        Returns:
            List of TestableSandbox objects
        """
        return self._testable_sandboxes
    
    def load_test_oracles(self, oracle_dir: str):
        """
        Load all test oracle markdown files from the specified directory
        
        Args:
            oracle_dir: Path to the directory containing test oracle files
        """
        oracle_path = Path(oracle_dir)
        self.test_oracles.load_from_directory(oracle_dir)
        
        self._testable_sandboxes = []
        
        # Walk through all subdirectories
        for path in oracle_path.rglob("*"):
            # Try to create a TestableSandbox for each potential directory
            if path.is_dir():
                sandbox = TestableSandbox.create_if_valid(path)
                if sandbox:
                    self._testable_sandboxes.append(sandbox)
    
    def get_test_oracles(self) -> TestOracles:
        """
        Get the test oracles object.
        
        Returns:
            TestOracles instance
        """
        return self.test_oracles