import json
from typing import Dict, Any
from .openai_client import OpenAIClient

class GetNextActionCommand:
    def __init__(
        self,
        openai_client: OpenAIClient,
        possible_actions: Dict[str, Dict[str, Any]],
        action_history=None,
        sut_state=None
    ):
        self.openai_client = openai_client
        self.possible_actions = possible_actions
        self.sut_state = sut_state
        self.action_history = action_history or []
    
    def execute(self):
        """
        Execute the command and return parsed JSON response with function name
        
        Returns:
            tuple: (function_name, dict with 'action' and 'parameters' keys)
        """
        self._create_messages(self.possible_actions, self.sut_state)
        
        function_schemas = [{
            "name": "select_next_action",
            "description": "Select the next action to take from the available options",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "The name of the action to take"
                    },
                    "parameters": {
                        "type": "object",
                        "description": "Parameters required for the action"
                    },
                    "test_intention": {
                        "type": "string",
                        "description": "The purpose of doing this action"
                    }
                },
                "required": ["action", "parameters", "test_intention"]
            }
        }, {
            "name": "test_done",
            "description": (
                "Call this when the test should end, either due to success "
                "or failure"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "result": {
                        "type": "string",
                        "enum": ["successful", "failed"],
                        "description": "Whether the test passed or failed"
                    },
                    "conclusion": {
                        "type": "string",
                        "description": "Explanation of why the test ended"
                    }
                },
                "required": ["result", "conclusion"]
            }
        }]
        
        response = self.openai_client.create_chat_completion(
            function_schema=function_schemas,
            action_history=self.action_history
        )
        
        try:
            return (
                response['name'],
                json.loads(response['arguments'])
            )
        except json.JSONDecodeError as e:
            error_msg = f"Failed to parse AI response as JSON: {response['arguments']}"
            raise ValueError(error_msg) from e
    
    def _create_messages(self, possible_actions, sut_state):
        actions_description = "\n".join(
            f"- {action_name}: {action_info['description']}" 
            for action_name, action_info in possible_actions.items()
        )
        
        if sut_state:
            self.openai_client.append_message(
                "system",
                f"Current system state:\n{json.dumps(sut_state, indent=2)}"
            )
        
        self.openai_client.append_message(
            "user",
            "Given these possible actions, choose the next action to take "
            "and specify any required parameters.\n\n"
            f"Available Actions:\n{actions_description}\n\n"
            "Call test_done if you spot any errors, consider the test goal "
            "is achieved, or if there are no possible actions available. "
            "Otherwise, respond by selecting the next action using "
            "select_next_action.\n"
        )
        
        return []  # Return empty list since messages are handled by OpenAIClient
    