"""
Description
===========

OpenWeatherMap weather forecast.

"""

from .openweathermap import OpenWeatherMap
from .openweathermap import OpenWeatherMapThread
from .openweathermap_plugin import OpenWeatherMapPlugin

__all__ = [
    "OpenWeatherMap",
    "OpenWeatherMapThread",
    "OpenWeatherMapPlugin"
]
