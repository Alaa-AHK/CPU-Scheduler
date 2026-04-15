# CPU Scheduler Simulator

![CPU Scheduler Simulator Screenshot](Documentation/images/Screenshot%202026-04-16%20002259.png)
A simulator designed to visualize and analyze various CPU scheduling algorithms. Built with a focus on modularity and real-time interaction, it provides a comprehensive tool for understanding how operating systems manage process execution and resource allocation.

---

## Features

* **Multiple Scheduling Algorithms**:
    * **FCFS** (First-Come, First-Served)
    * **SJF** (Shortest Job First - Preemptive and Non-Preemptive)
    * **Priority Scheduling** (Preemptive and Non-Preemptive)
    * **Round Robin** (RR)
* **Live Visualization**: Real-time Gantt chart updates and process status tracking.
* **Dynamic Simulation**: Add processes on-the-fly while the simulation is running.
* **Performance Metrics**: Automatic calculation of Average Waiting Time (**AWT**) and Average Turnaround Time (**ATT**).
* **Interactive Controls**: Start, pause, resume, or "Run All At Once" for instant results.

## Getting Started

### Prerequisites
* **Python 3.x**
* **PyQt5** (GUI library)

### Installation
1.  **Clone the repository**:
    ```bash
    git clone <https://github.com/Alaa-AHK/CPU-Scheduler>
    cd CPU_Scheduler
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

## Project Structure
The project is organized into modular components to ensure clear separation of logic and presentation:
```Plaintext
CPU_Scheduler/
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── Algorithms/              # Core logic for FCFS, SJF, RR, etc.
│   ├── FCFS.py
│   ├── SJF.py
│   ├── SRTF.py
│   ├── round_robin.py
│   ├── PPSJF.py
│   ├── PNPSJF.py
│   ├── main_Testing.py
├── Documentation/           # documentation Report
├── GUI/                     # UI components and window layouts
│   ├── main_window.py
│   ├── run_controller.py
│   └── gantt_widget.py
├── Logic/                   # Simulation engine and scheduler management
│   ├── execution.py
│   ├── process.py
│   ├── scheduler.py
│   └── simulation.py
```

### How to Use
* Select an Algorithm: Choose the desired scheduling strategy from the interface.

* Input Data: Define Process Name, Arrival Time, Burst Time, and Priority.

* Analyze Results: Review the final table for calculated timing statistics and efficiency metrics.
 
## Team Members

- Arsany Hany Anwar  
- Andrew Ehab Tharwat  
- Alaa Abdelhakeem Mahmoud  
- Rola Ahmed Kassem  
- Radwa Yasser Ahmed  
- Youmna Ahmed Farag  
- Ziad Ahmed Orabi
