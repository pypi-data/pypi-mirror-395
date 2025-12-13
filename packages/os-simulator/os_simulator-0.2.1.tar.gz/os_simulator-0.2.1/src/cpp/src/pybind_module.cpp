#include "scheduler/scheduler.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace scheduler;

Process dict_to_process(py::dict proc_dict) {
  return Process{proc_dict["pid"].cast<int>(),
                 proc_dict["arrival_time"].cast<int>(),
                 proc_dict["burst_time"].cast<int>()};
}

py::dict process_to_dict(const Process &process) {
  py::dict result;

  result["pid"] = process.pid;
  result["arrival_time"] = process.arrivalTime;
  result["burst_time"] = process.burstTime;
  result["waiting_time"] = process.waitingTime;
  result["turn_around_time"] = process.turnaroundTime;
  result["finish_time"] = process.finishTime;
  result["remaining_time"] = process.remainingTime;
  result["is_complete"] = process.isComplete;

  return result;
}

/**
 * @brief Run First Come First Served scheduling on a list of process
 * dictionaries.
 *
 * @param process_list Python list of dictionaries where each dictionary must
 * contain the keys `pid`, `arrival_time`, and `burst_time` (integers).
 * @return py::list A Python list of dictionaries representing the scheduled
 * processes. Each dictionary contains the original fields (`pid`,
 * `arrival_time`, `burst_time`) and scheduling results such as `waiting_time`,
 * `turn_around_time`, `finish_time`, `remaining_time`, and `is_complete`.
 */
py::list fcfs_scheduler_wrapper(py::list process_list) {
  std::vector<Process> processes;

  for (const auto &process : process_list) {
    Process convertedProcess = dict_to_process(process.cast<py::dict>());
    processes.push_back(convertedProcess);
  }

  std::vector<Process> result = fcfsScheduler(processes);

  py::list result_process_list;

  for (const auto &process : result) {
    py::dict convertedProcess = process_to_dict(process);
    result_process_list.append(convertedProcess);
  }

  return result_process_list;
}

/**
 * @brief Schedules processes using the Shortest Job First algorithm.
 *
 * Converts the provided Python list of process dictionaries into C++ Process
 * objects, runs the SJF scheduler, and returns the scheduled processes as a
 * Python list of dictionaries.
 *
 * @param process_list Python list of dictionaries, each containing the keys
 *                     `pid`, `arrival_time`, and `burst_time` (all integers).
 * @return py::list Python list of dictionaries where each dictionary contains
 *                  `pid`, `arrival_time`, `burst_time`, `waiting_time`,
 *                  `turn_around_time`, `finish_time`, `remaining_time`, and
 *                  `is_complete`.
 */
py::list sjf_scheduler_wrapper(py::list process_list) {
  std::vector<Process> processes;

  for (const auto &process : process_list) {
    Process convertedProcess = dict_to_process(process.cast<py::dict>());
    processes.push_back(convertedProcess);
  }

  std::vector<Process> result = sjfScheduler(processes);

  py::list result_process_list;

  for (const auto &process : result) {
    py::dict convertedProcess = process_to_dict(process);
    result_process_list.append(convertedProcess);
  }

  return result_process_list;
}

/**
 * @brief Apply Round Robin scheduling to a collection of processes using the
 * specified time quantum.
 *
 * @param process_list Python list of dictionaries where each dictionary must
 * contain at least `pid`, `arrival_time`, and `burst_time`.
 * @param time_quantum Time slice used by the Round Robin scheduler (same time
 * units as `burst_time` and `arrival_time`).
 * @return py::list Python list of process dictionaries augmented with
 * scheduling results: `waiting_time`, `turn_around_time`, `finish_time`,
 * `remaining_time`, and `is_complete`.
 */
py::list round_robin_scheduler_wrapper(py::list process_list,
                                       int time_quantum) {
  if (time_quantum <= 0) {
    throw std::invalid_argument("Time Quantum must be a positive value.");
  }

  std::vector<Process> processes;

  for (const auto &process : process_list) {
    Process convertedProcess = dict_to_process(process.cast<py::dict>());
    processes.push_back(convertedProcess);
  }

  std::vector<Process> result = roundRobinScheduler(processes, time_quantum);

  py::list result_process_list;

  for (const auto &process : result) {
    py::dict convertedProcess = process_to_dict(process);
    result_process_list.append(convertedProcess);
  }

  return result_process_list;
}

/**
 * @brief Creates the Python module exposing OS scheduling algorithm bindings.
 *
 * Registers a Pybind11 module named "scheduler_cpp" (module doc: "OS Scheduling
 * Algorithms") and exposes three functions to Python:
 *  - `fcfs_scheduler(processes)`: First Come First Served scheduling algorithm.
 *  - `sjf_scheduler(processes)`: Shortest Job First scheduling algorithm.
 *  - `round_robin_scheduler(processes, time_quantum)`: Round Robin scheduling
 * algorithm with a time quantum.
 */
PYBIND11_MODULE(os_algorithms, m) {
  m.doc() = "OS Scheduling Algorithms";

  m.def("fcfs_scheduler", &fcfs_scheduler_wrapper,
        "First Come First Served scheduling algorithm", py::arg("processes"));

  m.def("sjf_scheduler", &sjf_scheduler_wrapper,
        "Shortest Job First scheduling algorithm", py::arg("processes"));

  m.def("round_robin_scheduler", &round_robin_scheduler_wrapper,
        "Round Robin scheduling algorithm", py::arg("processes"),
        py::arg("time_quantum"));
}