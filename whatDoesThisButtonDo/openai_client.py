import os
from openai import OpenAI
from typing import List, Dict
import json
from abc import ABC, abstractmethod

class OpenAIClient:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = OpenAI(api_key=api_key)

    def create_chat_completion(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict],
        tool_choice: Dict[str, any],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> any:
        return self.client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            temperature=temperature,
            max_tokens=max_tokens
        )

class ChatCompletionCommand(ABC):
    @abstractmethod
    def execute(self) -> List[str]:
        pass

class GenerateTestCasesCommand(ChatCompletionCommand):
    def __init__(self, openai_client: OpenAIClient, test_oracles: List[Dict[str, str]]):
        self.openai_client = openai_client
        self.test_oracles = test_oracles

    def execute(self) -> List[str]:
        tools = self._get_tools()
        messages = self._create_messages()
        response = self.openai_client.create_chat_completion(
            messages=messages,
            tools=tools,
            tool_choice={"type": "function", "function": {"name": "add_test_cases"}},
        )
        return self._extract_test_cases(response)

    def _get_tools(self) -> List[Dict]:
        return [{
            "type": "function",
            "function": {
                "name": "add_test_cases",
                "description": (
                    "Add all test cases to the collection, ordered from highest to "
                    "lowest priority"
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "test_cases": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "description": {
                                        "type": "string",
                                        "description": (
                                            "Detailed description of the test case"
                                        )
                                    },
                                    "priority": {
                                        "type": "string",
                                        "enum": ["high", "medium", "low"],
                                        "description": "Priority level of the test case"
                                    }
                                },
                                "required": ["description", "priority"]
                            },
                            "description": (
                                "Array of prioritized test cases, ordered from "
                                "highest to lowest priority"
                            )
                        }
                    },
                    "required": ["test_cases"]
                }
            }
        }]

    def _create_messages(self) -> List[Dict[str, str]]:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a testing expert that specializes in exploratory testing. "
                    "Your role is to analyze test oracle documents and perform testing "
                    "tasks based on user requests."
                )
            }
        ]
        
        for oracle in self.test_oracles:
            content = (
                f"Here's a test oracle document named '{oracle['name']}':\n\n"
                f"{oracle['content']}"
            )
            messages.append({"role": "user", "content": content})
        
        messages.append({
            "role": "user",
            "content": (
                "Based on these test oracle documents, please generate a "
                "comprehensive list of test cases. Please prioritize test cases "
                "based on their importance, with highest priority given to core "
                "functionality, security, and data integrity tests."
            )
        })
        
        return messages

    def _extract_test_cases(self, response: any) -> List[str]:
        test_cases = []
        for choice in response.choices:
            if choice.message.tool_calls:
                for tool_call in choice.message.tool_calls:
                    if tool_call.function.name == "add_test_cases":
                        args = json.loads(tool_call.function.arguments)
                        test_cases.extend(
                            case["description"] for case in args["test_cases"]
                        )
        return test_cases

class OpenAITestGenerator:
    def __init__(self):
        self.openai_client = OpenAIClient()

    def generate_test_cases(self, test_oracles: List[Dict[str, str]]) -> List[str]:
        command = GenerateTestCasesCommand(self.openai_client, test_oracles)
        return command.execute() 