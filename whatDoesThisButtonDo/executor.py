from typing import Any, Dict, Optional, TYPE_CHECKING
from .test_sandbox import TestSandbox
from .test_scope import TestScope

if TYPE_CHECKING:
    from .executor_factory import ExecutorFactory

class Executor:
    """
    Responsible for executing tests and managing the test environment.
    Based on the domain model, Executor runs tests and manages the test sandbox.
    """
    
    def __init__(self, sandbox: TestSandbox):
        """
        Initialize Executor with a configured sandbox.
        
        Args:
            sandbox: Configured TestSandbox instance
        """
        self.sandbox = sandbox
        self.current_scope: Optional[TestScope] = None
        
    @classmethod
    def create(cls) -> 'ExecutorFactory':
        """
        Factory method to start building an Executor instance.
        
        Returns:
            ExecutorFactory instance for configuring the Executor
        """
        from .executor_factory import ExecutorFactory
        return ExecutorFactory()
    
    def set_scope(self, scope: TestScope) -> None:
        """Sets the test scope for execution"""
        self.current_scope = scope
        
    def reset_environment(self) -> None:
        """Resets the test environment to its initial state"""
        self.sandbox.reset()
        
    def execute_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a single test action in the sandbox environment.
        
        Args:
            action: Dictionary containing action details and parameters
            
        Returns:
            Dictionary containing the results of the action execution
        """
        if not self.current_scope:
            raise ValueError("Test scope must be set before execution")
            
        return self.sandbox.execute(action)
    
    def get_current_state(self) -> Dict[str, Any]:
        """Returns the current state of the application under test"""
        return self.sandbox.get_state() 