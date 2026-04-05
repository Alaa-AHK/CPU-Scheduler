# CPU-Scheduler

## Checklist of what is done and what is remmaing

### Algorithms
- [ ] FCFS (First Come First Serve)
- [ ] SJF Non-Preemptive (SJF)
- [ ] SJF Preemptive (SRTF)
- [x] Priority Non-Preemptive (PNPSJF)
- [x] Priority Preemptive (PPSJF)
- [x] Round Robin

### Inputs
- [x] Type of scheduler selection
- [ ] Number of processes
- [x] Process information per scheduler type
- [x] Dynamic process addition during runtime
- [x] Only ask for relevant info per algorithm
  - [x] FCFS: Arrival Time, Burst Time
  - [x] SJF: Arrival Time, Burst Time
  - [x] Priority: Arrival Time, Burst Time, Priority
  - [x] Round Robin: Arrival Time, Burst Time, Time Quantum

### Operation
- [x] Live scheduling (1 time unit = 1 second)
- [x] Remaining burst time updated as time progresses
- [x] Option to run without live scheduling (instant mode)
- [ ] Built project with ready to run executable (.exe)
- [ ] GUI desktop application

### Outputs
- [ ] Live Gantt Chart (timeline of process execution)
- [x] Average waiting time calculation
- [x] Average turnaround time calculation
- [x] Remaining burst time updated live

### Testing
- [x] Round Robin tested and verified
- [x] Priority Non-Preemptive tested and verified
- [x] Priority Preemptive tested and verified
- [ ] FCFS tested and verified
- [ ] SJF Non-Preemptive tested and verified
- [ ] SJF Preemptive tested and verified
- [x] Interactive test menu (choose algorithm + mode)
- [x] Live mode testing (1 second delay)
- [x] Instant mode testing (no delay)
- [ ] Dynamic process addition testing

---

## 📁 Project Structure
