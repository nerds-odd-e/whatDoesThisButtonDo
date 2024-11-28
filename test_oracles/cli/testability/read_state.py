from test_oracles.cli.testability.process_manager import process_manager
from queue import Empty

def read_state():
    """
    Read the current state of running CLI processes without stopping them.
    Collects any available output from the queues.
    
    Returns:
        Dict containing the current output state
    """
    results = []
    
    for process, queue in process_manager.get_processes():
        process_output = {
            "stdout": "",
            "stderr": "",
            "status": "running" if process.is_alive() else "terminated",
            "returncode": None
        }
        
        # Try to get any available output without blocking
        try:
            while not queue.empty():
                msg = queue.get_nowait()
                if msg.get("status") == "completed":
                    process_output.update({
                        "status": "completed",
                        "stdout": msg.get("stdout", ""),
                        "stderr": msg.get("stderr", ""),
                        "returncode": msg.get("returncode")
                    })
                elif msg.get("status") == "started":
                    # Skip the initial startup message
                    continue
        except Empty:
            pass
            
        results.append(process_output)
    
    return {
        "status": "success",
        "processes": results
    } 