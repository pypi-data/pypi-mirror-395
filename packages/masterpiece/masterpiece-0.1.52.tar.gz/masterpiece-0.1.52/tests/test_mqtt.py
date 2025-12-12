import unittest
from unittest.mock import MagicMock
from typing import Callable, Any, Type
from masterpiece.mqtt import Mqtt


class MqttMsg:
    def __init__(self) -> None:
        pass


class TestMqtt(unittest.TestCase):
    """Unit tests for the Mqtt abstract base class."""

    def setUp(self) -> None:
        """Set up mock Mqtt instance for testing."""

        # Mock the abstract methods by creating a subclass
        class MqttSubclass(Mqtt):
            def connect_to_server(
                self, host: str, port: int, keepalive: int, bind_address: str
            ) -> int:
                raise NotImplementedError

            def disconnect(self) -> None:
                raise NotImplementedError

            def subscribe(self, topic: str, qos: int) -> None:
                raise NotImplementedError

            def loop_stop(self) -> None:
                raise NotImplementedError

            def publish(self, topic: str, msg: str, qos: int, retain: bool) -> None:
                raise NotImplementedError

            def loop_start(self) -> None:
                raise NotImplementedError

            def loop_forever(self) -> None:
                raise NotImplementedError

            @property
            def on_message(self) -> Callable[[object, Any, Type[MqttMsg]], None]:
                return MagicMock()

            @on_message.setter
            def on_message(
                self, value: Callable[[object, Any, Type[MqttMsg]], None]
            ) -> None:
                pass

            @property
            def on_connect(self) -> Callable[[object, Any, int, int], None]:
                return MagicMock()

            @on_connect.setter
            def on_connect(
                self, value: Callable[[object, Any, int, int], None]
            ) -> None:
                pass

            @property
            def on_disconnect(self) -> Callable[[Any, Any, int], None]:
                return MagicMock()

            @on_disconnect.setter
            def on_disconnect(self, value: Callable[[Any, Any, int], None]) -> None:
                pass

        self.mqtt = MqttSubclass(name="TestMqtt")

    def test_connect_to_server_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            self.mqtt.connect_to_server("localhost", 1883, 60, "")

    def test_publish_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            self.mqtt.publish("test/topic", "message", 0, False)

    def test_subscribe_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            self.mqtt.subscribe("test/topic", 0)

    def test_loop_stop_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            self.mqtt.loop_stop()

    def test_disconnect_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            self.mqtt.disconnect()

    def test_loop_start_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            self.mqtt.loop_start()

    def test_loop_forever_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            self.mqtt.loop_forever()


if __name__ == "__main__":
    unittest.main()
