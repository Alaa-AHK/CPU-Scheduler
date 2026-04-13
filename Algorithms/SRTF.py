from Logic.scheduler import Scheduler
from Logic.process import Process
from typing import Optional

class SRTFScheduler(Scheduler):
    def __init__(self):
        super().__init__("Shortest Job First (Preemptive)")

    def get_next_process(self, current_time: int) -> Optional[Process]:
        ready_processes = self.get_arrived_processes(current_time)

        if not ready_processes:
            return self.current_process if not self.current_process.is_completed() else None

        ready_processes.sort(key=lambda p: (
            p.get_remaining_time(),
            p.get_arrival_time(),
            p.get_pid()
        ))

        shortest_ready = ready_processes[0]

        if self.current_process and not self.current_process.is_completed():
            current_is_shorter_or_equal = (
                self.current_process.get_remaining_time() <= shortest_ready.get_remaining_time()
            )
            return self.current_process if current_is_shorter_or_equal else shortest_ready

        return shortest_ready