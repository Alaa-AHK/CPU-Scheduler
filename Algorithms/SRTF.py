from Logic.scheduler import Scheduler
from Logic.process import Process
from typing import Optional

class SRTFScheduler(Scheduler):
    def __init__(self):
        super().__init__("Shortest Job First (Preemptive)")

    def get_next_process(self, current_time) -> Optional[Process]:
        ready_processes = self.get_arrived_processes(current_time)

        ready_processes.sort(key=lambda process: (process.get_burst_time(), process.get_arrival_time(), process.get_pid()))
        if not ready_processes:
            return self.current_process if self.current_process else None
        
        first_ready_process = ready_processes[0]
        next_process = first_ready_process
        # Compare between the current and the first ready processes
        if self.current_process and not self.current_process.is_completed() and self.current_process.get_remaining_time() <= first_ready_process.get_remaining_time():
            next_process = self.current_process

        return next_process
    