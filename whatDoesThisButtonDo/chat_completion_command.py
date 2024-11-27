from abc import ABC, abstractmethod
from typing import List

class ChatCompletionCommand(ABC):
    @abstractmethod
    def execute(self) -> List[str]:
        pass 