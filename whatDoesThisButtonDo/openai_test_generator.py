from typing import List, Dict
from .openai_client import OpenAIClient
from .generate_test_cases_command import GenerateTestCasesCommand

class OpenAITestGenerator:
    def __init__(self):
        self.openai_client = OpenAIClient()

    def generate_test_cases(self, test_oracles: List[Dict[str, str]]) -> List[str]:
        command = GenerateTestCasesCommand(self.openai_client, test_oracles)
        return command.execute() 