from scheduler import Scheduler
from process import Process
from typing import Optional
from collections import deque


class RoundRobin(Scheduler):

    def __init__(self, quantum: int):
        super().__init__("Round Robin")
        self.quantum = quantum
        self.ready_queue = deque()
        self.current_quantum_used = 0

    def _add_new_arrivals(self, current_time):
        for p in self.processes:
            if (
                p.get_arrival_time() <= current_time
                and not p.is_completed()
                and p not in self.ready_queue
                and p is not self.current_process
            ):
                self.ready_queue.append(p)

    def get_next_process(self, current_time) -> Optional[Process]:

        self._add_new_arrivals(current_time)
        if self.current_process is not None:

            if self.current_process.is_completed():
                self.current_process = None
                self.current_quantum_used = 0

            elif self.current_quantum_used >= self.quantum:
                self.ready_queue.append(self.current_process)
                self.current_process = None
                self.current_quantum_used = 0

            else:
                self.current_quantum_used += 1
                return self.current_process

        if self.ready_queue:
            next_proc = self.ready_queue.popleft()
            self.current_quantum_used = 1
            return next_proc

        return None

    def reset(self):
        super().reset()
        self.ready_queue = deque()
        self.current_quantum_used = 0