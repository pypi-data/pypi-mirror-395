from datetime import datetime, timedelta, timezone
import json
from typing_extensions import override
from typing import Any, Optional, cast
from masterpiece import MqttMsg, Mqtt
from juham_core import JuhamThread, JuhamCloudThread


class VisualCrossingThread(JuhamCloudThread):
    """Asynchronous thread for acquiring forecast from the VisualCrossing
    site."""

    # class attributes
    _forecast_topic: str = ""
    _base_url: str = ""
    _api_key: str = ""
    _location: str = ""
    _interval: float = 12 * 3600

    def __init__(self, client: Optional[Mqtt] = None):
        """Construct with the given mqtt client. Acquires data from the visual
        crossing web service and publishes the forecast data to
        forecast_topic.

        Args:
            client (object, optional): MQTT client. Defaults to None.
        """
        super().__init__(client)
        self.mqtt_client: Optional[Mqtt] = client

    @override
    def update_interval(self) -> float:
        return self._interval

    @override
    def make_weburl(self) -> str:
        if not self._api_key:
            self.error("Uninitialized api_key {self.get_class_id()}: {self._api_key}")
            return ""
        else:
            now = datetime.now()
            end = now + timedelta(days=1)
            start = now.strftime("%Y-%m-%d")
            stop = end.strftime("%Y-%m-%d")
            url = f"{self._base_url}{self._location}/{start}/{stop}?unitGroup=metric&contentType=json&include=hours&key={self._api_key}"
            # self.debug(url)
            return url

    def init(
        self, topic: str, base_url: str, interval: float, api_key: str, location: str
    ) -> None:
        """Initialize the  data acquisition thread

        Args:
            topic (str): mqtt topic to publish the acquired data
            base_url (str): url of the web service
            interval (float): update interval in seconds
            api_key (str): api_key, as required by the web service
            location (str): geographic location
        """
        self._forecast_topic = topic
        self._base_url = base_url
        self._interval = interval
        self._api_key = api_key
        self._location = location

    @override
    def process_data(self, data: Any) -> None:
        self.info("VisualCrossing process_data()")
        data = data.json()
        forecast: list[dict[str, Any]] = []
        self.info(f"VisualCrossing {data}")
        for day in data["days"]:
            for hour in day["hours"]:
                ts = int(hour["datetimeEpoch"])
                forecast.append(
                    {
                        "id": "visualcrossing",
                        "ts": ts,
                        "hour": datetime.fromtimestamp(ts, tz=timezone.utc).strftime(
                            "%H"
                        ),
                        "day": datetime.fromtimestamp(ts, tz=timezone.utc).strftime(
                            "%Y%m%d%H"
                        ),
                        "uvindex": hour["uvindex"],
                        "solarradiation": hour["solarradiation"],
                        "solarenergy": hour["solarenergy"],
                        "cloudcover": hour["cloudcover"],
                        "snow": hour["snow"],
                        "snowdepth": hour["snowdepth"],
                        "pressure": hour["pressure"],
                        "temp": hour["temp"],
                        "humidity": hour["humidity"],
                        "windspeed": hour["windspeed"],
                        "winddir": hour["winddir"],
                        "dew": hour["dew"],
                    }
                )
        msg = json.dumps(forecast)
        self.publish(self._forecast_topic, msg, qos=1, retain=True)
        self.info(f"VisualCrossing forecast published to {self._forecast_topic}")


class VisualCrossing(JuhamThread):
    """Constructs a data acquisition object for reading weather
    forecasts from the VisualCrossing web service. Subscribes to the
    forecast topic and writes hourly data such as solar energy, temperature,
    and other attributes relevant to home automation into a time series
    database.

    Spawns an asynchronous thread to run queries at the specified
    update_interval.
    """

    _VISUALCROSSING: str = "visualcrossing"

    workerThreadId: str = VisualCrossingThread.get_class_id()
    base_url: str = (
        "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
    )
    update_interval: float = 12 * 3600
    api_key: str = "SE9W7EHP775N7NDNW8ANM2MZN"
    location: str = "lahti,finland"

    def __init__(self, name: str = "visualcrossing") -> None:
        """Constructs VisualCrossing automation object for acquiring and publishing
        forecast data.

        Args:
            name (str, optional): name of the object. Defaults to "visualcrossing".
        """
        super().__init__(name)
        self.worker: Optional[VisualCrossingThread] = None
        self.forecast_topic: str = self.make_topic_name("forecast")
        self.debug(f"VisualCrossing with name {name} created")

    @override
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.forecast_topic)
            self.debug(f"VisualCrossing subscribed to topic {self.forecast_topic}")

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        if msg.topic == self.forecast_topic:
            em = json.loads(msg.payload.decode())
            self.on_forecast(em)
        else:
            super().on_message(client, userdata, msg)

    def on_forecast(self, em: dict[str, Any]) -> None:
        """Handle weather forecast data.

        Args:
            em (dict[str, Any]): forecast
        """
        # self.debug(f"VisualCrossing: got mqtt message {em}")

    @override
    def run(self) -> None:
        # create, initialize and start the asynchronous thread for acquiring forecast

        self.worker = cast(
            VisualCrossingThread, self.instantiate(VisualCrossing.workerThreadId)
        )
        self.worker.init(
            self.forecast_topic,
            self.base_url,
            self.update_interval,
            self.api_key,
            self.location,
        )
        self.debug(
            f"VisualCrossing run: {self.base_url}, {self.update_interval}s, location is {self.location}"
        )
        super().run()

    @override
    def to_dict(self) -> dict[str, Any]:
        data: dict[str, dict[str, Any]] = super().to_dict()
        data[self._VISUALCROSSING] = {
            "forecast_topic": self.forecast_topic,
            "base_url": self.base_url,
            "api_key": self.api_key,
            "update_interval": self.update_interval,
            "location": self.location,
        }
        return data

    @override
    def from_dict(self, data: dict[str, Any]) -> None:
        super().from_dict(data)
        if self._VISUALCROSSING in data:
            for key, value in data[self._VISUALCROSSING].items():
                setattr(self, key, value)
