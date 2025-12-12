import json
import unittest
import time
import math
from typing import Any
from masterpiece import MqttMsg
from unittest.mock import MagicMock, patch
from juham_automation.automation.heatingoptimizer import HeatingOptimizer
from juham_core.timeutils import quantize, timestamp
from datetime import datetime, timezone, timedelta


class SimpleMqttMsg(MqttMsg):
    def __init__(self, topic: str, payload: Any):
        self._topic = topic
        self._payload = payload

    @property
    def payload(self) -> Any:
        return self._payload

    @payload.setter
    def payload(self, value: Any) -> None:
        self._payload = value

    @property
    def topic(self) -> str:
        return self._topic

    @topic.setter
    def topic(self, value: str) -> None:
        self._topic = value


class HeatingOptimizerTest2(unittest.TestCase):
    def setUp(self) -> None:
        # Initialize with dummy values
        self.ho = HeatingOptimizer(
            name="TestHeater",
            temperature_sensor="temp1",
            start_hour=6,
            num_hours=4,
            spot_limit=0.3,
        )


        # Patch publish, info, debug, warning, error to avoid side effects
        self.patches = [
            patch.object(self.ho, "publish"),
            patch.object(self.ho, "info"),
            patch.object(self.ho, "debug"),
            patch.object(self.ho, "warning"),
            patch.object(self.ho, "error"),
        ]
        for p in self.patches:
            p.start()
        self.addCleanup(lambda: [p.stop() for p in self.patches])

        # Define simple spot prices and solar forecasts
        self.start_ts= timestamp()
        self.spots = [{"Timestamp": self.start_ts + i*self.ho.energy_balancing_interval, "PriceWithTax": 0.1+i*0.01, "Rank": i} for i in range(48)]

        # Feed to the optimizer
        ts_quantized = quantize(self.ho.energy_balancing_interval, self.start_ts)
        self.ho.on_spot(self.spots, ts_quantized)

        # note: solarenergy forecast with one hour intervals
        self.solar_forecast = [{"ts": self.start_ts + i*3600, "solarenergy": 0.5+i*0.1} for i in range(48)]
        self.ho.on_forecast(self.solar_forecast, ts_quantized)

    def test_sort_by_rank_and_power(self):
        ts_now = self.start_ts
        ranked = self.ho.sort_by_rank(self.spots, ts_now)
        self.assertEqual(len(ranked), len(self.spots))
        # Ensure ranking order
        self.assertTrue(all(ranked[i]["Rank"] <= ranked[i+1]["Rank"] for i in range(len(ranked)-1)))

        ranked_power = self.ho.sort_by_power(self.solar_forecast, ts_now)
        self.assertEqual(len(ranked_power), len(self.solar_forecast))
        self.assertTrue(all(ranked_power[i]["solarenergy"] >= ranked_power[i+1]["solarenergy"] for i in range(len(ranked_power)-1)))

    def test_compute_uoi(self):
        # Within schedule, cheap price
        uoi = self.ho.compute_uoi(price=0.1, slot=7 * 3600/self.ho.energy_balancing_interval)
        self.assertGreater(uoi, 0)
        # Price above expected_average_price
        self.ho.expected_average_price = 0.2
        uoi2 = self.ho.compute_uoi(price=0.3, slot=7 * 3600/self.ho.energy_balancing_interval)
        self.assertEqual(uoi2, 0.0)

    def test_compute_effective_price(self):
        price = self.ho.compute_effective_price(requested_power=6000, available_solpower=3000, spot=0.2)
        self.assertLess(price, 0.2)
        price2 = self.ho.compute_effective_price(requested_power=6000, available_solpower=7000, spot=0.2)
        self.assertEqual(price2, 0.0)

    def test_create_power_plan_and_heating_plan(self):
        self.assertIsNotNone(self.ho.ranked_spot_prices)
        self.assertIsNotNone(self.ho.ranked_solarpower)
        power_plan = self.ho.create_power_plan()
        self.assertTrue(len(power_plan) > 0)
        self.ho.power_plan = power_plan
        heating_plan = self.ho.create_heating_plan()
        self.assertTrue(len(heating_plan) > 0)
        # Each heating plan entry must contain required keys
        for entry in heating_plan:
            self.assertIn("State", entry)
            self.assertIn("Timestamp", entry)
            self.assertIn("UOI", entry)
            self.assertIn("Spot", entry)

    def test_consider_heating(self):
        self.ho.heating_plan = [{"Timestamp": datetime.now().timestamp(), "State": 1}]
        self.ho.current_temperature = 50.0
        self.ho.net_energy_balance_mode = False
        relay = self.ho.consider_heating(datetime.now().timestamp())
        self.assertIn(relay, (0,1))

    def test_on_netenergy_balance(self):
        msg = {"Unit": "TestHeater", "Mode": True}
        self.ho.on_netenergy_balance(msg)
        self.assertTrue(self.ho.net_energy_balance_mode)



class TestHeatingOptimizer(unittest.TestCase):
    def setUp(self) -> None:
        self.optimizer = HeatingOptimizer(
            name="test_optimizer",
            temperature_sensor="temp_sensor",
            start_hour=5,
            num_hours=3,
            spot_limit=0.25,
        )

        # Use patch.object to mock instance methods dynamically
        self.patcher_subscribe = patch.object(
            self.optimizer, "subscribe", autospec=True
        )
        self.patcher_debug = patch.object(self.optimizer, "debug", autospec=True)
        self.patcher_info = patch.object(self.optimizer, "info", autospec=True)
        self.patcher_error = patch.object(self.optimizer, "error", autospec=True)
        self.patcher_warning = patch.object(self.optimizer, "warning", autospec=True)

        # Start the patches
        self.mock_subscribe = self.patcher_subscribe.start()
        self.mock_debug = self.patcher_debug.start()
        self.mock_info = self.patcher_info.start()
        self.mock_error = self.patcher_error.start()
        self.mock_warning = self.patcher_warning.start()

    def tearDown(self) -> None:
        # Stop the patches to clean up
        self.patcher_subscribe.stop()
        self.patcher_debug.stop()
        self.patcher_info.stop()
        self.patcher_error.stop()
        self.patcher_warning.stop()

    def test_initialization(self) -> None:
        self.assertEqual(self.optimizer.heating_slots_per_day, 3*3600 // self.optimizer.energy_balancing_interval)
        self.assertEqual(self.optimizer.start_slot, 5 * 3600 // self.optimizer.energy_balancing_interval)
        self.assertEqual(self.optimizer.spot_limit, 0.25)
        self.assertEqual(self.optimizer.current_temperature, 100)
        self.assertFalse(self.optimizer.relay)

    def test_on_connect(self) -> None:
        self.optimizer.on_connect(None, None, 0, 0)
        self.mock_subscribe.assert_any_call(self.optimizer.topic_in_spot)
        self.mock_subscribe.assert_any_call(self.optimizer.topic_in_forecast)
        self.mock_subscribe.assert_any_call(self.optimizer.topic_in_temperature)
        self.mock_subscribe.assert_any_call(self.optimizer.topic_in_energybalance)

    def test_sort_by_rank(self) -> None:
        test_data = [
            {"Rank": 2, "Timestamp": 2000},
            {"Rank": 1, "Timestamp": 3000},
            {"Rank": 3, "Timestamp": 1000},
        ]
        sorted_data = self.optimizer.sort_by_rank(test_data, 1500)
        self.assertEqual(sorted_data[0]["Rank"], 1)
        self.assertEqual(sorted_data[1]["Rank"], 2)

    def test_sort_by_power(self) -> None:
        test_data = [
            {"solarenergy": 50, "ts": 2000},
            {"solarenergy": 100, "ts": 3000},
            {"solarenergy": 10, "ts": 1000},
        ]
        sorted_data = self.optimizer.sort_by_power(test_data, 1500)
        self.assertEqual(sorted_data[0]["solarenergy"], 100)
        self.assertEqual(sorted_data[1]["solarenergy"], 50)

    def test_on_message_temperature_update(self) -> None:
        mock_msg = SimpleMqttMsg(
            topic=self.optimizer.topic_in_temperature, payload=b'{"temperature": 55}'
        )
        self.optimizer.on_message(None, None, mock_msg)
        self.assertEqual(self.optimizer.current_temperature, 55)

    def test_consider_net_energy_balance(self) -> None:
        """Test case to simulate passing time and check energy balancing behavior."""
        data: dict[str, Any] = {"Unit": "main", "Mode": False}
        mock_msg = SimpleMqttMsg(
            topic=self.optimizer.topic_in_energybalance,
            payload=json.dumps(data).encode("utf-8"),
        )
        self.optimizer.on_message(None, None, mock_msg)
        self.assertFalse(
            self.optimizer.net_energy_balance_mode,
            f"At time {0}, heating should be OFF",
        )
        self.optimizer.on_message(
            None,
            None,
            SimpleMqttMsg(
                topic=self.optimizer.topic_in_energybalance,
                payload=json.dumps({"Unit": "sun", "Mode": True}).encode("utf-8"),
            ),
        )
        self.assertFalse(
            self.optimizer.net_energy_balance_mode,
            f"At time {0}, heating should be OFF",
        )



class HeatingOptimizerOnPowerPlanTest(unittest.TestCase):

    def setUp(self):
        self.ho = HeatingOptimizer(
            name="test_optimizer",
            temperature_sensor="temp1",
            start_hour=6,
            num_hours=4,
            spot_limit=0.3,
        )
        self.base_time = datetime.now(timezone.utc).replace(second=0, microsecond=0)
        self.base_ts = self.base_time.timestamp()

        # Mock MQTT publish to prevent real network interaction
        patcher = patch.object(self.ho, "publish", autospec=True)
        self.mock_publish = patcher.start()
        self.addCleanup(patcher.stop)

        # Mock logging to assert debug/info/warning/error messages
        for method in ["debug", "info", "warning", "error"]:
            setattr(self.ho, method, MagicMock())

        # Set relay state to a known value
        self.ho.current_relay_state = 0

        # Simulate ranked spot prices (needed for power_plan creation)
        self.ho.ranked_spot_prices = [
            {"Timestamp": (self.base_time + timedelta(hours=i)).timestamp(), "Rank": i, "PriceWithTax": 0.1 * i}
            for i in range(24)
        ]

        # Mock create_power_plan and create_heating_plan
        self.ho.create_power_plan = MagicMock(return_value=[
            {"ts": self.base_ts + i * 3600, "FOM": 0.1 * i} for i in range(24)
        ])
        self.ho.create_heating_plan = MagicMock(return_value=[
            {"ts": self.base_ts + i * 3600, "MinTemp": 18, "MaxTemp": 22} for i in range(24)
        ])

        # Mock consider_heating to alternate relay state
        self.ho.consider_heating = MagicMock(side_effect=[1, 0, 1, 0])

    @patch("juham_core.timeutils.timestamp")
    def test_on_powerplan_wait_for_prices(self, mock_ts):
        """Test early exit when no spot prices are available."""
        # Remove spot prices to simulate the waiting state
        self.ho.ranked_spot_prices = []
        mock_ts.return_value = self.base_ts + 61  # exceeds relay optimization gap
        self.ho.on_powerplan(ts_utc_now=mock_ts.return_value)
        self.ho.debug.assert_called_with(f"{self.ho.name} waiting  spot prices...", "")

    @patch("juham_core.timeutils.timestamp")
    def test_on_powerplan_create_power_and_heating_plan(self, mock_ts):
        """Test creation of power and heating plans when conditions are correct."""
        mock_ts.return_value = self.base_ts + 120  # enough elapsed time
        self.ho.on_powerplan(ts_utc_now=mock_ts.return_value)

        # Assert that both plans were created
        self.ho.create_power_plan.assert_called_once()
        self.ho.create_heating_plan.assert_called_once()
        self.ho.info.assert_any_call(f"{self.ho.name} power plan of length 24 created", str(self.ho.power_plan))

    @patch("juham_core.timeutils.timestamp")
    def test_on_powerplan_short_power_plan(self, mock_ts):
        """Test behavior when power plan is too short."""
        self.ho.create_power_plan.return_value = [{"ts": self.base_ts, "FOM": 0.1}]  # only 1 entry
        mock_ts.return_value = self.base_ts + 120
        self.ho.on_powerplan(ts_utc_now=mock_ts.return_value)

        self.ho.warning.assert_called_with(
            f"{self.ho.name} has suspiciously short 1  power plan, waiting for more data ..", ""
        )
        self.assertFalse(self.ho.heating_plan)  # should be cleared

    @patch("juham_core.timeutils.timestamp")
    def test_on_powerplan_short_heating_plan(self, mock_ts):
        """Test behavior when heating plan is too short."""
        self.ho.create_heating_plan.return_value = [{"ts": self.base_ts, "FOM": 0.1}]  # only 1 entry
        mock_ts.return_value = self.base_ts + 120
        self.ho.on_powerplan(ts_utc_now=mock_ts.return_value)

        self.ho.warning.assert_called_with(
            f"{self.ho.name} has too short heating plan 1, no can do", ""
        )
        self.assertFalse(self.ho.power_plan)  # should be cleared

    @patch("juham_core.timeutils.timestamp")
    def test_on_powerplan_relay_switch(self, mock_ts):
        """Test relay switching based on heating plan logic."""
        mock_ts.return_value = self.base_ts + 120
        self.ho.on_powerplan(ts_utc_now=mock_ts.return_value)

        # Check first relay change published
        self.mock_publish.assert_called_with(
            self.ho.topic_out_power, unittest.mock.ANY, 1, False
        )

        # Check info log with regex for timestamp
        args, kwargs = self.ho.info.call_args
        expected_pattern = rf"{self.ho.name} relay changed to 1 at .*"
        self.assertRegex(args[0], expected_pattern)  # Allow any timestamp
        self.assertEqual(args[1], "")


    def test_average_temperature_forecast(self):
        test_data = [
            {"solarenergy": 50, "temp":10, "ts": 2000},
            {"solarenergy": 100, "temp":20, "ts": 3000},
            {"solarenergy": 10, "temp":30, "ts": 1000},
        ]
        average : float = self.ho.next_day_mean_temperature_forecast(test_data, 1000)
        self.assertEqual(average, 20.0)
        average : float = self.ho.next_day_mean_temperature_forecast(test_data, 2200)
        self.assertEqual(average, 20.0)


    def test_opt(self):
        # --- Example Usage ---

        # System Parameters (Typical Boiler/House Settings)
        MIN_MONTHLY = 40.0  # Absolute lowest boiler temp in °C
        MAX_MONTHLY = 70.0  # Absolute highest boiler temp in °C
        TARGET_HOME_TEMP = 20.0 # Reference internal temperature for demand calculation
        self.ho.next_day_factor = 1.0  # Full impact of next day's forecast

        # --- Scenario 1: Very Cold Forecast (High Demand) ---
        min_a, max_a = self.ho.calculate_target_temps(
            MIN_MONTHLY, MAX_MONTHLY, -30.0, TARGET_HOME_TEMP
        )
        self.assertEqual(40.0, min_a);
        self.assertEqual(70.0, max_a);

        # --- Scenario 2: 0C Forecast (Low Demand) ---
        min_b, max_b = self.ho.calculate_target_temps(
            MIN_MONTHLY, MAX_MONTHLY, -20.0, TARGET_HOME_TEMP
        )
        self.assertEqual(40.0, min_b);
        self.assertEqual(64.0, max_b);

        # --- Scenario 3: Warm Forecast (Very Low Demand) ---
        min_c, max_c = self.ho.calculate_target_temps(
            MIN_MONTHLY, MAX_MONTHLY, -10, TARGET_HOME_TEMP
        )
        self.assertEqual(40.0, min_c);
        self.assertEqual(58.0, max_c);

        # --- Scenario 4: Hot Forecast  ---
        min_d, max_d = self.ho.calculate_target_temps(
            MIN_MONTHLY, MAX_MONTHLY, 0, TARGET_HOME_TEMP
        )
        self.assertEqual(40.0, min_d);
        self.assertEqual(52.0, max_d);
        min_e, max_e = self.ho.calculate_target_temps(
            MIN_MONTHLY, MAX_MONTHLY, 30, TARGET_HOME_TEMP
        )
        self.assertEqual(40.0, min_e);
        self.assertEqual(40.0, max_e);


class HeatingOptimizerTest3(unittest.TestCase):

    def setUp(self):
        # minimal constructor args
        self.opt = HeatingOptimizer(
            name="test",
            temperature_sensor="temp",
            start_hour=0,
            num_hours=1,
            spot_limit=1.0,
        )

    # ---------------------------------------------
    # TEST get_future_price()
    # ---------------------------------------------
    def test_get_future_price_returns_nan_when_empty(self):
        self.opt.ranked_spot_prices = []  # no spot prices

        result = self.opt.get_future_price(
            ts_utc_now=time.time(),
            num_hours=1,
            start_hour=0,
            stop_hour=1,
        )

        self.assertTrue(math.isnan(result))

    def test_get_future_price_selects_correct_slots(self):
        ts_now = 1_000_000
        hour = 3600

        # create fake ranked spots (already sorted by rank)
        # two of these fall inside 0–1 hours ahead
        self.opt.ranked_spot_prices = [
            {"Timestamp": ts_now + 100, "PriceWithTax": 10.0},
            {"Timestamp": ts_now + 2000, "PriceWithTax": 20.0},
            {"Timestamp": ts_now + 2*hour, "PriceWithTax": 30.0},  # outside window
        ]

        result = self.opt.get_future_price(
            ts_utc_now=ts_now,
            num_hours=1,      # requires 4 slots → but only two are available
            start_hour=0,
            stop_hour=1,
        )

        # average of 10 and 20
        self.assertAlmostEqual(result, 15.0)

    # ---------------------------------------------
    # TEST calculate_target_temps()
    # ---------------------------------------------
    def test_calculate_target_temps_respects_min_max(self):
        """
        Ensures spot-sensitivity offset does not exceed min/max temperature limits.
        """

        self.opt.spot_sensitivity = 10.0
        self.opt.spot_temp_offset = 10.0

        # mock a simple price difference effect
        tempMin, tempMax = self.opt.calculate_target_temps(
            40.0,
            60.0,
            next_day_mean_temp=0.0,
            target_temperature=22.0
        )

        self.assertGreaterEqual(tempMin, 40.0)
        self.assertLessEqual(tempMax, 60.0)

    def test_calculate_target_temps_increases_temperature_when_spot_high(self):
        """
        This assumes calculate_target_temps() increases target temp when spot is cheap today
        (preheating behaviour).
        """

        self.opt.spot_sensitivity = 10.0

        # simulate:
        # warmer target if tomorrow colder or spot incentive high
        t1 = self.opt.calculate_target_temps(40, 60, next_day_mean_temp=5, target_temperature=22)
        t2 = self.opt.calculate_target_temps(40, 60, next_day_mean_temp=-10, target_temperature=22)

        self.assertTrue(t2 >= t1)

    def test_calculate_target_temps_decreases_temperature_when_tomorrow_warmer(self):
        """
        If next-day mean temperature is high, target should drop (less heating needed).
        """

        t_cold = self.opt.calculate_target_temps(40, 60, next_day_mean_temp=-5, target_temperature=22)
        t_warm = self.opt.calculate_target_temps(40, 60, next_day_mean_temp=25, target_temperature=22)

        self.assertTrue(t_warm <= t_cold)


if __name__ == "__main__":
    unittest.main()
