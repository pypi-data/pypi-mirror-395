import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, cast
from typing_extensions import override

from masterpiece.mqtt import MqttMsg, Mqtt
from juham_core import JuhamCloudThread, JuhamThread


class OpenWeatherMapThread(JuhamCloudThread):
    """Asynchronous thread for acquiring forecast from the open weathermap.org web service
    site.
    Note: the service does not include solar power cast."""

    _forecast_topic = ""
    _interval: float = 60
    _appid = "f3954a78a9eaa74096305a29054d8c88"  # obtain from openweathermap.org
    _location = "Lahti,fi"
    _url = ""

    def __init__(self, client: Optional[Mqtt] = None) -> None:
        """Construct with the given mqtt client. Acquires data from the visual
        crossing web service and publishes the forecast data to
        ```forecast_topic```.

        Args:
            client (object, optional): MQTT client. Defaults to None.
        """
        super().__init__(client)
        self.mqtt_client: Optional[Mqtt] = client

    def init(
        self,
        forecast_topic: str,
        location: str,
        appid: str,
        url: str,
        update_interval: float,
    ):
        """Initialize thread

        Args:
            forecast_topic (str): topic to post the forecast
            location (str): geographic location
            appid (str): appid for the openweathermap service
            url (str): url to openweathermap service
            update_interval (float): update interval
        """
        self._forecast_topic = forecast_topic
        self._location = location
        self._appid = appid
        self._url = url
        self._interval = update_interval

    @override
    def update_interval(self) -> float:
        return self._interval

    @override
    def make_weburl(self) -> str:
        return f"{self._url}?q={self._location}&APPID={self._appid}"

    @override
    def process_data(self, data: Any) -> None:
        super().process_data(data)
        r = data.json()

        forecast: List = []

        for r in r["list"]:
            dt: float = r["dt"]
            # dt_txt: str = r["dt_txt"]
            temp: float = r["main"]["temp"]
            feels: float = r["main"]["feels_like"]
            pressure: float = r["main"]["pressure"]
            humidity: float = r["main"]["humidity"]
            windspeed: float = r["wind"]["speed"]

            rec = {
                "id": "openweathermap",
                "ts": dt,
                "hour": datetime.fromtimestamp(dt, tz=timezone.utc).strftime("%H"),
                "day": datetime.fromtimestamp(dt, tz=timezone.utc).strftime("%Y%m%d%H"),
                "temp": temp - 273,  # from Kelvin to Celcius
                "feels": feels - 273,
                "pressure": pressure,
                "humidity": humidity,
                "windspeed": windspeed,
            }
            forecast.append(rec)

        msg = json.dumps(forecast)
        self.publish(self._forecast_topic, msg, qos=1, retain=True)
        self.info(
            f"OpenWeatherMap forecast for the next {len(forecast)} days published"
        )


class OpenWeatherMap(JuhamThread):
    """This class constructs a data acquisition object for reading weather
    forecasts from 'openweathermap.org'. It subscribes to the
    forecast topic and writes hourly data such as solar energy, temperature,
    and other attributes relevant to home automation into a time series
    database.

    Spawns an asynchronous thread to run queries at the specified
    update_interval.
    """

    _OPENWEATHERMAP: str = "OpenWeatherMap"
    workerThreadId: str = OpenWeatherMapThread.get_class_id()
    bucket: str = "OpenWeather"
    appid: str = "f3954a78a9eaa74096305a29054d8c88"
    location: str = "Lahti,fi"
    url: str = "https://api.openweathermap.org/data/2.5/forecast"
    update_interval: float = 12 * 3600

    def __init__(self, name: str = "openweathermap") -> None:
        super().__init__(name)
        self.worker: Optional[OpenWeatherMapThread] = None
        self.forecast_topic: str = self.make_topic_name("forecast")

    @override
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.forecast_topic)

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        if msg.topic == self.forecast_topic:
            em = json.loads(msg.payload.decode())
            self.on_forecast(em)
        else:
            super().on_message(client, userdata, msg)

    def on_forecast(self, em: dict) -> None:
        """Handle weather forecast data.

        Args:
            em (dict): forecast
        """

    @override
    def run(self) -> None:
        # create, initialize and start the asynchronous thread for acquiring forecast
        self.worker = cast(
            OpenWeatherMapThread, self.instantiate(OpenWeatherMap.workerThreadId)
        )
        self.worker.init(
            self.forecast_topic,
            self.location,
            self.appid,
            self.url,
            self.update_interval,
        )
        super().run()

    @override
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data[self._OPENWEATHERMAP] = {
            "topic": self.forecast_topic,
            "location": self.location,
            "appid": self.appid,
            "url": self.url,
            "interval": self.update_interval,
        }
        return data

    @override
    def from_dict(self, data: Dict[str, Any]) -> None:
        super().from_dict(data)
        if self._OPENWEATHERMAP in data:
            for key, value in data[self._OPENWEATHERMAP].items():
                setattr(self, key, value)
