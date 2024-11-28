from multiprocessing import Process, Queue
from whatDoesThisButtonDo.cli import CommandLineApplication
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

def _run_cli(queue):
    """Run the CLI application in a separate process"""
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
        "success": success,
        "stdout": stdout.getvalue(),
        "stderr": stderr.getvalue(),
        "returncode": 0 if success else 1
    })

def run_cli():
    """
    Start the CLI application in a separate process and collect its output.
    
    Returns:
        Dict containing the command output and execution status
    """
    queue = Queue()
    p = None
    try:
        p = Process(target=_run_cli, args=(queue,))
        p.start()
        p.join(timeout=5)  # Add timeout to prevent hanging
        
        if p.is_alive():
            p.terminate()
            p.join()  # Wait for termination
            raise TimeoutError("Process took too long to complete")
            
        result = queue.get_nowait()  # Non-blocking get
        return result
        
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "returncode": -1
        }
    finally:
        # Clean up resources
        if p and p.is_alive():
            p.terminate()
            p.join()
        queue.close()
        queue.join_thread()

if __name__ == "__main__":
    result = run_cli()
    print("Execution Results:")
    print(f"Success: {result['success']}")
    print(f"Return Code: {result['returncode']}")
    print("\nStandard Output:")
    print(result['stdout'] or "(no output)")
    print("\nStandard Error:")
    print(result['stderr'] or "(no errors)") 