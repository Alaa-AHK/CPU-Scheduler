from typing import List, Optional
from Logic.scheduler import Scheduler
from Logic.process import Process

class SJFScheduler(Scheduler):
    def __init__(self):
        super().__init__("Shortest Job First (Non-Preemptive)")

    def get_next_process(self, current_time) -> Optional[Process]:
        if self.current_process and not self.current_process.is_completed():
            return self.current_process

        ready_processes = self.get_arrived_processes(current_time)
        if not ready_processes:
            return None
    
        # Sort list by burst time
        # If two processes have same SJT, process the first
        # If two processes have same arrival_time, process the lower pid
        ready_processes.sort(key=lambda process: (process.get_burst_time(), process.get_arrival_time(), process.get_pid()))
        return ready_processes[0]
