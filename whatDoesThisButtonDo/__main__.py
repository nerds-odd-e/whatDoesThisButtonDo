from pathlib import Path
from typing import Dict, List

from . import OpenAITestGenerator, GenerateTestPlanCommand
from .executor import Executor
from .test_sandbox import TestSandbox
from .test_scope import TestScope

class Application:
    """
    Main application class for WhatDoesThisButtonDo.
    Handles initialization, test oracle loading, and test execution.
    """
    
    def __init__(self):
        self.executor = self._create_executor()
        self.test_oracles: List[Dict[str, str]] = []
        
    def _create_executor(self) -> Executor:
        """Creates and configures the test executor"""
        return (Executor.create()
                .with_sandbox(TestSandbox, {
                    "environment": "test",
                    "cleanup_enabled": True
                })
                .with_scope(TestScope())
                .build())
    
    def load_test_oracles(self, oracle_dir: str) -> None:
        """
        Load all test oracle markdown files from the specified directory
        
        Args:
            oracle_dir: Path to the directory containing test oracle files
        """
        oracle_path = Path(oracle_dir)
        
        self.test_oracles = []
        for file in oracle_path.glob("*.md"):
            with open(file, 'r') as f:
                self.test_oracles.append({
                    'name': file.name,
                    'content': f.read()
                })
    
    def run(self, oracle_dir: str) -> None:
        """
        Main execution flow of the application
        
        Args:
            oracle_dir: Directory containing test oracle files
        """
        # Reset environment
        self.executor.reset_environment()
        
        # Load test oracles
        self.load_test_oracles(oracle_dir)
        
        try:
            # Initialize OpenAI client
            openai_client = OpenAITestGenerator()
            
            # Generate test cases directly using chat completion
            test_cases = openai_client.generate_test_cases(self.test_oracles)
            
            # Print generated test cases
            print("Generated Test Cases:")
            for i, test_case in enumerate(test_cases, 1):
                print(f"\nTest Case {i}:")
                print(test_case)
            
            # Generate and print test plan for the first test case
            if test_cases:
                print("\nGenerating Test Plan for First Test Case...")
                test_plan_command = GenerateTestPlanCommand(
                    openai_client.openai_client,
                    test_cases[0],
                    self.test_oracles
                )
                test_plan = test_plan_command.execute()
                print("\nTest Plan:")
                print(test_plan)
                
        except ValueError as e:
            print(f"Error: {e}")
            print("Please ensure OPENAI_API_KEY environment variable is set")
            raise
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

def main():
    """Entry point for the application"""
    try:
        app = Application()
        app.run("test_oracles")
    except Exception:
        exit(1)

if __name__ == "__main__":
    main() 