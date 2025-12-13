"""OS Simulator - Operating System Scheduling Algorithms

A Python package that implements various CPU scheduling algorithms with C++
optimization for performance. Includes First Come First Served (FCFS),
Shortest Job First (SJF), and Round Robin scheduling algorithms.

Example:
    from os_simulator import os_algorithms

    processes = [
        {"pid": 1, "arrival_time": 0, "burst_time": 5},
        {"pid": 2, "arrival_time": 1, "burst_time": 3},
    ]

    scheduled = os_algorithms.fcfs_scheduler(processes)
"""

__version__ = "0.2.1"
__author__ = "Will Swinson"

try:
    from .os_algorithms import fcfs_scheduler, sjf_scheduler, round_robin_scheduler
    __all__ = ["fcfs_scheduler", "sjf_scheduler", "round_robin_scheduler"]
except ImportError as e:
    # Graceful fallback if C++ extension isn't built
    import warnings
    warnings.warn(f"C++ scheduling algorithms not available: {e}")
    __all__ = []