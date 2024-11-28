import os
from openai import OpenAI

class OpenAIClient:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = OpenAI(api_key=api_key)
        
    def create_chat_completion(self, messages, model="gpt-3.5-turbo", temperature=0.7):
        """
        Create a chat completion using the OpenAI API
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