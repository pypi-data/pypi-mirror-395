import os
import socket
from typing import Any, Callable, Optional
from typing_extensions import override

import paho.mqtt.client as paho
from paho.mqtt.client import MQTTMessage as MqttMsg
from masterpiece.mqtt import Mqtt


class PahoMqtt(Mqtt):
    """MQTT broker implementation based on paho.mqtt.

    Creates a paho mosquitto client running on localhost and port 1883.
    """

    paho_version = 1

    def __init__(self, name: str = "paho") -> None:
        """Construct MQTT client for the configured mqtt broker of the
        configured paho_version.

        Args:
            name (str): name for the object.
        """
        super().__init__(name)
        if self.paho_version == 2:
            self.mqtt_client = paho.Client(
                paho.CallbackAPIVersion.VERSION1, name + str(os.getpid())
            )
        else:
            self.mqtt_client = paho.Client(name + str(os.getpid()))

    @override
    def connect_to_server(
        self,
        host: str = "localhost",
        port: int = 1883,
        keepalive: int = 60,
        bind_address: str = "",
    ) -> int:
        """Connects the client to the mqtt broker."""
        try:
            rc = self.mqtt_client.connect(host, port, keepalive, bind_address)
            self.info(f"Connected to MQTT broker at {host}:{port}")
            return rc
        except (socket.error, OSError) as e:
            self.error(f"Failed to connect to MQTT broker at {host}:{port}. Error: {e}")
            raise ConnectionError(
                f"Unable to connect to MQTT broker at {host}:{port}"
            ) from e
        except Exception as e:
            self.error(f"An unexpected error occurred: {e}")
            raise

    @override
    def disconnect(
        self, reasoncode: Optional[int] = None, properties: Optional[Any] = None
    ) -> None:
        """Disconnect.

        Args:
            reasoncode (Optional[int]): MQTT 5 reason code for disconnection. Defaults to None.
            properties (Optional[Any]): MQTT 5 properties for disconnection. Defaults to None.
        """
        try:
            self.mqtt_client.disconnect()
            self.info("Disconnected from MQTT broker.")
        except Exception as e:
            self.error(f"Failed to disconnect. Error: {e}")
            raise

    @override
    def subscribe(self, topic: str, qos: int = 0) -> None:
        """Subscribe to the given topic."""
        try:
            self.info(f"Subscribing to topic: {topic}")
            self.mqtt_client.subscribe(topic, qos)
        except Exception as e:
            self.error(f"Failed to subscribe to topic {topic}. Error: {e}")
            raise

    @override
    def loop_stop(self) -> None:
        """Stops the MQTT network loop."""
        try:
            self.mqtt_client.loop_stop()
            self.info("Stopped MQTT loop.")
        except Exception as e:
            self.error(f"Failed to stop MQTT loop. Error: {e}")
            raise

    @override
    def publish(self, topic: str, msg: str, qos: int = 0, retain: bool = False) -> None:
        """Publishes an MQTT message.

        This method sends a message to the MQTT broker and publishes it
        to the given topic.

        Parameters:
        topic (str): The topic the message is published to.
        msg (str): The message to be published.
        qos (int): Quality of Service level. Defaults to 0.
        retain (bool): Retain flag. Defaults to False.

        Raises:
        ValueError: If the message is not a string or is empty.
        ConnectionError: If there is a problem connecting to the MQTT broker.
        """
        if not isinstance(msg, str) or not msg.strip():
            raise ValueError("Message must be a non-empty string.")
        try:
            self.mqtt_client.publish(topic, msg, qos, retain)
        except (socket.error, OSError) as e:
            self.error(f"Failed to publish message to {topic}. Error: {e}")
            raise ConnectionError(f"Failed to publish message to {topic}") from e
        except Exception as e:
            self.error(f"An unexpected error occurred during publish: {e}")
            raise

    @override
    def loop_start(self) -> None:
        """Starts the MQTT network loop."""
        try:
            self.mqtt_client.loop_start()
            self.info("Started MQTT loop.")
        except Exception as e:
            self.error(f"Failed to start MQTT loop. Error: {e}")
            raise

    @override
    def loop_forever(self) -> None:
        """Blocks and runs the MQTT loop forever."""
        try:
            self.info("Entering MQTT loop.")
            self.mqtt_client.loop_forever()
        except Exception as e:
            self.error(f"Failed to run MQTT loop forever. Error: {e}")
            raise

    @property
    @override
    def on_message(self) -> Callable[[object, Any, MqttMsg], None]:
        return self.mqtt_client.on_message

    @on_message.setter
    @override
    def on_message(self, value: Callable[[object, Any, MqttMsg], None]) -> None:
        self.mqtt_client.on_message = value

    @property
    @override
    def on_connect(self) -> Callable[[object, Any, int, int], None]:
        return self.mqtt_client.on_connect

    @on_connect.setter
    @override
    def on_connect(self, value: Callable[[object, Any, int, int], None]) -> None:
        self.mqtt_client.on_connect = value

    @property
    @override
    def on_disconnect(self) -> Callable[[Any, Any, int], None]:
        return self.mqtt_client.on_disconnect

    @on_disconnect.setter
    @override
    def on_disconnect(self, value: Callable[[Any, Any, int], None]) -> None:
        self.mqtt_client.on_disconnect = value
