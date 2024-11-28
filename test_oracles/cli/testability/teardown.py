from multiprocessing.queues import Empty
from test_oracles.cli.testability.process_manager import process_manager

def teardown():
    """
    Stop all running CLI processes and clean up resources.
    """
    for process, queue in process_manager.get_processes():
        try:
            if process.is_alive():
                process.terminate()
                process.join(timeout=5)
                
                # Force kill if still alive
                if process.is_alive():
                    process.kill()
                    process.join()
            
            # Try to get any remaining output
            while True:
                try:
                    if queue.empty():
                        break
                    queue.get_nowait()
                except Empty:
                    # Queue is empty (race condition between empty() and get_nowait())
                    pass
                
        finally:
            try:
                queue.close()
                queue.cancel_join_thread()
            except (AttributeError, IOError, OSError):
                pass
            
            process_manager.remove_process(process) 