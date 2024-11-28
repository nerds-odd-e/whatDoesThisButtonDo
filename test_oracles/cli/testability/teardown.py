from test_oracles.cli.testability.process_manager import process_manager
from queue import Empty

def teardown():
    """
    Stop all running CLI processes and clean up resources.
    
    Returns:
        Dict containing the final status of all terminated processes
    """
    results = []
    
    for process, queue in process_manager.get_processes():
        if process.is_alive():
            process.terminate()
            process.join(timeout=5)
            
            # Force kill if still alive
            if process.is_alive():
                process.kill()
                process.join()
        
        # Try to get any remaining output
        try:
            while not queue.empty():
                results.append(queue.get_nowait())
        except Empty:
            # Queue might become empty between empty() check and get_nowait()
            pass
            
        queue.close()
        queue.join_thread()
    
    process_manager.clear_processes()
    
    return {
        "status": "completed",
        "terminated_processes": len(results),
        "process_results": results
    } 