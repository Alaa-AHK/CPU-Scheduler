from typing import List, Optional
from Algorithms import Scheduler, Process

class FCFSScheduler(Scheduler):
    def __init__(self):
        super().__init__("First-Come, First-Served (FCFS)")

    def get_next_process(self, current_time) -> Optional[Process]:
        ready_processes = self.get_arrived_processes(current_time)

        if not ready_processes:
            return None

        ready_processes.sort(key=lambda process: (process.get_arrival_time(), process.get_pid()))
        return ready_processes[0]
