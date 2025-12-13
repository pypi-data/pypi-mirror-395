import unittest
from typing import Dict, Any
import json
from unittest.mock import MagicMock, patch
from juham_shelly.shellyds18B20 import ShellyDS18B20
from masterpiece import Measurement
from masterpiece.mqtt import MqttMsg
from juham_core.timeutils import timestamp


class TestShellyDS18B20(unittest.TestCase):

    @patch("juham_core.juham.Mqtt")  # Mock the MqttClient used by ShellyDS18B20
    @patch("juham_core.juham_ts.JuhamTs")  # Patch JuhamTs to mock measurement attribute
    def setUp(self, MockJuhamTs: MagicMock, MockMqttClient: MagicMock) -> None:
        self.mock_client: MagicMock = MockMqttClient()
        self.shelly_device: ShellyDS18B20 = ShellyDS18B20(
            name="test_device", mqtt_prefix="test_prefix"
        )
        self.shelly_device.client = self.mock_client  # type: ignore

        patch.object(self.shelly_device, "write", MagicMock()).start()

        # Mock the database client and its measurement
        self.mock_measurement: Measurement = MagicMock(spec=Measurement)

        # Now patch the database_client to be an instance of JuhamTs
        self.mock_juham_ts_instance = MockJuhamTs.return_value
        self.mock_juham_ts_instance.measurement = self.mock_measurement
        self.mock_juham_ts_instance.database_client = self.mock_juham_ts_instance

        # Assign this mocked JuhamTs instance to shelly_device
        self.shelly_device.database_client = self.mock_juham_ts_instance

        # Ensure measurement mock is properly initialized
        self.mock_measurement.return_value = MagicMock(spec=Measurement)

    def test_measurement_mock(self) -> None:
        """Test that the measurement mock is correctly assigned."""
        self.assertIsNotNone(self.shelly_device.database_client)
        self.assertIsNotNone(self.shelly_device.database_client.measurement)
        # Check that the measurement mock is indeed a Measurement instance or mock
        self.assertTrue(
            isinstance(self.shelly_device.database_client.measurement, MagicMock)
        )

    def test_on_connect_success(self) -> None:
        """Test that the on_connect method subscribes to the topic on successful connection."""
        mock_userdata: Dict[str, Any] = {}
        mock_flags: int = 0
        mock_rc: int = 0
        with patch.object(self.shelly_device, "subscribe") as mock_subscribe:
            self.shelly_device.on_connect(
                self.mock_client, mock_userdata, mock_flags, mock_rc
            )
            mock_subscribe.assert_called_once_with("test_prefix/events/rpc")

    @patch(
        "juham_core.timeutils.timestamp"
    )  # Patch the timestamp function to return a fixed value
    def test_on_message_notify_status(self, mock_timestamp: MagicMock) -> None:
        """Test that on_message handles 'NotifyStatus' messages."""
        mock_msg: MagicMock = MagicMock(spec=MqttMsg)
        mock_msg.topic = "test_prefix/events/rpc"
        mock_msg.payload.decode.return_value = json.dumps(
            {
                "method": "NotifyStatus",
                "params": {
                    "ts": 1742114605.969054,
                    "temperature:sensor_1": {"tC": 25.0},
                },
            }
        )

        mock_timestamp.return_value = (
            1742114605.969054  # Mock the timestamp to match the expected value
        )

        with patch.object(self.shelly_device, "on_sensor") as mock_on_sensor:
            self.shelly_device.on_message(self.mock_client, {}, mock_msg)

            # Now the timestamp will match since we mocked it
            mock_on_sensor.assert_called_once_with(
                {"ts": 1742114605.969054, "temperature:sensor_1": {"tC": 25.0}}
            )

    def test_on_message_unknown_method(self) -> None:
        """Test that on_message handles an unknown method gracefully."""
        mock_msg: MagicMock = MagicMock(spec=MqttMsg)
        mock_msg.topic = "test_prefix/events/rpc"
        mock_msg.payload.decode.return_value = json.dumps(
            {"method": "UnknownMethod", "params": {}}
        )

        with patch.object(self.shelly_device, "warning") as mock_warning:
            self.shelly_device.on_message(self.mock_client, {}, mock_msg)
            mock_warning.assert_called_once_with(
                f"Unknown method {self.shelly_device.name} {self.shelly_device.shelly_device_topic} UnknownMethod",
                "{'method': 'UnknownMethod', 'params': {}}",  # Use single quotes here
            )

    @patch("masterpiece.timeseries.Measurement")  # Mock Measurement
    def test_on_sensor(self, MockMeasurement: MagicMock) -> None:
        """Test that on_sensor processes temperature readings correctly."""
        mock_point: MagicMock = MagicMock()
        MockMeasurement.return_value = mock_point

        sensor_data: Dict[str, Any] = {
            "ts": timestamp(),
            "temperature:sensor_1": {"tC": 25.0},
        }

        # Mock Mqtt class initialization and its publish method
        mock_mqtt_client = MagicMock()  # Mock the Mqtt client
        mock_mqtt_client.publish = MagicMock()  # Mock the publish method of Mqtt client

        # Now patch the mqtt_client on the instance of Juham
        with patch.object(self.shelly_device, "mqtt_client", mock_mqtt_client):
            with patch.object(self.shelly_device, "write") as mock_write:
                self.shelly_device.on_sensor(sensor_data)

                # Check if the publish method was called with the correct arguments
                mock_mqtt_client.publish.assert_called_once_with(
                    "/temperature/test_prefix/sensor_1",
                    json.dumps(
                        {
                            "sensor": "test_prefix/sensor_1",
                            "timestamp": sensor_data["ts"],
                            "temperature": 25,
                        }
                    ),
                    1,
                    True,
                )

                # Check if the time series data point was written
                mock_write.assert_called_once()

    def test_to_dict(self) -> None:
        """Test the to_dict method."""
        shelly_device_dict: Dict[str, Any] = self.shelly_device.to_dict()
        self.assertIn("DS18B20", shelly_device_dict)
        self.assertEqual(shelly_device_dict["DS18B20"]["shelly_topic"], "test_prefix/events/rpc")
        self.assertEqual(
            shelly_device_dict["DS18B20"]["temperature_topic"],
            "/temperature/",
        )

    def test_from_dict(self) -> None:
        """Test the from_dict method."""
        data: Dict[str, Any] = {
            "_class": "ShellyDS18B20",
            "_version": 0,
            "_base": {"name": "test_device", "mqtt_prefix": "test_prefix"},
            "_object": {},
            "DS18B20": {
                "shelly_topic": "test_prefix/events/rpc",
                "temperature_topic": "/temperature/",
            },
        }
        self.shelly_device.from_dict(data)
        self.assertEqual(self.shelly_device.shelly_topic, "test_prefix/events/rpc")
        self.assertEqual(self.shelly_device.temperature_topic, "/temperature/")





class TestShellyDS18B20_2(unittest.TestCase):
    def setUp(self):
        self.device = ShellyDS18B20(name="test", mqtt_prefix="dev1")

        # Mock side-effecting methods
        self.device.publish = MagicMock()
        self.device.write = MagicMock()
        self.device.warning = MagicMock()
        self.device.error = MagicMock()

        mock_point = MagicMock()
        mock_point.tag.return_value = mock_point
        mock_point.field.return_value = mock_point
        mock_point.time.return_value = mock_point

        self.device.measurement = MagicMock(return_value=mock_point)


    def test_valid_temperature(self):
        """Valid tC value → publish + write should be called once."""
        params = {
            "ts": 123456,
            "temperature:0": {"tC": 25},
        }

        self.device.on_sensor(params)

        # Publish should be called with integer temperature
        self.device.publish.assert_called_once()
        published_payload = self.device.publish.call_args[0][1]

        self.assertIn('"temperature": 25', published_payload)

        # Influx write should also be called
        self.device.write.assert_called_once()

        # No warnings/errors
        self.device.warning.assert_not_called()
        self.device.error.assert_not_called()

    def test_none_temperature(self):
        """tC = None → should skip silently and warn."""
        params = {
            "ts": 123456,
            "temperature:0": {"tC": None},
        }

        self.device.on_sensor(params)

        # No publish, no write
        self.device.publish.assert_not_called()
        self.device.write.assert_not_called()

        # Warning about null value must be logged
        self.device.warning.assert_called_once()
        self.device.error.assert_not_called()

    def test_invalid_temperature_string(self):
        """tC contains invalid string → skip and warn."""
        params = {
            "ts": 123456,
            "temperature:0": {"tC": "not-a-number"},
        }

        self.device.on_sensor(params)

        # No publish, no write
        self.device.publish.assert_not_called()
        self.device.write.assert_not_called()

        # Warning should be logged
        self.device.warning.assert_called_once()
        self.device.error.assert_not_called()

    def test_multiple_sensors_mixed_values(self):
        """One valid and one invalid sensor → only valid one processed."""
        params = {
            "ts": 123456,
            "temperature:0": {"tC": 20.2},          # valid
            "temperature:1": {"tC": None},          # invalid
            "temperature:2": {"tC": "corrupted"},   # invalid
        }

        self.device.on_sensor(params)

        # Only the valid one gets published
        self.assertEqual(self.device.publish.call_count, 1)
        # Only the valid one written
        self.assertEqual(self.device.write.call_count, 1)

        # Invalid sensors should produce warnings
        # (order is not guaranteed, so we check count)
        self.assertEqual(self.device.warning.call_count, 2)
        self.device.error.assert_not_called()



if __name__ == "__main__":
    unittest.main()
