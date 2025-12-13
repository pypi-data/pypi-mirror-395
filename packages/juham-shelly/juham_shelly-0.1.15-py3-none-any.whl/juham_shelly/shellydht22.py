import json
from typing import Any, Dict
from typing_extensions import override

from masterpiece.mqtt import MqttMsg
from juham_core.timeutils import epoc2utc
from .shelly import Shelly


class ShellyDHT22(Shelly):
    """Shelly Plus add-on with DHT22 humidity, temperature sensor.

    Listens MQTT messages from dht22 (am2302) humidity sensor attached to
    Shelly add-on module, publishes them to Juham MQTT, and writes them to time series database.

    Note: DHT22 humidity sensor has some serious issues with reliability. The
    readings are often way off, in fact, twice as high as they should be. And it seems
    after each  incorrect reading the sensor sends a new reading that is correct.
    This code tries to mitigate the issue by comparing the new reading to the previous
    one and if the difference is too big, the new reading is discarded.
    """

    _DHT22: str = "_dht22"
    shelly_topic = "/events/rpc"  # source topic

    def __init__(self, name: str, mqtt_prefix: str) -> None:
        super().__init__(name, mqtt_prefix)
        self.temperature_topic = self.make_topic_name("temperature/")  # target topic
        self.humidity_topic = self.make_topic_name("humidity/")  # target topic
        self.previous_humidity: float = 101.0  # initial value undefined
        self.previous_humidity_ts: float = 0.0
        self.shelly_device_topic = f"{self.mqtt_prefix}{self.shelly_topic}"
        
    @override
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.shelly_device_topic)

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        if self.shelly_device_topic in msg.topic:
            m = json.loads(msg.payload.decode())
            mth = m["method"]
            if mth == "NotifyStatus":
                params = m["params"]
                self.on_sensor(params)
            elif mth == "NotifyFullStatus":
                params = m["params"]
                self.on_sensor(params)
            else:
                self.warning(f"Unknown method {self.name} {self.shelly_device_topic} {mth}", str(m))
        else:
            super().on_message(client, userdata, msg)

    def on_sensor(self, params: dict[str, Any]) -> None:
        """Map Shelly Plus 1GM specific event to Juham format and post it to
        temperature topic.

        Args:
            params (dict): message from Shelly Plus 1 wifi relay
        """

        ts = params["ts"]
        for key, value in params.items():
            if key.startswith("humidity:"):
                humidity: float = value["rh"]
                if not self.valid_humidity(humidity, self.previous_humidity):
                    self.warning(
                        f"Discarding humidity reading {self.name} {self.mqtt_prefix}: {humidity}",
                        value,
                    )
                    continue
                self.previous_humidity = humidity
                self.on_value(ts, key, value, "humidity", "rh")
            elif key.startswith("temperature:"):
                self.on_value(ts, key, value, "temperature", "tC")
            elif key.startswith("ts"):
                pass
            elif key.startswith("sys"):
                pass
            else:
                self.warning(
                    f"Unknown msg {self.name} {self.shelly_device_topic}: {key}", value
                )
                pass

    def valid_humidity(self, value: float, prev_value: float) -> bool:
        """If the reading is approximately twice as big as the
        last known good reading, then assume the reading is incorrect.

        Args:
            value (float): sensor value
            prev_value (float): previous valid sensor value

        Returns:
            bool: true if the value is twice as big as the previous value
        """
        return value < 1.9 * prev_value

    def on_value(
        self, ts: float, key: str, value: dict[str, Any], attr: str, unit: str
    ) -> None:
        """Process humidity or temperature sensor reading to MQTT, by publishing it to Juham MQTT and
        writing it to InfluxDB.

        Args:
            ts (float): timestamp
            key (str): key
            value (dict[str, Any]): sensor value
            attr (str): attribute either 'temperature' or 'humidity'
            unit (str): unit either 'rh' or 'tC'
        """

        sensor_id = key.split(":")[1]
        humidity = value[unit]
        if humidity is None or not isinstance(humidity, (int, float)):
            self.warning(
                f"Invalid reading {self.name} {self.mqtt_prefix}: {humidity} {unit}",
                str(value),
            )
            return

        msg: dict[str, Any] = {
            "sensor": sensor_id,
            "timestamp": ts,
            attr: float(humidity),
        }
        self.publish(self.humidity_topic + sensor_id, json.dumps(msg), 1, True)
        try:
            point = (
                self.measurement(self.name)
                .tag("sensor", sensor_id)
                .field(attr, humidity)
                .time(epoc2utc(ts))
            )
            self.write(point)
        except Exception as e:
            self.error(f"Writing to influx failed {str(e)}")

    @override
    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = super().to_dict()
        data[self._DHT22] = {
            "shelly_topic": self.shelly_topic,
            "temperature_topic": self.temperature_topic,
        }
        return data

    @override
    def from_dict(self, data: Dict[str, Any]) -> None:
        super().from_dict(data)
        if self._DHT22 in data:
            for key, value in data[self._DHT22].items():
                setattr(self, key, value)
