import json
from typing import List, Dict
from .chat_completion_command import ChatCompletionCommand
from .openai_client import OpenAIClient

class GenerateTestCasesCommand(ChatCompletionCommand):
    def __init__(self, openai_client: OpenAIClient, test_oracles: List[Dict[str, str]]):
        self.openai_client = openai_client
        self.test_oracles = test_oracles

    def execute(self) -> List[str]:
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "generate_test_cases",
                    "description": (
                        "Generate test cases based on the provided test oracles"
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "test_cases": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                },
                                "description": "List of generated test cases"
                            }
                        },
                        "required": ["test_cases"]
                    }
                }
            }
        ]

        tool_choice = {"type": "function", "function": {"name": "generate_test_cases"}}

        response = self.openai_client.create_chat_completion(
            user_message="Generate test cases based on the provided test oracles.",
            tools=tools,
            tool_choice=tool_choice,
            test_oracles=self.test_oracles
        )

        function_call = response.choices[0].message.tool_calls[0].function
        test_cases = json.loads(function_call.arguments)["test_cases"]

        return test_cases
