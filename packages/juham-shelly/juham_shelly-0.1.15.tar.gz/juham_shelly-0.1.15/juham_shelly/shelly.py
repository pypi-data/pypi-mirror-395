from typing_extensions import override

from typing import Any, Dict
from juham_core import JuhamTs
from juham_core.timeutils import timestamp


class Shelly(JuhamTs):
    """Base class for shelly product family."""

    _SHELLY: str = "_shelly"

    def __init__(self, name: str, mqtt_prefix: str = "") -> None:
        """Initialize Shelly apparatus for use.

        Args:
            name (str): name identifying the shelly device.
            mqtt_prefix (str, optional): Device specific MQTT prefix for the topic
            publish their messages to. Defaults to "".
        """
        super().__init__(name)
        self.relay_started: float = 0
        self.mqtt_prefix: str = mqtt_prefix
        if self.mqtt_prefix == "":
            self.mqtt_prefix = name

    def elapsed(self, secs: float) -> float:
        """Check if a certain time interval has elapsed and update the start
        timestamp attribute to count elapsed seconds for future calls.

        Args:
            secs (float): The expected elapsed time in seconds since the previous call

        Returns:
            bool: True if the given number of seconds has elapsed, False otherwise.
        """

        tsnow = timestamp()
        if tsnow - self.relay_started < secs:
            return False
        self.relay_started = tsnow
        return True

    @override
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data[self._SHELLY] = {"mqtt_prefix": self.mqtt_prefix}
        return data

    @override
    def from_dict(self, data: Dict[str, Any]) -> None:
        super().from_dict(data)
        if self._SHELLY in data:
            for key, value in data[self._SHELLY].items():
                setattr(self, key, value)
