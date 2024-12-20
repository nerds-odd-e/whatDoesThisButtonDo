from test_oracles.cli.testability.run_cli import run_cli

def start():
    """
    Initialize the test oracle by returning the available actions.
    
    Returns:
        Dict containing the status and list of available actions
    """
    return {
        "status": "ready",
        "actions": [run_cli]
    } 