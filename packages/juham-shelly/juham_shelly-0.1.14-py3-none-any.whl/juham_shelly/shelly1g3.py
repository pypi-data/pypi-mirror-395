import json
from typing import Any, cast
from typing_extensions import override
from masterpiece.mqtt import MqttMsg
from .shelly import Shelly


class Shelly1G3(Shelly):
    """Automation class for controlling Shelly Wifi relay. Subscribes to
    the given 'power' topic and controls the Shelly relay accordingly.
    if the 'power' topic "State" is 0, the relay is turned off, if 1 then on.
    Note that the type of 'power["State"]' field is integer, not boolean.
    """

    power_topic = "power"  # Juham topic to listen
    shelly_relay_command = "/command/switch:0"  # Shelly specific relay to control

    def __init__(self, name: str, unit: str, relay: str) -> None:
        """Create automation for controlling the given

        Args:
            name (str): name of this node
            unit (str): unit to listen for power input
            relay (str) : Mqtt prefix of the shelly relay to be controlled
        """
        super().__init__(name, relay)
        self.relay_topic_out = f"{self.mqtt_prefix}{self.shelly_relay_command}"
        self.current_relay_state: int = -1
        self.power_topic_in = self.make_topic_name(self.power_topic)
        self.unit = unit

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
                self.publish(self.relay_topic_out, relay, 1, False)
                self.info(f"{self.name} {m['Unit']}  state changed to {relay}")
