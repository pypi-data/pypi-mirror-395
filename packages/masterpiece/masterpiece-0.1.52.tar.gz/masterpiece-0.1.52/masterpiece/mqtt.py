from abc import ABC, abstractmethod
from typing import Any, Callable

from .masterpiece import MasterPiece


from abc import ABC, abstractmethod
from typing import Any


class MqttMsg(ABC):
    """Abstract base class for MQTT messages."""

    @property
    @abstractmethod
    def payload(self) -> Any:
        """The payload of the MQTT message."""
        pass

    @payload.setter
    @abstractmethod
    def payload(self, value: Any) -> None:
        """Set the payload of the MQTT message."""
        pass

    @property
    @abstractmethod
    def topic(self) -> str:
        """The topic of the MQTT message."""
        pass

    @topic.setter
    @abstractmethod
    def topic(self, value: str) -> None:
        """Set the topic of the MQTT message."""
        pass


class Mqtt(MasterPiece, ABC):
    """Abstract base class for MQTT brokers.

    This class provides the foundation for implementing MQTT clients that
    interact with a broker, handling the connection, subscription, and
    message publishing.

    Note: Subclasses should implement the abstract methods to provide
    the actual behavior for connecting to an MQTT server, subscribing
    to topics, and handling the network loop. This class implies multi-threading,
    as the network loop should typically run in its own thread to handle
    incoming and outgoing MQTT messages concurrently.
    """

    connected_flag: bool = False
    host: str = "localhost"
    port: int = 1883
    keepalive: int = 60
    bind_address: str = ""
    _not_implemented: str = "Subclasses must implement this method."

    def __init__(self, name: str) -> None:
        """Initialize the MQTT base class with the given name.

        Args:
            name (str): The name to identify this instance of the MQTT client.
        """
        super().__init__(name)

    @abstractmethod
    def connect_to_server(
        self,
        host: str = "localhost",
        port: int = 1883,
        keepalive: int = 60,
        bind_address: str = "",
    ) -> int:
        """Connect to the MQTT server.

        This method establishes a connection to the MQTT broker. It is expected
        that subclasses provide the actual connection logic.

        Args:
            host (str, optional): The host address of the MQTT broker. Defaults to "localhost".
            port (int, optional): The port number for the MQTT broker. Defaults to 1883.
            keepalive (int, optional): The keep-alive time, in seconds. Defaults to 60.
            bind_address (str, optional): The local network address to bind to. Defaults to "".

        Returns:
            int: 0 if the connection is successful, non-zero values indicate errors.

        Raises:
            NotImplementedError: If this method is not implemented by the subclass.
        """
        raise NotImplementedError(self._not_implemented)

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from the MQTT broker.

        This method should gracefully disconnect the client from the MQTT broker.
        The subclass should implement the actual disconnection logic.

        Raises:
            NotImplementedError: If this method is not implemented by the subclass.
        """
        raise NotImplementedError(self._not_implemented)

    @abstractmethod
    def subscribe(self, topic: str, qos: int = 0) -> None:
        """Subscribe to the given MQTT topic.

        This method subscribes the client to a specific topic and will listen for
        messages published to that topic. The QoS (Quality of Service) level can
        be set for the subscription.

        Args:
            topic (str): The MQTT topic to subscribe to.
            qos (int, optional): The Quality of Service level for the subscription. Defaults to 0.

        Raises:
            NotImplementedError: If this method is not implemented by the subclass.
        """
        raise NotImplementedError(self._not_implemented)

    @abstractmethod
    def loop_stop(self) -> None:
        """Stop the MQTT network loop.

        This method should stop the MQTT client's network loop, preventing further
        message dispatching or processing. It is commonly used when the client
        needs to shut down or stop receiving messages.

        Raises:
            NotImplementedError: If this method is not implemented by the subclass.
        """
        raise NotImplementedError(self._not_implemented)

    @abstractmethod
    def publish(self, topic: str, msg: str, qos: int = 0, retain: bool = False) -> None:
        """Publish a message to a given MQTT topic.

        This method sends a message to the MQTT broker. It is expected that
        subclasses implement the logic for message publishing.

        Args:
            topic (str): The topic to which the message will be published.
            msg (str): The message to be published.
            qos (int, optional): The Quality of Service level for the message. Defaults to 0.
            retain (bool, optional): If True, the message will be retained by the broker. Defaults to False.

        Raises:
            NotImplementedError: If this method is not implemented by the subclass.
        """
        raise NotImplementedError(self._not_implemented)

    @abstractmethod
    def loop_start(self) -> None:
        """Start the MQTT network loop.

        This method should start the network loop in a separate thread to handle
        the asynchronous delivery of messages. The loop will handle incoming and
        outgoing messages as well as reconnections if the connection is lost.

        Note: Since the MQTT network loop typically runs in a separate thread,
              subclasses should ensure thread-safety for any shared resources.

        Raises:
            NotImplementedError: If this method is not implemented by the subclass.
        """
        raise NotImplementedError(self._not_implemented)

    @abstractmethod
    def loop_forever(self) -> None:
        """Run the MQTT network loop indefinitely.

        This method blocks and runs the MQTT network loop forever. It handles
        all incoming and outgoing messages in a non-blocking manner.

        Note: This is a blocking call. If this method is called, the client
              will keep running until explicitly stopped. It is commonly
              used for long-running MQTT clients in production environments.

        Raises:
            NotImplementedError: If this method is not implemented by the subclass.
        """
        raise NotImplementedError(self._not_implemented)

    @property
    @abstractmethod
    def on_message(self) -> Callable[[object, Any, MqttMsg], None]:
        """Callback handler for receiving MQTT messages.

        This method defines the callback function that will be called whenever
        a new message arrives on a subscribed topic.

        Returns:
            Callable[[object, Any, MqttMsg], None]: The function that handles incoming messages.

        Raises:
            NotImplementedError: If this method is not implemented by the subclass.
        """
        raise NotImplementedError(self._not_implemented)

    @on_message.setter
    @abstractmethod
    def on_message(self, value: Callable[[object, Any, MqttMsg], None]) -> None:
        """Set the message handler, a method to be called when new messages are published.

        Args:
            value (Callable): Python method to be called on arrival of messages.

        Raises:
            NotImplementedError: If this method is not implemented by the subclass.
        """
        raise NotImplementedError(self._not_implemented)

    @property
    @abstractmethod
    def on_connect(self) -> Callable[[object, Any, int, int], None]:
        """Callback handler for successful connections to the broker.

        This method defines the callback function that will be called when
        the client successfully connects to the MQTT broker.

        Returns:
            Callable[[object, Any, int, int], None]: The function that handles successful connection events.

        Raises:
            NotImplementedError: If this method is not implemented by the subclass.
        """
        raise NotImplementedError(self._not_implemented)

    @on_connect.setter
    @abstractmethod
    def on_connect(self, value: Callable[[object, Any, int, int], None]) -> None:
        """Set the connection handler, a method to be called on successful connection.

        Args:
            value (Callable): Python method to be called when the client successfully connects.

        Raises:
            NotImplementedError: If this method is not implemented by the subclass.
        """
        raise NotImplementedError(self._not_implemented)

    @property
    @abstractmethod
    def on_disconnect(self) -> Callable[[Any, Any, int], None]:
        """Callback handler for disconnect events.

        This method defines the callback function that will be called when
        the client disconnects from the MQTT broker.

        Returns:
            Callable[[Any, Any, int], None]: The function that handles disconnect events.

        Raises:
            NotImplementedError: If this method is not implemented by the subclass.
        """
        raise NotImplementedError(self._not_implemented)

    @on_disconnect.setter
    @abstractmethod
    def on_disconnect(self, value: Callable[[Any, Any, int], None]) -> None:
        """Set the disconnect handler, a method to be called when the client disconnects.

        Args:
            value (Callable): Python method to be called on disconnect.

        Raises:
            NotImplementedError: If this method is not implemented by the subclass.
        """
        raise NotImplementedError(self._not_implemented)
