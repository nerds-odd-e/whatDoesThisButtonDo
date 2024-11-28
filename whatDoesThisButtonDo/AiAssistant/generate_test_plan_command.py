from .chat_completion_command import ChatCompletionCommand

class GenerateTestPlanCommand(ChatCompletionCommand):
    def __init__(self, openai_client, test_case, test_oracles):
        messages = self._create_messages(test_case, test_oracles)
        super().__init__(openai_client, messages)
    
    def _create_messages(self, test_case, test_oracles):
        # Combine all test oracle content
        combined_content = "\n".join(oracle['content'] for oracle in test_oracles)
        
        prompt = (
            "Based on the following test oracles and test case, "
            "generate a detailed test plan:\n\n"
            f"Test Oracles:\n{combined_content}\n\n"
            f"Test Case:\n{test_case}"
        )
        
        return [
            {"role": "system", "content": "You are a helpful test plan generator."},
            {"role": "user", "content": prompt}
        ] 