from scheduler import Scheduler
from process import Process
from typing import Optional


class PriorityPreemptive(Scheduler):

    def __init__(self):
        super().__init__("Priority Preemptive")

    def _get_highest_priority(self, current_time):
        arrived = self.get_arrived_processes(current_time)

        if not arrived:
            return None

        best = arrived[0]
        for p in arrived:
            if p.get_priority() < best.get_priority():
                best = p
        return best

    def get_next_process(self, current_time) -> Optional[Process]:
        next_proc = self._get_highest_priority(current_time)
        return next_proc