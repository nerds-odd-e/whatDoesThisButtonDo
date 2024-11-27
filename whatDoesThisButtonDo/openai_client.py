import os
from openai import OpenAI
from typing import List, Dict

class OpenAITestGenerator:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = OpenAI(api_key=api_key)
    
    def generate_test_cases(self, test_oracles: List[Dict[str, str]]) -> List[str]:
        """
        Generates test cases using OpenAI chat completion API.
        
        Args:
            test_oracles: List of dictionaries containing test oracle content
                         Each dict should have 'name' and 'content' keys
            
        Returns:
            List of generated test cases
        """
        # Prepare messages for the chat
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a test case generator. Your role is to analyze test "
                    "oracle documents and generate comprehensive test cases. Please "
                    "prioritize test cases based on their importance, with highest "
                    "priority given to core functionality, security, and data "
                    "integrity tests."
                )
            }
        ]
        
        # Add test oracles as assistant messages
        for oracle in test_oracles:
            messages.append({
                "role": "user",
                "content": (
                    f"Here's a test oracle document named '{oracle['name']}':\n\n"
                    f"{oracle['content']}"
                )
            })
        
        # Add final user request
        messages.append({
            "role": "user",
            "content": (
                "Based on these test oracle documents, please generate a comprehensive "
                "list of test cases."
            )
        })
        
        # Update the API call to use function calling
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            tools=[{
                "type": "function",
                "function": {
                    "name": "add_test_cases",
                    "description": (
                        "Add all test cases to the collection, ordered from "
                        "highest to lowest priority"
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
                                                "Detailed description of the "
                                                "test case"
                                            )
                                        },
                                        "priority": {
                                            "type": "string",
                                            "enum": ["high", "medium", "low"],
                                            "description": (
                                                "Priority level of the test case"
                                            )
                                        }
                                    },
                                    "required": ["description", "priority"]
                                },
                                "description": (
                                    "Array of prioritized test cases, ordered "
                                    "from highest to lowest priority"
                                )
                            }
                        },
                        "required": ["test_cases"]
                    }
                }
            }],
            tool_choice={"type": "function", "function": {"name": "add_test_cases"}},
            temperature=0.7,
            max_tokens=2000
        )
        
        # Extract test cases from function calls
        test_cases = []
        for choice in response.choices:
            if choice.message.tool_calls:
                for tool_call in choice.message.tool_calls:
                    if tool_call.function.name == "add_test_cases":
                        import json
                        args = json.loads(tool_call.function.arguments)
                        # Extract just the descriptions, maintaining priority order
                        test_cases.extend(
                            case["description"] for case in args["test_cases"]
                        )
        
        return test_cases 