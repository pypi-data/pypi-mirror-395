from typing import Any
import unittest
from unittest.mock import patch, MagicMock
from juham_core import JuhamTs
from juham_shelly.shelly import Shelly


class TestShelly(unittest.TestCase):
    def setUp(self) -> None:
        self.shelly = Shelly("test_device", "test_prefix")

    def test_initialization(self) -> None:
        self.assertEqual(self.shelly.name, "test_device")
        self.assertEqual(self.shelly.mqtt_prefix, "test_prefix")
        self.assertEqual(self.shelly.relay_started, 0)

    def test_initialization_without_mqtt_prefix(self) -> None:
        shelly = Shelly("test_device")
        self.assertEqual(shelly.mqtt_prefix, "test_device")

    @patch("juham_shelly.shelly.timestamp", return_value=100.0)
    def test_elapsed_true(self, mock_timestamp: MagicMock) -> None:
        self.shelly.relay_started = 90.0
        result = self.shelly.elapsed(5.0)
        print(
            f"tsnow: {mock_timestamp.return_value}, relay_started: {self.shelly.relay_started}"
        )
        self.assertTrue(result)
        self.assertEqual(self.shelly.relay_started, mock_timestamp.return_value)

    @patch("juham_shelly.shelly.timestamp", return_value=95.0)
    def test_elapsed_false(self, mock_timestamp: MagicMock) -> None:
        self.shelly.relay_started = 90.0
        result = self.shelly.elapsed(10.0)
        print(
            f"tsnow: {mock_timestamp.return_value}, relay_started: {self.shelly.relay_started}"
        )
        self.assertFalse(result)
        self.assertEqual(
            self.shelly.relay_started, 90.0
        )  # Ensure relay_started is unchanged

    def test_to_dict(self) -> None:
        expected_dict: dict[str, Any] = {
            **JuhamTs.to_dict(self.shelly),
            "_shelly": {"mqtt_prefix": "test_prefix"},
        }
        self.assertEqual(self.shelly.to_dict(), expected_dict)

    def test_from_dict(self) -> None:
        data: dict[str, Any] = {
            "_class": "Shelly",
            "_object": {"name": "foo"},
            "_base": {},
            "_shelly": {"mqtt_prefix": "new_prefix"},
        }
        self.shelly.from_dict(data)
        self.assertEqual(self.shelly.mqtt_prefix, "new_prefix")


if __name__ == "__main__":
    unittest.main()
