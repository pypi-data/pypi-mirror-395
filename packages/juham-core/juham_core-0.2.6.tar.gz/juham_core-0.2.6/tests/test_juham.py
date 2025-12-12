import unittest
from unittest.mock import MagicMock, patch
from masterpiece import Mqtt, Measurement
from juham_core import Juham


class TestJuham(unittest.TestCase):
    def setUp(self) -> None:
        """Set up a Juham instance for testing."""
        self.juham = Juham(name="TestJuham")
        self.juham.mqtt_client = MagicMock(spec=Mqtt)

    def test_initialization(self) -> None:
        """Test that Juham initializes correctly."""
        self.assertEqual(self.juham.name, "TestJuham")
        self.assertIsNotNone(self.juham.mqtt_client)
        self.assertEqual(self.juham.mqtt_topic_base, "")

    def test_to_dict_with_defaults(self) -> None:
        """Test the to_dict method with default settings."""
        data = self.juham.to_dict()
        self.assertIn("_base", data)
        # mqtt_host: str = data["_base"]["mqtt_host"]
        # self.assertEqual(mqtt_host, Juham.mqtt_host)

    def test_from_dict_with_defaults(self):
        """Test the from_dict method."""
        data = {
            "_class": self.juham.get_class_id(),  # Use the same class ID as the instance
            "_version:": 0,
            "_base": {  # Add the expected "_base" key
                "mqtt_host": "test.mqtt.host",
            },
            "_object": {
                "name": "TestName",
                "payload": None,  # Example: Adjust this based on your class implementation
            },
        }

        # Call the from_dict method with the properly structured data
        self.juham.from_dict(data)

        # Assert that the attributes were set correctly
        self.assertEqual(self.juham.name, "TestName")
        self.assertEqual(
            self.juham.mqtt_host, "test.mqtt.host"
        )  # Check the "_base" key's effect
        self.assertIsNone(self.juham.payload)

    def test_initialize(self) -> None:
        """Test the initialize method."""
        with patch.object(self.juham, "init_mqtt") as mock_init_mqtt:
            self.juham.initialize()
            mock_init_mqtt.assert_called_once_with(self.juham.name)

    def test_on_message_shutdown(self) -> None:
        """Test the on_message method handles the shutdown command."""
        msg = MagicMock()
        msg.topic = self.juham.mqtt_topic_control
        msg.payload = '{"command": "shutdown"}'

        self.juham.on_message(None, None, msg)
        self.juham.mqtt_client.disconnect.assert_called_once()
        self.juham.mqtt_client.loop_stop.assert_called_once()

    def test_on_connect(self) -> None:
        """Test the on_connect method."""
        self.juham.on_connect(None, None, None, 0)
        self.juham.mqtt_client.subscribe.assert_called_once_with(
            self.juham.mqtt_topic_control
        )

    def test_make_topic_name(self) -> None:
        """Test the make_topic_name method."""
        self.juham.mqtt_root_topic = "root"
        topic = self.juham.make_topic_name("test")
        self.assertEqual(topic, "root/test")


if __name__ == "__main__":
    unittest.main()
