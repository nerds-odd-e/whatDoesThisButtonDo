from . import AIExploratoryTestAssistant
from .executor import Executor
from .test_scope import TestScope
import os


class Application:
    """
    Main application class for WhatDoesThisButtonDo.
    Handles initialization, test oracle loading, and test execution.
    """
    
    def __init__(self):
        pass
        
    def run(self, oracle_dir: str) -> None:
        """
        Main execution method that runs the test oracles
        
        Args:
            oracle_dir: Directory containing test oracle files
        """
        test_scope = TestScope()
        test_scope.load_test_oracles(oracle_dir)
        
        # Initialize OpenAI client with test oracles
        openai_client = AIExploratoryTestAssistant(
            test_oracles=test_scope.get_test_oracles(),
            api_key=os.getenv('OPENAI_API_KEY'),
            model="gpt-4-turbo-preview"
        )
        
        # Create and run executors for each sandbox
        for sandbox in test_scope.get_testable_sandboxes():
            executor = (Executor.create()
                    .with_sandbox(sandbox, {
                        "environment": "test",
                        "cleanup_enabled": True
                    })
                    .with_ai_assistant(openai_client)
                    .build())
            executor.explore()