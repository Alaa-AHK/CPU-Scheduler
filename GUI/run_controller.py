from PyQt5.QtCore import QObject, QThread, pyqtSignal

from Logic.process import Process
from Logic.simulation import Simulation

from Algorithms.FCFS import FCFSScheduler
from Algorithms.SJF import SJFScheduler
from Algorithms.SRTF import SRTFScheduler
from Algorithms.PNPSJF import PriorityNonPreemptive
from Algorithms.PPSJF import PriorityPreemptive
from Algorithms.round_robin import RoundRobin


class Worker(QObject):
    sig_tick = pyqtSignal(object, int, int)
    sig_done = pyqtSignal()

    def __init__(self, simulation: Simulation, use_delay: bool):
        super().__init__()
        self.sim = simulation
        self.use_delay = use_delay

    def run(self):
        prev = 0

        for p in self.sim._run_simulation(useDelay=self.use_delay):
            now = self.sim.scheduler.get_current_time()
            self.sig_tick.emit(p, prev, now)
            prev = now

        self.sig_done.emit()



class RunController(QObject):

    sig_tick = pyqtSignal(object, int, int)
    sig_done = pyqtSignal()
    sig_status = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.sim = None
        self.worker = None
        self.thread = None


    @staticmethod
    def make_scheduler(algo: str, quantum: int = 2):
        if algo == "FCFS":
            return FCFSScheduler()
        elif algo == "SJF (Non-Preemptive)":
            return SJFScheduler()
        elif algo == "SRTF (Preemptive SJF)":
            return SRTFScheduler()
        elif algo == "Priority (Non-Preemptive)":
            return PriorityNonPreemptive()
        elif algo == "Priority (Preemptive)":
            return PriorityPreemptive()
        elif algo == "Round Robin":
            return RoundRobin(quantum=quantum)

        raise ValueError("Unknown algorithm")


    def run_live(self, scheduler, process_dicts: list, speed: int = 1):
        self._setup(scheduler, process_dicts, speed)
        self.sig_status.emit("running live")
        self._launch(use_delay=True)

    def run_at_once(self, scheduler, process_dicts: list, speed: int = 1):
        self._setup(scheduler, process_dicts, speed)
        self.sig_status.emit("running instant")
        self._launch(use_delay=False)


    def _setup(self, scheduler, process_dicts: list, speed: int):

        for d in process_dicts:
            p = Process(
                pid=d["pid"],
                name=d["name"],
                arrival_time=d["arrival"],
                burst_time=d["burst"],
                priority=d.get("priority"),
            )
            scheduler.add_process(p)

        self.sim = Simulation(scheduler)
        self.sim.set_speed(speed)
        self.sim.start()


    def _launch(self, use_delay: bool):

        self.thread = QThread()
        self.worker = Worker(self.sim, use_delay)

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)

        self.worker.sig_tick.connect(self.sig_tick)
        self.worker.sig_done.connect(self._on_done)
        self.worker.sig_done.connect(self.thread.quit)

        self.thread.start()


    def pause(self):
        if self.sim:
            self.sim.set_paused(True)
        self.sig_status.emit("paused")

    def resume(self):
        if self.sim:
            self.sim.set_paused(False)
        self.sig_status.emit("running")


    def stop(self):
        if self.sim:
            self.sim.running = False

        if self.thread and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait(2000)

        self.sig_status.emit("stopped")


    def inject_process(self, name: str, burst: int, priority: int, pid: int):

        if not self.is_running():
            return

        self.sim.add_live_process(
            name=name,
            burst_time=burst,
            priority=priority,
            pid=pid
        )

        t = self.sim.scheduler.get_current_time()
        self.sig_status.emit(f"injected {name} at t={t}")

    def is_running(self) -> bool:
        return self.sim is not None and self.sim.is_running()

    def get_scheduler(self):
        return self.sim.scheduler if self.sim else None

    def _on_done(self):
        self.sig_done.emit()
        self.sig_status.emit("finished")