from ast import Str
from typing_extensions import override
from masterpiece import Plugin, Composite
from .openweathermap import OpenWeatherMap


class OpenWeatherMapPlugin(Plugin):
    """Plugin class, for installing a OpenWeatherMap classes into the host application."""

    def __init__(self, name: str = "openweather_map") -> None:
        """Create systemstatus object."""
        super().__init__(name)

    @override
    def install(self, app: Composite) -> None:
        # Create and insert a OpenWeathermap object into the host application.
        obj = OpenWeatherMap()
        app.add(obj)
