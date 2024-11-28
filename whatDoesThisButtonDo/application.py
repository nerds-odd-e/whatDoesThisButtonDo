from typing import List

from . import OpenAITestGenerator
from .executor import Executor
from .test_scope import TestScope


class Application:
    """
    Main application class for WhatDoesThisButtonDo.
    Handles initialization, test oracle loading, and test execution.
    """
    
    def __init__(self):
        pass  # Remove test_oracles field
        
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
        test_scope.load_test_oracles(oracle_dir)
        
        # Create executors for each sandbox
        executors = self._create_executors(test_scope)
        
        # Initialize OpenAI client
        openai_client = OpenAITestGenerator(test_scope.get_test_oracles())
        
        # Reset environment and explore with each executor
        for executor in executors:
            executor.set_ai_assistant(openai_client)
            executor.explore()