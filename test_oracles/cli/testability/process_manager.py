class ProcessManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProcessManager, cls).__new__(cls)
            cls._instance._running_processes = []
        return cls._instance
    
    def add_process(self, process, queue):
        self._running_processes.append((process, queue))
        
    def get_processes(self):
        return self._running_processes
        
    def clear_processes(self):
        self._running_processes.clear()

# Global instance
process_manager = ProcessManager() 