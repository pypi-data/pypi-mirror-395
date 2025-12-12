import json
from datetime import datetime, timezone
from typing import Any, Dict, cast
from typing_extensions import override

from masterpiece.mqtt import MqttMsg
from juham_core import Juham, MasterPieceThread, JuhamThread


class TemperatureSimThread(MasterPieceThread):
    """Thread simulating four temperature
    sensors."""

    def __init__(self) -> None:
        """Construct thread for simulating data from temperature sensors.

        """
        super().__init__(None)
        self.interval: float = 60.0
        self.temp: float = 0.0
        self.sensor_topic: str = ""

    def init(self, topic: str = "", temp: float = 0, interval: float = 60) -> None:
        """Initialize thread for publishing simulated temperature readings

        Args:
            topic (str, optional): Mqtt topic to publish the readings
            interval (float, optional): Update interval. Defaults to 60.
        """
        self.sensor_topic = topic
        self.interval = interval
        self.temp = temp

    @override
    def update_interval(self) -> float:
        return self.interval

    @override
    def update(self) -> bool:
        super().update()
        ts = datetime.now(timezone.utc).timestamp()
        # self.temp = self.temp + 0.1
        if self.temp > 70:
            self.temp = 40

        data: dict[str, Any] = {
            "method": "NotifyStatus",
            "params": {
                "ts": ts,
                "temperature:100": {
                    "tC": self.temp,  # Temperature in Celsius for sensor1
                },
                "temperature:101": {
                    "tC": self.temp * 0.9,  # Temperature in Celsius for sensor2
                },
                "temperature:102": {
                    "tC": self.temp * 0.8,  # Temperature in Celsius for sensor2
                },
                "temperature:103": {
                    "tC": self.temp * 0.7,  # Temperature in Celsius for sensor2
                },
            },
        }
        msg = json.dumps(data)
        self.publish(self.sensor_topic, msg)
        return True


class TemperatureSim(JuhamThread):
    """Simulator for temperature sensors.

    Spawns an asynchronous thread to generate data from temperature
    sensors.
    """
    _TEMPERATURESIM: str = "_temperaturesim"
    workerThreadId: str = TemperatureSimThread.get_class_id()
    update_interval: float = 60
    temperature_topic: str = "temperature"

    def __init__(
        self,
        name: str = "temperature-simulator",
        topic: str = "",
        interval: float = 60.0,
    ) -> None:
        """Create temperature Simulator.

        Args:
            name (str, optional): name of the object. Defaults to 'temperature-simulator'.
            topic (str, optional): shelly device specific topic. Defaults to None.
            interval (float, optional): _description_. Defaults to None.
        """
        super().__init__(name)
        self.active_liter_lpm = -1
        self.update_ts = None
        if topic:
            self.temperature_topic = topic
        if interval > 0.0:
            self.update_interval = interval
        self.sensor_topic = self.make_topic_name(self.temperature_topic)
        self.interval = interval


    @override
    def run(self) -> None:
        self.worker = cast(
            TemperatureSim,
            Juham.instantiate(TemperatureSimThread.get_class_id()),
        )
        self.worker.init(self.temperature_topic, 40, self.update_interval)
        super().run()

    @override
    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = super().to_dict()
        data[self._TEMPERATURESIM] = {
            "temperature_topic": self.temperature_topic,
        }
        return data

    @override
    def from_dict(self, data: Dict[str, Any]) -> None:
        super().from_dict(data)
        if self._TEMPERATURESIM in data:
            for key, value in data[self._TEMPERATURESIM].items():
                setattr(self, key, value)
