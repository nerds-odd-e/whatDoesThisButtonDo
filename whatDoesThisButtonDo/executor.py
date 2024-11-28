from typing import Any, Dict, TYPE_CHECKING

from whatDoesThisButtonDo.testable_sandbox import TestableSandbox
from .exploratory_test import ExploratoryTest
from . import OpenAITestGenerator

if TYPE_CHECKING:
    from .executor_factory import ExecutorFactory

class Executor:
    """
    Responsible for executing tests and managing the test environment.
    Based on the domain model, Executor runs tests and manages the test sandbox.
    """
    
    def __init__(self, testable_sandbox: TestableSandbox, config: Dict[str, Any]):
        """
        Initialize Executor with a testable sandbox.
        
        Args:
            testable_sandbox: TestableSandbox instance
            config: Configuration parameters for the sandbox
        """
        self.testable_sandbox = testable_sandbox
        self.config = config
        self.ai_assistant = None  # Will be set later
        
    @classmethod
    def create(cls) -> 'ExecutorFactory':
        """
        Factory method to start building an Executor instance.
        
        Returns:
            ExecutorFactory instance for configuring the Executor
        """
        from .executor_factory import ExecutorFactory
        return ExecutorFactory()
    
    def set_ai_assistant(self, ai_assistant: OpenAITestGenerator) -> None:
        """
        Sets the AI assistant to be used for exploration
        
        Args:
            ai_assistant: OpenAITestGenerator instance
        """
        self.ai_assistant = ai_assistant
    
    def explore(self) -> None:
        """
        Initiates exploratory testing using the configured sandbox and AI assistant
        """
        if self.ai_assistant is None:
            raise ValueError(
                "AI assistant not set. "
                "Call set_ai_assistant before explore."
            )
            
        exploratory_test = ExploratoryTest(
            self.testable_sandbox, 
            self.ai_assistant
        )
        exploratory_test.execute()
        