import json
from typing import List, Dict
from .chat_completion_command import ChatCompletionCommand
from .openai_client import OpenAIClient

class GenerateTestPlanCommand(ChatCompletionCommand):
    def __init__(
        self,
        openai_client: OpenAIClient,
        test_case: str,
        test_oracles: List[Dict[str, str]],
    ):
        self.openai_client = openai_client
        self.test_case = test_case
        self.test_oracles = test_oracles

    def execute(self) -> str:
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "generate_test_plan",
                    "description": (
                        "Generate a detailed test plan for the given test case"
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "test_plan": {
                                "type": "string",
                                "description": (
                                    "Detailed test plan including steps, "
                                    "prerequisites, and expected results"
                                )
                            }
                        },
                        "required": ["test_plan"]
                    }
                }
            }
        ]

        tool_choice = {"type": "function", "function": {"name": "generate_test_plan"}}

        response = self.openai_client.create_chat_completion(
            user_message=(
                f"Generate a test plan for this test case:\n"
                f"{self.test_case}"
            ),
            tools=tools,
            tool_choice=tool_choice,
            test_oracles=self.test_oracles
        )

        function_call = response.choices[0].message.tool_calls[0].function
        test_plan = json.loads(function_call.arguments)["test_plan"]

        return test_plan 