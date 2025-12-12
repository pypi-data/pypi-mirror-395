"""
supervisor.py

This module implements a SupervisorThread, a dedicated supervisory
monitor for a multi-threaded application. The design pattern is:

    • Each worker thread receives a shared error_queue.
    • When a worker experiences an unhandled exception, it pushes a tuple:
          (thread, exception, traceback_string)
      into the error_queue instead of silently dying.
    • The SupervisorThread runs as a daemon and continuously consumes
      error reports from this queue.
    • For each crashed worker, the supervisor logs the failure, stops
      the thread safely, and invokes custom recreate() logic to spawn
      and start a replacement thread.

This architecture creates a fault-tolerant micro-supervisor system
similar to Erlang/Elixir OTP supervisors: threads never die silently,
and the system can self-heal by restarting failed components.
"""

from multiprocessing import Event
from threading import Thread
from queue import Queue, Empty
from typing import Tuple
from masterpiece.masterpiecethread import MasterPieceThread
from typing import cast

class SupervisorThread(Thread):
    """Supervisor thread that monitors worker thread failures.

    This thread listens on a shared error queue. Worker threads push
    (thread, exception, traceback_string) tuples to this queue when they
    encounter unhandled exceptions. The supervisor reacts by:

        1. Logging the crash event.
        2. Stopping and joining the crashed thread.
        3. Recreating the worker using its custom `recreate()` method.
        4. Starting the replacement thread.

    The supervisor runs as a daemon thread so it does not block
    application shutdown.

    Attributes:
        q (Queue[Tuple[Thread, BaseException, str]]):
            A thread-safe queue containing crash reports from workers.
    """

    def __init__(self, error_queue: Queue[Tuple[Thread, BaseException, str]]) -> None:
        """
        Args:
            error_queue: Shared queue for crash reports from worker threads.
        """
        super().__init__(daemon=True)
        self.q: Queue[Tuple[Thread, BaseException, str]] = error_queue
        self._stop_event: Event = Event()

    def stop(self) -> None:
        """Request the supervisor to exit its loop cleanly."""
        self._stop_event.set()

    def run(self) -> None:
        """Main supervisor loop."""
        while not self._stop_event.is_set():
            try:
                # Block until a crash report is available, timeout to check stop flag
                item = self.q.get(timeout=1.0)
            except Empty:
                continue

            thread, exc, tb = item

            # Only handle MasterPieceThread instances
            if isinstance(thread, MasterPieceThread):
                mt: MasterPieceThread = cast(MasterPieceThread, thread)
                print(f"[Supervisor] ERROR: {mt.name} crashed: {exc}\n{tb}")

                # Stop and join old thread safely
                mt.stop()
                mt.join()

                # Recreate and restart
                try:
                    replacement: MasterPieceThread = mt.recreate()
                    replacement.start()
                    print(f"[Supervisor] Restarted thread {replacement.name}")
                    replacement.warning(f"Thread {mt.name} crashed with exception: {exc}. Restarted as {replacement.name}.")
                except Exception as recreate_exc:
                    print(f"[Supervisor] Failed to recreate thread {mt.name}: {recreate_exc}")
            else:
                print(f"[Supervisor] Thread {thread} is not a MasterPieceThread, cannot recreate")