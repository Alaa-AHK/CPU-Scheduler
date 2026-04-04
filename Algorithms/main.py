from process import Process
from scheduler import Scheduler
from execution import Execution
from simulation import Simulation
from typing import Optional


# ========================================
# A Dummy Scheduler Just For Testing
# (Simple FCFS — picks first arrived process)
# ========================================
class DummyScheduler(Scheduler):
    def __init__(self):
        super().__init__("Dummy FCFS")

    def get_next_process(self, current_time) -> Optional[Process]:
        arrived = self.get_arrived_processes(current_time)
        if not arrived:
            return None
        # Just pick the first arrived process
        return arrived[0]


# ========================================
# Test 1: Process Class
# ========================================
def test_process():
    print("=" * 40)
    print("TEST 1: Process Class")
    print("=" * 40)

    p = Process(pid=1, name="P1", arrival_time=0, burst_time=5, priority=2)

    print(f"Name: {p.get_name()}")
    print(f"PID: {p.get_pid()}")
    print(f"Arrival: {p.get_arrival_time()}")
    print(f"Burst: {p.get_burst_time()}")
    print(f"Priority: {p.get_priority()}")
    print(f"Remaining: {p.get_remaining_time()}")
    print(f"Is Completed: {p.is_completed()}")

    # Manually execute for 3 time units
    time_used = p.execute(current_time=0, time_quantum=3)
    print(f"\nAfter executing for {time_used} units:")
    print(f"Remaining: {p.get_remaining_time()}")
    print(f"Is Completed: {p.is_completed()}")

    # Execute remaining 2 units
    time_used = p.execute(current_time=3, time_quantum=3)
    print(f"\nAfter executing for {time_used} more units:")
    print(f"Remaining: {p.get_remaining_time()}")
    print(f"Is Completed: {p.is_completed()}")
    print(f"Waiting Time: {p.get_waiting_time()}")
    print(f"Turnaround Time: {p.get_turnaround_time()}")

    print()


# ========================================
# Test 2: Execution Class
# ========================================
def test_execution():
    print("=" * 40)
    print("TEST 2: Execution Class")
    print("=" * 40)

    e = Execution(start_time=0, end_time=3)
    print(f"Start: {e.get_start_time()}")
    print(f"End: {e.get_end_time()}")
    print(f"Duration: {e.duration()}")

    print()


# ========================================
# Test 3: Scheduler (using DummyScheduler)
# ========================================
def test_scheduler():
    print("=" * 40)
    print("TEST 3: Scheduler")
    print("=" * 40)

    scheduler = DummyScheduler()

    # Add processes
    scheduler.add_process(Process(pid=1, name="P1", arrival_time=0, burst_time=3))
    scheduler.add_process(Process(pid=2, name="P2", arrival_time=1, burst_time=4))
    scheduler.add_process(Process(pid=3, name="P3", arrival_time=2, burst_time=2))
    scheduler.add_process(Process(pid=4, name="P4", arrival_time=1, burst_time=1))

    # Print all processes
    print("Processes added:")
    for p in scheduler.get_processes():
        print(f"  {p.get_name()} | Arrival: {p.get_arrival_time()} | Burst: {p.get_burst_time()}")

    # Run tick by tick manually
    print("\nRunning tick by tick:")
    while not scheduler.all_processes_completed():
        process = scheduler.run_tick()
        if process:
            print(f"  Time {scheduler.get_current_time()}: "
                  f"{process.get_name()} running | "
                  f"Remaining: {process.get_remaining_time()}")
        else:
            print(f"  Time {scheduler.get_current_time()}: CPU Idle")

    # Print results
    print(f"\nAvg Waiting Time: {scheduler.get_average_waiting_time():.2f}")
    print(f"Avg Turnaround Time: {scheduler.get_average_turnaround_time():.2f}")

    print()


# ========================================
# Test 4: Simulation (No Delay for testing)
# ========================================
def test_simulation():
    print("=" * 40)
    print("TEST 4: Simulation")
    print("=" * 40)

    scheduler = DummyScheduler()
    simulation = Simulation(scheduler, delay=1.0)

    # Add processes
    simulation.add_process(Process(pid=1, name="P1", arrival_time=0, burst_time=3))
    simulation.add_process(Process(pid=2, name="P2", arrival_time=1, burst_time=2))

    # Start simulation
    simulation.start()
    print(f"Simulation running: {simulation.is_running()}")

    # Run without delay (useDelay=False)
    print("\nRunning simulation:")
    for process in simulation._run_simulation(useDelay=False):
        if process:
            print(f"  {process.get_name()} | "
                  f"Remaining: {process.get_remaining_time()}")
        else:
            print("  CPU Idle")

    # Results
    print(f"\nSimulation running: {simulation.is_running()}")
    print(f"Has results: {simulation.has_results()}")
    avg_wt, avg_tat = scheduler.calculate_metrics()
    print(f"Avg Waiting Time: {avg_wt:.2f}")
    print(f"Avg Turnaround Time: {avg_tat:.2f}")

    print()


# ========================================
# Run All Tests
# ========================================
if __name__ == "__main__":
    test_process()
    test_execution()
    test_scheduler()
    test_simulation()