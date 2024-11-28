"""
whatDoesThisButtonDo package
"""
from .AiAssistant.ai_exploratory_test_assistant import AIExploratoryTestAssistant
from .AiAssistant.openai_client import OpenAIClient

__all__ = [
    'OpenAIClient',
    'AIExploratoryTestAssistant'
]

__version__ = "0.0.1" 