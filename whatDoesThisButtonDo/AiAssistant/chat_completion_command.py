
class ChatCompletionCommand:
    def __init__(self, openai_client, messages):
        self.openai_client = openai_client
        self.messages = messages
    
    def execute(self):
        return self.openai_client.create_chat_completion(self.messages) 