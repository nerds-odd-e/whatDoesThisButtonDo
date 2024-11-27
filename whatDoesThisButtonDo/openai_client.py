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
                    "output test cases in a clear, numbered format."
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
        
        # Get completion from OpenAI
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )
        
        # Extract and parse the response
        content = response.choices[0].message.content
        return self._parse_test_cases(content)
    
    def _parse_test_cases(self, content: str) -> List[str]:
        """
        Parse test cases from chat completion response.
        Splits the response by newline and numbers to separate test cases.
        """
        # Split content by newlines and filter out empty lines
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        test_cases = []
        current_test_case = []
        
        for line in lines:
            # If line starts with a number and period (e.g., "1.", "2.", etc.)
            if any(line.startswith(f"{i}.") for i in range(1, 100)):
                # If we have a previous test case, add it to the list
                if current_test_case:
                    test_cases.append('\n'.join(current_test_case))
                    current_test_case = []
                current_test_case.append(line)
            else:
                current_test_case.append(line)
        
        # Add the last test case if exists
        if current_test_case:
            test_cases.append('\n'.join(current_test_case))
        
        return test_cases 