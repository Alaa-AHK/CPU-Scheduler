class Execution:
    def __init__(self, start_time: int, end_time: int):
        """
        Raises:
            ValueError: If start_time is negative or end_time <= start_time
        """
      
        if start_time < 0:
            raise ValueError(f"start_time must be >= 0, got {start_time}")
        if end_time <= start_time:
            raise ValueError(
                f"end_time must be > start_time, got end={end_time}, start={start_time}"
            )

        self.__start_time: int = start_time
        self.__end_time: int = end_time

    def duration(self) -> int:
        """Returns how long this execution slice lasted."""
        return self.__end_time - self.__start_time

    def get_start_time(self) -> int:
        return self.__start_time

    def set_start_time(self, start_time: int) -> None:
        if start_time < 0:
            raise ValueError(f"start_time must be >= 0, got {start_time}")
        if start_time >= self.__end_time:
            raise ValueError(
                f"start_time must be < end_time ({self.__end_time}), got {start_time}"
            )
        self.__start_time = start_time

    def get_end_time(self) -> int:
        return self.__end_time

    def set_end_time(self, end_time: int) -> None:
        if end_time <= self.__start_time:
            raise ValueError(
                f"end_time must be > start_time ({self.__start_time}), got {end_time}"
            )
        self.__end_time = end_time
    def overlaps(self, other: "Execution") -> bool:
        """
        Checks if this execution slice overlaps in time with another one.
        """
        return self.__start_time < other.get_end_time() and self.__end_time > other.get_start_time()
    def contains(self, time_point: int) -> bool:
        """
        Returns True if the given time point falls within this execution slice.
        """
        return self.__start_time <= time_point < self.__end_time
    def __eq__(self, other: object) -> bool:
        """Two executions are equal if they cover the exact same time range."""
        if not isinstance(other, Execution):
            return False
        return self.__start_time == other.get_start_time() and self.__end_time == other.get_end_time()

    def __str__(self) -> str:
        """Human-readable format for debugging."""
        return f"Execution[{self.__start_time} → {self.__end_time}] (duration={self.duration()})"

    def __repr__(self) -> str:
        return f"Execution(start={self.__start_time}, end={self.__end_time})"
