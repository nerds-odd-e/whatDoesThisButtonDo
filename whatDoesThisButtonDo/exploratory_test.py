from typing import TYPE_CHECKING
from .testable_sandbox import TestableSandbox
from .regression_test_proposal import RegressionTestProposal

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
        self.goal = {
            "title": "start cli with no parameter should receive helpful message",
            "description": (
                "Verify that when the CLI is started without any parameters, "
                "it displays a helpful message to remind the user that a "
                "oracle_dir is required."
            )
        }
        self.regression_proposal = RegressionTestProposal(
            sandbox_name=testable_sandbox.name,
            test_title=self.goal["title"],
            test_description=self.goal["description"]
        )
        
    def execute(self) -> RegressionTestProposal:
        """
        Executes the exploratory testing process and returns a regression test proposal
        
        Returns:
            RegressionTestProposal containing the test steps and results
        """
        try:
            # Create an AI assistant thread for this test execution
            ai_thread = self.ai_assistant.create_test_execution_thread(self.goal)
            
            possible_next_actions = self.testable_sandbox.start()
            current_state = {
                "status": "started",
                "message_to_ai": "Please select the first action."
            }
            
            step_count = 0
            max_steps = 100
            
            while True:
                step_count += 1
                if step_count > max_steps:
                    raise RuntimeError(
                        f"Test exceeded maximum number of steps ({max_steps}). "
                        "Possible infinite loop detected."
                    )
                
                # Get AI's chosen action and parameters using the thread
                ai_tool_call_name, action_choice = ai_thread.get_next_action(
                    possible_next_actions,
                    current_state
                )
                
                # Handle test_done function
                if ai_tool_call_name == "test_done":
                    print(f"Test completed - Result: {action_choice['result']}")
                    print(f"Conclusion: {action_choice['conclusion']}")
                    self.regression_proposal.test_result = action_choice['result']
                    self.regression_proposal.test_conclusion = (
                        action_choice['conclusion']
                    )
                    break
                
                # Record the action in the proposal
                self.regression_proposal.add_step(
                    ai_tool_call_name,
                    action_choice["action"],
                    action_choice.get("parameters")
                )
                
                # If AI decides to stop testing, break the loop
                if action_choice is None:
                    break
                
                print(f"Tool Call: {ai_tool_call_name}")
                print(f"Action: {action_choice}")

                # Execute the chosen action in the sandbox
                parameters = action_choice.get("parameters", None)
                
                if ai_tool_call_name == "assertion_for_regression":
                    # Execute the assertion check
                    self.testable_sandbox.execute_assertion(
                        action_choice["action"],
                        action_choice.get("parameters", {}),
                        current_state
                    )
                    # Report assertion success
                    ai_thread.action_executed(
                        ai_tool_call_name,
                        action_choice,
                        "assertion passed"
                    )
                else:
                    # Execute regular action and update possible next actions
                    possible_next_actions = self.testable_sandbox.execute_action(
                        action_choice["action"],
                        parameters
                    )
                    # Read and print the current state after the action
                    current_state = self.testable_sandbox.read_state()
                    ai_thread.action_executed(
                        ai_tool_call_name, 
                        action_choice, 
                        current_state.get("status", None)
                    )
                    print("Current state:", current_state)
                
            return self.regression_proposal
            
        finally:
            # Ensure teardown is called even if an exception occurs
            self.testable_sandbox.teardown()