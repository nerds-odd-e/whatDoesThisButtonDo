from openai import OpenAI
from ..test_oracles import TestOracles

class OpenAIClient:
    def __init__(self, test_oracles: TestOracles, api_key: str, model: str):
        if not api_key:
            raise ValueError("API key cannot be empty")
        self.client = OpenAI(api_key=api_key)
        self.test_oracles = test_oracles
        self.model = model
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
        messages: list,
        function_schema: dict = None,
        action_history: list = None
    ) -> str:
        """
        Create a chat completion using the OpenAI API with function calling

        Args:
            messages: List of message objects with role and content
            function_schema: Optional function definition for tool calling
            action_history: List of previous actions and their results

        Returns:
            str: The function call arguments as a JSON string

        Raises:
            Exception: If there's an error creating the chat completion
        """
        chat_messages = [
            self.system_message,
            {"role": "assistant", "content": self.test_oracles.as_assistant_message()},
        ]
        
        # Add function messages for action history
        if action_history:
            for entry in action_history:
                chat_messages.append({
                    "role": "function",
                    "name": entry["function_name"],
                    "content": str({
                        "action": entry["action"],
                        "status": entry["status"]
                    })
                })
        
        # Add the provided messages
        chat_messages.extend(messages)
        
        try:
            # Add tools if function schema is provided
            kwargs = {
                "model": self.model,
                "messages": chat_messages,
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