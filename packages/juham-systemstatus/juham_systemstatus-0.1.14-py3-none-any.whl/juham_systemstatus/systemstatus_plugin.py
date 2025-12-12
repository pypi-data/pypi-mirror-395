from ast import Str
from typing_extensions import override
from masterpiece import Plugin, Composite
from .systemstatus import SystemStatus


class SystemStatusPlugin(Plugin):
    """Plugin for installing a SystemStatus object into the host application."""

    def __init__(self, name: str = "system_status") -> None:
        """Create systemstatus object."""
        super().__init__(name)

    @override
    def install(self, app: Composite) -> None:
        # install to the application
        obj = SystemStatus()
        app.add(obj)
