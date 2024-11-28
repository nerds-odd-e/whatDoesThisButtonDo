from .chat_completion_command import ChatCompletionCommand

class GenerateTestCasesCommand(ChatCompletionCommand):
    def __init__(self, openai_client, test_oracles):
        messages = self._create_messages(test_oracles)
        super().__init__(openai_client, messages)
    
    def _create_messages(self, test_oracles):
        # Combine all test oracle content
        combined_content = "\n".join(oracle['content'] for oracle in test_oracles)
        
        prompt = (
            "Based on the following test oracles, generate a list of test cases:"
            f"\n\n{combined_content}"
        )
        
        return [
            {"role": "system", "content": "You are a helpful test case generator."},
            {"role": "user", "content": prompt}
        ]
    
    def execute(self):
        response = super().execute()
        # Split the response into individual test cases
        test_cases = [case.strip() for case in response.split('\n') if case.strip()]
        return test_cases 