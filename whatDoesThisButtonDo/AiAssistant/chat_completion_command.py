from typing import List, Dict

from whatDoesThisButtonDo.AiAssistant.openai_client import OpenAIClient

class ChatCompletionCommand:
    def __init__(self, openai_client: 'OpenAIClient', messages: List[Dict[str, str]]):
        self.openai_client = openai_client
        self.messages = messages
    
    def execute(self) -> str:
        return self.openai_client.create_chat_completion(self.messages) 