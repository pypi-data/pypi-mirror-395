"""Type stubs for os_algorithms C++ module."""

from typing import List, TypedDict


class ProcessDict(TypedDict):
    """Process dictionary structure."""
    pid: int
    arrival_time: int
    burst_time: int
    waiting_time: int
    turn_around_time: int
    finish_time: int
    remaining_time: int
    is_complete: bool


def fcfs_scheduler(processes: List[ProcessDict]) -> List[ProcessDict]:
    """
    First Come First Served scheduling algorithm.

    Args:
        processes: List of process dictionaries with pid, arrival_time, burst_time

    Returns:
        List of scheduled processes with timing information
    """
    ...


def sjf_scheduler(processes: List[ProcessDict]) -> List[ProcessDict]:
    """
    Shortest Job First scheduling algorithm.

    Args:
        processes: List of process dictionaries with pid, arrival_time, burst_time

    Returns:
        List of scheduled processes with timing information
    """
    ...


def round_robin_scheduler(processes: List[ProcessDict], time_quantum: int) -> List[ProcessDict]:
    """
    Round Robin scheduling algorithm with time quantum.

    Args:
        processes: List of process dictionaries with pid, arrival_time, burst_time
        time_quantum: Time slice for round robin scheduling

    Returns:
        List of scheduled processes with timing information
    """
    ...