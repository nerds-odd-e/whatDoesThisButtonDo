
class AIExploratoryTestAssistant:
    def __init__(self, test_oracles, api_key: str, model: str):
        self.test_oracles = test_oracles
        self.api_key = api_key
        self.model = model

    def create_thread(self):
        """
        Creates a new AI assistant thread for handling test interactions
        
        Returns:
            AIAssistantThread: A new thread instance for test execution
        """
        from .ai_assistant_thread import AIAssistantThread
        return AIAssistantThread(
            test_oracles=self.test_oracles,
            api_key=self.api_key,
            model=self.model
        ) 