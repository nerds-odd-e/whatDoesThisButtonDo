from typing import TYPE_CHECKING
from .testable_sandbox import TestableSandbox

if TYPE_CHECKING:
    from . import OpenAITestGenerator

class ExploratoryTest:
    """
    Handles exploratory testing of a sandbox environment using AI assistance
    """
    
    def __init__(
        self, 
        testable_sandbox: TestableSandbox, 
        ai_assistant: 'OpenAITestGenerator'
    ):
        """
        Initialize ExploratoryTest with a sandbox and AI assistant
        
        Args:
            testable_sandbox: The sandbox environment to explore
            ai_assistant: AI assistant to help guide the exploration
        """
        self.testable_sandbox = testable_sandbox
        self.ai_assistant = ai_assistant
        
    def execute(self) -> None:
        """
        Executes the exploratory testing process
        """
        result = self.testable_sandbox.start()
        print(result)