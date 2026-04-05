from scheduler import Scheduler
from process import Process
from typing import Optional


class PriorityNonPreemptive(Scheduler):

    def __init__(self):
        super().__init__("Priority Non-Preemptive")

    def _get_highest_priority(self, current_time):
        arrived = self.get_arrived_processes(current_time)

        if not arrived:
            return None

        highest_prior = arrived[0]
        for p in arrived:
            if p.get_priority() < highest_prior.get_priority():
                highest_prior = p
        return highest_prior

    def get_next_process(self, current_time) -> Optional[Process]:

        if self.current_process is not None:
            if self.current_process.is_completed():
                self.current_process = None

            else:
                return self.current_process

        next_proc = self._get_highest_priority(current_time)
        return next_proc