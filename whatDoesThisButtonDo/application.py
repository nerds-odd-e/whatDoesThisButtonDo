from typing import Dict, List

from . import OpenAITestGenerator, GenerateTestPlanCommand
from .executor import Executor
from .test_scope import TestScope


class Application:
    """
    Main application class for WhatDoesThisButtonDo.
    Handles initialization, test oracle loading, and test execution.
    """
    
    def __init__(self):
        self.test_oracles: List[Dict[str, str]] = []
        
    def _create_executors(self, test_scope: TestScope) -> List[Executor]:
        """Creates and configures executors for each testable sandbox"""
        executors = []
        for sandbox in test_scope.get_testable_sandboxes():
            executor = (Executor.create()
                    .with_sandbox(sandbox, {
                        "environment": "test",
                        "cleanup_enabled": True
                    })
                    .build())
            executors.append(executor)
        return executors

    def run(self, oracle_dir: str) -> None:
        """
        Main execution method that runs the test oracles
        
        Args:
            oracle_dir: Directory containing test oracle files
        """
        test_scope = TestScope()
        self.test_oracles = test_scope.load_test_oracles(oracle_dir)
        
        # Create executors for each sandbox
        executors = self._create_executors(test_scope)
        
        # Reset environment for each executor
        for executor in executors:
            executor.explore()
        
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