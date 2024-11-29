from .openai_client import OpenAIClient
from .get_next_action_command import GetNextActionCommand

class AITestExecutionThread:
    def __init__(self, test_oracles, api_key: str, model: str, goal):
        self.openai_client = OpenAIClient(
            test_oracles=test_oracles,
            api_key=api_key,
            model=model
        )
        self.action_history = []
        
        goal_message = (
            f"Test Goal: {goal['title']}\n"
            f"Description: {goal['description']}"
        )
        self.openai_client.append_message("user", goal_message)

    def get_next_action(self, possible_actions, sut_state):
        """
        Get the AI's choice for the next action to take
        
        Args:
            possible_actions: List of possible actions with their descriptions
            sut_state: Current state of the system under test
            
        Returns:
            tuple: (function_name, dict with action and parameters)
                  or (None, None) to indicate testing should stop
        """
        command = GetNextActionCommand(
            self.openai_client,
            possible_actions,
            self.action_history,
            sut_state
        )
        return command.execute()

    def action_executed(self, function_name, action_choice, status):
        """
        Record an executed action and its result in the history
        
        Args:
            function_name: Name of the function that was called
            action_choice: The action that was executed
            status: The status after execution
        """
        history_entry = {
            "function_name": function_name,
            "action": action_choice,
            "status": status
        }
        self.action_history.append(history_entry) 