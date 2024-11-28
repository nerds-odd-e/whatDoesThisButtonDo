from typing import Any, Dict, List
from pathlib import Path

class TestScope():
    """
    Base class for test scope implementations.
    TestScope defines the boundaries and constraints for testing.
    """
    
    def __init__(self, **kwargs):
        """
        Initialize the test scope with configuration.
        
        Args:
            **kwargs: Configuration parameters for the scope
        """
        self.config = kwargs
        self.test_oracles: List[Dict[str, str]] = []
    
    def is_action_allowed(self, action: Dict[str, Any]) -> bool:
        """
        Checks if an action is within the defined test scope.
        
        Args:
            action: Dictionary containing action details
            
        Returns:
            Boolean indicating if the action is allowed
        """
        return True
    
    def get_available_actions(self) -> List[Dict[str, Any]]:
        """
        Returns the list of available actions within the scope.
        
        Returns:
            List of dictionaries containing available actions
        """
        return []
    
    def get_constraints(self) -> Dict[str, Any]:
        """
        Returns the constraints that define the test scope.
        
        Returns:
            Dictionary containing scope constraints
        """
        return {}
    
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
        return self.test_oracles