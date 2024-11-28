from typing import List, Dict
import os
from openai import OpenAI

class OpenAIClient:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = OpenAI(api_key=api_key)
        
    def create_chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "gpt-3.5-turbo", 
        temperature: float = 0.7
    ) -> str:
        """
        Create a chat completion using the OpenAI API

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            model: The OpenAI model to use
            temperature: Controls randomness in the response (0.0-1.0)

        Returns:
            str: The generated response text

        Raises:
            Exception: If there's an error creating the chat completion
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Error creating chat completion: {str(e)}") 