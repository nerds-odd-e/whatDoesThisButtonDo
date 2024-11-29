from openai import OpenAI
from ..test_oracles import TestOracles

class OpenAIClient:
    def __init__(self, test_oracles: TestOracles, api_key: str, model: str):
        if not api_key:
            raise ValueError("API key cannot be empty")
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.messages = [{
            "role": "system",
            "content": (
                "You are an expert in testing software applications. "
                "You are given a list of test oracles to help you "
                "understand the system under test and the expected testing rules. "
                "There will also be requirements the system must meet. "
            )
        }]
        # Add test oracles message
        self.append_message("assistant", test_oracles.as_assistant_message())

    def append_message(self, role: str, content: str):
        """Add a new message to the conversation history"""
        self.messages.append({"role": role, "content": content})

    def create_chat_completion(
        self, 
        function_schema: list = None,
        action_history: list = None
    ) -> dict:
        """
        Create a chat completion using the OpenAI API with function calling

        Args:
            function_schema: Optional function definition for tool calling
            action_history: List of previous actions and their results

        Returns:
            dict: The tool call arguments as a JSON string

        Raises:
            Exception: If there's an error creating chat completion
        """
        chat_messages = self.messages.copy()
        
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
        
        try:
            kwargs = {
                "model": self.model,
                "messages": chat_messages,
            }
            
            if function_schema:
                kwargs["tools"] = [
                    {"type": "function", "function": schema}
                    for schema in function_schema
                ]
                if len(function_schema) == 1:
                    tool_choice = {
                        "type": "function",
                        "function": {"name": function_schema[0]["name"]}
                    }
                    kwargs["tool_choice"] = tool_choice
                
            response = self.client.chat.completions.create(**kwargs)
            
            if function_schema and response.choices[0].message.tool_calls:
                tool_call = response.choices[0].message.tool_calls[0]
                return {
                    'name': tool_call.function.name,
                    'arguments': tool_call.function.arguments
                }
                
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Error creating chat completion: {str(e)}") 