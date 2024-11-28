"""
AiAssistant package for handling AI-related functionality.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List

class AiAssistant(ABC):
    """
    Abstract base class for AI Assistant implementations.
    Based on the domain model, AI Assistant helps understand test oracles
    and assists in exploratory testing.
    """
    
    @abstractmethod
    def understand_test_oracles(self, test_oracles: List[str]) -> Dict[str, Any]:
        """
        Analyzes and understands the test oracles provided.
        
        Args:
            test_oracles: List of test oracle descriptions or rules
            
        Returns:
            Dictionary containing the understood test criteria and constraints
        """
        pass
    
    @abstractmethod
    def suggest_next_action(self, current_state: Dict[str, Any], 
                          test_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Suggests the next testing action based on current state and history.
        
        Args:
            current_state: Current application state
            test_history: History of previous test actions and results
            
        Returns:
            Dictionary containing the suggested next action and its parameters
        """
        pass
    
    @abstractmethod
    def analyze_findings(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes test results to identify potential issues or insights.
        
        Args:
            test_results: Results from the latest test execution
            
        Returns:
            Dictionary containing analysis results including potential bugs,
            missing requirements, or suspicious behaviors
        """
        pass 