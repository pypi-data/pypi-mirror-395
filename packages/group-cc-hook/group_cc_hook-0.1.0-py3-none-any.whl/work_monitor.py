"""
Pure Python implementation of work monitoring functionality.
Replaces the C++ extension (my_extension.cpp) with native Python code.
Uses multiprocessing to avoid Python GIL limitations for timeout monitoring.
"""

import multiprocessing
import os
import signal
import threading
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

try:
    import torch
    import torch.distributed as dist
except (ImportError, ModuleNotFoundError):
    # Allow module import in non-PyTorch environment
    torch = None
    dist = None

# ============ Debug logging control ============
DEBUG_ENABLED = os.environ.get("PG_HOOK_DEBUG", "0") == "1"
INFO_ENABLED = os.environ.get("PG_HOOK_INFO", "1") != "0"  # INFO enabled by default


def debug_log(msg: str):
    """Print debug log, only outputs when DEBUG_ENABLED=True"""
    if DEBUG_ENABLED:
        print(f"[DEBUG Python] {msg}", flush=True)


def info_log(msg: str):
    """Print info log, only outputs when INFO_ENABLED=True"""
    if INFO_ENABLED:
        print(f"[Python] {msg}", flush=True)


# ===============================================


@dataclass
class TimedWork:
    """Represents a work object with timing information"""

    work: Any
    op_name: str
    enqueue_time: float
    rank: int = -1


def _timeout_monitor_process(
    timeout_seconds: float,
    work_queue: multiprocessing.Queue,
    completion_queue: multiprocessing.Queue,
    stop_event: multiprocessing.Event,
    parent_pid: int,
):
    """
    Separate process for timeout monitoring.
    This runs in a separate process to avoid GIL limitations.

    Args:
        timeout_seconds: Timeout threshold in seconds
        work_queue: Queue to receive new work items (op_name, enqueue_time, rank)
        completion_queue: Queue to receive completion notifications (op_name)
        stop_event: Event to signal process shutdown
        parent_pid: PID of parent process to send signals to
    """
    debug_log("Timeout monitor process started")

    # Track pending work items: {op_name: (enqueue_time, rank)}
    pending_work: Dict[str, tuple] = {}

    while not stop_event.is_set():
        # Check for new work items
        try:
            while not work_queue.empty():
                item = work_queue.get_nowait()
                if item is None:  # Sentinel for shutdown
                    break
                op_name, enqueue_time, rank = item
                pending_work[op_name] = (enqueue_time, rank)
                debug_log(f"Timeout monitor: Tracking {op_name}")
        except Exception:
            pass

        # Check for completed work
        try:
            while not completion_queue.empty():
                op_name = completion_queue.get_nowait()
                if op_name in pending_work:
                    enqueue_time, rank = pending_work.pop(op_name)
                    elapsed_ms = int((time.time() - enqueue_time) * 1000)
                    if rank >= 0:
                        info_log(
                            f"Rank {rank}: {op_name} complete, time: {elapsed_ms} ms"
                        )
                    else:
                        info_log(f"!!!{op_name} complete, time: {elapsed_ms} ms")
        except Exception:
            pass

        # Check for timeouts
        current_time = time.time()
        timeout_ms = int(timeout_seconds * 1000)

        # Create list copy to allow modification during iteration
        for op_name, (enqueue_time, rank) in list(pending_work.items()):
            elapsed_ms = int((current_time - enqueue_time) * 1000)

            if elapsed_ms > timeout_ms:
                # Timeout detected
                if rank >= 0:
                    print(
                        f"[Python Process] Rank {rank}: {op_name} timeout, sending SIGUSR1",
                        flush=True,
                    )
                else:
                    print(
                        f"[Python Process] {op_name} timeout, sending SIGUSR1",
                        flush=True,
                    )

                try:
                    os.kill(parent_pid, signal.SIGUSR1)
                    time.sleep(300)
                except (OSError, ValueError) as e:
                    print(f"[Python Process] Failed to send SIGUSR1: {e}", flush=True)

                pending_work.pop(op_name)

        # Sleep to avoid busy-waiting (10ms for balance between responsiveness and CPU usage)
        time.sleep(0.010)

    debug_log("Timeout monitor process stopped")


class WorkMonitor:
    """
    Python implementation of work monitoring with timeout detection.
    Uses a separate process for timeout monitoring to avoid GIL limitations.
    """

    def __init__(self, timeout_seconds: float = 300.0):
        """
        Initialize work monitor.

        Args:
            timeout_seconds: Timeout in seconds (default: 300 = 5 minutes)
        """
        self.timeout_seconds = timeout_seconds
        self.pending_work: Dict[str, TimedWork] = {}
        self.work_lock = threading.Lock()

        # Multiprocessing components for timeout monitoring process
        self.work_queue = multiprocessing.Queue()
        self.completion_queue = multiprocessing.Queue()
        self.stop_event = multiprocessing.Event()
        self.monitor_process: Optional[multiprocessing.Process] = None

        # Thread for checking work completion in main process
        self.checker_thread: Optional[threading.Thread] = None
        self.checker_stop_flag = threading.Event()

    def start_monitor(self):
        """Start the monitoring process and checker thread"""
        if self.monitor_process is not None and self.monitor_process.is_alive():
            debug_log("Monitor process already running")
            return

        # Start the timeout monitoring process
        self.stop_event.clear()
        self.monitor_process = multiprocessing.Process(
            target=_timeout_monitor_process,
            args=(
                self.timeout_seconds,
                self.work_queue,
                self.completion_queue,
                self.stop_event,
                os.getpid(),
            ),
            daemon=True,
        )
        self.monitor_process.start()
        debug_log("Python work monitor process started")

        # Start the work completion checker thread
        self.checker_stop_flag.clear()
        self.checker_thread = threading.Thread(
            target=self._check_work_completion_loop, daemon=True
        )
        self.checker_thread.start()
        debug_log("Python work checker thread started")

    def stop_monitor(self):
        """Stop the monitoring process and checker thread"""
        # Stop checker thread first
        if self.checker_thread is not None:
            self.checker_stop_flag.set()
            if self.checker_thread.is_alive():
                self.checker_thread.join(timeout=2.0)
            self.checker_thread = None
            debug_log("Python work checker thread stopped")

        # Stop monitor process
        if self.monitor_process is not None:
            self.stop_event.set()
            try:
                self.work_queue.put(None)  # Sentinel to wake up process
            except Exception:
                pass

            if self.monitor_process.is_alive():
                self.monitor_process.join(timeout=6.0)
                if self.monitor_process.is_alive():
                    self.monitor_process.terminate()
                    self.monitor_process.join(timeout=1.0)

            self.monitor_process = None
            debug_log("Python work monitor process stopped")

        # Clean up pending work
        debug_log("Cleaning up pending work objects...")
        with self.work_lock:
            self.pending_work.clear()

    def enqueue_work(self, work: Any, op_name: str, rank: int = -1):
        """
        Add work object to the monitoring queue.

        Args:
            work: The work object to monitor
            op_name: Name of the operation
            rank: Rank of the process (default: -1 for unknown)
        """
        timed_work = TimedWork(
            work=work, op_name=op_name, enqueue_time=time.time(), rank=rank
        )

        with self.work_lock:
            self.pending_work[op_name] = timed_work

        # Send to timeout monitor process
        try:
            self.work_queue.put((op_name, timed_work.enqueue_time, rank))
        except Exception as e:
            debug_log(f"Failed to send work to monitor process: {e}")

        debug_log(f"Rank {rank}: Enqueued work: {op_name}")

    def _check_work_completion_loop(self):
        """
        Thread that checks work completion status in the main process.
        This needs to run in the main process because work objects can't be serialized.
        """
        debug_log("Work completion checker loop started")

        while not self.checker_stop_flag.is_set():
            completed_work = []

            # Check all pending work within a single critical section
            # to avoid race conditions
            with self.work_lock:
                # Create list copy to allow modification during iteration
                for op_name, timed_work in list(self.pending_work.items()):
                    if self._is_work_completed(timed_work.work):
                        completed_work.append(op_name)
                        # Remove atomically within the same critical section
                        self.pending_work.pop(op_name)

            # Notify timeout monitor process of completed work
            for op_name in completed_work:
                try:
                    self.completion_queue.put(op_name)
                    debug_log(f"Marked {op_name} as completed")
                except Exception as e:
                    debug_log(f"Failed to notify completion: {e}")

            # Sleep briefly before next check
            time.sleep(0.010)  # 10ms

        debug_log("Work completion checker loop stopped")

    def _is_work_completed(self, work: Any) -> bool:
        """
        Check if a work object has completed.

        Args:
            work: The work object to check

        Returns:
            True if completed, False otherwise
        """
        if work is None:
            return True

        # Check if work has isCompleted method
        if hasattr(work, "isCompleted"):
            try:
                return work.isCompleted()
            except (AttributeError, RuntimeError) as e:
                debug_log(f"Error checking work completion: {e}")
                return False

        # Check if work has is_completed method (alternative naming)
        if hasattr(work, "is_completed"):
            try:
                return work.is_completed()
            except (AttributeError, RuntimeError) as e:
                debug_log(f"Error checking work completion: {e}")
                return False

        # If no completion check method, assume completed
        debug_log("Work object has no completion check method, assuming completed")
        return True


# Global instance for backward compatibility
_global_monitor: Optional[WorkMonitor] = None


def start_monitor(timeout_seconds: float = 300.0):
    """Start the global work monitor"""
    global _global_monitor

    if _global_monitor is None:
        _global_monitor = WorkMonitor(timeout_seconds=timeout_seconds)

    _global_monitor.start_monitor()


def stop_monitor():
    """Stop the global work monitor"""

    if _global_monitor is not None:
        _global_monitor.stop_monitor()


def enqueue_work(work: Any, op_name: str, rank: int = -1):
    """Enqueue work to the global monitor"""
    global _global_monitor

    if _global_monitor is None:
        debug_log("Warning: Global monitor not initialized, creating new instance")
        _global_monitor = WorkMonitor()
        _global_monitor.start_monitor()

    _global_monitor.enqueue_work(work, op_name, rank)
