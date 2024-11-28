from typing import Any, Dict, Optional, Type
from .executor import Executor
from .test_sandbox import TestSandbox
from .test_scope import TestScope

class ExecutorFactory:
    """
    Factory class for creating and configuring Executor instances.
    Handles the creation and setup of test environments and scopes.
    """
    
    def __init__(self):
        self._sandbox_class: Optional[Type[TestSandbox]] = None
        self._sandbox_config: Dict[str, Any] = {}
        self._scope: Optional[TestScope] = None
        
    def with_sandbox(self, 
                    sandbox_class: Type[TestSandbox], 
                    config: Dict[str, Any] = None) -> 'ExecutorFactory':
        """
        Configures the sandbox type and its configuration.
        
        Args:
            sandbox_class: The TestSandbox class to use
            config: Configuration parameters for the sandbox
            
        Returns:
            self for method chaining
        """
        self._sandbox_class = sandbox_class
        self._sandbox_config = config or {}
        return self
        
    def with_scope(self, scope: TestScope) -> 'ExecutorFactory':
        """
        Sets the test scope for the executor.
        
        Args:
            scope: TestScope instance defining the testing boundaries
            
        Returns:
            self for method chaining
        """
        self._scope = scope
        return self
        
    def build(self) -> Executor:
        """
        Creates and returns a configured Executor instance.
        
        Returns:
            Configured Executor instance
            
        Raises:
            ValueError: If required configurations are missing
        """
        if not self._sandbox_class:
            raise ValueError("Sandbox class must be configured before building")
            
        # Create sandbox instance with config
        sandbox = self._sandbox_class(**self._sandbox_config)
        
        # Create executor
        executor = Executor(sandbox)
        
        # Configure scope if provided
        if self._scope:
            executor.set_scope(self._scope)
            
        return executor 