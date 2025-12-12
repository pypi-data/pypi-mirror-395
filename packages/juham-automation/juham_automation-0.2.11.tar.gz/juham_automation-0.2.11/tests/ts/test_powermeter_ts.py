from typing import Any
import unittest
from unittest.mock import MagicMock, patch
import json
from juham_automation.ts.powermeter_ts import PowerMeterTs  # adjust import path
from masterpiece.mqtt import MqttMsg

class TestPowerMeterTs(unittest.TestCase):
    def setUp(self):
        self.pm = PowerMeterTs(name="test_powermeter")

        # Mock measurement chain
        mock_point = MagicMock()
        mock_point.tag.return_value = mock_point
        mock_point.field.return_value = mock_point
        mock_point.time.return_value = mock_point
        self.pm.measurement = MagicMock(return_value=mock_point)
        self.pm.write = MagicMock()
        self.pm.error = MagicMock()

        # Patch epoc2utc
        patcher = patch("juham_automation.ts.powermeter_ts.epoc2utc", return_value="utc-ts")
        self.addCleanup(patcher.stop)
        patcher.start()

    def test_on_message_valid_topic(self):
        payload_dict : dict[str, Any]= {
            "real_a": 10.0,
            "real_b": 20.0,
            "real_c": 30.0,
            "real_total": 60.0,
            "timestamp": 123456
        }
        payload = json.dumps(payload_dict).encode()
        msg = MagicMock()
        msg.topic = self.pm.power_topic
        msg.payload = payload

        self.pm.record_power = MagicMock()
        self.pm.on_message(None, None, msg)
        self.pm.record_power.assert_called_once_with(payload_dict)

    def test_on_message_other_topic(self):
        msg = MagicMock()
        msg.topic = "other/topic"
        msg.payload = b"{}"

        with patch.object(self.pm.__class__.__bases__[0], "on_message") as mock_super:
            self.pm.on_message(None, None, msg)
            mock_super.assert_called_once_with(None, None, msg)

    def test_record_power_writes_correctly(self):
        em = {
            "real_a": 1.1,
            "real_b": 2.2,
            "real_c": 3.3,
            "real_total": 6.6,
            "timestamp": 654321
        }
        self.pm.record_power(em)
        self.pm.write.assert_called_once()
        field_calls = self.pm.measurement().field.call_args_list
        # Check all fields
        self.assertEqual(field_calls[0].args, ("real_A", 1.1))
        self.assertEqual(field_calls[1].args, ("real_B", 2.2))
        self.assertEqual(field_calls[2].args, ("real_C", 3.3))
        self.assertEqual(field_calls[3].args, ("total_real_power", 6.6))

    def test_record_power_exception_handled(self):
        em = {
            "real_a": 1,
            "real_b": 2,
            "real_c": 3,
            "real_total": 6,
            "timestamp": 111
        }
        self.pm.write.side_effect = Exception("DB error")
        self.pm.record_power(em)
        self.pm.error.assert_called_once()
        self.assertIn("DB error", self.pm.error.call_args[0][0])

if __name__ == "__main__":
    unittest.main()
