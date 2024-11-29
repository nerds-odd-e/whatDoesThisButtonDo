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
            # Create an AI assistant thread for this test execution
            ai_thread = self.ai_assistant.create_thread()
            
            possible_next_actions = self.testable_sandbox.start()
            current_state = {"status": "started"}
            
            while possible_next_actions:
                # Get AI's chosen action and parameters using the thread
                action_choice = ai_thread.get_next_action(
                    possible_next_actions,
                    current_state
                )
                
                # If AI decides to stop testing, break the loop
                if action_choice is None:
                    break
                
                print(action_choice)

                # Execute the chosen action in the sandbox
                parameters = action_choice.get("parameters", None)
                possible_next_actions = self.testable_sandbox.execute_action(
                    action_choice["action"],
                    parameters
                )
                
                # Read and print the current state after the action
                current_state = self.testable_sandbox.read_state()
                print("Current state:", current_state)
        finally:
            # Ensure teardown is called even if an exception occurs
            self.testable_sandbox.teardown()