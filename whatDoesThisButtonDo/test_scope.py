from typing import Dict, List
from pathlib import Path

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
        self._testable_sandboxes: List[Path] = []
    
    def get_testable_sandboxes(self) -> List[Path]:
        """
        Get the list of folders that contain a testability subfolder.
        
        Returns:
            List of Path objects representing folders containing testability subfolders
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
            # Check for testability folders
            if path.is_dir() and path.name == "testability":
                self._testable_sandboxes.append(path.parent)
        
        return self.test_oracles