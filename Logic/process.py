from Core import Execution
from typing import Optional


class Process:
    """
    Represents a process in the CPU scheduler simulation.
    """

    def __init__(self, pid: int, name: str, arrival_time: int, burst_time: int, priority=None ):
        if burst_time <= 0:
            raise ValueError(f"burst_time must be > 0, got {burst_time}")
        if arrival_time < 0:
            raise ValueError(f"arrival_time must be >= 0, got {arrival_time}")

        self.__pid: int = pid
        self.__name: str = name
        self.__arrival_time: int = arrival_time
        self.__burst_time: int = burst_time
        self.__priority: Optional[int] = priority
        self.__remaining_time: int = burst_time
        self.__start_time: Optional[int] = None
        self.__completion_time: Optional[int] = None
        self.__waiting_time: int = 0
        self.__turnaround_time: int = 0
        self.__response_time: Optional[int] = None
        self.__execution_history: list[Execution] = list()

    def reset(self):
        """Reset the process state for a new simulation."""
        self.__remaining_time = self.__burst_time
        self.__start_time = None
        self.__completion_time = None
        self.__waiting_time = 0
        self.__turnaround_time = 0
        self.__response_time = None
        self.__execution_history = list()

    def is_completed(self):
        """Check if the process has completed execution."""
        return self.__remaining_time <= 0

    def calculate_turnaround_time(self):
        """Calculate and set the turnaround time."""
        if self.__completion_time is not None:
            self.__turnaround_time = self.__completion_time - self.__arrival_time

    def calculate_waiting_time(self):
        if self.__turnaround_time is not None:
            self.__waiting_time = self.__turnaround_time - self.__burst_time

    def execute(self, current_time: int, time_quantum: int = 1) -> int:
        if self.is_completed():
            return 0

        if self.__start_time is None:
            self.__start_time = current_time

        if self.__response_time is None:
            self.__response_time = current_time - self.__arrival_time

        execution_time = min(self.__remaining_time, time_quantum)
        self.__remaining_time -= execution_time

        self.__execution_history.append(
            Execution(start_time=current_time, end_time=current_time + execution_time)
        )

        if self.is_completed():
            self.__completion_time = current_time + execution_time
            self.calculate_turnaround_time()
            self.calculate_waiting_time()

        return execution_time

    def clone(self):
        """Create a fresh clone of this process with no runtime state."""
        return Process(
            pid=self.__pid,
            name=self.__name,
            arrival_time=self.__arrival_time,
            burst_time=self.__burst_time,
            priority=self.__priority,
        )



    def get_pid(self) -> int:
        return self.__pid

    def get_name(self) -> str:
        return self.__name

    def get_start_time(self) -> Optional[int]:
        return self.__start_time

    def get_arrival_time(self) -> int:
        return self.__arrival_time

    def get_waiting_time(self) -> int:
        return self.__waiting_time

    def get_turnaround_time(self) -> int:
        return self.__turnaround_time

    def get_completion_time(self) -> Optional[int]:
        return self.__completion_time

    def get_response_time(self) -> Optional[int]:
        return self.__response_time

    def get_execution_history(self) -> list[Execution]:
        return self.__execution_history

    def get_priority(self) -> Optional[int]:
        return self.__priority

    def get_burst_time(self) -> int:
        return self.__burst_time

    def get_remaining_time(self) -> int:
        return self.__remaining_time


    def get_progress(self) -> float:

        return (self.__burst_time - self.__remaining_time) / self.__burst_time

    def has_started(self) -> bool:
        """Returns True if the process has received CPU time at least once."""
        return self.__start_time is not None

    def __str__(self):
        """Human-readable string representation for debugging."""
        status = (
            "COMPLETED"
            if self.is_completed()
            else f"RUNNING ({self.__remaining_time}/{self.__burst_time})"
        )
        output = [
            f"Process {self.__pid} ({self.__name}):",
            f"  Status:         {status}",
            f"  Arrival time:   {self.__arrival_time}",
            f"  Burst time:     {self.__burst_time}",
            f"  Priority:       {self.__priority}",
            f"  Waiting time:   {self.__waiting_time}",
            f"  Turnaround:     {self.__turnaround_time}",
            f"  Response time:  {self.__response_time}",
        ]
        return "\n".join(output)


    def __repr__(self) -> str:
        """Short representation useful when printing lists of processes."""
        return (
            f"Process(pid={self.__pid}, name='{self.__name}', "
            f"burst={self.__burst_time}, remaining={self.__remaining_time}, "
            f"arrival={self.__arrival_time})"
        )
