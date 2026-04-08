import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QLabel, QTableWidget,
    QTableWidgetItem, QFrame, QSpinBox, QLineEdit
)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CPU Scheduler UI")
        self.resize(900, 600)

        self.next_pid = 1

        main_layout = QVBoxLayout(self)

        # 🔹 Top controls
        top_layout = QHBoxLayout()

        # Algorithm ComboBox
        self.algorithmComboBox = QComboBox()
        self.algorithmComboBox.addItems([
            "FCFS",
            "SJF (Preemptive)",
            "SJF (Non-Preemptive)",
            "Priority (Preemptive)",
            "Priority (Non-Preemptive)",
            "Round Robin"
        ])

        top_layout.addWidget(QLabel("Algorithm:"))
        top_layout.addWidget(self.algorithmComboBox)

        # Time Quantum (hidden initially)
        self.timeQuantumSpinBox = QSpinBox()
        self.timeQuantumSpinBox.setMinimum(1)
        self.timeQuantumSpinBox.setValue(2)
        top_layout.addWidget(QLabel("Quantum:"))
        top_layout.addWidget(self.timeQuantumSpinBox)

        main_layout.addLayout(top_layout)

        # 🔹 Input fields
        input_layout = QHBoxLayout()

        self.nameInput = QLineEdit()
        self.nameInput.setPlaceholderText("Process Name")

        self.arrivalInput = QSpinBox()
        self.arrivalInput.setPrefix("Arrival: ")

        self.burstInput = QSpinBox()
        self.burstInput.setPrefix("Burst: ")
        self.burstInput.setValue(1)

        input_layout.addWidget(self.nameInput)
        input_layout.addWidget(self.arrivalInput)
        input_layout.addWidget(self.burstInput)

        main_layout.addLayout(input_layout)

        # 🔹 Buttons
        btn_layout = QHBoxLayout()

        self.addBtn = QPushButton("Add Process")
        self.removeBtn = QPushButton("Remove")
        self.resetBtn = QPushButton("Reset")
        self.runLiveBtn = QPushButton("Run Live")
        self.runOnceBtn = QPushButton("Run At Once")

        btn_layout.addWidget(self.addBtn)
        btn_layout.addWidget(self.removeBtn)
        btn_layout.addWidget(self.resetBtn)
        btn_layout.addWidget(self.runLiveBtn)
        btn_layout.addWidget(self.runOnceBtn)

        main_layout.addLayout(btn_layout)

        # 🔹 Table
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            ["PID", "Name", "Arrival", "Burst"]
        )

        main_layout.addWidget(self.table)

        # 🔹 Gantt placeholder
        self.ganttFrame = QFrame()
        self.ganttFrame.setFrameShape(QFrame.Box)
        self.ganttFrame.setMinimumHeight(200)

        main_layout.addWidget(QLabel("Gantt Chart:"))
        main_layout.addWidget(self.ganttFrame)

        # 🔥 connections
        self.addBtn.clicked.connect(self.add_process)
        self.removeBtn.clicked.connect(self.remove_process)
        self.resetBtn.clicked.connect(self.reset_table)
        self.algorithmComboBox.currentIndexChanged.connect(self.update_visibility)

        self.update_visibility()

    # 🔹 Add process
    def add_process(self):
        row = self.table.rowCount()
        self.table.insertRow(row)

        name = self.nameInput.text() or f"P{self.next_pid}"

        self.table.setItem(row, 0, QTableWidgetItem(str(self.next_pid)))
        self.table.setItem(row, 1, QTableWidgetItem(name))
        self.table.setItem(row, 2, QTableWidgetItem(str(self.arrivalInput.value())))
        self.table.setItem(row, 3, QTableWidgetItem(str(self.burstInput.value())))
        self.table.setItem(row, 4, QTableWidgetItem(str(self.priorityInput.value())))

        self.next_pid += 1

    def remove_process(self):
        selected = self.table.selectedItems()
        if selected:
            self.table.removeRow(selected[0].row())

    def reset_table(self):
        self.table.setRowCount(0)
        self.next_pid = 1

    # 🔥 show/hide fields
    def update_visibility(self):
        algo = self.algorithmComboBox.currentText()

        # Quantum
        if "Round Robin" in algo:
            self.timeQuantumSpinBox.setEnabled(True)
        else:
            self.timeQuantumSpinBox.setEnabled(False)
