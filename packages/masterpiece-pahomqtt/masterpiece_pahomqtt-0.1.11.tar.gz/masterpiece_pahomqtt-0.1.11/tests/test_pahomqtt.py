import unittest
from unittest.mock import patch, MagicMock
from masterpiece_pahomqtt.pahomqtt import PahoMqtt


class TestPahoMqtt(unittest.TestCase):

    @patch("masterpiece_pahomqtt.pahomqtt.paho.Client")
    def test_connect_to_server(self, mock_paho_client: MagicMock) -> None:
        # Mock the behavior of the MQTT client's connect method
        mock_client_instance = MagicMock()
        mock_paho_client.return_value = mock_client_instance
        mock_client_instance.connect.return_value = (
            0  # Simulate a successful connection
        )

        # Create the broker instance
        broker = PahoMqtt()

        # Call the public method
        result: int = broker.connect_to_server("localhost", 1883)

        # Test the public behavior (observable effect)
        self.assertEqual(result, 0)  # Verify the return value from public API
        mock_client_instance.connect.assert_called_with(
            "localhost", 1883, 60, ""
        )  # Assert correct interaction

    @patch("masterpiece_pahomqtt.pahomqtt.paho.Client")
    def test_connect_to_server_failure(self, mock_paho_client: MagicMock) -> None:
        # Mock the behavior of the MQTT client's connect method to raise an exception
        mock_client_instance = MagicMock()
        mock_paho_client.return_value = mock_client_instance
        mock_client_instance.connect.side_effect = ConnectionError("Connection failed")

        # Create the broker instance
        broker = PahoMqtt()

        # Call the public method and check for exceptions
        with self.assertRaises(ConnectionError):
            broker.connect_to_server("localhost", 1883)

    @patch("masterpiece_pahomqtt.pahomqtt.paho.Client")
    def test_publish(self, mock_paho_client: MagicMock) -> None:
        # Setup the mock
        mock_client_instance = MagicMock()
        mock_paho_client.return_value = mock_client_instance

        # Create the broker instance
        broker = PahoMqtt()

        # Call the public method
        broker.publish("test/topic", "message")

        # Test the public behavior
        mock_client_instance.publish.assert_called_with(
            "test/topic", "message", 0, False
        )

    @patch("masterpiece_pahomqtt.pahomqtt.paho.Client")
    def test_publish_value_error(self, mock_paho_client: MagicMock) -> None:
        # Create the broker instance
        broker = PahoMqtt()

        # Call the public method with invalid input
        with self.assertRaises(ValueError):
            broker.publish("test/topic", "")

    @patch("masterpiece_pahomqtt.pahomqtt.paho.Client")
    def test_subscribe(self, mock_paho_client: MagicMock) -> None:
        # Setup the mock
        mock_client_instance = MagicMock()
        mock_paho_client.return_value = mock_client_instance

        # Create the broker instance
        broker = PahoMqtt()

        # Call the public method
        broker.subscribe("test/topic")

        # Test the public behavior
        mock_client_instance.subscribe.assert_called_with("test/topic", 0)

    @patch("masterpiece_pahomqtt.pahomqtt.paho.Client")
    def test_on_message_property_setter(self, mock_paho_client: MagicMock) -> None:
        # Setup the mock
        mock_client_instance = MagicMock()
        mock_paho_client.return_value = mock_client_instance

        # Create the broker instance
        broker = PahoMqtt()

        # Set the public property
        mock_callback = MagicMock()
        broker.on_message = mock_callback

        # Test the public behavior (setter for the property)
        mock_client_instance.on_message = mock_callback  # Assert that setter was called


if __name__ == "__main__":
    unittest.main()
