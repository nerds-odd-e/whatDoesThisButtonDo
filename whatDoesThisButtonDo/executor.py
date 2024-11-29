from typing import Any, Dict

from whatDoesThisButtonDo.testable_sandbox import TestableSandbox
from .exploratory_test import ExploratoryTest
from whatDoesThisButtonDo.AiAssistant.ai_exploratory_test_assistant import (
    AIExploratoryTestAssistant
)

class ExecutorFactory:
    """
    Factory class for creating and configuring Executor instances.
    Handles the creation and setup of test environments and scopes.
    """
    
    def __init__(self):
        self._testable_sandbox = None
        self._sandbox_config: Dict[str, Any] = {}
        self._ai_assistant = None
        
    def with_sandbox(self, 
                    testable_sandbox: TestableSandbox, 
                    config: Dict[str, Any] = None) -> 'ExecutorFactory':
        self._testable_sandbox = testable_sandbox
        self._sandbox_config = config or {}
        return self
        
    def with_ai_assistant(
        self, 
        ai_assistant: AIExploratoryTestAssistant
    ) -> 'ExecutorFactory':
        self._ai_assistant = ai_assistant
        return self
        
    def build(self) -> 'Executor':
        if not self._testable_sandbox:
            raise ValueError("Testable sandbox must be configured before building")
            
        if not self._ai_assistant:
            raise ValueError("AI assistant must be configured before building")
            
        return Executor(
            self._testable_sandbox, 
            self._sandbox_config, 
            self._ai_assistant
        )

class Executor:
    """
    Responsible for executing tests and managing the test environment.
    Based on the domain model, Executor runs tests and manages the test sandbox.
    """
    
    def __init__(
        self, 
        testable_sandbox: TestableSandbox, 
        config: Dict[str, Any],
        ai_assistant: AIExploratoryTestAssistant
    ):
        """
        Initialize Executor with a testable sandbox and AI assistant.
        
        Args:
            testable_sandbox: TestableSandbox instance
            config: Configuration parameters for the sandbox
            ai_assistant: OpenAITestGenerator instance for test generation
        """
        self.testable_sandbox = testable_sandbox
        self.config = config
        self.ai_assistant = ai_assistant
        
    @classmethod
    def create(cls) -> ExecutorFactory:
        """
        Factory method to start building an Executor instance.
        
        Returns:
            ExecutorFactory instance for configuring the Executor
        """
        return ExecutorFactory()
    
    def explore(self) -> None:
        """
        Initiates exploratory testing using the configured sandbox and AI assistant
        """
        exploratory_test = ExploratoryTest(
            self.testable_sandbox, 
            self.ai_assistant
        )
        exploratory_test.execute()
        