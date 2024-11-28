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
                
    def as_assistant_message(self) -> str:
        """
        Formats the test oracles into a JSON structure for AI consumption
        
        Returns:
            str: A formatted string containing all test oracle contents as JSON
        """
        if not self._oracles:
            return "No test oracles have been loaded."
        
        import json
        
        message = "# Test Oracles\n\n"
        message += "Below is a JSON structure containing all test oracles that define "
        message += "the testing rules and expectations:\n\n"
        message += "```json\n"
        message += json.dumps(self._oracles, indent=2)
        message += "\n```"
        
        return message
                