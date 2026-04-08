from Logic.scheduler import Scheduler
from Logic.process import Process
from typing import Optional

class SRTFScheduler(Scheduler):
    def __init__(self):
        super().__init__("Shortest Job First (Preemptive)")

    def get_next_process(self, current_time) -> Optional[Process]:
        ready_processes = self.arrived_processes(current_time)

        ready_processes.sort(key=lambda process: (process.get_burst_time(), process.get_arrival_time(), process.get_pid()))
        if not ready_processes:
            return self.current_process if self.current_process else None

        next_process = ready_processes[0] if (ready_processes[0].burst_time < self.current_process.burst_time) else self.current_process
        return next_process
    