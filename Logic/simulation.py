import time
from Logic.process import Process  #src.models.process
from Logic.scheduler import Scheduler    # src.core.scheduler 
import threading

# Simulation is the top-level controller that the GUI talks to.
# It wraps the scheduler and owns the simulation loop — it's the piece
class Simulation:
    def __init__(self, scheduler: Scheduler, delay: float = 1.0):
        self.scheduler = scheduler
        self.delay = delay        # Seconds between ticks. Default is 1.0 (real-time, 1 unit = 1 second)
        self.running = False      # Flipped to True when the user hits Start
        self.paused = False       # Toggled by the pause/resume button
        self.processes_timeline = []


    # ─── Process Management ───────────────────────────────────────────────────

    def add_process(self, process: Process):
        # Just passes the process down to the scheduler.
        self.scheduler.add_process(process)

    def add_live_process(
        self, name: str, burst_time: int, priority: int, pid: int
    ) -> Process:
        # This is the "add while running" feature. 
        # Instead of asking the user for an arrival time, we use the current simulation time automatically — so the process joins the ready queue  on the very next tick without any extra input from the user.
        current_time = self.scheduler.get_current_time()

        process = Process(
            pid=pid,
            name=name,
            arrival_time=current_time,  # Arrives right now, at this moment in the simulation
            burst_time=burst_time,
            priority=priority,
        )
        self.add_process(process)

        return process

    def remove_process(self, pid: int):
        # Delegates removal down to the scheduler, which handles cleaning up the process from all internal lists.
        self.scheduler.remove_process(pid)


    # ─── Simulation Control ───────────────────────────────────────────────────

    def reset(self):
        # Wipes everything — resets the scheduler clock and restores
        self.scheduler.hard_reset()

    def is_running(self) -> bool:
        # The GUI checks this to know whether the simulation is currently active.
        return self.running

    def start(self):
        # Called when the user clicks "Start". Marks the simulation as running and makes sure it's not stuck in a paused state from before.
        self.running = True
        self.paused = False

    def is_paused(self) -> bool:
        # The GUI checks this to decide whether to show "Resume" or "Pause".
        return self.paused

    def set_paused(self, paused: bool):
        # Toggles the pause state. The simulation loop checks this flag each tick to decide whether to keep going or hold.
        self.paused = paused

    def set_speed(self, speed_factor: int):
        # Adjusts how fast the simulation runs by changing the delay between ticks.
        # Speed 1x → 1.0s delay (real time)
        # Speed 2x → 0.5s delay
        # Speed 4x → 0.25s delay
        # Speed 0 or below → near-instant (0.001s), used as a safe lower bound
        if speed_factor <= 0:
            self.delay = 0.001
        else:
            self.delay = 1.0 / speed_factor


    # ─── Simulation Loop ──────────────────────────────────────────────────────

    def _run_simulation(self, useDelay: bool = True):
        # Instead of running the whole simulation at once and blocking everything, it runs one tick at a time and hands the result back to whoever called it (the GUI), which then updates the Gantt chart and the table before  coming back for the next tick.
        # Setting useDelay=False skips the sleep entirely, giving instant results.
        # That's the "At-Once" mode — same logic, just no waiting between ticks.

        # print("Starting tick loop")
        while (self.running) and (not self.scheduler.all_processes_completed()):
            # print("Running Tick...")
            current_process = self.scheduler.run_tick()

            if useDelay:
                # Wait one real second (or however long the delay is set to) before moving to the next tick — this is what creates the live feel.
                time.sleep(self.delay)

            # print("Yielding current process")
            # Hand the current state back to the GUI so it can update the visuals.
            # Execution will resume here on the next iteration.
            yield current_process
            # print("After yield")

        # Loop ended — either the user stopped it or all processes finished.
        self.running = False
        return self.running
    

    