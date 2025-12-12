import unittest
import json
from unittest import mock
from typing import Any, Dict
from unittest.mock import MagicMock, patch
from masterpiece import MqttMsg
from juham_automation.ts.energybalancer_ts import EnergyBalancerTs

class TestEnergyBalancerTs(unittest.TestCase):
    def setUp(self):
        self.eb = EnergyBalancerTs(name="test_eb")

        # Mock side-effecting methods
        self.eb.write = MagicMock()
        self.eb.error = MagicMock()

        # Mock measurement chain
        mock_point = MagicMock()
        mock_point.tag.return_value = mock_point
        mock_point.field.return_value = mock_point
        mock_point.time.return_value = mock_point
        self.eb.measurement = MagicMock(return_value=mock_point)

        # Mock epoc2utc
        patcher = patch("juham_automation.ts.energybalancer_ts.epoc2utc", return_value="utc-ts")
        self.addCleanup(patcher.stop)
        patcher.start()

    def test_status_valid(self):
        msg : dict[str, Any]= {
            "Unit": "A",
            "Mode": "Auto",
            "Power": 123.45,
            "Timestamp": 123456
        }
        self.eb.on_status(msg)
        self.eb.write.assert_called_once()
        self.eb.error.assert_not_called()

    def test_status_missing_fields(self):
        msg = {
            "Unit": "A",
            "Mode": "Auto"
            # missing Power and Timestamp
        }
        self.eb.on_status(msg)
        self.eb.write.assert_not_called()
        self.eb.error.assert_called_once()
        
    def test_diagnostics_valid(self):
        msg = {
            "EnergyBalancer": "EB1",
            "CurrentBalance": 50,
            "NeededBalance": 30,
            "Timestamp": 123456
        }
        self.eb.on_diagnostics(msg)
        self.eb.write.assert_called_once()
        self.eb.error.assert_not_called()

    def test_diagnostics_missing_timestamp(self):
        msg = {
            "EnergyBalancer": "EB1",
            "CurrentBalance": 50,
            "NeededBalance": 30
            # missing Timestamp
        }
        self.eb.on_diagnostics(msg)
        self.eb.write.assert_not_called()
        self.eb.error.assert_called_once()

    def test_status_invalid_power_type(self):
        """Power given as string should still be converted to float"""
        msg = {
            "Unit": "A",
            "Mode": "Auto",
            "Power": "123.45",
            "Timestamp": 123456
        }
        # Should not raise exception
        try:
            self.eb.on_status(msg)
        except Exception as e:
            self.fail(f"on_status crashed: {e}")
        self.eb.write.assert_called_once()

    def test_diagnostics_invalid_balance_type(self):
        """CurrentBalance/NeededBalance can be any type, should not crash"""
        msg = {
            "EnergyBalancer": "EB1",
            "CurrentBalance": "50",
            "NeededBalance": "30",
            "Timestamp": 123456
        }
        try:
            self.eb.on_diagnostics(msg)
        except Exception as e:
            self.fail(f"on_diagnostics crashed: {e}")
        self.eb.write.assert_called_once()


if __name__ == "__main__":
    unittest.main()
