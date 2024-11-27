import os
from openai import OpenAI
from typing import List, Dict

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