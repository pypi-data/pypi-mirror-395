import unittest
from masterpiece import MqttMsg
from juham_automation.ts.power_ts import PowerTs
import unittest
from unittest.mock import MagicMock, patch
import json
from masterpiece.mqtt import MqttMsg

class TestPowerTs(unittest.TestCase):
    def setUp(self):
        self.pt = PowerTs(name="test_power")

        # Mock measurement chain
        mock_point = MagicMock()
        mock_point.tag.return_value = mock_point
        mock_point.field.return_value = mock_point
        mock_point.time.return_value = mock_point
        self.pt.measurement = MagicMock(return_value=mock_point)
        self.pt.write = MagicMock()
        self.pt.debug = MagicMock()

        # Patch epoc2utc
        patcher = patch("juham_automation.ts.power_ts.epoc2utc", return_value="utc-ts")
        self.addCleanup(patcher.stop)
        patcher.start()

    def test_on_message_valid(self):
        payload_dict = {
            "Unit": "Unit1",
            "State": 123.4,
            "Timestamp": 987654
        }
        payload = json.dumps(payload_dict).encode()
        msg = MagicMock()
        msg.topic = self.pt.topic_name
        msg.payload = payload

        self.pt.on_message(None, None, msg)

        # write() should be called once
        self.pt.write.assert_called_once()

        # Check that tag and field were set correctly
        point_calls = self.pt.measurement().tag.call_args_list
        self.assertEqual(point_calls[0].args[0], "unit")
        self.assertEqual(point_calls[0].args[1], "Unit1")

        field_calls = self.pt.measurement().field.call_args_list
        self.assertEqual(field_calls[0].args[0], "state")
        self.assertEqual(field_calls[0].args[1], 123.4)

    def test_on_message_missing_unit(self):
        payload_dict = {
            "State": 123.4,
            "Timestamp": 987654
        }
        payload = json.dumps(payload_dict).encode()
        msg = MagicMock()
        msg.topic = self.pt.topic_name
        msg.payload = payload

        self.pt.on_message(None, None, msg)

        # write() should NOT be called if Unit is missing
        self.pt.write.assert_not_called()

    def test_on_message_other_topic(self):
        msg = MagicMock()
        msg.topic = "other/topic"
        msg.payload = b"{}"

        # Patch base class on_message to check delegation
        with patch.object(self.pt.__class__.__bases__[0], "on_message") as mock_super:
            self.pt.on_message(None, None, msg)
            mock_super.assert_called_once_with(None, None, msg)

if __name__ == "__main__":
    unittest.main()
