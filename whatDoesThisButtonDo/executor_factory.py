from typing import Any, Dict

from whatDoesThisButtonDo.testable_sandbox import TestableSandbox
from .executor import Executor

class ExecutorFactory:
    """
    Factory class for creating and configuring Executor instances.
    Handles the creation and setup of test environments and scopes.
    """
    
    def __init__(self):
        self._testable_sandbox = None
        self._sandbox_config: Dict[str, Any] = {}
        
    def with_sandbox(self, 
                    testable_sandbox: TestableSandbox, 
                    config: Dict[str, Any] = None) -> 'ExecutorFactory':
        """
        Configures the testable sandbox and its configuration.
        
        Args:
            testable_sandbox: The TestableSandbox instance to use
            config: Configuration parameters for the sandbox
            
        Returns:
            self for method chaining
        """
        self._testable_sandbox = testable_sandbox
        self._sandbox_config = config or {}
        return self
        
    def build(self) -> Executor:
        """
        Creates and returns a configured Executor instance.
        
        Returns:
            Configured Executor instance
            
        Raises:
            ValueError: If required configurations are missing
        """
        if not self._testable_sandbox:
            raise ValueError("Testable sandbox must be configured before building")
            
        return Executor(self._testable_sandbox, self._sandbox_config) 