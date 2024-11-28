import os
from openai import OpenAI
from ..test_oracles import TestOracles

class OpenAIClient:
    def __init__(self, test_oracles: TestOracles):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = OpenAI(api_key=api_key)
        self.test_oracles = test_oracles
        self.system_message = {
            "role": "system",
            "content": (
                "You are an expert in testing software applications. "
                "You are given a list of test oracles to help you "
                "understand the system under test and the expected testing rules. "
                "There will also be requirements the system must meet. "
            )
        }
        
    def create_chat_completion(
        self, 
        user_message: str,
        model: str = "gpt-3.5-turbo", 
        temperature: float = 0.7
    ) -> str:
        """
        Create a chat completion using the OpenAI API

        Args:
            user_message: The user's message content as a string
            model: The OpenAI model to use
            temperature: Controls randomness in the response (0.0-1.0)

        Returns:
            str: The generated response text

        Raises:
            Exception: If there's an error creating the chat completion
        """
        messages = [
            self.system_message,
            {"role": "user", "content": user_message}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Error creating chat completion: {str(e)}") 