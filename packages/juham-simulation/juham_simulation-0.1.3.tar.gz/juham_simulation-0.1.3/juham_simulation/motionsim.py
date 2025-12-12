import json
import time

from typing import Any, Dict, cast
from typing_extensions import override
from masterpiece.mqtt import MqttMsg
from juham_core import Juham, MasterPieceThread, JuhamThread



class MotionSimThread(MasterPieceThread):
    """Thread simulating motion sensor."""

    def __init__(self, topic: str = "", interval: float = 60) -> None:
        """Construct thread for simulating motion sensor data.

        Args:
            topic (str, optional): MQTT topic to post the sensor readings. Defaults to None.
            interval (float, optional): Interval specifying how often the sensor is read. Defaults to 60 seconds.
        """
        super().__init__(None)
        self.sensor_topic: str = topic
        self.interval: float = interval

    @override
    def update_interval(self) -> float:
        return self.interval

    @override
    def update(self) -> bool:
        super().update()

        m: dict[str, Any] = {
            "tmp": {"value": 22.5},  # Room temperature value
            "sensor": {
                "vibration": True,  # Vibration status
                "motion": False,  # Motion status
            },
            "unixtime": int(time.time()),
        }

        msg = json.dumps(m)
        self.publish(self.sensor_topic, msg, 1, True)
        return True


class MotionSim(JuhamThread):
    """Motion simulator. Spawns a thread
    to generate MQTT messages of motion sensor"""

    workerThreadId = MotionSimThread.get_class_id()
    sensor_topic = "shellies/shellymotion2/info"
    update_interval = 60

    def __init__(
        self,
        name: str = "motionsensor",
        topic: str = "",
        interval: float = 60,
    ) -> None:
        """Create Shelly motion sensor simulator.

        Args:
            name (str, optional): Name of the object. Defaults to 'shellymotionsensor'.
            topic (str, optional): MQTT topic to publish motion sensor events. Defaults to None.
            interval (float, optional): interval between events, in seconds. Defaults to None.
        """
        super().__init__(name)
        self.active_liter_lpm = -1
        self.update_ts = None
        if topic:
            self.topic = topic
        if interval:
            self.interval = interval

    
    @override
    def run(self) -> None:
        self.worker = cast(
            MotionSimThread,
            Juham.instantiate(MotionSimThread.get_class_id()),
        )
        self.worker.sensor_topic = self.sensor_topic
        self.worker.interval = self.update_interval
        super().run()

    @override
    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = super().to_dict()
        data["_MotionSim"] = {"motion_topic": self.sensor_topic}
        return data

    @override
    def from_dict(self, data: Dict[str, Any]) -> None:
        super().from_dict(data)
        if "_MotionSim" in data:
            for key, value in data["_MotionSim"].items():
                setattr(self, key, value)
