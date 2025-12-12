import json
from threading import Thread, Event
import threading
import time
import datetime
from queue import Queue
from typing import Optional, Tuple, Type
from typing import Any, Optional, cast
from typing_extensions import override
from masterpiece import MasterPiece
from masterpiece.mqtt import Mqtt, MqttMsg


class MasterPieceThread(Thread, MasterPiece):
    """Base class for threads used for tasks such as data acquisition
    that need to be run asynchronously. This class defines the `update()`
    method, in which subclasses can execute their specific code. The
    `update_interval()` method (default is 60 seconds) determines how
    frequently the `update()` method is called.

    Args:
        Thread (client): MQTT client for the thread
    """

    systemstatus_topic: str = "system"
    log_topic: str = "log"
    mqtt_root_topic :str = ""
    update_thresold: float = 5.0  # seconds

    def __init__(self, client: Optional[Mqtt], **kwargs: Any) -> None:
        """Construct worker thread for acquiring data and publishing it to
        MQTT

        Args:
            client (Optional[PahoMqtt]): Mqtt client, for communication
        """
        super().__init__()
        MasterPiece.__init__(self)
        self.mqtt_client: Optional[Mqtt] = client

        # for recreating the thread in case of crash
        #self._constructor_args = args
        self._constructor_kwargs = kwargs.copy()

        self.stay = True
        self.name = "unnamed thread"
        self._stop_event = Event()
        self._error_queue : Optional[Queue[Tuple["MasterPieceThread", BaseException, str]]] = None  # optional queue for supervisor
        if self.mqtt_root_topic != "" and self.systemstatus_topic != "":
            self.systemstatus_topic: str = (
                f"{self.mqtt_root_topic}/{self.systemstatus_topic}"
            )
        else:
            self.systemstatus_topic : str = ""

        if self.mqtt_root_topic != "" and self.log_topic != "":
            self.log_topic: str = (
                f"{self.mqtt_root_topic}/{self.log_topic}"
            )
        else:
            self.log_topic :str = ""

    def recreate(self) -> "MasterPieceThread":
        """Recreate a new instance of this thread using the same constructor args.

        Returns:
            MasterPieceThread: New thread instance with same configuration.
        """
        cls: Type[MasterPieceThread] = self.__class__
        new_thread : MasterPieceThread = cls(self.mqtt_client, **self._constructor_kwargs)
        new_thread.name = self.name
        new_thread._error_queue = self._error_queue
        return new_thread

    def stop(self) -> None:
        """Request the thread to stop processing further tasks.

        Note that the method does not wait the thread to terminate.  If
        the thread is sleeping, it will be awakened and stopped. If the
        thread is in the middle of its code execution, it will finish
        its current job before stopping.  In oder to wait until the
        thread has completed its call join() method.
        """
        self._stop_event.set()


    def run(self) -> None:
        """Thread loop with crash protection."""
        try:
            self._run_loop()
        except Exception as exc:
            import traceback
            tb = traceback.format_exc()
            self.error(f"Thread {self.name} crashed: {exc}", tb)
            # Optionally: send crash info to parent/supervisor
            if self._error_queue != None:
                self._error_queue.put((self, exc, tb))
            raise


    def _run_loop(self) -> None:
        """Thread  loop.

        Calls update() method in a loop and if the return value is True
        sleeps the update_interval() number of seconds before the next
        update call. If the update method returns False then the error
        is logged, and the sleep time is shortened to 5 seconds to
        retry. After three subsequent failures the update_interval is
        reset to original
        """
        self.debug(
            f"Thread {self.name} started with update interval {self.update_interval()}"
        )

        failures: int = 0
        updates: int = 0
        while not self._stop_event.is_set():
            start_time: float = time.time()
            if not self.update():
                seconds: float = 5
                failures = failures + 1
                self.error(
                    f"Thread {self.name} update {str(updates)} failure {str(failures)}, retry after {str(seconds)} ..."
                )
                if failures > 3:
                    failures = 0
                    seconds = self.update_interval()
            else:
                seconds = self.update_interval()
            updates = updates + 1
            self.process_system_status(start_time)
            self._stop_event.wait(seconds)
        self.debug(f"Thread {self.name} stopped")
        # self.mqtt_client = None

    def process_system_status(self, start_time: float) -> bool:
        """Publish system status information to systemstatus MQTT topic.
        Args:
            start_time (float): start time of the update method call in seconds
        Returns:
            bool: True if elapsed time threshold was exceeded and 
            system status was published, False otherwise
        """
        if self.systemstatus_topic != "":
            end_time: float = time.time()
            self.update_metrics(end_time - start_time)
            if self._elapsed > self.update_thresold:
                sysinfo: dict[str, dict[str, float]] = {
                    "threads": {self.name: self.acquire_time_spent()}
                }
                self.publish(
                    self.systemstatus_topic,
                    json.dumps(sysinfo),
                    qos=0,
                    retain=False,
                )
                return True
        return False

    def update_interval(self) -> float:
        """Fetch the update interval in seconds. The default is 60.

        Returns:
            float: number of seconds
        """
        return 60.0

    def update(self) -> bool:
        """Method called from the threads run loop.

        Up to the sub classes to implement.

        Returns:
            bool: True upon succesfull update. False implies an error .
        """
        return True

    def log(self, type: str, msg: str, details: str) -> None:
        """Log event to event log.

        Args:
            type (str): one of the following: "info", "debug", "warning", "error"
            msg (str): message to be logged
            details (str): detailed description
        """
        if self.mqtt_client is not None:
            ts = datetime.datetime.now(datetime.timezone.utc).timestamp()
            data :  dict[str, Any] = {"Timestamp": ts, "Source": self.name, "Class": type, "Msg": msg, "Details": details}
            msg = json.dumps(data)
            self.publish(self.log_topic, msg, qos=1, retain=False)

    def publish(
        self, topic: str, message: str, qos: int = 1, retain: bool = True
    ) -> None:
        """Publish the given message to given MQTT topic with specified
        quality of service and retain.

        Args:
            topic (str): topic
            message (str): message to be published
            qos (int): quality of service
            retain (bool): retain the message
        """
        if self.mqtt_client != None:
            mqtt_client: Mqtt = cast(Mqtt, self.mqtt_client)
            mqtt_client.publish(topic, message, qos, retain)

    @override
    def error(self, msg: str, details: str = "") -> None:
        self.log("Error", msg, details)

    @override
    def warning(self, msg: str, details: str = "") -> None:
        self.log("Warning", msg, details)

    @override
    def info(self, msg: str, details: str = "") -> None:
        self.log("Info", msg, details)

    @override
    def debug(self, msg: str, details: str = "") -> None:
        self.log("Debug", msg, details)
