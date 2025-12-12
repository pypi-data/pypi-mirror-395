import unittest
from unittest.mock import MagicMock, patch
import time
import json
from juham_core.timeutils import quantize, timestamp
from juham_automation.automation import WaterCirculator  

class TestWaterCirculator(unittest.TestCase):
    def setUp(self):
        # Patch timestamp to return a predictable value
        self.patcher = patch('juham_core.timeutils.timestamp', return_value=1000.0)

        self.mock_timestamp = self.patcher.start()
        
        # Instantiate WaterCirculator
        self.circulator = WaterCirculator("TestUnit", "TempSensor")
        
        # Mock the publish and logging method
        self.circulator.publish = MagicMock()
        self.circulator.info = MagicMock()
        self.circulator.debug = MagicMock()
    
    def tearDown(self):
        self.patcher.stop()

    def test_initial_state(self):
        self.assertFalse(self.circulator.current_motion)
        self.assertEqual(self.circulator.water_temperature, 0)
        self.assertEqual(self.circulator.water_temperature_updated, 0)
        self.assertFalse(self.circulator.initialized)


    def test_on_temperature_sensor_updates_state(self):
        self.circulator.on_temperature_sensor({"temperature": 42}, 1000.0)
        self.assertEqual(self.circulator.water_temperature, 42)
        self.assertEqual(self.circulator.water_temperature_updated, 1000.0)

    @patch("juham_automation.automation.watercirculator.timestamp", return_value=1000.0)
    def test_on_motion_sensor_starts_pump_when_cold(self, mock_timestamp):
        # simulate motion detected, water below min_temperature
        self.circulator.water_temperature = 35
        self.circulator.current_motion = False
        self.circulator.initialized = False

        self.circulator.on_motion_sensor({"sensor": "Hall", "motion": True, "vibration": False}, 1000.0)
        self.assertTrue(self.circulator.current_motion)
        self.assertEqual(self.circulator.relay_started_ts, 1000.0)
        self.circulator.publish.assert_called_with(
            self.circulator.topic_power,
            json.dumps({"Unit": "TestUnit", "Timestamp": 1000.0, "State": 1}),
            1,
            False
        )
        self.assertTrue(self.circulator.initialized)

    @patch("juham_automation.automation.watercirculator.timestamp", return_value=1000.0)
    def test_on_motion_sensor_does_not_start_when_hot(self, mock_timestamp):
        # water temperature above min_temperature
        self.circulator.water_temperature = 38
        self.circulator.current_motion = False
        self.circulator.initialized = False

        self.circulator.on_motion_sensor({"sensor": "Hall", "motion": True, "vibration": False}, 1000.0)
        self.assertFalse(self.circulator.current_motion)
        self.circulator.publish.assert_called_with(
            self.circulator.topic_power,
            json.dumps({"Unit": "TestUnit", "Timestamp": 1000.0, "State": 0}),
            1,
            False
        )

    @patch("juham_automation.automation.watercirculator.timestamp", return_value=1000.0)
    def test_on_motion_sensor_extends_running_time(self, mock_timestamp):
        # Pump already running
        self.circulator.current_motion = True
        self.circulator.relay_started_ts = 900.0
        self.circulator.water_temperature = 35

        self.circulator.on_motion_sensor({"sensor": "Hall", "motion": True, "vibration": False}, 1000.0)
        self.circulator.publish.assert_called_with(
            self.circulator.topic_power,
            json.dumps({"Unit": "TestUnit", "Timestamp": 1000.0, "State": 1}),
            1,
            False
        )
        self.assertEqual(self.circulator.relay_started_ts, 1000.0)

    @patch("juham_automation.automation.watercirculator.timestamp", return_value=1000.0)
    def test_on_motion_sensor_stops_after_uptime(self, mock_timestamp):
        # Pump running, motion lost, elapsed time > uptime
        self.circulator.current_motion = True
        self.circulator.relay_started_ts = 0
        self.circulator.initialized = True

        self.circulator.on_motion_sensor({"sensor": "Hall", "motion": False, "vibration": False}, 2000.0)
        self.circulator.publish.assert_called_with(
            self.circulator.topic_power,
            json.dumps({"Unit": "TestUnit", "Timestamp": 1000.0, "State": 0}),
            1,
            False
        )
        self.assertFalse(self.circulator.current_motion)
        self.assertTrue(self.circulator.initialized)

    @patch("juham_automation.automation.watercirculator.timestamp", return_value=1000.0)
    def test_on_motion_sensor_continues_running_if_within_uptime(self, mock_timestamp):
        self.circulator.current_motion = True
        self.circulator.relay_started_ts = 950.0  # elapsed = 50 < uptime
        self.circulator.initialized = True

        self.circulator.on_motion_sensor({"sensor": "Hall", "motion": False, "vibration": False}, 1000.0)
        self.circulator.publish.assert_called_with(
            self.circulator.topic_power,
            json.dumps({"Unit": "TestUnit", "Timestamp": 1000.0, "State": 1}),
            1,
            False
        )
        self.assertTrue(self.circulator.current_motion)

    @patch("juham_automation.automation.watercirculator.timestamp", return_value=1000.0)
    def test_on_connect_subscribes_and_resets_relay(self, mock_timestamp):
        self.circulator.on_connect(client=None, userdata=None, flags=None, rc=0)
        self.circulator.publish.assert_called_with(
            self.circulator.topic_power,
            json.dumps({"Unit": "TestUnit", "Timestamp": 1000.0, "State": 0}),
            1,
            False
        )

if __name__ == "__main__":
    unittest.main()
