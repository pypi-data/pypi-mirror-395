import unittest
from unittest.mock import MagicMock, patch
from masterpiece import TimeSeries, Measurement
from juham_core.juham_ts import JuhamTs


class TestJuhamTs(unittest.TestCase):
    def setUp(self) -> None:
        """Set up a JuhamTs instance for testing."""
        self.juham_ts = JuhamTs(name="TestJuhamTs")
        self.juham_ts.database_client = MagicMock(spec=TimeSeries)

    def test_initialization(self) -> None:
        """Test that JuhamTs initializes correctly."""
        self.assertEqual(self.juham_ts.name, "TestJuhamTs")
        self.assertIsNotNone(self.juham_ts.database_client)

    def test_to_dict_with_defaults(self) -> None:
        """Test the to_dict method with default settings."""
        data = self.juham_ts.to_dict()
        self.assertIn("_database", data)
        # database_client: str = data["_database"]["db_client"]
        # self.assertEqual(database_client, JuhamTs.database_client)

    def test_from_dict_with_defaults(self):
        """Test the from_dict method."""
        data = {
            "_class": self.juham_ts.get_class_id(),  # Use the same class ID as the instance
            "_version:": 0,
            "_base": {  # Add the expected "_base" key
                "mqtt_host": "test.mqtt.host",
            },
            "_database": {  # Add the expected "_database" key
                "db_client": {
                    "_class": "TimeSeries",
                    # Add other necessary attributes for the database client
                },
            },
            "_object": {
                "name": "TestName",
                "payload": None,  # Example: Adjust this based on your class implementation
            },
        }

        # Call the from_dict method with the properly structured data
        self.juham_ts.from_dict(data)

        # Assert that the attributes were set correctly
        self.assertEqual(self.juham_ts.name, "TestName")
        self.assertIsNotNone(self.juham_ts.database_client)

    def test_initialize(self) -> None:
        """Test the initialize method."""
        with patch.object(self.juham_ts, "init_database") as mock_init_db, patch.object(
            self.juham_ts, "init_mqtt"
        ) as mock_init_mqtt:
            self.juham_ts.initialize()
            mock_init_db.assert_called_once_with(self.juham_ts.name)
            mock_init_mqtt.assert_called_once_with(self.juham_ts.name)

    def test_write_with_success(self) -> None:
        """Test the write method when the database client writes successfully."""
        mock_measurement = MagicMock(spec=Measurement)
        self.juham_ts.database_client.write.return_value = None
        self.juham_ts.write(mock_measurement)
        self.juham_ts.database_client.write.assert_called_once_with(mock_measurement)

    def test_write_with_retries(self) -> None:
        """Test the write method retries on failure."""
        mock_measurement = MagicMock(spec=Measurement)
        self.juham_ts.database_client.write.side_effect = Exception("Write error")
        self.juham_ts.write(mock_measurement)
        self.assertEqual(
            self.juham_ts.database_client.write.call_count, self.juham_ts.write_attempts
        )

    def test_read_last_value(self) -> None:
        """Test the read_last_value method."""
        self.juham_ts.database_client.read_last_value.return_value = {"value": 42}
        result = self.juham_ts.read_last_value("measurement")
        self.assertEqual(result, {"value": 42})
        self.juham_ts.database_client.read_last_value.assert_called_once_with(
            "measurement", None, None
        )


if __name__ == "__main__":
    unittest.main()
