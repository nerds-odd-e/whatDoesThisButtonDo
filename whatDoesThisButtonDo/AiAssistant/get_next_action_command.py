import json
from .chat_completion_command import ChatCompletionCommand

class GetNextActionCommand(ChatCompletionCommand):
    def __init__(self, openai_client, possible_actions):
        messages = self._create_messages(possible_actions)
        super().__init__(openai_client, messages)
    
    def execute(self):
        """
        Execute the command and return parsed JSON response
        
        Returns:
            dict: Contains 'action' and 'parameters' keys
        """
        response = super().execute()
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse AI response as JSON: {response}") from e
    
    def _create_messages(self, possible_actions):
        actions_description = "\n".join(
            f"- {action_name}: {action_info['description']}" 
            for action_name, action_info in possible_actions.items()
        )
        
        prompt = (
            "Given these possible actions, choose the next action to take "
            "and specify any required parameters.\n\n"
            f"Available Actions:\n{actions_description}\n\n"
            "Respond in the following JSON format:\n"
            "{\n"
            '    "action": "action_name",\n'
            '    "parameters": {"param1": "value1", "param2": "value2"}\n'
            "}"
        )
        
        return [
            {
                "role": "system", 
                "content": (
                    "You are a helpful test explorer. "
                    "Choose actions that will help thoroughly test the system."
                )
            },
            {"role": "user", "content": prompt}
        ] 