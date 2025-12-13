# OS Simulator

A high-performance Python package implementing CPU scheduling algorithms with C++ optimization.

## Features

- **First Come First Served (FCFS)**: Simple queue-based scheduling
- **Shortest Job First (SJF)**: Optimal average waiting time scheduling
- **Round Robin (RR)**: Time-slice based preemptive scheduling
- **C++ Performance**: Optimized implementations using pybind11
- **Easy Integration**: Simple Python interface for complex algorithms

## Installation

```bash
pip install os-simulator
```

## Quick Start

```python
from os_simulator import os_algorithms

# Define processes
processes = [
    {"pid": 1, "arrival_time": 0, "burst_time": 5},
    {"pid": 2, "arrival_time": 1, "burst_time": 3},
    {"pid": 3, "arrival_time": 2, "burst_time": 8},
]

# Run FCFS scheduling
scheduled = os_algorithms.fcfs_scheduler(processes)

# Run SJF scheduling
scheduled = os_algorithms.sjf_scheduler(processes)

# Run Round Robin with time quantum of 2
scheduled = os_algorithms.round_robin_scheduler(processes, 2)
```

## Algorithm Details

### FCFS (First Come First Served)
Processes are scheduled in order of arrival time. Simple but can cause convoy effect.

### SJF (Shortest Job First)
Schedules shortest burst time processes first. Optimal for average waiting time.

### Round Robin
Each process gets a fixed time quantum. Fair scheduling with controlled response time.

## Development

```bash
git clone https://github.com/Will-Swinson/os-simulator
cd os-simulator
pip install -e .
```

## License

MIT License - see LICENSE file for details.
