import unittest
from unittest.mock import MagicMock, patch
from queue import Queue, Empty

from masterpiece.supervisor import SupervisorThread
from masterpiece.masterpiecethread import MasterPieceThread

class TestSupervisorThread(unittest.TestCase):

    def setUp(self):
        # Patch Thread.start so SupervisorThread doesn't actually spawn a real OS thread
        patcher = patch("threading.Thread.start", MagicMock())
        self.addCleanup(patcher.stop)
        self.mock_start = patcher.start()

    def test_supervisor_handles_single_crash(self):
        q  = Queue()

        # Create supervisor (but do NOT start the thread)
        supervisor = SupervisorThread(q)

        # --- Prepare a fake worker thread ---
        worker = MagicMock(spec=MasterPieceThread)
        worker.name = "Worker1"
        worker.stop = MagicMock()
        worker.join = MagicMock()

        # The recreated worker
        replacement = MagicMock(spec=MasterPieceThread)
        replacement.start = MagicMock()

        worker.recreate = MagicMock(return_value=replacement)

        # Enqueue a fake crash event
        exc = RuntimeError("boom")
        tb = "fake traceback"
        q.put((worker, exc, tb))

        # --- Run ONE iteration of the supervisor loop manually ---
        # Instead of supervisor.start(), just call run() once
        # But run() loops forever -> simulate by patching queue.get to raise after first call
        with patch.object(q, "get", side_effect=[(worker, exc, tb), KeyboardInterrupt]):
            try:
                supervisor.run()
            except KeyboardInterrupt:
                pass

        # Assertions
        worker.stop.assert_called_once()
        worker.join.assert_called_once()
        worker.recreate.assert_called_once()
        replacement.start.assert_called_once()

    def test_supervisor_processes_multiple_crashes(self):
        q = Queue()
        supervisor = SupervisorThread(q)

        worker1 = MagicMock(spec=MasterPieceThread)
        worker1.name = "WorkerA"
        repl1 = MagicMock()
        worker1.recreate.return_value = repl1

        worker2 = MagicMock(spec=MasterPieceThread)
        worker2.name = "WorkerB"
        repl2 = MagicMock()
        worker2.recreate.return_value = repl2

        # Patch queue.get to feed two crashes then stop
        events = [
            (worker1, RuntimeError("A"), "tbA"),
            (worker2, RuntimeError("B"), "tbB"),
            KeyboardInterrupt,  # stop loop
        ]

        def fake_get(timeout=None):
            evt = events.pop(0)
            if evt is KeyboardInterrupt:
                raise evt
            return evt

        with patch.object(q, "get", side_effect=fake_get):
            try:
                supervisor.run()
            except KeyboardInterrupt:
                pass

        # Assertions for worker1
        worker1.stop.assert_called_once()
        worker1.join.assert_called_once()
        repl1.start.assert_called_once()

        # Assertions for worker2
        worker2.stop.assert_called_once()
        worker2.join.assert_called_once()
        repl2.start.assert_called_once()


if __name__ == "__main__":
    unittest.main()
