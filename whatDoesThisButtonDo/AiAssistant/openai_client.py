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
        function_schema: dict = None,
        model: str = "gpt-3.5-turbo", 
        temperature: float = 0.7
    ) -> str:
        """
        Create a chat completion using the OpenAI API with function calling

        Args:
            user_message: The user's message content as a string
            function_schema: Optional function definition for tool calling
            model: The OpenAI model to use
            temperature: Controls randomness in the response (0.0-1.0)

        Returns:
            str: The function call arguments as a JSON string

        Raises:
            Exception: If there's an error creating the chat completion
        """
        messages = [
            self.system_message,
            {"role": "assistant", "content": self.test_oracles.as_assistant_message()},
            {"role": "user", "content": user_message}
        ]
        
        try:
            # Add tools if function schema is provided
            kwargs = {
                "model": model,
                "messages": messages,
                "temperature": temperature
            }
            
            if function_schema:
                kwargs["tools"] = [{
                    "type": "function",
                    "function": function_schema
                }]
                tool_choice = {
                    "type": "function",
                    "function": {"name": function_schema["name"]}
                }
                kwargs["tool_choice"] = tool_choice
                
            response = self.client.chat.completions.create(**kwargs)
            
            # Handle function calling response
            if function_schema and response.choices[0].message.tool_calls:
                tool_call = response.choices[0].message.tool_calls[0]
                return tool_call.function.arguments
                
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Error creating chat completion: {str(e)}") 