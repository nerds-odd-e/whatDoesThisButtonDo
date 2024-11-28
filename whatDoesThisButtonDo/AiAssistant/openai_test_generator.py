from .openai_client import OpenAIClient
from .generate_test_cases_command import GenerateTestCasesCommand

class OpenAITestGenerator:
    def __init__(self, test_oracles):
        self.openai_client = OpenAIClient()
        self.test_oracles = test_oracles

    def generate_test_cases(self):
        command = GenerateTestCasesCommand(self.openai_client, self.test_oracles)
        return command.execute() 