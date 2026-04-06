from abc import ABC, abstractmethod
from typing import List, Optional
from Core import Process  #src.models.process 


# Every scheduling algorithm in this project inherits from this class.
class Scheduler(ABC):

    def __init__(self, name):
        self.name = name
        self.time_slice = 1  # How many time units a process runs per tick. Round Robin will override this.
        self.processes: list[Process] = list()
        self.current_time = 0
        self.current_process: Optional[Process] = None  # Whatever is currently on the CPU (None if idle)
        self.completed_processes: list[Process] = list()


    # ─── Process Management ───────────────────────────────────────────────────

    def add_process(self, process: Process) -> None:        # Add a single process to the scheduler's list.
        self.processes.append(process)

    def add_processes(self, processes: list[Process]) -> None:  
        self.processes.extend(processes)

    def get_processes(self) -> list[Process]:
        # Returns the full list of processes, including ones still running and ones already completed.
        return self.processes


    # ─── Reset ────────────────────────────────────────────────────────────────

    def reset(self):
        self.current_time = 0
        self.current_process = None
        self.completed_processes = list()

    def hard_reset(self):
        self.reset()
        for process in self.processes:
            process.reset()


    # ─── Clock & Queue ────────────────────────────────────────────────────────

    def get_current_time(self) -> int:
        # Returns where the simulation clock currently stands.
        return self.current_time

    def all_processes_completed(self) -> bool:
        # Returns True only when every single process has finished running.
        return all(process.is_completed() for process in self.processes)

    def get_arrived_processes(self, current_time) -> List[Process]: # Ready queue 
        # Every algorithm calls this to get the list of candidates for the next tick.
        return [
            p
            for p in self.processes
            if (p.get_arrival_time() <= current_time) and (not p.is_completed())
        ]


    # ─── Metrics ──────────────────────────────────────────────────────────────

    def get_average_waiting_time(self):
        # Adds up the waiting time of every process and divides by the total count.
        # Returns 0 if there are no processes, to avoid a division-by-zero crash.
        if not self.processes:
            return 0.0
        sum_waiting_time = 0
        for process in self.processes:
            sum_waiting_time += process.get_waiting_time()
        no_of_processes = len(self.processes)
        return sum_waiting_time / no_of_processes

    def get_average_turnaround_time(self):
        # Same idea as waiting time above — sum all turnaround times and average them.
        if not self.processes:
            return 0.0
        sum_turnaround_time = 0
        for process in self.processes:
            sum_turnaround_time += process.get_turnaround_time()
        no_of_processes = len(self.processes)
        return sum_turnaround_time / no_of_processes
    
    def get_average_response_time(self):
            # Response time is only meaningful for processes that have already started,
            # so we filter to those first before calculating the average.
            responded = [p for p in self.processes if p.get_response_time() is not None]
            if not responded:
                return 0.0
            return sum(responded) / len(responded)


    def calculate_metrics(self):
        # One convenient call that returns both averages as a tuple.
        # The GUI calls this at the end of the simulation to display the final stats.
        return (self.get_average_waiting_time(), self.get_average_turnaround_time())

   


    # ─── Process Lookup & Removal ─────────────────────────────────────────────

    def find_proccess_by_pid(self, pid: int) -> Optional[Process]:
        # Walks through the process list looking for a matching PID.
        # Returns the process if found, or None if nothing matches.
        for process in self.processes:
            if process.get_pid() == pid:
                return process
        return None

    def remove_process(self, pid: int) -> None:
        # Finds the process by PID first, then removes it from both lists it might
        # appear in — the main process list and the completed list.
        process = self.find_proccess_by_pid(pid)
        if process in self.processes:
            self.processes.remove(process)
            if process in self.completed_processes:
                self.completed_processes.remove(process)


    # ─── Core Abstract Method ─────────────────────────────────────────────────

    @abstractmethod
    def get_next_process(self, current_time) -> Optional[Process]:
        # This is the only method each algorithm MUST implement on its own.
        pass


    # ─── Tick ─────────────────────────────────────────────────────────────────

    def run_tick(self) -> Process:
        # This is the heartbeat of the scheduler — it runs once every second.
        # It asks the algorithm who goes next, runs that process for one time unit,
        # checks if it finished, then advances the clock.

        print("getting next process")
        next_process = self.get_next_process(self.current_time)

        time_used = self.time_slice  # Default time used — may be less if process finishes early
        print("inside tick")

        if next_process:
            self.current_process = next_process
            # execute() returns how much time was actually used,
            time_used = self.current_process.execute(self.current_time, self.time_slice)

            if self.current_process.is_completed():
                # Move it to the completed list so metrics can be read later
                self.completed_processes.append(self.current_process)
        else:
            # No process is ready yet — CPU is idle this tick
            self.current_process = None

        # Always advance the clock, whether the CPU was busy or idle
        self.current_time += time_used

        return self.current_process

