from typing import Any
import unittest
from unittest.mock import MagicMock, patch
import json
from juham_automation.ts.powerplan_ts import PowerPlanTs  # adjust import path
from masterpiece.mqtt import MqttMsg

class TestPowerPlanTs(unittest.TestCase):
    def setUp(self):
        self.pp = PowerPlanTs(name="test_powerplan")

        # Mock measurement chain
        mock_point = MagicMock()
        mock_point.tag.return_value = mock_point
        mock_point.field.return_value = mock_point
        mock_point.time.return_value = mock_point
        self.pp.measurement = MagicMock(return_value=mock_point)
        self.pp.write = MagicMock()

        # Patch epoc2utc
        patcher = patch("juham_automation.ts.powerplan_ts.epoc2utc", return_value="utc-ts")
        self.addCleanup(patcher.stop)
        patcher.start()

    def test_on_message_valid_topic_all_fields(self):
        payload_dict : dict[str, Any] = {
            "Unit": "Unit1",
            "State": 1,
            "Schedule": [1,0,1],
            "UOI": 0.85,
            "Timestamp": 123456,
            "NextDayTemperature": 20,
            "NextDaySolarpower": 50,
            "MinTempLimit": 18,
            "MaxTempLimit": 25
        }
        payload = json.dumps(payload_dict).encode()
        msg = MagicMock()
        msg.topic = self.pp.powerplan_topic
        msg.payload = payload

        self.pp.on_message(None, None, msg)
        self.pp.write.assert_called_once()
        # Check optional fields added
        calls = self.pp.measurement().field.call_args_list
        field_names = [call.args[0] for call in calls]
        self.assertIn("MinTemp", field_names)
        self.assertIn("MaxTemp", field_names)
        self.assertIn("TempForecast", field_names)
        self.assertIn("SolarForecast", field_names)

    def test_on_message_valid_topic_missing_optional(self):
        payload_dict : dict[str, Any]= {
            "Unit": "Unit1",
            "State": 0,
            "Schedule": [0,1,0],
            "UOI": 0.5,
            "Timestamp": 654321
        }
        payload = json.dumps(payload_dict).encode()
        msg = MagicMock()
        msg.topic = self.pp.powerplan_topic
        msg.payload = payload

        self.pp.on_message(None, None, msg)
        self.pp.write.assert_called_once()
        # Optional fields should NOT be present
        calls = self.pp.measurement().field.call_args_list
        field_names = [call.args[0] for call in calls]
        self.assertNotIn("MinTemp", field_names)
        self.assertNotIn("MaxTemp", field_names)
        self.assertNotIn("TempForecast", field_names)
        self.assertNotIn("SolarForecast", field_names)

    def test_on_message_other_topic(self):
        msg = MagicMock()
        msg.topic = "other/topic"
        msg.payload = b"{}"

        with patch.object(self.pp.__class__.__bases__[0], "on_message") as mock_super:
            self.pp.on_message(None, None, msg)
            mock_super.assert_called_once_with(None, None, msg)

if __name__ == "__main__":
    unittest.main()
