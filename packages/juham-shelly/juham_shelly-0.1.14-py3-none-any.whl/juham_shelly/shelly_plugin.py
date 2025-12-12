from typing_extensions import override
from masterpiece import Plugin, Composite


class ShellyPlugin(Plugin):
    """Plugin class for installing and instantiating Shelly's into the host application."""

    def __init__(self, name: str = "shelly_plugin") -> None:
        """Create shelly_plugin."""
        super().__init__(name)

    @override
    def install(self, app: Composite) -> None:
        # nothing to install 
        pass
