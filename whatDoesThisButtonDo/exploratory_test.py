from typing import TYPE_CHECKING
from .testable_sandbox import TestableSandbox

if TYPE_CHECKING:
    from . import AIExploratoryTestAssistant

class ExploratoryTest:
    """
    Handles exploratory testing of a sandbox environment using AI assistance
    """
    
    def __init__(
        self, 
        testable_sandbox: TestableSandbox, 
        ai_assistant: 'AIExploratoryTestAssistant'
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
        try:
            possible_next_actions = self.testable_sandbox.start()
            
            while possible_next_actions:
                # Get AI's chosen action and parameters
                action_choice = self.ai_assistant.get_next_action(possible_next_actions)
                
                print(action_choice)

                # Execute the chosen action in the sandbox
                parameters = action_choice.get("parameters", None)
                possible_next_actions = self.testable_sandbox.execute_action(
                    action_choice["action"],
                    parameters
                )
        finally:
            # Ensure teardown is called even if an exception occurs
            self.testable_sandbox.teardown()