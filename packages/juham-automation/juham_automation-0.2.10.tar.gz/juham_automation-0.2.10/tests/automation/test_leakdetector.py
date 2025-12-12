import unittest
from unittest.mock import patch, MagicMock
from typing import Any
from masterpiece.mqtt import MqttMsg
from juham_automation.automation.leakdetector import LeakDetector

class MqttTestMsg:
    def __init__(self, topic: str, payload: bytes):
        self.topic = topic
        self.payload = payload


class TestLeakDetector(unittest.TestCase):

    def setUp(self) -> None:
        self.leak_detector = LeakDetector()
        self.leak_detector.activity_timeout = 300.0  # Set timeout to 5 minutes

    def test_initialization(self) -> None:
        self.assertFalse(self.leak_detector.leak_detected)
        self.assertEqual(self.leak_detector.zero_usage_periods_count, 0)
        self.assertTrue(self.leak_detector.watermeter_full_topic.endswith("watermeter"))
        self.assertTrue(self.leak_detector.motion_full_topic.endswith("motion"))

    def test_to_from_dict(self) -> None:
        state = self.leak_detector.to_dict()
        new_instance = LeakDetector()
        new_instance.from_dict(state)
        self.assertEqual(new_instance.motion_topic, self.leak_detector.motion_topic)

    @patch.object(LeakDetector, "subscribe")
    def test_on_connect_success(self, mock_subscribe: MagicMock) -> None:
        self.leak_detector.on_connect(None, None, 0, 0)
        self.assertEqual(mock_subscribe.call_count, 2)

    @patch.object(LeakDetector, "process_water_meter_data")
    @patch.object(LeakDetector, "process_motion_data")
    def test_on_message_routing(
        self, mock_motion: MagicMock, mock_water: MagicMock
    ) -> None:
        water_payload = MqttTestMsg(
            topic=self.leak_detector.watermeter_full_topic,
            payload=b'{"active_lpm": 1.0, "ts": 123}',
        )

        motion_payload = MqttTestMsg(
            topic=self.leak_detector.motion_full_topic,
            payload=b'{"motion": true, "ts": 123}',
        )

        self.leak_detector.on_message(None, None, water_payload)
        mock_water.assert_called_once()

        self.leak_detector.on_message(None, None, motion_payload)
        mock_motion.assert_called_once()

    @patch("juham_automation.automation.leakdetector.timestamp", return_value=1000.0)
    def test_detect_activity_true(self, _: MagicMock) -> None:
        self.leak_detector.motion_last_detected_ts = 500000.0
        self.assertTrue(self.leak_detector.detect_activity(1000.0))

    def test_detect_activity_false(self) -> None:
        self.leak_detector.motion_last_detected_ts = 0.0
        self.assertFalse(self.leak_detector.detect_activity(500000.0))

    @patch.object(LeakDetector, "publish")
    @patch.object(LeakDetector, "warning")
    def test_process_water_leak_detected(
        self, mock_warning: MagicMock, mock_publish: MagicMock
    ) -> None:
        self.leak_detector.motion_last_detected_ts = 0.0  # No motion
        data = {"active_lpm": 1.2, "ts": 1000000.0}

        # Process water meter data
        self.leak_detector.process_water_meter_data(data)

        # Assert leak is detected
        self.assertTrue(self.leak_detector.leak_detected)
        self.assertEqual(self.leak_detector.zero_usage_periods_count, 0)
        mock_warning.assert_called_once()
        mock_publish.assert_called_once()

    @patch.object(LeakDetector, "publish")
    def test_process_water_leak_reset(self, mock_publish: MagicMock) -> None:
        self.leak_detector.leak_detected = True
        self.leak_detector.zero_usage_periods_count = 61
        data = {"active_lpm": 0.0, "ts": 2000.0}

        # Process water meter data
        self.leak_detector.process_water_meter_data(data)

        # Assert leak is reset
        self.assertFalse(self.leak_detector.leak_detected)
        self.assertEqual(self.leak_detector.motion_last_detected_ts, 2000.0)
        mock_publish.assert_called_once()

    @patch.object(LeakDetector, "publish")
    def test_process_water_normal_usage(self, mock_publish: MagicMock) -> None:
        self.leak_detector.motion_last_detected_ts = 900.0
        self.leak_detector.detect_activity = MagicMock(return_value=True)
        data = {"active_lpm": 2.0, "ts": 1000.0}

        # Process water meter data
        self.leak_detector.process_water_meter_data(data)

        # Assert no leak detected and no warning
        self.assertFalse(self.leak_detector.leak_detected)
        self.assertEqual(self.leak_detector.zero_usage_periods_count, 0)
        mock_publish.assert_called_once()

    def test_process_motion_data(self) -> None:
        self.leak_detector.motion_last_detected_ts = 0.0
        data = {"motion": True, "ts": 1337.0}

        # Process motion data
        self.leak_detector.process_motion_data(data)

        # Assert last motion timestamp updated
        self.assertEqual(self.leak_detector.motion_last_detected_ts, 1337.0)


if __name__ == "__main__":
    unittest.main()
