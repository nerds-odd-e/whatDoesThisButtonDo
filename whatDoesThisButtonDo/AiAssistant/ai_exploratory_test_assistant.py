from .openai_client import OpenAIClient
from .get_next_action_command import GetNextActionCommand

class AIExploratoryTestAssistant:
    def __init__(self, test_oracles):
        self.openai_client = OpenAIClient()
        self.test_oracles = test_oracles

    def get_next_action(self, possible_actions):
        """
        Get the AI's choice for the next action to take
        
        Args:
            possible_actions: List of possible actions with their descriptions
            
        Returns:
            dict: Contains 'action' name and 'parameters' for the chosen action
        """
        command = GetNextActionCommand(self.openai_client, possible_actions)
        response = command.execute()
        return response 