class AIExploratoryTestAssistant:
    def __init__(self, test_oracles, api_key: str, model: str):
        self.test_oracles = test_oracles
        self.api_key = api_key
        self.model = model

    def create_test_execution_thread(self, goal):
        """
        Creates a new AI assistant thread for handling test interactions
        
        Args:
            goal: Dictionary containing test goal information
        
        Returns:
            AIAssistantThread: A new thread instance for test execution
        """
        from .ai_test_execution_thread import AITestExecutionThread
        return AITestExecutionThread(
            test_oracles=self.test_oracles,
            api_key=self.api_key,
            model=self.model,
            goal=goal
        ) 