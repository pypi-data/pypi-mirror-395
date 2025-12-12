from typing import Any, Dict
import unittest
from unittest.mock import patch, MagicMock
import json
from masterpiece.mqtt import MqttMsg
from juham_openweathermap.openweathermap import OpenWeatherMap, OpenWeatherMapThread


class SimpleMqttMsg(MqttMsg):
    def __init__(self, topic: str, payload: Any):
        self._topic = topic
        self._payload = payload

    @property
    def payload(self) -> Any:
        return self._payload

    @payload.setter
    def payload(self, value: Any) -> None:
        self._payload = value

    @property
    def topic(self) -> str:
        return self._topic

    @topic.setter
    def topic(self, value: str) -> None:
        self._topic = value


class TestOpenWeatherMapThread(unittest.TestCase):

    @patch("juham_core.juham_cloud.requests.get")  # Mock HTTP requests
    def test_make_weburl(self, mock_get: MagicMock) -> None:
        thread = OpenWeatherMapThread()
        thread.init("test/topic", "Lahti,fi", "test_appid", "http://test_url", 60)

        expected_url = "http://test_url?q=Lahti,fi&APPID=test_appid"
        self.assertEqual(thread.make_weburl(), expected_url)

    @patch.object(OpenWeatherMapThread, "publish")
    def test_process_data(self, mock_publish: MagicMock) -> None:
        thread = OpenWeatherMapThread()
        thread.init("/test", "Lahti,fi", "test_appid", "http://test_url", 60)

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "list": [
                {
                    "dt": 1710000000,
                    "main": {
                        "temp": 300,
                        "feels_like": 298,
                        "pressure": 1013,
                        "humidity": 60,
                    },
                    "wind": {"speed": 5.0},
                }
            ]
        }
        thread.process_data(mock_response)

        mock_publish.assert_called_once()
        published_msg = json.loads(mock_publish.call_args[0][1])
        self.assertEqual(published_msg[0]["temp"], 27)  # 300K - 273 = 27C
        self.assertEqual(published_msg[0]["pressure"], 1013)
        self.assertEqual(published_msg[0]["humidity"], 60)
        self.assertEqual(published_msg[0]["windspeed"], 5.0)


class TestOpenWeatherMap(unittest.TestCase):

    @patch.object(OpenWeatherMap, "subscribe")
    def test_on_connect(self, mock_subscribe: MagicMock) -> None:
        ow = OpenWeatherMap()
        ow.on_connect(None, None, 0, 0)
        mock_subscribe.assert_called_with(ow.forecast_topic)

    @patch.object(OpenWeatherMap, "on_forecast")
    def test_on_message(self, mock_on_forecast: MagicMock) -> None:
        ow = OpenWeatherMap()
        test_payload = json.dumps({"temp": 25})
        msg = SimpleMqttMsg(topic=ow.forecast_topic, payload=test_payload.encode())
        ow.on_message(None, None, msg)
        mock_on_forecast.assert_called_once_with(json.loads(test_payload))

    def test_to_dict(self) -> None:
        ow = OpenWeatherMap()
        data = ow.to_dict()
        self.assertIn("OpenWeatherMap", data)
        self.assertEqual(data["OpenWeatherMap"]["location"], "Lahti,fi")

    def test_from_dict(self) -> None:
        ow = OpenWeatherMap()
        new_data: Dict[str, Any] = {
            "_class": "OpenWeatherMap",
            "_version": 0,
            "_object": {"name": "owm", "payload": None},
            "_base": {},
            "OpenWeatherMap": {
                "location": "NewLocation",
                "appid": "new_appid",
                "interval": 7200,
            },
        }
        ow.from_dict(new_data)
        self.assertEqual(ow.location, "NewLocation")
        self.assertEqual(ow.appid, "new_appid")
        self.assertEqual(ow.update_interval, 43200)


if __name__ == "__main__":
    unittest.main()
