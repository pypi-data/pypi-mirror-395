import unittest
from unittest.mock import MagicMock, patch
from juham_automation.ts.electricityprice_ts import ElectricityPriceTs


class TestElectricityPriceTs(unittest.TestCase):
    def setUp(self):
        self.ts = ElectricityPriceTs(name="testprice")

        # Mock side-effecting methods
        self.ts.write = MagicMock()

        # Mock measurement chain
        mock_point = MagicMock()
        mock_point.tag.return_value = mock_point
        mock_point.field.return_value = mock_point
        mock_point.time.return_value = mock_point
        self.ts.measurement = MagicMock(return_value=mock_point)

        # Mock epoc2utc
        patcher = patch("juham_automation.ts.electricityprice_ts.epoc2utc", return_value="utc-ts")
        self.addCleanup(patcher.stop)
        patcher.start()

    def test_valid_spot(self):
        """All valid entries with GridCost → write() called once per entry"""
        msg = [
            {"Timestamp": 123, "PriceWithTax": 50.5, "GridCost": 10.0},
            {"Timestamp": 124, "PriceWithTax": 51.0, "GridCost": 11.0},
        ]

        self.ts.on_spot(msg)

        self.assertEqual(self.ts.write.call_count, 2)

    def test_missing_gridcost(self):
        """Entries missing GridCost are skipped"""
        msg = [
            {"Timestamp": 123, "PriceWithTax": 50.5},  # skipped
            {"Timestamp": 124, "PriceWithTax": 51.0, "GridCost": 11.0},  # valid
        ]

        self.ts.on_spot(msg)

        # Only one valid entry
        self.assertEqual(self.ts.write.call_count, 1)

    def test_empty_list(self):
        """Empty input list → no write calls"""
        self.ts.on_spot([])

        self.ts.write.assert_not_called()

    def test_invalid_price(self):
        """Non-float PriceWithTax should still be processed"""
        msg = [
            {"Timestamp": 123, "PriceWithTax": "50.5", "GridCost": 10.0},
        ]

        # Should not crash
        try:
            self.ts.on_spot(msg)
        except Exception as e:
            self.fail(f"on_spot crashed with exception: {e}")

        self.assertEqual(self.ts.write.call_count, 1)


if __name__ == "__main__":
    unittest.main()
