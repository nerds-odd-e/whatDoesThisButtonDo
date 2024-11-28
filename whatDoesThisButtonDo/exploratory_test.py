from typing import Any, Dict, List
from .AiAssistant import AiAssistant
from .executor import Executor

class ExploratoryTest:
    """
    Manages exploratory testing sessions with AI assistance.
    Based on the domain model, ExploratoryTest coordinates between
    AI Assistant and Executor to perform intelligent exploration.
    """
    
    def __init__(self, executor: Executor, ai_assistant: AiAssistant):
        self.executor = executor
        self.ai_assistant = ai_assistant
        self.test_history: List[Dict[str, Any]] = []
        self.findings: List[Dict[str, Any]] = []
        self.understood_oracles: Dict[str, Any] = {}
        
    def start_exploration(self, test_oracles: List[str]) -> None:
        """
        Initiates an exploratory testing session.
        
        Args:
            test_oracles: List of test oracle descriptions or rules
        """
        # Reset environment before starting
        self.executor.reset_environment()
        
        # Have AI understand the test oracles and store them
        self.understood_oracles = (
            self.ai_assistant.understand_test_oracles(test_oracles)
        )
        self.test_history = []
        self.findings = []
        
    def execute_next_step(self) -> Dict[str, Any]:
        """
        Executes the next test step as suggested by the AI assistant.
        
        Returns:
            Dictionary containing the results of the test step
        """
        # Get current state
        current_state = self.executor.get_current_state()
        
        # Add understood oracles to the context for AI decision making
        context = {
            "current_state": current_state,
            "test_history": self.test_history,
            "understood_oracles": self.understood_oracles
        }
        
        # Get AI suggestion for next action with full context
        next_action = self.ai_assistant.suggest_next_action(
            current_state=context["current_state"], 
            test_history=context["test_history"]
        )
        
        # Execute the suggested action
        result = self.executor.execute_action(next_action)
        
        # Analyze results
        analysis = self.ai_assistant.analyze_findings(result)
        
        # Update history and findings
        self.test_history.append({
            "action": next_action,
            "result": result,
            "analysis": analysis
        })
        
        if analysis.get("issues"):
            self.findings.extend(analysis["issues"])
            
        return result
    
    def get_findings(self) -> List[Dict[str, Any]]:
        """Returns all findings from the exploratory testing session"""
        return self.findings