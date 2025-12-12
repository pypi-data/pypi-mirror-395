from typing import Any
import unittest
from unittest.mock import MagicMock
from juham_shelly.shellydht22 import ShellyDHT22
from masterpiece.timeseries import Measurement

from juham_core.timeutils import epoc2utc


class TestShellyDHT22(unittest.TestCase):
    def setUp(self) -> None:
        self.device = ShellyDHT22("test_device", "test_prefix")
        self.device.warning = MagicMock()  # Mock the warning method
        self.device.publish = MagicMock()
        self.device.write = MagicMock()

        # Mock database_client and its methods
        self.mock_measurement: Measurement = MagicMock(spec=Measurement)
        self.device.database_client = MagicMock()
        self.device.database_client.measurement = MagicMock(
            return_value=self.mock_measurement
        )
        self.device.database_client.write = MagicMock()  # Prevent actual writes

    def test_valid_humidity(self) -> None:
        self.device.database_client.measurement = self.mock_measurement
        # Normal cases
        self.assertTrue(self.device.valid_humidity(50, 50))  # No change
        self.assertTrue(self.device.valid_humidity(60, 50))  # 20% increase
        self.assertFalse(
            self.device.valid_humidity(100, 50)
        )  # Exactly double (should fail)
        self.assertFalse(
            self.device.valid_humidity(110, 50)
        )  # More than double (should fail)

        # Edge case where previous value is undefined (101.0 initial value)
        self.assertTrue(self.device.valid_humidity(102, 101))  # Slight increase is fine
        self.assertFalse(self.device.valid_humidity(202, 101))  # Exactly double

    def test_on_sensor_valid_humidity(self) -> None:
        self.device.database_client.measurement = self.mock_measurement
        params: dict[str, Any] = {"ts": 1700000000, "humidity:1": {"rh": 50}}
        self.device.on_sensor(params)
        self.assertEqual(self.device.previous_humidity, 50)
        self.device.publish.assert_called()

    def test_on_sensor_discard_invalid_humidity(self) -> None:
        self.device.database_client.measurement = self.mock_measurement
        # First valid reading
        params: dict[str, Any] = {"ts": 1700000000, "humidity:1": {"rh": 50}}
        self.device.on_sensor(params)
        self.assertEqual(self.device.previous_humidity, 50)

        # Invalid reading (twice as high)
        params = {"ts": 1700000001, "humidity:1": {"rh": 101}}
        self.device.on_sensor(params)
        self.device.warning.assert_called()  # Should trigger warning
        self.assertEqual(self.device.previous_humidity, 50)  # Should not update

        # Next correct reading
        params = {"ts": 1700000002, "humidity:1": {"rh": 51}}
        self.device.on_sensor(params)
        self.assertEqual(self.device.previous_humidity, 51)  # Should update


if __name__ == "__main__":
    unittest.main()
