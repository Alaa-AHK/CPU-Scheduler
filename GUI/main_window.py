import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QSpinBox,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QLineEdit, QAbstractItemView
)
from PyQt5.QtCore import Qt

from GUI.gantt_widget import GanttChart
from GUI.run_controller import RunController

ALGOS = [
    "FCFS",
    "SJF (Non-Preemptive)",
    "SRTF (Preemptive SJF)",
    "Priority (Non-Preemptive)",
    "Priority (Preemptive)",
    "Round Robin",
]


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CPU Scheduler Simulator")
        self.resize(1050, 750)
        self.setStyleSheet("""
            QWidget {
                background-color: #F0F4F8;
                color: #2C3E50;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 0.5px;
                color: #2C3E50;
            }
            QPushButton {
                background-color: #8DABC4;
                color: #1A252F;
                font-size: 13px;
                font-weight: bold;
                border-radius: 6px;
                padding: 8px 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #A3BDD3;
            }
            QPushButton:pressed {
                background-color: #799AB5;
            }
            QPushButton:disabled {
                background-color: #BCCCDC;
                color: #7F8C8D;
            }
            QLineEdit, QSpinBox, QComboBox {
                background-color: #FFFFFF;
                border: 2px solid #D9E2EC;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 13px;
                color: #2C3E50;
            }
            QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
                border: 2px solid #8DABC4;
            }
            QComboBox::drop-down {
                border: none;
            }
            QTableWidget {
                background-color: #FFFFFF;
                alternate-background-color: #F8FAFC;
                border: 1px solid #D9E2EC;
                border-radius: 4px;
                gridline-color: #E4E7EB;
                font-size: 13px;
                color: #2C3E50;
            }
            QHeaderView::section {
                background-color: #E2EAF2;
                color: #2C3E50;
                font-weight: bold;
                padding: 6px;
                border: 1px solid #C5D4E3;
            }
            QTableWidget::item:selected {
                background-color: #ABC4DA;
                color: #1A252F;
            }
        """)

        self._process_store: list[dict] = []
        self._next_pid = 1
        self._controller: RunController = None
        self._sim_running = False

        self._build_ui()

    # ─── UI construction ──────────────────────────────────────────────────────

    def _on_algo_changed(self, text: str):
        is_round_robin = "Round Robin" in text
        is_priority_algo = "Priority" in text

        self.lblQuantum.setEnabled(is_round_robin)
        self.spinQuantum.setEnabled(is_round_robin)
        self.lblPriority.setEnabled(is_priority_algo)
        self.spinPriority.setEnabled(is_priority_algo)

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setSpacing(8)
        root.setContentsMargins(20, 20, 20, 20)

        # ── Row 1: algorithm + quantum + priority ─────────────────────────────
        row1 = QHBoxLayout()
        row1.setSpacing(8)

        row1.addWidget(QLabel("Choose an Algorithm:"))
        self.comboAlgo = QComboBox()
        self.comboAlgo.addItems(ALGOS)
        self.comboAlgo.currentTextChanged.connect(self._on_algo_changed)
        self.comboAlgo.setMinimumWidth(320)
        row1.addWidget(self.comboAlgo)
        row1.addSpacing(120)

        self.lblQuantum = QLabel("Quantum:")
        self.spinQuantum = QSpinBox()
        self.spinQuantum.setMinimum(1)
        self.spinQuantum.setMaximum(99)
        self.spinQuantum.setValue(1)
        self.spinQuantum.setFixedWidth(120)
        row1.addWidget(self.lblQuantum)
        row1.addWidget(self.spinQuantum)
        row1.addSpacing(10)

        self.lblPriority = QLabel("Priority:")
        self.spinPriority = QSpinBox()
        self.spinPriority.setMinimum(1)
        self.spinPriority.setMaximum(99)
        self.spinPriority.setValue(1)
        self.spinPriority.setFixedWidth(120)
        row1.addWidget(self.lblPriority)
        row1.addWidget(self.spinPriority)

        row1.addStretch()
        self._on_algo_changed(self.comboAlgo.currentText())

        root.addLayout(row1)

    #     row1.addWidget(QLabel("Speed:"))
    #     self.sliderSpeed = QSlider(Qt.Horizontal)
    #     self.sliderSpeed.setMinimum(1)
    #     self.sliderSpeed.setMaximum(8)
    #     self.sliderSpeed.setValue(1)
    #     self.sliderSpeed.setFixedWidth(80)
    #     self.sliderSpeed.valueChanged.connect(lambda v: self.lblSpeed.setText(f"{v}x"))
    #     row1.addWidget(self.sliderSpeed)
    #     self.lblSpeed = QLabel("1x")
    #     row1.addWidget(self.lblSpeed)

        row1.addStretch()
        self.lblStatus = QLabel("idle")
        row1.addWidget(self.lblStatus)


        # ── Row 2: process input form ─────────────────────────────────────────
        row2 = QHBoxLayout()
        row2.setSpacing(4)

        row2.addWidget(QLabel("Name:"))
        self.edtName = QLineEdit()
        self.edtName.setPlaceholderText("Process")
        self.edtName.setFixedWidth(120)
        row2.addWidget(self.edtName)
        row2.addSpacing(10)

        row2.addWidget(QLabel("Arrival:"))
        self.spinArrival = QSpinBox()
        self.spinArrival.setMinimum(0)
        self.spinArrival.setMaximum(9999)
        self.spinArrival.setFixedWidth(80)
        row2.addWidget(self.spinArrival)
        row2.addSpacing(10)

        row2.addWidget(QLabel("Burst:"))
        self.spinBurst = QSpinBox()
        self.spinBurst.setMinimum(1)
        self.spinBurst.setMaximum(9999)
        self.spinBurst.setValue(0)
        self.spinBurst.setFixedWidth(80)
        row2.addWidget(self.spinBurst)
        row2.addSpacing(150)


        self.btnAdd = QPushButton("Add Process")
        self.btnAdd.clicked.connect(self._on_add_process)
        row2.addWidget(self.btnAdd)
        row2.addSpacing(30)

        self.btnRemove = QPushButton("Remove Selected Process")
        self.btnRemove.clicked.connect(self._on_remove_process)
        row2.addWidget(self.btnRemove)
        row2.addSpacing(30)

        self.btnInject = QPushButton("Inject Live Process")
        self.btnInject.setEnabled(False)
        self.btnInject.setToolTip("Add a process at the current simulation time")
        self.btnInject.clicked.connect(self._on_inject_live)
        row2.addWidget(self.btnInject)

    #     row2.addStretch()
        root.addLayout(row2)

    #     # ── Row 3: run buttons ────────────────────────────────────────────────
        row3 = QHBoxLayout()

        self.btnRunLive = QPushButton("Run Live")
        self.btnRunOnce = QPushButton("Run At Once")
        self.btnPause   = QPushButton("Pause")
        self.btnReset   = QPushButton("Reset")

        self.btnPause.setEnabled(False)
        self.btnRunLive.clicked.connect(self._on_run_live)
        self.btnRunOnce.clicked.connect(self._on_run_at_once)
        self.btnPause.clicked.connect(self._on_pause_resume)
        self.btnReset.clicked.connect(self._on_reset)

        # Add Run Live and Run At Once to the left, Pause and Reset to the right
        row3.addWidget(self.btnRunLive)
        row3.addWidget(self.btnRunOnce)
        row3.addStretch()
        self.btnPause.setStyleSheet("background-color: #FFF9DB; color: #665c00; border-radius: 6px; padding: 8px 16px; border: none; font-weight: bold;")
        self.btnReset.setStyleSheet("background-color: #FFE5E5; color: #8B0000; border-radius: 6px; padding: 8px 16px; border: none; font-weight: bold;")
        row3.addWidget(self.btnPause)
        row3.addWidget(self.btnReset)
        root.addLayout(row3)

        # ── Table on top, Gantt + average info below ───────────────────────────
        root.addWidget(QLabel("Processes:"))
        self.procTable = QTableWidget(0, 5)
        self.procTable.setHorizontalHeaderLabels(["PID", "Name", "Arrival", "Burst", "Priority"])
        self.procTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.procTable.verticalHeader().setVisible(False)
        self.procTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.procTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        root.addWidget(self.procTable, 1)

        root.addWidget(QLabel("Gantt Chart:"))
        self.gantt = GanttChart()
        root.addWidget(self.gantt, 1)

        bottom_lay = QHBoxLayout()
        
        # Left side: Results
        res_lay = QVBoxLayout()
        res_lay.addWidget(QLabel("Results:"))
        self.metricsTable = QTableWidget(0, 4)
        self.metricsTable.setHorizontalHeaderLabels(
            ["Name", "Waiting", "Turnaround", "Response"]
        )
        self.metricsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.metricsTable.verticalHeader().setVisible(False)
        self.metricsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.metricsTable.setMaximumHeight(150)
        res_lay.addWidget(self.metricsTable)
        bottom_lay.addLayout(res_lay)
        
        # Right side: Remaining Time
        rem_lay = QVBoxLayout()
        rem_lay.addWidget(QLabel("Live Remaining Burst:"))
        self.remainingTable = QTableWidget(0, 3)
        self.remainingTable.setHorizontalHeaderLabels(["PID", "Name", "Remaining"])
        self.remainingTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.remainingTable.verticalHeader().setVisible(False)
        self.remainingTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.remainingTable.setMaximumHeight(150)
        rem_lay.addWidget(self.remainingTable)
        bottom_lay.addLayout(rem_lay)

        root.addLayout(bottom_lay)

        self.lblAvg = QLabel("Avg Waiting: —    Avg Turnaround: —    ")
        root.addWidget(self.lblAvg)

        self._on_algo_changed(self.comboAlgo.currentText())

    # ─── UI event handlers ────────────────────────────────────────────────────

    def _on_add_process(self):
        name     = self.edtName.text().strip() or f"P{self._next_pid}"
        priority = self.spinPriority.value() if "Priority" in self.comboAlgo.currentText() else None
        data = {
            "pid":      self._next_pid,
            "name":     name,
            "arrival":  self.spinArrival.value(),
            "burst":    self.spinBurst.value(),
            "priority": priority,
        }
        self._process_store.append(data)
        self._add_row_to_proc_table(data)
        self.edtName.clear()
        self._next_pid += 1

    def _on_remove_process(self):
        rows = self.procTable.selectionModel().selectedRows()
        if not rows:
            return
        row = rows[0].row()
        pid = int(self.procTable.item(row, 0).text())
        self.procTable.removeRow(row)
        self._process_store = [p for p in self._process_store if p["pid"] != pid]

    def _on_inject_live(self):
        if not self._controller or not self._sim_running:
            return
        
        current_time = self._controller.get_scheduler().get_current_time()
        
        name     = self.edtName.text().strip() or f"P{self._next_pid}"
        priority = self.spinPriority.value() if "Priority" in self.comboAlgo.currentText() else 0
        data = {
            "pid":      self._next_pid,
            "name":     name,
            "arrival":  current_time,
            "burst":    self.spinBurst.value(),
            "priority": priority,
        }
        self._process_store.append(data)
        self._add_row_to_proc_table(data, note=" (live)")
        self.edtName.clear()
        self._next_pid += 1
        self._controller.inject_process(
            name=data["name"], burst=data["burst"],
            priority=priority, pid=data["pid"],
        )

    def _on_run_live(self):
        if not self._process_store:

            self.lblStatus.setText("add processes first")

            return
        self._start_sim(live=True)

    def _on_run_at_once(self):
        if not self._process_store:

            self.lblStatus.setText("add processes first")

            return
        self._start_sim(live=False)

    def _on_pause_resume(self):
        if not self._controller:
            return
        if self.btnPause.text() == "Pause":
            self._controller.pause()
            self.btnPause.setText("Resume")
            if "Priority" in self.comboAlgo.currentText():
                self.spinPriority.setEnabled(True)
                self.lblPriority.setEnabled(True)
            if "Round Robin" in self.comboAlgo.currentText():
                self.spinQuantum.setEnabled(True)
                self.lblQuantum.setEnabled(True)
        else:
            self._controller.resume()
            self.btnPause.setText("Pause")
            self.spinPriority.setEnabled(False)
            self.lblPriority.setEnabled(False)
            self.spinQuantum.setEnabled(False)
            self.lblQuantum.setEnabled(False)

    def _on_reset(self):
        if self._controller:
            self._controller.stop()
        self._controller   = None
        self._sim_running  = False
        self._process_store = []
        self._next_pid      = 1

        self.gantt.clear()
        self.metricsTable.setRowCount(0)
        self.remainingTable.setRowCount(0)
        self.procTable.setRowCount(0)
        self.lblAvg.setText("Avg Waiting: —    Avg Turnaround: —    ")
        self.btnPause.setText("Pause")
        self._set_controls_running(False)

    # ─── Simulation start ─────────────────────────────────────────────────────

    def _start_sim(self, live: bool):
        if self._controller:
            self._controller.stop()

        self.gantt.clear()
        self.metricsTable.setRowCount(0)
        self.remainingTable.setRowCount(0)

        scheduler = RunController.make_scheduler(
            self.comboAlgo.currentText(),
            self.spinQuantum.value()
        )

        self._controller = RunController(self)
        self._controller.sig_tick.connect(self._on_tick)
        self._controller.sig_done.connect(self._on_sim_done)

        self._controller.sig_status.connect(self.lblStatus.setText)

        self._sim_running = True
        self._set_controls_running(True)

        if live:
            self._controller.run_live(scheduler, self._process_store, speed=1)
        else:
            self._controller.run_at_once(scheduler, self._process_store, speed=1)

    # ─── Simulation callbacks ─────────────────────────────────────────────────

    def _on_tick(self, process, start: int, end: int):
        self.gantt.add_slot(process, start, end)
        if self._controller:
            self._refresh_metrics(self._controller.get_scheduler())

    def _on_sim_done(self):
        self._sim_running = False
        self._set_controls_running(False)
        if self._controller:
            self._refresh_metrics(self._controller.get_scheduler())

    # ─── Helpers ──────────────────────────────────────────────────────────────

    def _set_controls_running(self, running: bool):
        self.btnRunLive.setEnabled(not running)
        self.btnRunOnce.setEnabled(not running)
        self.btnAdd.setEnabled(not running)
        self.btnRemove.setEnabled(not running)
        self.btnInject.setEnabled(running)

        #self.btnPause.setEnabled(running)

        self.btnPause.setEnabled(True)
        self.comboAlgo.setEnabled(not running)
        self.spinArrival.setEnabled(not running)
        
        if running:
            self.spinQuantum.setEnabled(False)
            self.lblQuantum.setEnabled(False)
            self.spinPriority.setEnabled(False)
            self.lblPriority.setEnabled(False)
        else:
            self._on_algo_changed(self.comboAlgo.currentText())

    def _add_row_to_proc_table(self, data: dict, note: str = ""):
        row = self.procTable.rowCount()
        self.procTable.insertRow(row)
        pri     = str(data["priority"]) if data["priority"] is not None else "—"
        arrival = str(data["arrival"]) if data["arrival"] >= 0 else "live"
        for col, val in enumerate([str(data["pid"]), data["name"] + note, arrival, str(data["burst"]), pri]):
            self.procTable.setItem(row, col, QTableWidgetItem(val))

    def _refresh_metrics(self, scheduler):
        if not scheduler:
            return

        self.metricsTable.setRowCount(0)
        self.remainingTable.setRowCount(0)
        for p in scheduler.get_processes():
            # metrics row
            row = self.metricsTable.rowCount()
            self.metricsTable.insertRow(row)
            rt  = str(p.get_response_time()) if p.get_response_time() is not None else "—"
            for col, val in enumerate([
                p.get_name(), str(p.get_waiting_time()), str(p.get_turnaround_time()), rt,
            ]):
                self.metricsTable.setItem(row, col, QTableWidgetItem(val))

            # remaining row
            rem_row = self.remainingTable.rowCount()
            self.remainingTable.insertRow(rem_row)
            for col, val in enumerate([
                str(p.get_pid()), p.get_name(), str(p.get_remaining_time())
            ]):
                self.remainingTable.setItem(rem_row, col, QTableWidgetItem(val))

        avg_wt  = scheduler.get_average_waiting_time()
        avg_tat = scheduler.get_average_turnaround_time()
        self.lblAvg.setText(
            f"Avg Waiting: {avg_wt:.2f}    Avg Turnaround: {avg_tat:.2f}    "
            f"Simulation Length: {scheduler.get_current_time()}"
        )
