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
        self.test_oracles: List[Dict[str, str]] = []
        
    def _create_executor(self, test_scope: TestScope) -> Executor:
        """Creates and configures the test executor"""
        return (Executor.create()
                .with_sandbox(TestSandbox, {
                    "environment": "test",
                    "cleanup_enabled": True
                })
                .with_scope(test_scope)
                .build())
    
    def run(self, oracle_dir: str) -> None:
        """
        Main execution flow of the application
        
        Args:
            oracle_dir: Directory containing test oracle files
        """
        # Create TestScope instance
        test_scope = TestScope()
        
        # Load test oracles
        self.test_oracles = test_scope.load_test_oracles(oracle_dir)
        
        # Create executor with test_scope as a parameter
        executor = self._create_executor(test_scope)
        
        # Update references from self.executor to executor
        executor.reset_environment()
        
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