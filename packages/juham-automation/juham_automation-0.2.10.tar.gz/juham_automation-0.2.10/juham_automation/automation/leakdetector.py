"""
Leak Detector based on Motion Detection and Water Meter Monitoring.

This class listens to water meter and motion sensor topics to detect potential water leaks.
If a leak is detected, the system triggers a leak alarm.
"""
import json
from datetime import datetime
from typing import Any
from typing_extensions import override
from masterpiece.mqtt import MqttMsg
from juham_core.timeutils import timestamp
from juham_core import Juham


class LeakDetector(Juham):
    """
    Water Leak Detector Class

    Listens to water meter and motion sensor topics to identify potential water leaks.
    If water consumption is detected without corresponding motion, or if water usage
    remains constant for prolonged periods, a leak alarm is triggered.

    Detection considers the time since the last motion detection and compares it to
    the configured leak detection period, which is the maximum runtime of water-consuming
    appliances.
    """

    _LEAKDETECTOR: str = "leakdetector"
    _LEAKDETECTOR_ATTRS: list[str] = [
        "watermeter_topic",
        "motion_topic",
        "motion_last_detected_ts",
    ]

    watermeter_topic: str = "watermeter"
    motion_topic: str = "motion"
    leak_detection_period: float = (
        3 * 3600.0
    )  # Maximum runtime for appliances, in seconds
    location: str = "home"
    conseq_zero_periods: int = (
        60  # this many subsequent zero flow reports imply no leak
    )

    def __init__(self, name: str = "leakdetector") -> None:
        """
        Initialize the leak detector.

        Args:
            name (str, optional): Name of the detector instance. Defaults to "leakdetector".
        """
        super().__init__(name)
        self.motion_last_detected_ts: float = timestamp()
        self.watermeter_full_topic: str = self.make_topic_name(self.watermeter_topic)
        self.motion_full_topic: str = self.make_topic_name(self.motion_topic)
        self.leak_detected: bool = False
        self.zero_usage_periods_count: int = 0

    @override
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        """
        Handle MQTT connection. Subscribe to water meter and motion topics.
        """
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.watermeter_full_topic)
            self.subscribe(self.motion_full_topic)

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        """
        Process incoming MQTT messages for water meter and motion topics.
        """
        payload = json.loads(msg.payload.decode())
        if msg.topic == self.watermeter_full_topic:
            self.process_water_meter_data(payload)
        elif msg.topic == self.motion_full_topic:
            self.process_motion_data(payload)
        else:
            super().on_message(client, userdata, msg)

    def detect_activity(self, current_ts: float) -> bool:
        """
        Check if activity (motion) has been detected within the leak detection period.

        Args:
            current_ts (float): Current timestamp.

        Returns:
            bool: True if activity detected within the period, False otherwise.
        """
        elapsed_time = current_ts - self.motion_last_detected_ts
        return elapsed_time < self.leak_detection_period

    def publish_leak_status(self, current_ts: float, leak_suspected: bool) -> None:
        """
        Publish the leak detection status.

        Args:
            current_ts (float): Current timestamp.
            leak_suspected (bool): Whether a leak is suspected.
        """
        status : dict[str, Any] = {
            "location": self.location,
            "sensor": self.name,
            "leak_suspected": leak_suspected,
            "ts": current_ts,
        }
        payload = json.dumps(status)
        self.publish(self.watermeter_full_topic, payload, qos=1, retain=False)

    def process_water_meter_data(self, data: dict[str, float]) -> None:
        """
        Handle water meter data and apply leak detection logic.

        Args:
            data (dict): Water meter data containing flow rate and timestamp.
        """
        if "active_lpm" in data and "ts" in data:
            flow_rate = data["active_lpm"]
            current_ts = data["ts"]

            if flow_rate > 0.0:
                if not self.detect_activity(current_ts):
                    if not self.leak_detected:
                        self.leak_detected = True
                        readable :str = datetime.fromtimestamp(self.motion_last_detected_ts).strftime("%Y-%m-%d %H:%M:%S")
                        self.warning(f"LEAK SUSPECT", f"Flow {flow_rate} lpm, last detected motion {readable}")

                self.zero_usage_periods_count = 0
            else:
                self.zero_usage_periods_count += 1
                if self.zero_usage_periods_count > self.conseq_zero_periods:
                    self.leak_detected = False
                    self.motion_last_detected_ts = current_ts
            self.publish_leak_status(current_ts, self.leak_detected)

    def process_motion_data(self, data: dict[str, float]) -> None:
        """
        Update the last detected motion timestamp.

        Args:
            data (dict): Motion sensor data containing timestamp.
        """
        if "motion" in data and data["motion"]:
            self.motion_last_detected_ts = data["ts"]

    @override
    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        attributes = {attr: getattr(self, attr) for attr in self._LEAKDETECTOR_ATTRS}
        data[self._LEAKDETECTOR] = attributes
        return data

    @override
    def from_dict(self, data: dict[str, Any]) -> None:
        super().from_dict(data)
        if self._LEAKDETECTOR in data:
            attributes = data[self._LEAKDETECTOR]
            for attr in self._LEAKDETECTOR_ATTRS:
                setattr(self, attr, attributes.get(attr, None))
