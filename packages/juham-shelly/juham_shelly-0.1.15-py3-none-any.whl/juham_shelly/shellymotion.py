import json
from typing import Any, Dict, Optional
from typing_extensions import override

from masterpiece import Measurement
from masterpiece.mqtt import MqttMsg
from juham_core.timeutils import epoc2utc
from .shelly import Shelly


class ShellyMotion(Shelly):
    """Shelly Motion 2 - a wifi motion sensor with light and temperature metering."""

    shelly_topic = "shellies/shellymotion2/info"  # source topic

    def __init__(self, name: str = "shellymotion", mqttprefix="") -> None:
        super().__init__(name, mqttprefix)
        self.motion_topic = self.make_topic_name("motion")
        self.shelly_device_topic = f"{mqttprefix}{self.shelly_topic}"
        
    @override
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.shelly_topic)

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        if self.shelly_device_topic == msg.topic:
            if not msg.payload:
                self.error(f"Empty payload on topic {msg.topic}")
                return
            payload : Optional[bytes] = None
            try:
                payload = msg.payload.decode(errors="replace")
                m = json.loads(payload)
            except Exception as e:
                self.error(f"JSON parse error on topic {msg.topic}: {e}, payload={payload!r}")
                return
            self.on_sensor(m)
        else:
            super().on_message(client, userdata, msg)

    def on_sensor(self, m: dict[str, Any]) -> None:
        """Handle motion sensor event. This method reads the incoming event,
        translates it, and publishes it to the Juham topic. It also writes the
        attributes to the time series database.

        Args:
            m (dict): MQTT event from Shelly motion sensor
        """

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
            "shelly_topic": self.shelly_device_topic,
            "motion_topic": self.motion_topic,
        }
        return data

    @override
    def from_dict(self, data: Dict[str, Any]) -> None:
        super().from_dict(data)
        if "_shellymotion" in data:
            for key, value in data["_shellymotion"].items():
                setattr(self, key, value)
