# CPU-Scheduler

A simulator designed to visualize and analyze various CPU scheduling algorithms. Built with a focus on modularity and real-time interaction, it provides a comprehensive tool for understanding how operating systems manage process execution and resource allocation.

---

## ✨ Features

* **Multiple Scheduling Algorithms**:
    * **FCFS** (First-Come, First-Served)
    * **SJF** (Shortest Job First - Preemptive and Non-Preemptive)
    * **Priority Scheduling** (Preemptive and Non-Preemptive)
    * **Round Robin** (RR)
* **Live Visualization**: Real-time Gantt chart updates and process status tracking.
* **Dynamic Simulation**: Add processes on-the-fly while the simulation is running.
* **Performance Metrics**: Automatic calculation of Average Waiting Time (**AWT**) and Average Turnaround Time (**ATT**).
* **Interactive Controls**: Start, pause, resume, or "Run All At Once" for instant results.

## 🚀 Getting Started

### Prerequisites
* **Python 3.x**
* **Pip** (Python package manager)

### Installation
1.  **Clone the repository**:
    ```bash
    git clone [https://github.com/ashmod/Chronos.git](https://github.com/ashmod/Chronos.git)
    cd Chronos
    ```
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application
To launch the simulator:
```bash
python main.py
```

## 📁 Project Structure
The project is organized into modular components to ensure clear separation of logic and presentation:
```Plaintext
CPU-Scheduler/
├── main.py              # Application entry point
├── build.py             # Script for building the executable
├── example_processes.csv # Sample data for testing
└── src/
    ├── algorithms/      # Core logic for FCFS, SJF, RR, etc.
    ├── core/            # Simulation engine and scheduler management
    ├── gui/             # UI components and window layouts
    ├── models/          # Data structures for Processes
    ├── resources/       # UI assets and icons
    └── scenes/          # Application screens (Main Menu, Simulator)
```

### 📊 How to Use
* Select an Algorithm: Choose the desired scheduling strategy from the interface.

* Input Data: Define Process Name, Arrival Time, Burst Time, and Priority.

* Adjust Simulation: Use the speed slider to control the visualizer pace.

* Analyze Results: Review the final table for calculated timing statistics and efficiency metrics.
