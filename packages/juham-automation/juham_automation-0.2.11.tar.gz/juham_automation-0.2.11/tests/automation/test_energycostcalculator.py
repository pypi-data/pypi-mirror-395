import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone, timedelta
from juham_automation.automation.energycostcalculator import EnergyCostCalculator
import json
from juham_core.timeutils import quantize

class EnergyCostCalculatorTest(unittest.TestCase):

    year : int = 2024
    month : int = 6
    day : int = 30

    def setUp(self):
        """Prepare calculators with different energy balancing intervals."""
        self.calculator_15min = self.create_calculator(15)
        self.calculator_1h = self.create_calculator(60)
        self.energy = 1000.0  
        
        self.ecc = EnergyCostCalculator("test_ecc")
        # Provide a simple spot price profile (hourly)
        base = datetime(self.year, self.month, self.day, 0, 0, tzinfo=timezone.utc)
        self.ecc.spots = [
            {"Timestamp": (base + timedelta(hours=i)).timestamp(), "PriceWithTax": 0.1 * i}
            for i in range(48)
        ]
        self.ecc.total_balance_interval = 0
        self.ecc.total_balance_hour = 0
        self.ecc.total_balance_day = 0
        self.ecc.net_energy_balance_cost_interval = 0.0
        self.ecc.net_energy_balance_cost_hour = 0.0
        self.ecc.net_energy_balance_cost_day = 0.0
        self.ecc.current_ts = 0
        self.ecc.energy_balancing_interval = 900  # 15 min

    def test_constructor(self) -> None:
        """Test construction of EnergyCostCalculator."""
        ok = True
        try:
            object = EnergyCostCalculator()
            self.assertIsNotNone(object)
        except Exception:
            ok = False
        self.assertTrue(ok)

    def create_calculator(self, ebi: int) -> EnergyCostCalculator:
        """Create EnergyCostCalculator with the given energy balancing interval
        and linearly changing spot energy prices.
        """
        # Total simulation time: 48 hours
        total_seconds = 48 * 3600
        num_intervals = total_seconds // ebi

        base_ts = datetime(self.year, self.month, self.day, 0, 0, tzinfo=timezone.utc).timestamp()
        spot: list[dict[str, float]] = []

        for i in range(int(num_intervals) + 1):  # +1 to include the end timestamp
            ts = base_ts + i * ebi
            price = i / num_intervals  # linearly from 0.0 to 1.0
            spot.append(
                {
                    "Timestamp": ts,
                    "PriceWithTax": price,
                }
            )

        calculator = EnergyCostCalculator("test")
        calculator.energy_balancing_interval = ebi
        calculator.spots = spot
        return calculator


    def test_get_classid(self) -> None:
        """Assert the class identifier is valid."""
        _class_id = EnergyCostCalculator.get_class_id()
        self.assertEqual("EnergyCostCalculator", _class_id)

    def test_cost_per_joule(self) -> None:
        """Test method for mapping energy price per kWh to Ws (Watt seconds,
        i.e. Joules)"""
        obj = self.create_calculator(900)
        ws = obj.map_kwh_prices_to_joules(1000.0 * 3600)
        self.assertAlmostEqual(1.0, ws, delta=1e-7)

    def test_cost_calculator_linear(self) -> None:
        obj = self.create_calculator(15)  # 15 min intervals, linear spot prices

        ts_start = datetime(self.year, self.month, self.day, 14, 0, tzinfo=timezone.utc).timestamp()
        ts_end = datetime(self.year, self.month, self.day, 15, 0, tzinfo=timezone.utc).timestamp()
        energy = 1000.0  # watts

        cost = obj.calculate_net_energy_cost(ts_start, ts_end, energy)

        # Convert spot price to per-Joule units for consistency
        price_start = obj.map_kwh_prices_to_joules(obj.get_price_at(ts_start))
        price_end = obj.map_kwh_prices_to_joules(obj.get_price_at(ts_end))
        expected = energy * (price_start + price_end) / 2 * (ts_end - ts_start)

        self.assertAlmostEqual(expected, cost, delta=1e-7)

    def test_get_price_at_start_15min(self):
        """Test price lookup at the beginning of the interval."""
        ts = datetime(2024, 6, 30, 0, 0, tzinfo=timezone.utc).timestamp()
        price = self.calculator_15min.get_price_at(ts)
        self.assertAlmostEqual(price, 0.0)

    def test_get_price_at_middle_15min(self):
        """Test price lookup halfway through the price sequence."""
        # Timestamp around 24 hours into June 30
        ts = datetime(2024, 7, 1, 0, 0, tzinfo=timezone.utc).timestamp()
        price = self.calculator_15min.get_price_at(ts)
        # Middle price should be about 0.5 for linear pricing across 48h
        self.assertAlmostEqual(price, 0.5, places=2)

    def test_get_price_at_end_1h(self):
        """Test price lookup at the last timestamp."""
        ts = datetime(2024, 7, 1, 23, 0, tzinfo=timezone.utc).timestamp()
        price = self.calculator_1h.get_price_at(ts)
        # Last (47th) out of 48 linear price points
        self.assertAlmostEqual(price, 47 / 48, places=2)

    def test_get_price_at_exact_match_1h(self):
        """Ensure exact timestamp matching works."""
        ts = datetime(2024, 6, 30, 1, 0, tzinfo=timezone.utc).timestamp()
        price = self.calculator_1h.get_price_at(ts)
        # 1 hour in, price is 1/48
        self.assertAlmostEqual(price, 1 / 48)

    def test_get_price_at_before_first(self):
        """Test behavior for timestamp before the spot data range."""
        ts = datetime(2024, 6, 29, 23, 59, tzinfo=timezone.utc).timestamp()
        price = self.calculator_15min.get_price_at(ts)
        self.assertAlmostEqual(price, 0.0)

    def test_get_price_at_after_last(self):
        """Test behavior for timestamp after the spot data range."""
        ts = datetime(2024, 7, 2, 0, 0, tzinfo=timezone.utc).timestamp()
        price = self.calculator_1h.get_price_at(ts)
        self.assertAlmostEqual(price, 1.0)


    def integrate_cost(self, calc, ts_start, ts_end, energy):
        """Integrate cost using get_price_at() in steps of energy_balancing_interval."""
        cost = 0.0
        interval = calc.energy_balancing_interval
        current = ts_start
        while current < ts_end:
            next_ts = min(ts_end, current + interval)
            price_start = calc.get_price_at(current)
            price_end = calc.get_price_at(next_ts)
            avg_price = (price_start + price_end) / 2.0  # trapezoid integration
            dt = next_ts - current
            cost += energy * avg_price * dt / 3600.0  # converting seconds → hours
            current = next_ts
        return cost

    def test_integrated_cost_linear_profile(self):
        """Check that integrated cost is same for 15 min and 1-hour intervals."""
        ts_start = datetime(2024, 6, 30, 0, 0, tzinfo=timezone.utc).timestamp()
        ts_end = datetime(2024, 6, 30, 12, 0, tzinfo=timezone.utc).timestamp()  # 12 hours

        cost_15min = self.integrate_cost(self.calculator_15min, ts_start, ts_end, self.energy)
        cost_1h = self.integrate_cost(self.calculator_1h, ts_start, ts_end, self.energy)

        # For linear prices, integrated cost should be almost identical
        self.assertAlmostEqual(cost_15min, cost_1h, places=6)

        # Optionally print for debugging
        print(f"Cost 15 min interval: {cost_15min}")
        print(f"Cost 1 hour interval: {cost_1h}")



    @patch.object(EnergyCostCalculator, "publish")
    @patch.object(EnergyCostCalculator, "info")
    def test_on_powerconsumption_initial(self, mock_info, mock_publish):
        # Initial call with current_ts == 0 should initialize values
        ts = datetime(2024, 6, 30, 10, 5, tzinfo=timezone.utc).timestamp()
        self.ecc.on_powerconsumption(ts, {"real_total": 1000.0})

        self.assertEqual(self.ecc.current_ts, ts)
        self.assertAlmostEqual(
            self.ecc.net_energy_balance_start_interval,
            quantize(self.ecc.energy_balancing_interval, ts)
        )
        self.assertAlmostEqual(
            self.ecc.net_energy_balance_start_hour,
            quantize(3600, ts)
        )
        mock_info.assert_not_called()
        mock_publish.assert_not_called()  # nothing to publish on first call

    @patch.object(EnergyCostCalculator, "publish")
    def test_on_powerconsumption_accumulation(self, mock_publish):
        ts0 = datetime(2024, 6, 30, 10, 0, tzinfo=timezone.utc).timestamp()
        self.ecc.spots = [{"Timestamp": ts0, "PriceWithTax": 1.0}]
        
        # First call initializes current_ts, does not accumulate yet
        self.ecc.on_powerconsumption(ts0, {"real_total": 1000.0})
        
        # Second call after 15 minutes
        ts1 = ts0 + 900
        self.ecc.on_powerconsumption(ts1, {"real_total": 1000.0})
        
        self.assertGreater(self.ecc.total_balance_interval, 0)
        self.assertGreater(self.ecc.total_balance_hour, 0)

    @patch.object(EnergyCostCalculator, "publish")
    @patch.object(EnergyCostCalculator, "info")
    def test_on_powerconsumption_day_accumulation(self, mock_info, mock_publish):
        """Simulate enough 15-min intervals to accumulate day totals"""
        start_ts = datetime(2024, 6, 30, 0, 0, tzinfo=timezone.utc).timestamp()
        power = 1000.0  # 1 kW

        # Simulate 24 hours + 1 interval to trigger day accumulation
        for i in range((24 * 3600 // self.ecc.energy_balancing_interval) + 1):
            ts = start_ts + i * self.ecc.energy_balancing_interval
            self.ecc.on_powerconsumption(ts, {"real_total": power})

        # Now the day balance should be > 0
        self.assertGreater(self.ecc.total_balance_day, 0)
        self.assertGreater(self.ecc.total_balance_hour, 0)
        #FIXME self.assertEqual(self.ecc.total_balance_interval, 0.25, 1e-3)
        # Check that publish was called multiple times
        self.assertTrue(mock_publish.called)

    @patch.object(EnergyCostCalculator, "publish")
    def test_on_powerconsumption_interval_reset(self, mock_publish):
        ts0 = datetime(2024, 6, 30, 10, 0, tzinfo=timezone.utc).timestamp()
        self.ecc.on_powerconsumption(ts0, {"real_total": 1000.0})

        # Call after one full interval to trigger reset
        ts_next_interval = ts0 + self.ecc.energy_balancing_interval + 1
        self.ecc.on_powerconsumption(ts_next_interval, {"real_total": 1000.0})

        # Interval counters should have reset
        self.assertEqual(self.ecc.total_balance_interval, 0)
        self.assertEqual(self.ecc.net_energy_balance_cost_interval, 0.0)
        # Hour/day counters should not reset yet
        self.assertGreater(self.ecc.total_balance_hour, 0)
        self.assertEqual(self.ecc.total_balance_day, 0)

    @patch.object(EnergyCostCalculator, "publish")
    def test_on_powerconsumption_hour_reset(self, mock_publish):
        ts0 = datetime(self.year, self.month, self.day, 10, 0, tzinfo=timezone.utc).timestamp()
        self.ecc.on_powerconsumption(ts0, {"real_total": 1000.0})

        # Advance more than 1 hour
        ts_next_hour = ts0 + 3601
        self.ecc.on_powerconsumption(ts_next_hour, {"real_total": 1000.0})

        self.assertEqual(self.ecc.total_balance_hour, 0)
        self.assertEqual(self.ecc.net_energy_balance_cost_hour, 0.0)
        # Interval and day counters may still be non-zero
        self.assertGreaterEqual(self.ecc.total_balance_interval, 0)
        self.assertEqual(self.ecc.total_balance_day, 0)

    @patch.object(EnergyCostCalculator, "publish")
    def test_on_powerconsumption_day_reset(self, mock_publish):
        ts0 = datetime(self.year, self.month, self.day, 0, 0, tzinfo=timezone.utc).timestamp()
        self.ecc.on_powerconsumption(ts0, {"real_total": 1000.0})

        # Advance more than 24h
        ts_next_day = ts0 + 24 * 3600 + 1
        self.ecc.on_powerconsumption(ts_next_day, {"real_total": 1000.0})

        self.assertEqual(self.ecc.total_balance_day, 0)
        self.assertEqual(self.ecc.net_energy_balance_cost_day, 0.0)


if __name__ == "__main__":
    unittest.main()
