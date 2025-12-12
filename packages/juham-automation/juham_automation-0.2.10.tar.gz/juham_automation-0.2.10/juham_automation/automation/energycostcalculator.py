from typing import Any
from typing_extensions import override
import json
from masterpiece.mqtt import MqttMsg
from juham_core import Juham
from juham_core.timeutils import (
    elapsed_seconds_in_day,
    elapsed_seconds_in_hour,
    elapsed_seconds_in_interval,
    quantize,
    timestamp,
)


class EnergyCostCalculator(Juham):
    """The EnergyCostCalculator class calculates the net energy balance and cost between produced
    (or consumed) energy for Time-Based Settlement (TBS). It performs the following functions:

    * Subscribes to 'spot' and 'power' MQTT topics.
    * Calculates the net energy and the rate of change of the net energy per hour and per day (24h)
    * Calculates the cost of energy consumed/produced based on the spot prices.
    * Publishes the calculated values to the MQTT net energy balance and cost topics.


    This information helps other home automation components optimize energy usage and
    minimize electricity bills.
    """

    _kwh_to_joule_coeff: float = 1000.0 * 3600
    _joule_to_kwh_coeff: float = 1.0 / _kwh_to_joule_coeff

    energy_balancing_interval: int = 900 # in seconds (15 minutes)

    def __init__(self, name: str = "ecc") -> None:
        super().__init__(name)
        self.current_ts: float = 0
        self.total_balance_interval : float = 0
        self.total_balance_hour: float = 0
        self.total_balance_day: float = 0
        self.net_energy_balance_cost_interval: float = 0
        self.net_energy_balance_cost_hour: float = 0
        self.net_energy_balance_cost_day: float = 0
        self.net_energy_balance_start_interval : float = elapsed_seconds_in_interval(timestamp(), self.energy_balancing_interval)
        self.net_energy_balance_start_hour : float = elapsed_seconds_in_hour(timestamp())
        self.net_energy_balance_start_day : float = elapsed_seconds_in_day(timestamp())
        self.spots: list[dict[str, float]] = []
        self.init_topics()

    def init_topics(self) -> None:
        self.topic_in_spot = self.make_topic_name("spot")
        self.topic_in_powerconsumption = self.make_topic_name("powerconsumption")
        self.topic_out_net_energy_balance = self.make_topic_name("net_energy_balance")
        self.topic_out_energy_cost = self.make_topic_name("net_energy_cost")

    @override
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.topic_in_spot)
            self.subscribe(self.topic_in_powerconsumption)

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        ts_now = timestamp()

        m = json.loads(msg.payload.decode())
        if msg.topic == self.topic_in_spot:
            self.on_spot(m)
        elif msg.topic == self.topic_in_powerconsumption:
            self.on_powerconsumption(ts_now, m)
        else:
            super().on_message(client, userdata, msg)

    def on_spot(self, spot: dict[Any, Any]) -> None:
        """Stores the received per slot electricity prices to spots list.

        Args:
            spot (list): list of spot prices
        """

        for s in spot:
            self.spots.append(
                {"Timestamp": s["Timestamp"], "PriceWithTax": s["PriceWithTax"]}
            )

    def map_kwh_prices_to_joules(self, price: float) -> float:
        """Convert the given electricity price in kWh to Watt seconds (J)
        Args:
            price (float): electricity price given as kWh
        Returns:
            Electricity price per watt second (J)
        """
        return price * self._joule_to_kwh_coeff


    def get_price_at(self, ts: float) -> float:
        """Return the spot price applicable at the given timestamp.

        Args:
            ts (float): current time (epoch seconds)

        Returns:
            float: PriceWithTax for the slot that contains ts. Returns the last
                known price if ts is equal/after the last spot timestamp.
                Returns 0.0 and logs an error if no matching slot is found.
        """
        if not self.spots:
            self.error(f"PANIC: no spot prices available; lookup ts={ts}")
            return 0.0

        # ensure spots sorted by timestamp (defensive)
        try:
            # cheap check — assumes list of dicts with "Timestamp"
            if any(self.spots[i]["Timestamp"] > self.spots[i + 1]["Timestamp"] for i in range(len(self.spots) - 1)):
                self.spots.sort(key=lambda r: r["Timestamp"])
        except Exception:
            # if unexpected structure, still try safe path below and log
            self.debug("get_price_at: spot list structure unexpected while checking sort order", "")

        for i in range(0, len(self.spots) - 1):
            r0 = self.spots[i]
            r1 = self.spots[i + 1]
            ts0 = r0["Timestamp"]
            ts1 = r1["Timestamp"]
            if ts >= ts0 and ts < ts1:
                return r0["PriceWithTax"]

        # If timestamp is exactly equal to the last spot timestamp or beyond
        last = self.spots[-1]
        if ts >= last["Timestamp"]:
            return last["PriceWithTax"]

        # If we get here, ts is before the first spot timestamp
        first = self.spots[0]
        self.error(
            f"PANIC: Timestamp {ts} out of bounds for spot price lookup; "
            f"first=(ts={first['Timestamp']}, price={first.get('PriceWithTax')}), "
            f"last=(ts={last['Timestamp']}, price={last.get('PriceWithTax')}), "
            f"len(spots)={len(self.spots)}"
        )
        return 0.0



    def calculate_net_energy_cost(
        self, ts_prev: float, ts_now: float, energy: float
    ) -> float:
        """
        Calculate the cost (or revenue) of energy consumed/produced over the given time interval.
        Positive values indicate revenue, negative values indicate cost.

        Args:
            ts_prev (float): Start timestamp of the interval
            ts_now (float): End timestamp of the interval
            energy (float): Energy consumed during the interval (in watts or Joules)

        Returns:
            float: Total cost/revenue for the interval
        """
        cost = 0.0
        current = ts_prev
        interval = self.energy_balancing_interval

        while current < ts_now:
            next_ts = min(ts_now, current + interval)
            # Get spot price at start and end of interval
            price_start = self.map_kwh_prices_to_joules(self.get_price_at(current))
            price_end = self.map_kwh_prices_to_joules(self.get_price_at(next_ts))

            # Trapezoidal integration: average price over interval
            avg_price = (price_start + price_end) / 2.0
            dt = next_ts - current
            cost += energy * avg_price * dt

            current = next_ts

        return cost


    def on_powerconsumption(self, ts_now: float, m: dict[Any, Any]) -> None:
        """Calculate net energy cost and update the hourly consumption attribute
        accordingly.

        Args:
           ts_now (float): time stamp of the energy consumed
           m (dict): Juham MQTT message holding energy reading
        """
        power = m["real_total"]
        if not self.spots:
            self.info("Waiting for electricity prices...")
        elif self.current_ts == 0:
            self.net_energy_balance_cost_interval = 0.0
            self.net_energy_balance_cost_hour = 0.0
            self.net_energy_balance_cost_day = 0.0
            self.current_ts = ts_now
            self.net_energy_balance_start_interval = quantize(
                self.energy_balancing_interval, ts_now
            )
            self.net_energy_balance_start_hour = quantize(
                3600, ts_now
            )
        else:
            # calculate cost of energy consumed/produced
            dp: float = self.calculate_net_energy_cost(self.current_ts, ts_now, power)
            self.net_energy_balance_cost_interval = self.net_energy_balance_cost_interval + dp
            self.net_energy_balance_cost_hour = self.net_energy_balance_cost_hour + dp
            self.net_energy_balance_cost_day = self.net_energy_balance_cost_day + dp

            # calculate and publish energy balance
            dt = ts_now - self.current_ts  # time elapsed since previous call
            balance = dt * power  # energy consumed/produced in this slot in Joules
            self.total_balance_interval = (
                self.total_balance_interval + balance * self._joule_to_kwh_coeff
            )
            self.total_balance_hour = (
                self.total_balance_hour + balance * self._joule_to_kwh_coeff
            )
            self.total_balance_day = (
                self.total_balance_day + balance * self._joule_to_kwh_coeff
            )
            self.publish_net_energy_balance(ts_now, self.name, balance, power)
            self.publish_energy_cost(
                ts_now,
                self.name,
                self.net_energy_balance_cost_interval,
                self.net_energy_balance_cost_hour,
                self.net_energy_balance_cost_day,
            )

            # Check if the current energy balancing interval has ended
            # If so, reset the net_energy_balance attribute for the next interval
            if ts_now - self.net_energy_balance_start_interval > self.energy_balancing_interval:
                # publish average energy cost per hour
                if abs(self.total_balance_interval) > 0:
                    msg = {
                        "name": self.name,
                        "average_interval": self.net_energy_balance_cost_interval
                        / self.total_balance_interval,
                        "ts": ts_now,
                    }
                    self.publish(self.topic_out_energy_cost, json.dumps(msg), 0, False)

                # reset for the next hour
                self.total_balance_interval = 0
                self.net_energy_balance_cost_interval = 0.0
                self.net_energy_balance_start_interval = ts_now

            # Check if the current energy balancing interval has ended
            # If so, reset the net_energy_balance attribute for the next interval
            if ts_now - self.net_energy_balance_start_hour > 3600:
                # publish average energy cost per hour
                if abs(self.total_balance_hour) > 0:
                    msg = {
                        "name": self.name,
                        "average_hour": self.net_energy_balance_cost_hour
                        / self.total_balance_hour,
                        "ts": ts_now,
                    }
                    self.publish(self.topic_out_energy_cost, json.dumps(msg), 0, False)

                # reset for the next hour
                self.total_balance_hour = 0
                self.net_energy_balance_cost_hour = 0.0
                self.net_energy_balance_start_hour = ts_now

            if ts_now - self.net_energy_balance_start_day > 24 * 3600:
                if abs(self.total_balance_day) > 0:
                    msg = {
                        "name": self.name,
                        "average_day": self.net_energy_balance_cost_day
                        / self.total_balance_day,
                        "ts": ts_now,
                    }
                    self.publish(self.topic_out_energy_cost, json.dumps(msg), 0, False)
                # reset for the next day
                self.total_balance_day = 0
                self.net_energy_balance_cost_day = 0.0
                self.net_energy_balance_start_day = ts_now

            self.current_ts = ts_now

    def publish_net_energy_balance(
        self, ts_now: float, site: str, energy: float, power: float
    ) -> None:
        """Publish the net energy balance for the current energy balancing interval, as well as
        the real-time power at which energy is currently being produced or consumed (the
        rate of change of net energy).

        Args:
            ts_now (float): timestamp
            site (str): site
            energy (float): cost or revenue.
            power (float) : momentary power (rage of change of energy)
        """
        msg = {"site": site, "power": power, "energy": energy, "ts": ts_now}
        self.publish(self.topic_out_net_energy_balance, json.dumps(msg), 1, True)

    def publish_energy_cost(
        self, ts_now: float, site: str, cost_interval : float, cost_hour: float, cost_day: float
    ) -> None:
        """Publish daily, hourly and per interval energy cost/revenue

        Args:
            ts_now (float): timestamp
            site (str): site
            cost_hour (float): cost or revenue per hour.
            cost_day (float) : cost or revenue per day
        """
        msg = {"name": site, "cost_interval": cost_interval, "cost_hour": cost_hour, "cost_day": cost_day, "ts": ts_now}
        self.publish(self.topic_out_energy_cost, json.dumps(msg), 1, True)
