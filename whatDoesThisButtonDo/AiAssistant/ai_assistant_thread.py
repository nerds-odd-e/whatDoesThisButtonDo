from .openai_client import OpenAIClient
from .get_next_action_command import GetNextActionCommand

class AIAssistantThread:
    def __init__(self, test_oracles, api_key: str, model: str):
        self.openai_client = OpenAIClient(
            test_oracles=test_oracles,
            api_key=api_key,
            model=model
        )

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
        command = GetNextActionCommand(self.openai_client, possible_actions)
        response = command.execute()
        return response 