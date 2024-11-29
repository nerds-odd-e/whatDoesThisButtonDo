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
            tuple: (function_name, dict with action details)
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
    "name": "assertion_for_regression",
    "description": "Make an assertion about the current state before proceeding.",
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["assert_state"],
                "description": "The assertion to make"
            },
            "parameters": {
                "type": "object",
                "description": "Parameters for the assertion",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": (
                            "JSON path to the element to assert "
                            "(e.g., 'user.name.first')"
                        )
                    },
                    "condition": {
                        "type": "string",
                        "enum": [
                            "equals", 
                            "not_equals", 
                            "contains", 
                            "not_contains", 
                            "matches_regex"
                        ],
                        "description": "The condition to check"
                    },
                    "value": {
                        "type": "string",
                        "description": "The expected value or pattern"
                    }
                },
                "required": ["path", "condition", "value"]
            },
            "assertion_purpose": {
                "type": "string",
                "description": "Why this assertion is important for the test"
            }
        },
        "required": ["action", "parameters", "assertion_purpose"]
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
        ) or "No actions available in current state"
        
        if sut_state:
            self.openai_client.append_message(
                "system",
                f"Current system state:\n{json.dumps(sut_state, indent=2)}"
            )
        
        message = (
    "At this state in the test, you have:\n"
    f"# Available Actions:\n{actions_description}\n\n"
    "# Available Assertions:\n"
    "- assert_state: Verify a condition on a specific part of the state.\n"
    "  * 'path': JSON path to the element to check (e.g., 'processes[0].stderr' for\n"
    "    first process output, 'error' for error messages).\n"
    "  * 'condition': One of ['equals', 'not_equals', 'contains',\n"
    "    'not_contains', 'matches_regex'].\n"
    "  * 'value': The expected value or pattern.\n"
    "  * For CLI output, use 'matches_regex' with (?s).* to match\n"
    "    across multiple lines.\n"
    "  * Example:\n"
    "    action: 'assert_state'\n"
    "    parameters:\n"
    "      path: 'processes[0].stderr'\n"
    "      condition: 'matches_regex'\n"
    "      value: '(?s).*required: oracle_dir.*'\n\n"
    "Given these available actions and assertions, you can:\n"
    "1. Make assertions about the current state using assertion_for_regression.\n"
    "2. Choose the next action using select_next_action (ONLY from the Available\n"
    "   Actions list above).\n"
    "3. End the test using test_done.\n\n"
    "Important: Make only one function call at a time. The next action MUST be chosen\n"
    "from the Available Actions list above - if no actions are available, you can\n"
    "only make assertions or call test_done. Add assertions only when they provide\n"
    "meaningful validation of critical application state - avoid assertions that are\n"
    "too sensitive to unrelated changes or when the test has just started. Don't\n"
    "repeat the last assertion. Call test_done if you spot any errors, consider the\n"
    "test goal is achieved, or if there are no possible actions available.\n"
)

        self.openai_client.append_message("user", message)
        return []
    