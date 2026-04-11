import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from Logic.process import Process
from Algorithms.round_robin import RoundRobin
from Algorithms.PNPSJF import PriorityNonPreemptive
from Algorithms.PPSJF import PriorityPreemptive
from Algorithms.SJF import SJFScheduler
from Algorithms.SRTF import SRTFScheduler
from Algorithms.FCFS import FCFSScheduler
from Logic.simulation import Simulation

def print_processes(processes):
    print(f"\n  {'Name':<6} {'Arrival':<10} {'Burst':<8} {'Priority':<10}")
    print(f"  {'-'*34}")
    for p in processes:
        pri = p.get_priority() if p.get_priority() is not None else "N/A"
        print(f"  {p.get_name():<6} {p.get_arrival_time():<10} "
              f"{p.get_burst_time():<8} {str(pri):<10}")

def print_results(scheduler):
    print(f"\n  {'Name':<6} {'Waiting':<10} {'Turnaround':<12}")
    print(f"  {'-'*28}")
    for p in scheduler.get_processes():
        print(f"  {p.get_name():<6} {p.get_waiting_time():<10} "
              f"{p.get_turnaround_time():<12}")

    avg_wt, avg_tat = scheduler.calculate_metrics()
    print(f"\n  Avg Waiting Time:    {avg_wt:.2f}")
    print(f"  Avg Turnaround Time: {avg_tat:.2f}")
    print()

def run_test(scheduler, processes, live=False):
    print("=" * 50)
    mode = "LIVE" if live else "INSTANT"
    print(f"  TEST: {scheduler.name} [{mode} MODE]")
    print("=" * 50)

    simulation = Simulation(scheduler, delay=1.0)

    for p in processes:
        simulation.add_process(p)

    # Print processes
    processes = scheduler.get_processes()
    print_processes(processes)

    # Run
    simulation.start()
    print(f"\n  {'Time':<6} {'Process':<10} {'Remaining':<12}")
    print(f"  {'-'*28}")

    for process in simulation._run_simulation(useDelay=live):
        time = scheduler.get_current_time()
        if process:
            print(f"  {time:<6} {process.get_name():<10} "
                  f"{process.get_remaining_time():<12}")
        else:
            print(f"  {time:<6} {'IDLE':<10}")

    # Results
    print_results(scheduler)


def get_test_cases():
    test_1 = [
        Process(pid=1, name="P1", arrival_time=0, burst_time=8, priority=3),
        Process(pid=2, name="P2", arrival_time=1, burst_time=4, priority=2),
        Process(pid=3, name="P3", arrival_time=2, burst_time=2, priority=1),
        Process(pid=4, name="P4", arrival_time=3, burst_time=4, priority=4),
    ]

    test_2 = [
        Process(pid=1, name="P1", arrival_time=0, burst_time=4),
        Process(pid=2, name="P2", arrival_time=1, burst_time=3),
        Process(pid=3, name="P3", arrival_time=6, burst_time=2),
        Process(pid=4, name="P4", arrival_time=3, burst_time=3),
    ]

    return test_1

# Define Tests
def test_round_robin(live=False):
    scheduler = RoundRobin(quantum=2)
    processes = get_test_cases()
    run_test(scheduler, processes, live)

def test_priority_np(live=False):
    scheduler = PriorityNonPreemptive()
    processes = get_test_cases()
    run_test(scheduler, processes, live)

def test_priority_p(live=False):
    scheduler = PriorityPreemptive()
    processes = get_test_cases()
    run_test(scheduler, processes, live)

def test_FCFS(live=False):
    scheduler = FCFSScheduler()
    processes = get_test_cases()
    run_test(scheduler, processes, live)

def test_SJF(live=False):
    scheduler = SJFScheduler()
    processes = get_test_cases()
    run_test(scheduler, processes, live)

def test_SRTF(live=False):
    scheduler = SRTFScheduler()
    processes = get_test_cases()
    run_test(scheduler, processes, live)

def menu():
    while True:
        print("\n" + "=" * 50)
        print("  CPU Scheduler Tester")
        print("=" * 50)
        print("  1. Round Robin")
        print("  2. Priority Non-Preemptive")
        print("  3. Priority Preemptive")
        print("  4. First Come First Served")
        print("  5. Shortest Job First")
        print("  6. Preemptive Shortest Job First (SRTF)")
        print("  7. Run All")
        print("  0. Exit")
        print("=" * 50)

        choice = input("  Choose algorithm (0-7): ").strip()
        if choice == "0":
            print("  Goodbye! 👋")
            break

        mode = input("  Live mode? (y/n): ").strip().lower()
        live = mode == "y"

        if choice == "1":
            test_round_robin(live)
        elif choice == "2":
            test_priority_np(live)
        elif choice == "3":
            test_priority_p(live)
        elif choice == "4":
            test_FCFS(live)        
        elif choice == "5":
            test_SJF(live)        
        elif choice == "6":
            test_SRTF(live)
        elif choice == "7":
            test_round_robin(live)
            test_priority_np(live)
            test_priority_p(live)
            test_FCFS(live)        
            test_SJF(live)        
            test_SRTF(live)
        else:
            print("  Invalid choice! Try again.")


if __name__ == "__main__":
    menu()