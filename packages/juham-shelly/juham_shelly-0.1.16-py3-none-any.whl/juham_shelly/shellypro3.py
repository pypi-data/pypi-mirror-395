import json
from typing import Any, Dict, cast
from typing_extensions import override
from masterpiece.mqtt import MqttMsg
from .shelly import Shelly


class ShellyPro3(Shelly):
    """The Shelly Pro wifi/ethernet relay with three independently controllable
    relays. Subscribes to the Juham power input topic and controls the Shelly relays accordingly.
    """

    power_topic = "power"  # Juham topic to listen

    def __init__(
        self, name: str, unit: str, relay: str, l1: bool, l2: bool, l3: bool
    ) -> None:
        """Initialize Shelly Pro 3 switch. Listens the Juham power topic and specific unit in it,
        and controls the given l1,l2,l3 contactors accordingly.

        Args:
            name (str): name of the automation object
            unit (str): unit name controlling this relay
            relay (str): Mqtt prefix of the shelly device to be controlled
            l1, l2, l3 (bool): Phase conductors to be turned on/off
        """
        super().__init__(name, relay)
        self.relay_topic_out = f"{self.mqtt_prefix}/command/switch:"
        self.current_relay_state: int = 0
        self.power_topic_in = self.make_topic_name(self.power_topic)
        self.unit = unit
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3

    @override
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.power_topic_in)

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        if self.power_topic_in in msg.topic:
            self.on_power(json.loads(msg.payload.decode()))
        else:
            super().on_message(client, userdata, msg)

    def on_power(self, m: dict[str, str]) -> None:
        """Process power_topic message.

        Args:
            m (dict): holding data from the power sensor
        """
        if "Unit" in m and m["Unit"] == self.unit:
            new_state = cast(int, m["State"])

            if new_state != self.current_relay_state:
                self.current_relay_state = new_state
                if new_state == 0:
                    relay = "off"
                else:
                    relay = "on"
                if self.l1 == True:
                    self.publish(f"{self.relay_topic_out}0", relay, 1, False)
                if self.l2 == True:
                    self.publish(f"{self.relay_topic_out}1", relay, 1, False)
                if self.l3 == True:
                    self.publish(f"{self.relay_topic_out}2", relay, 1, False)
                self.info(f"{self.name} {m['Unit']}  state changed to {relay}")

    @override
    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = super().to_dict()
        data["_shellypro3"] = {
            "power_topic_in": self.power_topic_in,
        }
        return data

    @override
    def from_dict(self, data: Dict[str, Any]) -> None:
        super().from_dict(data)
        if "_shellypro3" in data:
            for key, value in data["_shellypro3"].items():
                setattr(self, key, value)
