from multiprocessing import Process, Queue
from whatDoesThisButtonDo.cli import CommandLineApplication
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
from test_oracles.cli.testability.process_manager import process_manager

def _run_cli(queue, cli_args=None):
    """Run the CLI application in a separate process"""
    # Signal that process has started
    queue.put({"status": "started"})
    
    import sys
    if cli_args is not None:
        sys.argv = [sys.argv[0]] + cli_args  # Preserve program name and add new args
    else:
        sys.argv = [sys.argv[0]]  # Keep only the program name when no args provided
    
    stdout = StringIO()
    stderr = StringIO()
    success = True
    
    try:
        with redirect_stdout(stdout), redirect_stderr(stderr):
            app = CommandLineApplication()
            app.run()
    except SystemExit as e:
        success = (e.code == 0)
    except Exception as e:
        stderr.write(str(e))
        success = False
    
    queue.put({
        "status": "completed",
        "success": success,
        "stdout": stdout.getvalue(),
        "stderr": stderr.getvalue(),
        "returncode": 0 if success else 1
    })

def run_cli():
    """
    Start the CLI application.
    
    Returns:
        Dict containing empty initial state
    """
    queue = Queue()
    p = Process(target=_run_cli, args=(queue,))
    p.start()
    
    # Wait for process to signal it has started (with timeout)
    try:
        start_status = queue.get(timeout=10)  # 10 second timeout
        if start_status.get("status") != "started":
            raise RuntimeError("Process failed to start properly")
        process_manager.add_process(p, queue)
    except Exception as e:
        p.terminate()
        p.join()
        raise RuntimeError(f"Failed to start CLI process: {str(e)}")
    
    return {
        "status": "running",
        "actions": []
    } 