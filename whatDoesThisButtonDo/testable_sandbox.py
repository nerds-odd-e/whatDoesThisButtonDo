from pathlib import Path
from typing import Optional

class TestableSandbox:
    """
    Represents a sandbox directory that contains testability features.
    """
    def __init__(self, path: Path):
        """
        Initialize a testable sandbox.
        
        Args:
            path: Path to the sandbox directory
        """
        self.path = path
        self.testability_dir = path / "testability"

    @property
    def name(self) -> str:
        """Get the name of the sandbox directory."""
        return self.path.name

    @property
    def is_valid(self) -> bool:
        """Check if this is a valid testable sandbox."""
        return self.testability_dir.is_dir()

    def start(self) -> dict:
        """
        Loads and executes the start function from the testability directory.
        
        Returns:
            A dictionary mapping function names to their documentation
        """
        import importlib.util
        import sys
        
        # Load the start.py module from testability directory
        start_path = self.testability_dir / "start.py"
        if not start_path.is_file():
            raise FileNotFoundError("start.py not found in testability directory")
            
        spec = importlib.util.spec_from_file_location("start", start_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["start"] = module
        spec.loader.exec_module(module)
        
        if not hasattr(module, "start"):
            raise AttributeError("start function not found in start.py")
            
        result = module.start()
        
        # Process the actions list into a dictionary of function documentation
        if not isinstance(result, dict) or 'actions' not in result:
            raise ValueError("start() must return a dict with 'actions' field")
            
        return {
            func.__name__: {'description': func.__doc__ or ''} 
            for func in result['actions']
        }

    @classmethod
    def create_if_valid(cls, path: Path) -> Optional['TestableSandbox']:
        """
        Factory method to create a TestableSandbox if the path is valid.
        
        Args:
            path: Path to check and create sandbox from
            
        Returns:
            TestableSandbox instance if valid, None otherwise
        """
        sandbox = cls(path)
        return sandbox if sandbox.is_valid else None 

    def execute_action(
        self, 
        action_name: str, 
        parameters: Optional[dict] = None
    ) -> dict:
        """
        Executes the specified action with given parameters from the testability 
        directory.
        
        Args:
            action_name: Name of the action function to execute
            parameters: Optional dictionary of parameters to pass to the action function
            
        Returns:
            A dictionary mapping function names to their documentation for next 
            possible actions
        """
        import importlib.util
        import sys
        
        # Add testability directory to Python path
        if str(self.testability_dir) not in sys.path:
            sys.path.insert(0, str(self.testability_dir))
        
        # Load the action module from testability directory
        action_path = self.testability_dir / f"{action_name}.py"
        if not action_path.is_file():
            raise FileNotFoundError(
                f"{action_name}.py not found in testability directory"
            )
            
        # Import the action module
        spec = importlib.util.spec_from_file_location(action_name, action_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[action_name] = module
        spec.loader.exec_module(module)
        
        # Get and execute the action function
        if not hasattr(module, action_name):
            raise AttributeError(
                f"Function {action_name} not found in {action_name}.py"
            )
            
        action_func = getattr(module, action_name)
        result = action_func(**(parameters or {}))
        
        # Process the next possible actions with better error handling
        if not isinstance(result, dict):
            raise ValueError(f"Action function must return a dict, got {type(result)}")
            
        if 'actions' not in result:
            # If no actions field, treat the result itself as the final state
            return {}  # No more actions available
            
        if not result['actions']:
            return {}  # Empty actions list means no more actions
            
        return {
            func.__name__: {'description': func.__doc__ or ''} 
            for func in result['actions']
        }

    def teardown(self) -> None:
        """
        Loads and executes the teardown function from the testability directory.
        """
        import importlib.util
        import sys
        
        # Load the teardown.py module from testability directory
        teardown_path = self.testability_dir / "teardown.py"
        if not teardown_path.is_file():
            raise FileNotFoundError("teardown.py not found in testability directory")
            
        spec = importlib.util.spec_from_file_location("teardown", teardown_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["teardown"] = module
        spec.loader.exec_module(module)
        
        if not hasattr(module, "teardown"):
            raise AttributeError("teardown function not found in teardown.py")
            
        module.teardown()