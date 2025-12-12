import unittest
import json
from masterpiece import MqttMsg
from juham_automation.ts.log_ts import LogTs
from unittest.mock import MagicMock, patch
from masterpiece.mqtt import MqttMsg

class TestLogTs(unittest.TestCase):
    def setUp(self):
        self.logts = LogTs(name="test_log")

        # Mock measurement chain
        mock_point = MagicMock()
        mock_point.tag.return_value = mock_point
        mock_point.field.return_value = mock_point
        mock_point.time.return_value = mock_point
        self.logts.measurement = MagicMock(return_value=mock_point)
        self.logts.write = MagicMock()

        # Patch epoc2utc
        patcher = patch("juham_automation.ts.log_ts.epoc2utc", return_value="utc-ts")
        self.addCleanup(patcher.stop)
        patcher.start()

    def test_on_message_valid_topic(self):
        payload_dict = {
            "Class": "Warning",
            "Source": "Module1",
            "Msg": "Something happened",
            "Details": "Extra info",
            "Timestamp": 123456
        }
        payload = json.dumps(payload_dict).encode()
        msg = MagicMock()
        msg.topic = self.logts.topic_name
        msg.payload = payload

        self.logts.on_message(None, None, msg)

        # write() should be called once
        self.logts.write.assert_called_once()
        # check that field values passed
        point_call = self.logts.measurement().field.call_args_list
        fields = {call.args[0]: call.args[1] for call in point_call}
        self.assertEqual(fields["source"], "Module1")
        self.assertEqual(fields["msg"], "Something happened")
        self.assertEqual(fields["details"], "Extra info")
        self.assertEqual(fields["Timestamp"], 123456)

    def test_on_message_write_exception(self):
        # Simulate write() throwing an exception
        payload_dict = {
            "Class": "Error",
            "Source": "Module2",
            "Msg": "Crash",
            "Details": "Stacktrace",
            "Timestamp": 654321
        }
        payload = json.dumps(payload_dict).encode()
        msg = MagicMock()
        msg.topic = self.logts.topic_name
        msg.payload = payload

        self.logts.write.side_effect = Exception("DB error")

        # Exception should be caught, no crash
        try:
            self.logts.on_message(None, None, msg)
        except Exception:
            self.fail("on_message() raised exception unexpectedly")

    def test_on_message_other_topic(self):
        msg = MagicMock()
        msg.topic = "other/topic"
        msg.payload = b"{}"

        # Patch base class on_message to check delegation
        with patch.object(self.logts.__class__.__bases__[0], "on_message") as mock_super:
            self.logts.on_message(None, None, msg)
            mock_super.assert_called_once_with(None, None, msg)


if __name__ == "__main__":
    unittest.main()
