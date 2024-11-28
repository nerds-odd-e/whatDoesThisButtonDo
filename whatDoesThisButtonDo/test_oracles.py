from typing import Dict, List
from pathlib import Path

class TestOracles:
    """
    Represents a collection of test oracles that define testing rules and expectations
    """
    
    def __init__(self):
        self._oracles: List[Dict[str, str]] = []
        
    def load_from_directory(self, oracle_dir: str) -> None:
        """
        Load all test oracle markdown files from the specified directory
        
        Args:
            oracle_dir: Path to the directory containing test oracle files
        """
        oracle_path = Path(oracle_dir)
        
        self._oracles = []
        for file in oracle_path.glob("*.md"):
            with open(file, 'r') as f:
                self._oracles.append({
                    'name': file.name,
                    'content': f.read()
                })
                