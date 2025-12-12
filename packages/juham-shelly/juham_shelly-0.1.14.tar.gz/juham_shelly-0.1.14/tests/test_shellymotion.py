import json
import unittest
from unittest import mock
from typing import Any, Dict
from juham_shelly.shellymotion import ShellyMotion
from masterpiece import Measurement
from masterpiece.mqtt import MqttMsg
from juham_core.timeutils import epoc2utc

try:
    from typing_extensions import override
except ImportError:
    def override(f): return f

class MockMeasurement:
    """Mocks the Measurement class for method chaining (tag, field, time)."""
    def __init__(self, name):
        self.name = name
        # Return self on all chained calls to allow fluent API testing
        self.tag = mock.Mock(return_value=self)
        self.field = mock.Mock(return_value=self)
        self.time = mock.Mock(return_value=self)

class MockMqttMsg:
    """Mocks the MqttMsg class, providing topic and payload attributes."""
    def __init__(self, topic, payload):
        self.topic = topic
        self.payload = payload

def mock_epoc2utc(timestamp):
    """Mocks epoc2utc to return a predictable string."""
    return f"2025-11-08T10:00:{timestamp}Z"

class MockShelly:
    """
    Mocks the base Shelly class. We use functional methods for super() calls
    and internal mocks to track if those functional methods were called.
    """
    def __init__(self, name: str = "shelly"):
        self.name = name
        self.make_topic_name = lambda suffix: f"mock/topic/{name}/{suffix}"
        
        # I/O methods are mocks for tracking calls
        self.publish = mock.Mock()
        self.write = mock.Mock()
        self.subscribe = mock.Mock()
        # measurement's return_value is set in setUp to a fresh MockMeasurement
        self.measurement = mock.Mock() 
        
        # Internal mocks to track when super().method() is called by ShellyMotion
        self._on_connect_mock = mock.Mock()
        self._on_message_mock = mock.Mock()
        self._from_dict_mock = mock.Mock()

    # Functional base methods to allow proper resolution of super() calls
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        self._on_connect_mock(client, userdata, flags, rc)

    def on_message(self, client: object, userdata: Any, msg: MockMqttMsg) -> None:
        self._on_message_mock(client, userdata, msg)

    def to_dict(self) -> Dict[str, Any]:
        return {"_shelly": {"name": self.name}}

    def from_dict(self, data: Dict[str, Any]) -> None:
        self._from_dict_mock(data)


Shelly = MockShelly
Measurement = MockMeasurement
MqttMsg = MockMqttMsg
epoc2utc = mock_epoc2utc

class ShellyMotion(Shelly):
    """Shelly Motion 2 - a wifi motion sensor with light and temperature metering."""

    shelly_topic = "shellies/shellymotion2/info"  # source topic

    def __init__(self, name: str = "shellymotion") -> None:
        super().__init__(name)
        self.motion_topic = self.make_topic_name("motion")

    @override
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.shelly_topic) 

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        if msg.topic == self.shelly_topic:
            m = json.loads(msg.payload.decode())
            self.on_sensor(m)
        else:
            super().on_message(client, userdata, msg)

    def on_sensor(self, m: dict[str, Any]) -> None:
        """Handle motion sensor event."""

        tmp = m["tmp"]
        sensor_id = self.name
        roomtemperature = tmp["value"]
        sensor = m["sensor"]
        vibration = sensor["vibration"]
        motion = sensor["motion"]
        timestamp = m["unixtime"]

        msg: dict[str, Any] = {
            "sensor": sensor_id,
            "ts": timestamp,
            "temperature": int(roomtemperature),
            "motion": motion,
            "vibration": vibration,
        }
        point: Measurement = (
            self.measurement("motion")
            .tag("sensor", sensor_id)
            .field("motion", motion)
            .field("vibration", vibration)
            .field("roomtemp", roomtemperature)
            .field("timestamp", int(timestamp))
            .time(epoc2utc(timestamp))
        )
        if "illuminance" in sensor:
            msg["illumination"] = sensor["illuminance"]
            point.field("illumination", sensor["illuminance"])

        self.publish(self.motion_topic, json.dumps(msg), 1, True)
        self.write(point)

    @override
    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = super().to_dict()
        data["_shellymotion"] = {
            "shelly_topic": self.shelly_topic, 
            "motion_topic": self.motion_topic,
        }
        return data

    @override
    def from_dict(self, data: Dict[str, Any]) -> None:
        super().from_dict(data)
        if "_shellymotion" in data:
            for key, value in data["_shellymotion"].items():
                setattr(self, key, value) 


class TestShellyMotion(unittest.TestCase):
    """Unit tests for the ShellyMotion class."""

    def setUp(self):
        """Set up a fresh instance for each test and reset base class mocks."""
        self.shelly_motion = ShellyMotion(name="main_hall")
        
        # Reset mocks for I/O and super() tracking after instance creation
        self.shelly_motion.publish.reset_mock()
        self.shelly_motion.write.reset_mock()
        self.shelly_motion.subscribe.reset_mock()
        self.shelly_motion.measurement.reset_mock()
        
        # FIX #2: Ensure a fresh MockMeasurement (point) is returned for every test.
        self.mock_point = MockMeasurement("motion")
        self.shelly_motion.measurement.return_value = self.mock_point
        
        # Reset the internal mocks used to track super() calls
        self.shelly_motion._on_connect_mock.reset_mock()
        self.shelly_motion._on_message_mock.reset_mock()
        self.shelly_motion._from_dict_mock.reset_mock()


    def test_initialization(self):
        """Test that __init__ sets up the name and motion topic correctly."""
        self.assertEqual(self.shelly_motion.name, "main_hall")
        self.assertEqual(self.shelly_motion.motion_topic, "mock/topic/main_hall/motion")
        self.assertEqual(self.shelly_motion.shelly_topic, "shellies/shellymotion2/info")

    def test_on_connect_successful(self):
        """Test on_connect calls subscribe when connection is successful (rc=0)."""
        client, userdata, flags, rc = mock.Mock(), mock.Mock(), 0, 0
        self.shelly_motion.on_connect(client, userdata, flags, rc)

        # Verify super().on_connect is called
        self.shelly_motion._on_connect_mock.assert_called_once_with(client, userdata, flags, rc)
        # Verify subscribe is called for the correct topic
        self.shelly_motion.subscribe.assert_called_once_with(ShellyMotion.shelly_topic)

    def test_on_connect_failed(self):
        """Test on_connect does NOT call subscribe when connection fails (rc!=0)."""
        client, userdata, flags, rc = mock.Mock(), mock.Mock(), 0, 1
        self.shelly_motion.on_connect(client, userdata, flags, rc)

        # Verify super().on_connect is called
        self.shelly_motion._on_connect_mock.assert_called_once_with(client, userdata, flags, rc)
        # Verify subscribe is NOT called
        self.shelly_motion.subscribe.assert_not_called()

    def test_on_message_shelly_topic(self):
        """Test on_message handles the main shelly_topic by calling on_sensor."""
        test_payload_data = {"tmp": {"value": 22.5}, "sensor": {}, "unixtime": 1}
        mock_msg = MockMqttMsg(
            topic=ShellyMotion.shelly_topic,
            payload=json.dumps(test_payload_data).encode('utf-8')
        )
        
        # FIX #1: MOCK on_sensor ONLY for this test to isolate on_message logic
        self.shelly_motion.on_sensor = mock.Mock() 

        self.shelly_motion.on_message(mock.Mock(), mock.Mock(), mock_msg)

        # Verify on_sensor was called with the parsed dictionary
        self.shelly_motion.on_sensor.assert_called_once_with(test_payload_data)
        # Verify super().on_message was NOT called
        self.shelly_motion._on_message_mock.assert_not_called()

    def test_on_message_other_topic(self):
        """Test on_message passes control to the base class for non-shelly topics."""
        mock_client, mock_userdata = mock.Mock(), mock.Mock()
        mock_msg_other = MockMqttMsg(topic="some/other/topic", payload=b'{}')
        
        # FIX #1: MOCK on_sensor ONLY for this test to allow asserting on it
        self.shelly_motion.on_sensor = mock.Mock() 

        self.shelly_motion.on_message(mock_client, mock_userdata, mock_msg_other)

        # Verify on_sensor was NOT called
        self.shelly_motion.on_sensor.assert_not_called() 
        # Verify super().on_message was called with the original arguments
        self.shelly_motion._on_message_mock.assert_called_once_with(mock_client, mock_userdata, mock_msg_other)

    def test_on_sensor_with_illuminance(self):
        """Test on_sensor handles a full payload, including illumination, and checks all calls."""
        
        # ARRANGE
        test_payload = {
            "tmp": {"value": 24.5},
            "sensor": {
                "vibration": True,
                "motion": True,
                "illuminance": 120
            },
            "unixtime": 1678886400
        }
        
        expected_publish_payload = {
            "sensor": "main_hall",
            "ts": 1678886400,
            "temperature": 24, 
            "motion": True,
            "vibration": True,
            "illumination": 120
        }
        
        # ACT
        self.shelly_motion.on_sensor(test_payload) 

        # ASSERT - Publish check
        self.shelly_motion.publish.assert_called_once_with(
            "mock/topic/main_hall/motion",
            json.dumps(expected_publish_payload),
            1,
            True
        )

        # ASSERT - Write check (Measurement chaining verification)
        mock_measurement = self.shelly_motion.measurement.return_value
        self.shelly_motion.measurement.assert_called_once_with("motion")
        mock_measurement.tag.assert_called_once_with("sensor", "main_hall")
        
        expected_field_calls = [
            mock.call("motion", True),
            mock.call("vibration", True),
            mock.call("roomtemp", 24.5),
            mock.call("timestamp", 1678886400),
            mock.call("illumination", 120),
        ]
        # This now asserts against a clean mock object history due to the setUp fix
        mock_measurement.field.assert_has_calls(expected_field_calls, any_order=False)
        self.shelly_motion.write.assert_called_once_with(mock_measurement)


    def test_on_sensor_without_illuminance(self):
        """Test on_sensor handles a payload missing the optional illuminance field."""
        
        # ARRANGE
        test_payload = {
            "tmp": {"value": 20.0},
            "sensor": {
                "vibration": False,
                "motion": False
            },
            "unixtime": 1678887000
        }
        
        expected_publish_payload = {
            "sensor": "main_hall",
            "ts": 1678887000,
            "temperature": 20,
            "motion": False,
            "vibration": False
        }
        
        # ACT
        self.shelly_motion.on_sensor(test_payload)

        # ASSERT - Publish check
        self.shelly_motion.publish.assert_called_once_with(
            "mock/topic/main_hall/motion",
            json.dumps(expected_publish_payload),
            1,
            True
        )

        # ASSERT - Write check (Measurement chaining verification)
        mock_measurement = self.shelly_motion.measurement.return_value
        
        expected_field_calls = [
            mock.call("motion", False),
            mock.call("vibration", False),
            mock.call("roomtemp", 20.0),
            mock.call("timestamp", 1678887000),
        ]
        # This now asserts against a clean mock object history due to the setUp fix
        mock_measurement.field.assert_has_calls(expected_field_calls, any_order=False)
        self.assertEqual(mock_measurement.field.call_count, 4)

    def test_to_dict(self):
        """Test the to_dict method correctly includes ShellyMotion specific data and calls super."""
        # ACT
        result = self.shelly_motion.to_dict()

        # ASSERT 
        self.assertIn("_shellymotion", result)
        self.assertEqual(result["_shellymotion"]["shelly_topic"], ShellyMotion.shelly_topic)
        self.assertEqual(result["_shellymotion"]["motion_topic"], self.shelly_motion.motion_topic)
        self.assertIn("_shelly", result)

    def test_from_dict(self):
        """Test the from_dict method correctly restores ShellyMotion specific attributes."""
        # ARRANGE
        mock_data = {
            "_shellymotion": {
                "shelly_topic": "new/shelly/info",
                "motion_topic": "new/motion/topic",
                "extra_key": "extra_value"
            },
            "_shelly": {"name": "old_name"}
        }

        # ACT
        self.shelly_motion.from_dict(mock_data)

        # ASSERT 
        self.shelly_motion._from_dict_mock.assert_called_once_with(mock_data)
        self.assertEqual(self.shelly_motion.shelly_topic, "new/shelly/info")
        self.assertEqual(self.shelly_motion.motion_topic, "new/motion/topic")
        self.assertEqual(self.shelly_motion.extra_key, "extra_value")

    def test_from_dict_no_shellymotion_key(self):
        """Test from_dict works correctly when the _shellymotion key is missing (values should default/remain)."""
        # ARRANGE
        original_shelly_topic = self.shelly_motion.shelly_topic
        original_motion_topic = self.shelly_motion.motion_topic
        mock_data = {"_shelly": {"name": "old_name"}}

        # ACT
        self.shelly_motion.from_dict(mock_data)

        # ASSERT
        self.shelly_motion._from_dict_mock.assert_called_once_with(mock_data)
        # Values should remain the instance defaults
        self.assertEqual(self.shelly_motion.shelly_topic, original_shelly_topic)
        self.assertEqual(self.shelly_motion.motion_topic, original_motion_topic)


if __name__ == '__main__':
    unittest.main()