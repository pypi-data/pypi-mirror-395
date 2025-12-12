import unittest
import json
from unittest import mock
from typing import Any, Dict, List
from unittest.mock import MagicMock
import unittest
from unittest.mock import MagicMock, patch
import json
from juham_automation.ts.forecast_ts import ForecastTs  # adjust import path
from masterpiece.mqtt import MqttMsg

class TestForecastTs(unittest.TestCase):
    def setUp(self):
        self.ft = ForecastTs(name="test_forecast")
        
        # Mock the measurement chain
        mock_point = MagicMock()
        mock_point.tag.return_value = mock_point
        mock_point.field.return_value = mock_point
        mock_point.time.return_value = mock_point
        self.ft.measurement = MagicMock(return_value=mock_point)
        self.ft.write = MagicMock()
        self.ft.error = MagicMock()
        self.ft.info = MagicMock()
        self.ft.debug = MagicMock()
        
        # Patch epoc2utc
        patcher = patch("juham_automation.ts.forecast_ts.epoc2utc", return_value="utc-ts")
        self.addCleanup(patcher.stop)
        patcher.start()

    def test_on_forecast_valid_records(self):
        records = [
            {"hour": 1, "ts": 123456, "temp": 20, "day": 1},
            {"hour": 2, "ts": 123457, "temp": 21, "day": 1, "id": "sensor1"},
        ]
        self.ft.on_forecast(records)
        self.assertEqual(self.ft.write.call_count, 2)
        self.ft.info.assert_called_once()
        
    def test_on_forecast_missing_hour(self):
        records = [
            {"ts": 123456, "temp": 20, "day": 1},
        ]
        self.ft.on_forecast(records)
        self.ft.write.assert_not_called()
        self.ft.error.assert_called_once()
        
    def test_on_forecast_numeric_conversion(self):
        records = [
            {"hour": 1, "ts": 123456, "temp": "20", "solarradiation": "5", "day": 1}
        ]
        self.ft.on_forecast(records)

        # Retrieve calls to field()
        field_calls = self.ft.measurement().field.call_args_list

        # Filter numeric fields
        numeric_fields = ("temp", "solarradiation")
        for call in field_calls:
            # The first positional argument is the field name
            field_name = call.args[0]
            if field_name in numeric_fields:
                # The second positional argument is the value
                value = call.args[1]
                self.assertIsInstance(value, float)

    def test_on_message_forecast_topic(self):
        payload = json.dumps([{"hour": 1, "ts": 123456}]).encode()
        msg = MagicMock()
        msg.topic = self.ft.forecast_topic
        msg.payload = payload

        self.ft.on_forecast = MagicMock()
        self.ft.on_message(None, None, msg)
        self.ft.on_forecast.assert_called_once()
        arg = self.ft.on_forecast.call_args[0][0]
        self.assertEqual(arg[0]["hour"], 1)

    def test_on_message_other_topic(self):
        msg = MagicMock()
        msg.topic = "other/topic"
        msg.payload = b"{}"
        with patch.object(self.ft.__class__.__bases__[0], "on_message") as mock_super:
            self.ft.on_message(None, None, msg)
            mock_super.assert_called_once_with(None, None, msg)


if __name__ == "__main__":
    unittest.main()
