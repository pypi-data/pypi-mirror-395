from masterpiece import MqttMsg
from juham_automation.ts.energycostcalculator_ts import EnergyCostCalculatorTs
import unittest
import json
from unittest import mock
from typing import Any, Dict, List
from unittest.mock import MagicMock, patch
from masterpiece.mqtt import MqttMsg

class TestEnergyCostCalculatorTs(unittest.TestCase):
    def setUp(self):
        self.ecc = EnergyCostCalculatorTs(name="test_ecc")

        # Mock write_point
        self.ecc.write_point = MagicMock()

        # Patch timestampstr so it returns a fixed string
        patcher = patch("juham_automation.ts.energycostcalculator_ts.timestampstr", return_value="utc-ts")
        self.addCleanup(patcher.stop)
        patcher.start()

    def test_record_powerconsumption_valid(self):
        msg = {"name": "SiteA", "ts": 123456, "consumption": 100}
        self.ecc.record_powerconsumption(msg)
        self.ecc.write_point.assert_called_once_with(
            "energycost", {"site": "SiteA"}, msg, "utc-ts"
        )

    def test_record_powerconsumption_missing_name(self):
        msg = {"ts": 123456, "consumption": 100}
        with self.assertRaises(KeyError):
            self.ecc.record_powerconsumption(msg)

    def test_record_powerconsumption_missing_ts(self):
        msg = {"name": "SiteA", "consumption": 100}
        with self.assertRaises(KeyError):
            self.ecc.record_powerconsumption(msg)

    from unittest.mock import MagicMock

    def test_on_message_valid_topic(self):
        payload = json.dumps({"name": "SiteA", "ts": 123456, "consumption": 100}).encode()
        
        # Create a mock message instead of MqttMsg
        msg = MagicMock()
        msg.topic = self.ecc.topic_net_energy_balance
        msg.payload = payload

        self.ecc.record_powerconsumption = MagicMock()
        self.ecc.on_message(None, None, msg)

        self.ecc.record_powerconsumption.assert_called_once_with({
            "name": "SiteA",
            "ts": 123456,
            "consumption": 100
        })


    def test_on_message_other_topic(self):
        payload = json.dumps({"name": "SiteA", "ts": 123456, "consumption": 100}).encode()
        
        # Mock message
        msg = MagicMock()
        msg.topic = "other/topic"
        msg.payload = payload

        # Patch the base class on_message to check delegation
        with patch.object(self.ecc.__class__.__bases__[0], "on_message") as mock_super:
            self.ecc.on_message(None, None, msg)
            mock_super.assert_called_once_with(None, None, msg)



if __name__ == "__main__":
    unittest.main()
