import json
from typing import Any, Dict
from typing_extensions import override

from masterpiece.mqtt import MqttMsg

from juham_core.timeutils import epoc2utc
from .shelly import Shelly


class ShellyPro3EM(Shelly):
    """The Shelly Pro3EM energy meter.

    Publishes the active power (also called real power) to MQTT, as it
    represents the part of the power that can be converted to useful
    work. Full set of measurements e.g. reactive power, current, and
    voltage, available  from the sensor, are written to a time series
    database for inspection purposes.
    """

    shelly_topic = "shellypro3em-powermeter/events/rpc"  # input topic

    def __init__(self, name: str = "shellypro3em", mqtt_prefix :str ="") -> None:
        super().__init__(name, mqtt_prefix)
        self.power_topic = self.make_topic_name("powerconsumption")  # target topic
        self.shelly_device_topic = f"{mqtt_prefix}{self.shelly_topic}"
        
    @override
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.shelly_device_topic)

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        if self.shelly_device_topic == msg.topic:
            if not msg.payload:
                self.error(f"Empty payload on topic {msg.topic}")
                return            
            try:
                payload_text = msg.payload.decode(errors="replace")
                m = json.loads(payload_text)
                self.on_powermeter_message(m)
            except Exception as e:
                self.error(f"JSON parse error on topic {msg.topic}", f"{e} payload={msg.payload!r}")
                return
        else:
            super().on_message(client, userdata, msg)
            
    def on_powermeter_message(self, m: Dict[str, Any]) -> None:
        """Handle incoming Shelly Pro3EM powermeter message.
        Args:
            m (dict): message from the Shelly Pro3EM device
        """
        if "method" in m:
            mth = m["method"]
            if mth == "NotifyStatus":
                params = m["params"]
                ts = params["ts"]
                if "em:0" in params:
                    self.on_em_0(ts, params["em:0"])
                elif "emdata:0" in params:
                    self.on_emdata_0(ts, params["emdata:0"])
                else:
                    pass
            elif mth == "NotifyEvent":
                self.debug(f"Unhandled method {mth}", f"{m}")
            else:
                self.error(f"Unknown method {mth}", f"{m}")
        else:
            self.error("No method field in message", f"{m}")

    def on_em_0(self, ts: float, em: dict[str, Any]) -> None:
        """Handle the incoming Shelly message containing all power meter
        readings. Publish the real power component, which is of interest to
        Juham, and record all measurements to the time series database.

        Args:
            ts (float): time stamp of the event
            em (dict): message from the Shelly device
        """
        self.publish_active_power(ts, em)
        self.record_power(ts, em)

    def publish_active_power(self, ts: float, em: dict[str, Any]) -> None:
        """Publish the active power, also known as real power. This is that
        part of the  power that can be converted to useful work.

        Args:
            ts (str): time stamp of the event
            em (dict): message from the Shelly device
        """
        msg: dict[str, Any] = {
            "timestamp": ts,
            "real_a": em["a_act_power"],
            "real_b": em["b_act_power"],
            "real_c": em["c_act_power"],
            "real_total": em["total_act_power"],
        }
        self.publish(self.power_topic, json.dumps(msg), 1, True)

    def record_power(self, ts: float, em: dict[str, Any]) -> None:
        """Given current time in UTC and energy meter message update the time
        series database accordingly.

        Args:
            ts (float): utc time
            em (dict): energy meter message
        """
        point = (
            self.measurement("powermeter")
            .tag("sensor", "em0")
            .field("real_A", em["a_act_power"])
            .field("real_B", em["b_act_power"])
            .field("real_C", em["c_act_power"])
            .field("total_real_power", em["total_act_power"])
            .field("total_apparent_power", em["total_aprt_power"])
            .field("apparent_a", em["a_aprt_power"])
            .field("apparent_b", em["b_aprt_power"])
            .field("apparent_c", em["c_aprt_power"])
            .field("current_a", em["a_current"])
            .field("current_b", em["b_current"])
            .field("current_c", em["c_current"])
            .field("current_n", em["n_current"])
            .field("current_total", em["total_current"])
            .field("voltage_a", em["a_voltage"])
            .field("voltage_b", em["b_voltage"])
            .field("voltage_c", em["c_voltage"])
            .field("freq_a", em["a_freq"])
            .field("freq_b", em["b_freq"])
            .field("freq_c", em["c_freq"])
            .time(epoc2utc(ts))
        )
        try:
            self.write(point)
        except Exception as e:
            self.error(f"Writing to influx failed {str(e)}")

    def on_emdata_0(self, ts: float, em: dict[str, Any]) -> None:
        """Handle energy meter sensor message.

        Args:
            ts (str): utc time
            em (dict): energy meter sensor specific message
        """
        point = (
            self.measurement("powermeter")
            .tag("sensor", "emdata0")
            .field("total_act_energy_A", em["a_total_act_energy"])
            .field("total_act_energy_B", em["b_total_act_energy"])
            .field("total_act_energy_C", em["c_total_act_energy"])
            .field("total_act_ret_energy_A", em["a_total_act_ret_energy"])
            .field("total_act_ret_energy_B", em["b_total_act_ret_energy"])
            .field("total_act_ret_energy_C", em["c_total_act_ret_energy"])
            .field("total_act", em["total_act"])
            .field("total_act_ret", em["total_act_ret"])
            .time(epoc2utc(ts))
        )
        try:
            self.write(point)
            # self.debug(
            #    f"Total energy consumed {em['total_act']}, exported {em['total_act_ret']}"
            # )
        except Exception as e:
            self.error(f"Writing to influx failed {str(e)}")

    @override
    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = super().to_dict()
        data["_shellypro3em"] = {
            "shelly_topic": self.shelly_device_topic,
            "power_topic": self.power_topic,
        }
        return data

    @override
    def from_dict(self, data: Dict[str, Any]) -> None:
        super().from_dict(data)
        if "_shellypro3em" in data:
            for key, value in data["_shellypro3em"].items():
                setattr(self, key, value)
