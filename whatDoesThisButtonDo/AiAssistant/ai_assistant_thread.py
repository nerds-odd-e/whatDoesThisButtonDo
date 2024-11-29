from .openai_client import OpenAIClient
from .get_next_action_command import GetNextActionCommand

class AIAssistantThread:
    def __init__(self, test_oracles, api_key: str, model: str):
        self.openai_client = OpenAIClient(
            test_oracles=test_oracles,
            api_key=api_key,
            model=model
        )
        self.action_history = []

    def get_next_action(self, possible_actions, sut_state):
        """
        Get the AI's choice for the next action to take
        
        Args:
            possible_actions: List of possible actions with their descriptions
            sut_state: Current state of the system under test
            
        Returns:
            dict: Contains 'action' name and 'parameters' for the chosen action,
                 or None to indicate testing should stop
        """
        command = GetNextActionCommand(
            self.openai_client,
            possible_actions,
            self.action_history
        )
        response = command.execute()
        return response

    def action_executed(self, action_choice, current_state):
        """
        Record an executed action and its result in the history
        
        Args:
            action_choice: The action that was executed
            current_state: The resulting state after execution
        """
        history_entry = {
            "function_name": "select_next_action",
            "action": action_choice,
            "status": current_state.get("status", None)
        }
        self.action_history.append(history_entry) 