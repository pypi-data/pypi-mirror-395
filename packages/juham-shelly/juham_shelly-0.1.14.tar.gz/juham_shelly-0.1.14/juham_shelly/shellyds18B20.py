import json
from typing import Any, Dict
from typing_extensions import override
from masterpiece.timeseries import Measurement

from masterpiece.mqtt import MqttMsg
from juham_core.timeutils import epoc2utc, timestamp
from .shelly import Shelly


class ShellyDS18B20(Shelly):
    """Shelly Plus 1 smart relay with DS18B20 temperature sensors .

    Listens MQTT messages from DS18B20 temperature sensors attached to
    Shelly 1 PM Add on module, posts them to Juham temperature topic, and writes
    them to time series database.
    """

    _DS18B20: str = "DS18B20"
    shelly_topic = "/events/rpc"  # source topic

    def __init__(self, name: str, mqtt_prefix: str) -> None:
        """Create Shelly Plus AddOn with DS18B20 temperature sensors attached.

        Args:
            name (str): name of the object
            mqtt_prefix (str): Mqtt prefix identifying this shelly device
        """
        super().__init__(name, mqtt_prefix)
        self.relay_started: float = 0
        self.temperature_topic = self.make_topic_name("temperature/")  # target topic
        self.shelly_device_topic = f"{self.mqtt_prefix}{self.shelly_topic}"

    @override
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.shelly_device_topic)

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        if self.shelly_device_topic in msg.topic:
            tsnow = timestamp()
            self.relay_started = tsnow

            m = json.loads(msg.payload.decode())
            mth = m["method"]
            if mth == "NotifyStatus":
                params = m["params"]
                self.on_sensor(params)
            elif m["method"] == "NotifyFullStatus":
                params = m["params"]
                self.on_sensor(params)
            else:
                self.warning(f"Unknown method {self.name} {self.shelly_device_topic} {mth}", str(m))
        else:
            super().on_message(client, userdata, msg)

    def on_sensor(self, params: dict[str, Any]) -> None:
        """Map Shelly Plus 1 specific event to juham format and post it to
        temperature topic.

        Args:
            params (dict): message from Shelly Plus 1 wifi relay
        """
        ts = params["ts"]


        for key, value in params.items():
            if key.startswith("temperature:"):
                sensor_id = self.mqtt_prefix + "/" + key.split(":")[1]
                temperature_reading = value
                temperature_celsius = temperature_reading.get("tC")

                if temperature_celsius is None:
                    self.warning("Null temperature value", str(params))
                    continue  

                try:
                    temperature_int = int(temperature_celsius)
                except (TypeError, ValueError) as e:
                    self.warning(f"Invalid temperature value for sensor {sensor_id} : {str(temperature_celsius)}")
                    continue

                msg : dict[str, Any]= {
                    "sensor": sensor_id,
                    "timestamp": ts,
                    "temperature": temperature_int,
                }
                self.publish(
                    self.temperature_topic + sensor_id,
                    json.dumps(msg),
                    1,
                    True
                )

                try:
                    point: Measurement = (
                        self.measurement("boiler")
                        .tag("sensor", self.mqtt_prefix)
                        .field(sensor_id, temperature_celsius)
                        .time(epoc2utc(ts))
                    )
                    self.write(point)

                except Exception as e:
                    self.error(f"Writing to influx failed {str(e)}")



    @override
    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = super().to_dict()
        data[self._DS18B20] = {
            "shelly_topic": self.shelly_device_topic,
            "temperature_topic": self.temperature_topic,
        }
        return data

    @override
    def from_dict(self, data: Dict[str, Any]) -> None:
        super().from_dict(data)
        if self._DS18B20 in data:
            for key, value in data[self._DS18B20].items():
                setattr(self, key, value)
