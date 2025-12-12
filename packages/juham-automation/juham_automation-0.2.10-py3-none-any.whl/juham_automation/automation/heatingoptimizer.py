from datetime import datetime
import json
import time
import math
from typing import Any
from typing_extensions import override

from masterpiece.mqtt import MqttMsg
from juham_core import Juham
from juham_core.timeutils import (
    quantize,
    timestamp,
    timestampstr,
)



class HeatingOptimizer(Juham):
    """Automation class for optimized control of temperature driven home energy consumers e.g hot
    water radiators. Reads spot prices, solar electricity forecast, temperature forecast, power meter and
    the current temperature of the system to be heated to optimize energyc consumption and 
    minimize electricity bill.

    Represents a heating system that knows the power rating of its radiator (e.g., 3kW).
    Any number of heating devices can co-exist, each with its own heating optimizer with 
    different temperature, schedule and electricity price ratings.

    The system subscribes to the 'power' topic to track the current power balance. If the solar panels
    generate more energy than is being consumed, the optimizer activates a relay to ensure that all excess energy
    produced within that balancing interval is used for heating. The goal is to achieve a net zero energy 
    balance for each slot, ensuring that any surplus energy from the solar panels is fully utilized.

    The heating plan is published to 'topic_powerplan' topic for monitoring purposes.
    Radiator relay state is published to 'power' topic, to actualize the heating plan.

    Computes also UOI - optimization utilization index for each slot, based on the spot price and the solar power forecast.
    For negative energy balance this determines when energy is consumed. Value of 0 means the slot is expensive, 
    value of 1 means the slot is free. The UOI threshold determines the slots that are allowed to be consumed.
    """

    energy_balancing_interval: float = 900 
    """Energy balancing interval, as regulated by the  industry/converment. In seconds"""

    radiator_power: float = 6000  # W
    """Radiator power in Watts. This is the maximum power that the radiator can consume."""

    heating_slots_per_day: float = 4
    """ Number of slots per day the radiator is allowed to heat."""

    schedule_start_slot: float = 0
    """Start slots of the heating schedule."""

    schedule_stop_slot: float = 0
    """Stop slot of the heating schedule. Heating is allowed only between start-stop slots."""

    timezone: str = "Europe/Helsinki"
    """ Timezone of the heating system. This is used to convert UTC timestamps to local time."""

    expected_average_price: float = 0.2
    """Expected average price of electricity, beyond which the heating is avoided."""

    uoi_threshold: float = 0.8
    """Utilization Optimization Index threshold. This is the minimum UOI value that is allowed 
    for the heating to be activated."""

    balancing_weight: float = 1.0
    """Weight determining how large a share of the time slot a consumer receives compared to others ."""

    spot_sensitivity: float = 20.0
    """Sensitivity of the heating plan to spot price changes. Higher values mean more aggressive."""

    spot_temp_offset: float = 20.0
    """Safety limit to spot driven temp. adjustment, the maximum number of 
    degrees I’m allowed to adjust
    """

    temperature_limits: dict[int, tuple[float, float]] = {
        1: (60.0, 70.0),  # January
        2: (55.0, 70.0),  # February
        3: (50.0, 65.0),  # March
        4: (20.0, 60.0),  # April
        5: (10.0, 55.0),  # May
        6: (10.0, 38.0),  # June
        7: (10.0, 40.0),  # July
        8: (35.0, 45.0),  # August
        9: (40.0, 55.0),  # September
        10: (45.0, 60.0),  # October
        11: (50.0, 65.0),  # November
        12: (55.0, 70.0),  # December
    }
    """Temperature limits for each month. The minimum temperature is maintained regardless of the cost.
    The limits are defined as a dictionary where the keys are month numbers (1-12)
    and the values are tuples of (min_temp, max_temp). The min_temp and max_temp values are in 
    degrees Celsius."""

    next_day_factor: float = 1.0
    """Factor to adjust the temperature limits based on the next day's average temperature forecast.
    A value of 0.0 means that the next day's temperature is irrelevant. A value of 1.0 means that the next 
    day's temperature fully affects the temperature limits."""

    max_expected_temp_difference : float = 50.0
    """Maximum expected temperature difference (Target - Forecast) 
    used for normalizing the heating need to a 0-1 scale."""

    target_home_temperature : float = 22.0
    """Target home temperature in degrees Celsius."""
    
    def __init__(
        self,
        name: str,
        temperature_sensor: str,
        start_hour: int,
        num_hours: int,
        spot_limit: float,
    ) -> None:
        """Create power plan for automating temperature driven systems, e.g. heating radiators
        to optimize energy consumption based on electricity prices.

        Electricity Price MQTT Topic: This specifies the MQTT topic through which the controller receives
        hourly electricity price forecasts for the next day or two.
        Radiator Control Topic: The MQTT topic used to control the radiator relay.
        Temperature Sensor Topic: The MQTT topic where the temperature sensor publishes its readings.
        Electricity Price Slot Range: A pair of integers determining which electricity price slots the
        controller uses. The slots are ranked from the cheapest to the most expensive. For example:
        - A range of 0, 3 directs the controller to use electricity during the three cheapest hours.
        - A second controller with a range of 3, 2 would target the next two cheapest hours, and so on.
        Maximum Electricity Price Threshold: An upper limit for the electricity price, serving as an 
        additional control.
        The controller only operates within its designated price slots if the prices are below this threshold.

        The maximum price threshold reflects the criticality of the radiator's operation:

        High thresholds indicate that the radiator should remain operational regardless of the price.
        Low thresholds imply the radiator can be turned off during expensive periods, suggesting it 
        has a less critical role.

        By combining these attributes, the controller ensures efficient energy usage while maintaining 
        desired heating levels.

        Args:
            name (str): name of the heating radiator
            temperature_sensor (str): temperature sensor of the heating radiator
            start_hour (int): ordinal of the first allowed electricity price slot to be consumed
            num_hours (int): the number of slots allowed
            spot_limit (float): maximum price allowed
        """
        super().__init__(name)

        self.heating_slots_per_day = num_hours * ( 3600 / self.energy_balancing_interval)
        self.start_slot = start_hour * (3600 / self.energy_balancing_interval)
        self.spot_limit = spot_limit

        self.topic_in_spot = self.make_topic_name("spot")
        self.topic_in_forecast = self.make_topic_name("forecast")
        self.topic_in_temperature = self.make_topic_name(temperature_sensor)
        self.topic_powerplan = self.make_topic_name("powerplan")
        self.topic_in_energybalance = self.make_topic_name("energybalance/status")
        self.topic_out_energybalance = self.make_topic_name("energybalance/consumers")
        self.topic_out_power = self.make_topic_name("power")

        self.current_temperature : float = 100.0
        self.current_relay_state : int = -1
        self.heating_plan: list[dict[str, int]] = [] # in slots
        self.power_plan: list[dict[str, Any]] = [] # in slots
        self.ranked_spot_prices: list[dict[Any, Any]] = [] 
        self.ranked_solarpower: list[dict[Any, Any]] = [] 
        self.relay: bool = False
        self.relay_started_ts: float = 0
        self.net_energy_balance_mode: bool = False
        self.next_day_mean_temp: float = 0.0
        self.next_day_solar_energy: float = 0.0
        self.min_temp : float = 0.0
        self.max_temp : float = 0.0
        self.new_power_plan: bool = True

    @override
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.topic_in_spot)
            self.subscribe(self.topic_in_forecast)
            self.subscribe(self.topic_in_temperature)
            self.subscribe(self.topic_in_energybalance)
            self.register_as_consumer()

    def is_slot_within_schedule(self, slot: int, start_slot: int, stop_slot: int) -> bool:
        """Check if the given slot is within the schedule.

        Args:
            slot (int): slot to check
            start_slot (int): start slot of the schedule
            stop_slot (int): stop slot of the schedule  
        Returns:
            bool: true if the slot is within the schedule
        """
        if start_slot < stop_slot:
            return slot >= start_slot and slot < stop_slot
        else:
            return slot >= start_slot or slot < stop_slot   
        

    def slots_per_day(self) -> int:
        return int(24 * 3600 / self.energy_balancing_interval)


    def timestamp_slot(self, ts: float) -> int:
        """Get the time slot for the given timestamp and interval.

        Args:
            ts (float): timestamp
            interval (float): interval in seconds
        
        Returns:
            float: time slot
        """
        dt = datetime.utcfromtimestamp(ts)
        total_seconds = dt.hour * 3600 + dt.minute * 60 + dt.second
        slot : int = total_seconds // self.energy_balancing_interval
        return slot


    def register_as_consumer(self) -> None:
        """Register this device as a consumer to the energy balancer. The energy balancer will then add 
        this device to its list of consumers and will tell the device when to heat."""

        consumer: dict[str, Any] = {
            "Unit": self.name,
            "Power": self.radiator_power,
            "Weight": self.balancing_weight,
        }
        self.publish(self.topic_out_energybalance, json.dumps(consumer), 1, False)
        self.info(
            f"Registered {self.name} as consumer with {self.radiator_power}W power",
            "",
        )

    def get_temperature_limits_for_current_month(self) -> tuple[float, float]:
        current_month: int = datetime.now().month
        # Get the min and max temperatures for the current month
        min_temp, max_temp = self.temperature_limits[current_month]
        return min_temp, max_temp


    def compute_optimal_temp(self,
        today_price: float,
        tomorrow_price: float,
        minTemp: float,
        maxTemp: float,
        k: float = 10.0,
        max_offset: float = 5.0,
    ) -> float:
        """ Computes an optimal boiler target temperature based on electricity price
        forecasts for today and tomorrow. The boiler is treated as a thermal 
        storage system: if electricity is cheaper today than tomorrow, the 
        controller increases the target temperature (preheating); if electricity 
        is cheaper tomorrow, the controller decreases the target temperature 
        (saving energy today).

        The adjustment is computed from the price ratio (tomorrow/today) using 
        a sensitivity coefficient `k`. The resulting temperature deviation is 
        clamped to `[-max_offset, +max_offset]` to ensure safe and stable 
        operation.

        Args:
            today_price (float): Average price of the cheapest relevant heating 
                window during the current day (0-24 hours ahead).
            tomorrow_price (float): Average price of the cheapest relevant 
                heating window for the next day (24-48 hours ahead).
            minTemp (float): Minimum allowed boiler temperature in degrees Celsius.
            maxTemp (float): Normal maximum boiler temperature in degrees Celsius.
            k (float, optional): Sensitivity factor controlling how strongly 
                the temperature reacts to price differences. Higher values 
                produce more aggressive adjustments. Defaults to 10.0.
            max_offset (float, optional): Maximum allowed degree offset applied 
                above or below `maxTemp`. Prevents overheating or excessive 
                underheating. Defaults to 5.0.

        Returns:
            float: The computed target temperature in degrees Celsius, clamped 
            within `[minTemp, maxTemp]`.

        Raises:
            ValueError: If input prices are non-positive or if temperature limits 
                are inconsistent.

        """

        price_ratio = tomorrow_price / max(0.001, today_price)

        # Positive if tomorrow is more expensive
        adjustment = k * (price_ratio - 1.0)

        # Clamp to +/- max_offset degrees
        adjustment = max(-max_offset, min(max_offset, adjustment))

        # New temperature target
        T_target = maxTemp + adjustment

        # Clamp to allowed boiler range
        T_target = max(minTemp, min(maxTemp, T_target))

        return T_target


    def get_forecast_optimized_temperature_limits(self) -> tuple[float, float]:
        """Get the forecast optimized temperature limits for the current heating plan.
        Returns: tuple: (min_temp, max_temp)
        """

        # get the monthly temperature limits
        min_temp, max_temp = self.get_temperature_limits_for_current_month()
        if not self.ranked_solarpower or len(self.ranked_solarpower) < 4:
            self.warning(
                f"{self.name} short forecast {len(self.ranked_solarpower)}, no forecast optimization applied.",
                "",
            )
            return min_temp, max_temp

        return self.calculate_target_temps(
            min_temp, max_temp, self.next_day_mean_temp, self.target_home_temperature)


    def sort_by_rank(
        self, slot: list[dict[str, Any]], ts_utc_now: float
    ) -> list[dict[str, Any]]:
        """Sort the given electricity prices by their rank value. Given a list
        of electricity prices, return a sorted list from the cheapest to the
        most expensive hours. Entries that represent electricity prices in the
        past are excluded.

        Args:
            hours (list): list of hourly electricity prices
            ts_utc_now (float): current time

        Returns:
            list: sorted list of electricity prices
        """
        sh = sorted(slot, key=lambda x: x["Rank"])
        ranked_hours: list[dict[str, Any]] = []
        for h in sh:
            utc_ts = h["Timestamp"]
            if utc_ts >= ts_utc_now:
                ranked_hours.append(h)

        return ranked_hours

    def sort_by_power(
        self, forecast: list[dict[Any, Any]], ts_utc: float
    ) -> list[dict[Any, Any]]:
        """Sort forecast of solarpower to decreasing order.

        Args:
            solarpower (list): list of entries describing hourly solar energy forecast
            ts_utc(float): start time, for exluding entries that are in the past

        Returns:
            list: list from the highest solarenergy to lowest.
        """

        # if all items have solarenergy key then
        # sh = sorted(solarpower, key=lambda x: x["solarenergy"], reverse=True)
        # else skip items that don't have solarenergy key
        sh = sorted(
            [item for item in forecast if "solarenergy" in item],
            key=lambda x: x["solarenergy"],
            reverse=True,
        )
       
        self.debug(
            f"{self.name} sorted {len(sh)} days of forecast starting at {timestampstr(ts_utc)}"
        )
        ranked_slots: list[dict[str, Any]] = []

        for h in sh:
            utc_ts: float = float(h["ts"])
            if utc_ts >= ts_utc:
                ranked_slots.append(h)
        self.debug(
            f"{self.name} forecast sorted for the next {str(len(ranked_slots))} hours"
        )
        return ranked_slots


    def next_day_mean_temperature_forecast(self, forecast: list[dict[Any, Any]], ts_utc: float)  -> float:
        """return the average temperature for the next day based on the forecast.
         
        Args:
            forecast (list): list of entries describing hourly solar energy forecast
            ts_utc(float): start time, for exluding entries that are in the past

        Returns:
            list: list from the highest solarenergy to lowest.
        """
        total_temp: float = 0.0
        count: int = 0
        for item in forecast:
            utc_ts: float = float(item["ts"])
            if utc_ts >= ts_utc and "temp" in item:
                total_temp = total_temp + item["temp"]
                count = count + 1
        average_temp : float = total_temp / count if count > 0 else 0
        return average_temp

    def next_day_solar_energy_forecast(self, forecast: list[dict[Any, Any]], ts_utc: float)  -> float:
        """Compute the expected solar energy based on the forecast. The more solar energy is expected
        the more the heating can be allowed to lower temperatures.
         
        Args:
            forecast (list): list of entries describing solar energy forecast
            ts_utc(float): start time, for exluding entries that are in the past

        Returns:
            list: expected solarenergy available during the heating period.
        """
        total_energy: float = 0.0
        solarenergy_found: bool = False
        for item in forecast:
            if "solarenergy" in item:
                solarenergy_found = True
                utc_ts: float = float(item["ts"])
                if utc_ts >= ts_utc:
                    total_energy = total_energy + item["solarenergy"]
        
        if not solarenergy_found:
            self.debug(f"No solarenergy forecast found")
        else:
            self.debug(f"Next day solar energy forecast is {total_energy:.1f} W")
        return total_energy


    def get_future_price(
        self,
        ts_utc_now: float,
        num_hours: float,
        start_hour: float,
        stop_hour: float,
    ) -> float:
        slots_needed = int(num_hours * 4)
        seconds_per_hour = 3600

        window_start_ts = ts_utc_now + start_hour * seconds_per_hour
        window_stop_ts = ts_utc_now + stop_hour * seconds_per_hour

        window_slots = [
            s for s in self.ranked_spot_prices
            if window_start_ts <= s["Timestamp"] < window_stop_ts
        ]

        # already sorted by rank, so just take the first N
        selected = window_slots[:slots_needed]

        if not selected:
            return float("nan")

        return sum(s["PriceWithTax"] for s in selected) / len(selected)


    def on_spot(self, m: list[dict[str, Any]], ts_quantized: float) -> None:
        """Handle the spot prices.

        Args:
            list[dict[str, Any]]: list of spot prices
            ts_quantized (float): current time
        """
        self.spot_prices = m
        self.ranked_spot_prices = self.sort_by_rank(m, ts_quantized)

    def on_forecast(
        self, forecast: list[dict[str, Any]], ts_utc_quantized: float
    ) -> None:
        """Handle the solar forecast.

        Args:
            m (list[dict[str, Any]]): list of forecast prices
            ts_quantized (float): current time
        """
        # reject forecasts that don't have solarenergy key
        for f in forecast:
            if not "solarenergy" in f:
                return

        self.ranked_solarpower = self.sort_by_power(forecast, ts_utc_quantized)
        if(len(self.ranked_solarpower)) == 0:
            self.warning(f"{self.name} no valid solar power forecast received")
            return

        self.info(
            f"{self.name} solar energy forecast received and ranked for {len(self.ranked_solarpower)} slots"
        )
        self.power_plan = []  # reset power plan, it depends on forecast
        self.next_day_mean_temp = self.next_day_mean_temperature_forecast(forecast, time.time() + 24 * 60 * 60)
        self.next_day_solar_energy = self.next_day_solar_energy_forecast(forecast, time.time() + 24 * 60 * 60)  
        self.new_power_plan = True
        self.min_temp, self.max_temp = self.get_forecast_optimized_temperature_limits()

        self.info(
            f"{self.name} Next day temp and solar forecasts are {self.next_day_mean_temp:.1f}°C and {self.next_day_solar_energy:.1f}°kW"
        )

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        m = None
        ts: float = timestamp()
        ts_utc_quantized: float = quantize(self.energy_balancing_interval, ts - self.energy_balancing_interval)
        if msg.topic == self.topic_in_spot:
            self.on_spot(json.loads(msg.payload.decode()), ts_utc_quantized)
            return
        elif msg.topic == self.topic_in_forecast:
            self.on_forecast(json.loads(msg.payload.decode()), ts_utc_quantized)
            return
        elif msg.topic == self.topic_in_temperature:
            m = json.loads(msg.payload.decode())
            self.current_temperature = m["temperature"]
        elif msg.topic == self.topic_in_energybalance:
            decoded_payload = msg.payload.decode()
            m = json.loads(decoded_payload)
            self.on_netenergy_balance(m)
        else:
            super().on_message(client, userdata, msg)
            return
        self.on_powerplan(ts)

    def on_powerplan(self, ts_utc_now: float) -> None:
        """Apply the power plan. Check if the relay needs to be switched on or off.
        The relay is switched on if the current temperature is below the maximum
        temperature and the current time is within the heating plan. The relay is switched off
        if the current temperature is above the maximum temperature or the current time is outside.

        Args:
            ts_utc_now (float): utc time
        """

        # optimization, check only once a minute
        elapsed: float = ts_utc_now - self.relay_started_ts
        if elapsed < 60:
            return
        self.relay_started_ts = ts_utc_now

        if not self.ranked_spot_prices:
            self.debug(f"{self.name} waiting  spot prices...", "")
            return

        if not self.power_plan:
            self.power_plan = self.create_power_plan()
            self.heating_plan = []
            self.info(
                f"{self.name} power plan of length {len(self.power_plan)} created",
                str(self.power_plan),
            )

        if not self.power_plan:
            self.error(f"{self.name} failed to create a power plan", "")
            return

        if len(self.power_plan) < 3:
            self.warning(
                f"{self.name} has suspiciously short {len(self.power_plan)}  power plan, waiting for more data ..",
                "",
            )
            self.heating_plan = []
            self.power_plan = []
            return

        if not self.ranked_solarpower or len(self.ranked_solarpower) < 4:
            self.warning(
                f"{self.name} short of forecast {len(self.ranked_solarpower)}, optimization compromised..",
                "",
            )

        if not self.heating_plan:
            self.heating_plan = self.create_heating_plan()
            if not self.heating_plan:
                self.error(f"{self.name} failed to create heating plan")
                return
            else:
                self.info(
                    f"{self.name} heating plan of length {len(self.heating_plan)} created",
                    "",
                )

        self.publish_heating_plan(self.heating_plan)

        if len(self.heating_plan) < 3:
            self.warning(
                f"{self.name} has too short heating plan {len(self.heating_plan)}, no can do",
                "",
            )
            self.heating_plan = []
            self.power_plan = []
            return

        relay: int = self.consider_heating(ts_utc_now)
        if self.current_relay_state != relay:
            heat: dict[str, Any] = {
                "Unit": self.name,
                "Timestamp": ts_utc_now,
                "State": relay,
            }
            self.publish(self.topic_out_power, json.dumps(heat), 1, False)
            self.info(
                f"{self.name} relay changed to {relay} at {timestampstr(ts_utc_now)}",
                "",
            )
            self.current_relay_state = relay

    def on_netenergy_balance(self, m: dict[str, Any]) -> None:
        """Check when there is enough energy available for the radiator to heat
        in the remaining time within the balancing interval.

        Args:
            ts (float): current time

        Returns:
            bool: true if production exceeds the consumption
        """
        if m["Unit"] == self.name:
            self.net_energy_balance_mode = m["Mode"]

    def consider_heating(self, ts: float) -> int:
        """Consider whether the target boiler needs heating. Check first if the solar
        energy is enough to heat the water the remaining time in the current slot.
        If not, follow the predefined heating plan computed earlier based on the cheapest spot prices.

        Args:
            ts (float): current UTC time

        Returns:
            int: 1 if heating is needed, 0 if not
        """

        # check if we have excess energy to spent within the current slot
        if self.net_energy_balance_mode:
            return 1

        slot : int = self.timestamp_slot(ts)
        state: int = -1

        # check if we are within the heating plan and see what the plan says
        for pp in self.heating_plan:
            ppts: float = pp["Timestamp"]
            h: float = self.timestamp_slot(ppts)
            if h == slot:
                state = pp["State"]
                break

        if state == -1:
            self.error(f"{self.name} cannot find heating plan for slot {slot}")
            return 0

        # don't heat if the current temperature is already high enough
        if self.current_temperature > self.max_temp:
            return 0
        #  heat if the current temperature is below the required minimum
        if self.current_temperature < self.min_temp:
            return 1

        return state  # 1 = heating, 0 = not heating

    # compute utilization optimization index
    def compute_uoi(
        self,
        price: float,
        slot: float,
    ) -> float:
        """Compute UOI - utilization optimization index.

        Args:
            price (float): effective price for this device
            slot  (float) : the slot of the day

        Returns:
            float: utilization optimization index
        """

        if not self.is_slot_within_schedule(
            slot, self.schedule_start_slot, self.schedule_stop_slot
        ):
            return 0.0

        if price < 0.0001:
            return 1.0  # use
        elif price > self.expected_average_price:
            return 0.0  # try not to use
        else:
            fom = self.expected_average_price / price
            return fom

    def compute_effective_price(
        self, requested_power: float, available_solpower: float, spot: float
    ) -> float:
        """Compute effective electricity price. If there is enough solar power then
        electricity price is zero.

        Args:
            requested_power (float): requested power
            available_solpower (float): current solar power forecast
            spot (float): spot price

        Returns:
            float: effective price for the requested power
        """

        # if we have enough solar power, use it
        if requested_power < available_solpower:
            return 0.0

        # check how  much of the power is solar and how much is from the grid
        solar_factor: float = available_solpower / requested_power

        effective_spot: float = spot * (1 - solar_factor)

        return effective_spot

    def align_forecast_to_slots(self, solar_forecast: list[dict]) -> list[dict]:
        """Resample hourly solar forecast to match slot interval."""
        slots_per_hour = 3600 // self.energy_balancing_interval
        expanded = []

        for entry in solar_forecast:  # each entry has "ts" (start of hour) and "solarenergy" (in kW)
            start_ts = entry["Timestamp"]
            for i in range(slots_per_hour):
                slot_ts = start_ts + i * self.energy_balancing_interval
                expanded.append({
                    "Timestamp": slot_ts,
                    "Solarenergy": entry["Solarenergy"] / slots_per_hour  # split evenly
                })

        return expanded


    def create_power_plan(self) -> list[dict[Any, Any]]:
        """Create power plan.

        Returns:
            list: list of utilization entries
        """
        ts_utc_quantized = quantize(self.energy_balancing_interval, timestamp() - self.energy_balancing_interval)
        starts: str = timestampstr(ts_utc_quantized)
        self.info(
            f"{self.name} created power plan starting at {starts} with {len(self.ranked_spot_prices)} slots of spot prices",
            "",
        )

        # syncronize spot and solarenergy by timestamp
        spots: list[dict[Any, Any]] = []
        for s in self.ranked_spot_prices:
            if s["Timestamp"] > ts_utc_quantized:
                spots.append(
                    {"Timestamp": s["Timestamp"], "PriceWithTax": s["PriceWithTax"]}
                )

        if len(spots) == 0:
            self.info(
                f"No spot prices initialized yet, can't proceed",
                "",
            )
            return []
        self.info(
            f"Have spot prices for the next {len(spots)} slots",
            "",
        )

        # Expand solar forecast to match spot price resolution
        raw_powers = [
            {"Timestamp": s["ts"], "Solarenergy": s["solarenergy"]}
            for s in self.ranked_solarpower
            if s["ts"] >= ts_utc_quantized
        ]

        powers : list[dict[str, Any]]  = self.align_forecast_to_slots(raw_powers)


        num_powers: int = len(powers)
        if num_powers == 0:
            self.debug(
                f"No solar forecast initialized yet, proceed without solar forecast",
                "",
            )
        else:
            self.debug(
                f"Have solar forecast  for the next {num_powers} slots",
                "",
            )
        hplan: list[dict[str, Any]] = []
        slot: int = 0
        if len(powers) >= 8:  # at least 8 slot of solar energy forecast
            for spot, solar in zip(spots, powers):
                ts = spot["Timestamp"]
                solarenergy = solar["Solarenergy"] * 1000  # argh, this is in kW
                spotprice = spot["PriceWithTax"]
                effective_price: float = self.compute_effective_price(
                    self.radiator_power, solarenergy, spotprice
                )
                slot = self.timestamp_slot(ts)
                fom = self.compute_uoi(spotprice, slot)
                plan: dict[str, Any] = {
                    "Timestamp": ts,
                    "FOM": fom,
                    "Spot": effective_price,
                }
                hplan.append(plan)
        else:  # no solar forecast available, assume no free energy available
            for spot in spots:
                ts = spot["Timestamp"]
                solarenergy = 0.0
                spotprice = spot["PriceWithTax"]
                effective_price = spotprice  # no free energy available
                slot = self.timestamp_slot(ts)
                fom = self.compute_uoi(effective_price, slot)
                plan = {
                    "Timestamp": spot["Timestamp"],
                    "FOM": fom,
                    "Spot": effective_price,
                }
                hplan.append(plan)

        shplan = sorted(hplan, key=lambda x: x["FOM"], reverse=True)

        self.debug(f"{self.name} powerplan starts {starts} up to {len(shplan)} slots")
        return shplan


    def calculate_target_temps(self,
        monthly_temp_min: float,
        monthly_temp_max: float,
        next_day_mean_temp: float,
        target_temperature: float
    ) -> tuple[float, float]:
        """
        Calculates the minimum and maximum target temperatures for the current heating plan, 
        blending the fixed monthly limits with the next day's forecast.

        The minimum temperature is fixed at the monthly minimum, as the system 
        must always prevent the temperature from dropping below this threshold.

        The maximum temperature is adjusted based on the predicted heating demand 
        derived from the forecast and scaled by the next_day_factor.

        Args:
            monthly_temp_min (float): The default, absolute minimum boiler temperature (e.g., 60°C).
            monthly_temp_max (float): The default, absolute maximum boiler temperature (e.g., 85°C).
            next_day_mean_temp (float): The average temperature forecasted for tomorrow (e.g., 5°C).
            target_temperature (float): The internal/reference temperature used to 
                determine the heating required for the next day (e.g., 20°C).

        Returns:
            tuple[float, float]: (min_temp_today, max_temp_today)
        """

        # Ensure the factor is within valid bounds
        factor = max(0.0, min(1.0, self.next_day_factor))

        # --- 2. Calculate Required Heating Need based on Forecast ---
        # Calculate the raw heating demand proxy: (Baseline - Forecast)
        # The greater this difference, the colder the next day, and the more energy (higher max temp) is needed today.
        # We use max(0, ...) to ensure demand is not negative if the forecast is warmer than the target.
        demand_difference = max(0.0, target_temperature - next_day_mean_temp)

        # Normalize the demand difference into a 0.0 to 1.0 'Need Ratio'
        # 0.0 = No extra heating needed (warm forecast)
        # 1.0 = Maximal heating needed (very cold forecast)
        need_ratio = min(1.0, demand_difference / self.max_expected_temp_difference)

        # --- 3. Determine the Forecast-Driven Target Max Temperature ---
        # The available range for heating capacity
        boiler_range = monthly_temp_max - monthly_temp_min

        # Calculate the max temperature required based purely on the forecast (if factor=1)
        # If need_ratio is 1.0, T_max_target = monthly_temp_max
        # If need_ratio is 0.0, T_max_target = monthly_temp_min
        T_max_target = monthly_temp_min + (need_ratio * boiler_range)

        # --- 4. Apply the Blending Factor ---
        # The minimum temperature remains fixed (no drop below the minimum limit)
        min_temp_today = monthly_temp_min

        # The max temperature is a blend:
        # (factor * T_max_target) + ((1 - factor) * monthly_temp_max)
        # factor = 1 -> uses T_max_target (full forecast impact)
        # factor = 0 -> uses monthly_temp_max (full monthly default capacity)
        max_temp_today = (factor * T_max_target) + ((1 - factor) * monthly_temp_max)



        # adjust the temperature limits based on the electricity prices
        ts : float = timestamp()
        num_hours : float = self.heating_slots_per_day * self.energy_balancing_interval / 3600.0
        tomorrow_price : float = self.get_future_price(ts, num_hours, 24, 48)
        today_price : float = self.get_future_price(ts, num_hours, 0,24)
        if math.isnan(tomorrow_price) or math.isnan(today_price):
            self.warning(f"{self.name} no future prices for temperature optimization, using unadjusted temps", 
                         f"min:{min_temp_today}, max:{max_temp_today}")
            return (min_temp_today, max_temp_today) 
        spot_adjusted_max : float = self.compute_optimal_temp(today_price, tomorrow_price, min_temp_today, max_temp_today, 
                                                          self.spot_sensitivity, self.spot_temp_offset)
        # Return the results
        return (min_temp_today, spot_adjusted_max)


    def enable_relay(
        self, slot: int, spot: float, fom: float, end_slot: int
    ) -> bool:
        return (
            slot >= self.start_slot
            and slot < end_slot
            and float(spot) < self.spot_limit
            and fom > self.uoi_threshold
        )

    def create_heating_plan(self) -> list[dict[str, Any]]:
        """Create heating plan.

        Returns:
            int: list[dict[str, Any]] of heating entries
        """

        state = 0
        heating_plan: list[dict[str, Any]] = []
        slot: int = 0
        for hp in self.power_plan:
            ts: float = hp["Timestamp"]
            fom = hp["FOM"]
            spot = hp["Spot"]
            end_slot: float = self.start_slot + self.heating_slots_per_day
            slot: float = self.timestamp_slot(ts)
            schedule_on: bool = self.is_slot_within_schedule(
                slot, self.schedule_start_slot, self.schedule_stop_slot
            )

            if self.enable_relay(slot, spot, fom, end_slot) and schedule_on:
                state = 1
            else:
                state = 0
            heat: dict[str, Any] = {
                "Unit": self.name,
                "Timestamp": ts,
                "State": state,
                "Schedule": schedule_on,
                "UOI": fom,
                "Spot": spot,
            }

            heating_plan.append(heat)
            slot = slot + 1

        self.info(f"{self.name} heating plan of {len(heating_plan)} slots created", "")
        return heating_plan


    def publish_heating_plan(self, heatingplan : list[dict[str, Any]]) -> None:
        """Publish the heating plan. If new heating plan, then publish also the next day's
        solar energy and temperature forecasts along with the min and max temperature limits.
    
        Args:
            heatingplan: list of heating entries
        """

        hplen : int = len(heatingplan)
        for index, hp in enumerate(heatingplan):
            if index == 0 or index >= hplen-1:
                hp_to_publish = hp.copy() 
                hp_to_publish["NextDaySolarpower"] = self.next_day_solar_energy
                hp_to_publish["NextDayTemperature"] = self.next_day_mean_temp
                hp_to_publish["MinTempLimit"] = self.min_temp
                hp_to_publish["MaxTempLimit"] = self.max_temp
            
                self.publish(self.topic_powerplan, json.dumps(hp_to_publish), 1, False)
                self.new_power_plan = False # Should be set here when metadata is sent
            else:
                self.publish(self.topic_powerplan, json.dumps(hp), 1, False)

