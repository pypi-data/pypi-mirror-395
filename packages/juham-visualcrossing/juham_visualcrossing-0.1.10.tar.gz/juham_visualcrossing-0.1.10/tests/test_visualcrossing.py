import unittest

from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
import json
from typing_extensions import Any
from juham_visualcrossing.visualcrossing import VisualCrossing, VisualCrossingThread


class MockResponse:

    def __init__(self, data: Any) -> None:
        self._data = data

    def json(self) -> Any:
        return self._data


# Assuming your classes are imported as follows:
# from your_module import VisualCrossingThread, VisualCrossing, Mqtt


class TestVisualCrossingThread(unittest.TestCase):

    @patch("juham_visualcrossing.visualcrossing.Mqtt")
    def test_visualcrossing_thread_init(self, MockMqtt: MagicMock) -> None:
        # Mock the MQTT client
        mock_client = MockMqtt.return_value
        thread: VisualCrossingThread = VisualCrossingThread(mock_client)

        # Assert that the MQTT client is assigned
        self.assertEqual(thread.mqtt_client, mock_client)

    @patch("juham_visualcrossing.visualcrossing.datetime")
    def test_make_weburl(self, MockDatetime: MagicMock) -> None:
        # Mock datetime to return a specific date
        mock_now = datetime(2023, 10, 20)
        mock_end = mock_now + timedelta(days=1)

        # Mock the return value of now() and strftime() on the mocked datetime
        MockDatetime.now.return_value = mock_now
        MockDatetime.return_value.strftime.side_effect = lambda fmt: (
            mock_now.strftime(fmt) if fmt != "%Y-%m-%d" else mock_end.strftime(fmt)
        )

        # Initialize and set class-level attributes
        thread = VisualCrossingThread(None)
        thread.init(
            "forecast_topic", "https://api.example.com/", 3600, "API_KEY", "city"
        )

        # Call method
        result = thread.make_weburl()

        # Expected URL based on the mocked datetime
        expected_url = "https://api.example.com/city/2023-10-20/2023-10-21?unitGroup=metric&contentType=json&include=hours&key=API_KEY"

        # Assert the result is as expected
        self.assertEqual(result, expected_url)

    # @patch("juham_visualcrossing.visualcrossing.json.dumps")
    # @patch("juham_visualcrossing.visualcrossing.Mqtt")
    def test_process_data(self) -> None:
        # Setup mock MQTT and data
        mock_client = MagicMock()
        thread = VisualCrossingThread(mock_client)

        # Prepare mock response data
        mock_data: dict[str, list[dict[str, list[dict[str, Any]]]]] = {
            "days": [
                {
                    "hours": [
                        {
                            "datetimeEpoch": 1632952200,
                            "uvindex": 5,
                            "solarradiation": 1.5,
                            "solarenergy": 10.5,
                            "cloudcover": 80,
                            "snow": 0,
                            "snowdepth": 0,
                            "pressure": 1015,
                            "temp": 20,
                            "humidity": 60,
                            "windspeed": 5,
                            "winddir": 180,
                            "dew": 10,
                        }
                    ]
                }
            ]
        }

        with patch.object(thread, "publish") as mock_publish, patch.object(
            thread, "info"
        ) as mock_info:
            # Act
            thread.process_data(MockResponse(mock_data))

            # Assert
            mock_publish.assert_called_once()


class TestVisualCrossing(unittest.TestCase):

    def test_visualcrossing_init(self) -> None:
        # Instantiate VisualCrossing and check its properties
        vc = VisualCrossing(name="test_visualcrossing")

        self.assertEqual(vc.forecast_topic, vc.make_topic_name("forecast"))

    @patch("juham_visualcrossing.visualcrossing.VisualCrossingThread")
    def test_visualcrossing_on_connect(
        self, MockVisualCrossingThread: MagicMock
    ) -> None:
        # Mock the thread and MQTT client

        vc = VisualCrossing(name="test_visualcrossing")

        # Ensure forecast_topic is set
        vc.forecast_topic = "/forecast"  # Make sure forecast_topic has a value

        # Mock subscribe method before calling on_connect
        with patch.object(vc, "subscribe", MagicMock()):

            # Mock the MQTT connection callback
            mock_client = MagicMock()
            userdata = None
            flags = 0
            rc = 0  # Success

            # Call the on_connect method
            vc.on_connect(mock_client, userdata, flags, rc)

            # Assert that it subscribed to the topic
            vc.subscribe.assert_called_once_with(vc.forecast_topic)

    @patch("juham_visualcrossing.visualcrossing.VisualCrossingThread")
    def test_visualcrossing_run(self, MockVisualCrossingThread: MagicMock) -> None:
        # Mock the thread's methods
        mock_thread = MockVisualCrossingThread.return_value
        vc = VisualCrossing(name="test_visualcrossing")

        # Patch instantiate to return our mock
        vc.instantiate = MagicMock(return_value=mock_thread)

        # Initialize with required attributes
        vc.forecast_topic = "forecast_topic"
        vc.base_url = "https://example.com"
        vc.update_interval = 3600
        vc.api_key = "API_KEY"
        vc.location = "city"

        # Call the method
        vc.run()

        # Check if the thread was initialized correctly
        mock_thread.init.assert_called_once_with(
            "forecast_topic", "https://example.com", 3600, "API_KEY", "city"
        )

    def test_visualcrossing_to_dict(self) -> None:
        vc = VisualCrossing(name="test_visualcrossing")
        vc.forecast_topic = "forecast_topic"
        vc.base_url = "https://example.com"
        vc.api_key = "API_KEY"
        vc.update_interval = 3600
        vc.location = "city"

        expected_dict: dict[str, Any] = {
            "_class": "VisualCrossing",
            "_version": 0,
            "_object": {"name": "test_visualcrossing", "payload": None},
            "_base": {},
            "visualcrossing": {
                "forecast_topic": "forecast_topic",
                "base_url": "https://example.com",
                "api_key": "API_KEY",
                "update_interval": 3600,
                "location": "city",
            },
        }

        # Check if the to_dict method works
        result = vc.to_dict()
        self.assertEqual(result["visualcrossing"], expected_dict["visualcrossing"])

    @patch("juham_visualcrossing.visualcrossing.VisualCrossingThread")
    def test_visualcrossing_from_dict(
        self, MockVisualCrossingThread: MagicMock
    ) -> None:
        data: dict[str, Any] = {
            "_class": "VisualCrossing",
            "_version": 0,
            "_object": {"name": "visualcrossing", "payload": None},
            "_base": {},
            "visualcrossing": {
                "forecast_topic": "forecast_topic",
                "base_url": "https://example.com",
                "api_key": "API_KEY",
                "update_interval": 3600,
                "location": "dusseldorf",
            },
        }

        vc = VisualCrossing(name="test_visualcrossing")
        vc.from_dict(data)

        # Assert that the from_dict method correctly assigns values
        self.assertEqual(vc.forecast_topic, "forecast_topic")
        self.assertEqual(vc.base_url, "https://example.com")
        self.assertEqual(vc.api_key, "API_KEY")
        self.assertEqual(vc.update_interval, 3600)
        self.assertEqual(vc.location, "dusseldorf")


if __name__ == "__main__":
    unittest.main()
