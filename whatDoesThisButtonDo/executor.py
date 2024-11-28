from typing import Any, Dict, TYPE_CHECKING

from whatDoesThisButtonDo.testable_sandbox import TestableSandbox
from .exploratory_test import ExploratoryTest
from whatDoesThisButtonDo.AiAssistant.ai_exploratory_test_assistant import (
    AIExploratoryTestAssistant
)

if TYPE_CHECKING:
    from .executor_factory import ExecutorFactory

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
    def create(cls) -> 'ExecutorFactory':
        """
        Factory method to start building an Executor instance.
        
        Returns:
            ExecutorFactory instance for configuring the Executor
        """
        from .executor_factory import ExecutorFactory
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
        