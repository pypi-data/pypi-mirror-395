import json
from typing import Any, Dict, Optional, cast
from typing_extensions import override
from masterpiece import MasterPiece, MasterPieceThread
from masterpiece.mqtt import Mqtt, MqttMsg
from juham_core import timestamp, JuhamThread

class WaterMeterSimThread(MasterPieceThread):
    """Thread that reads WaterMeterSim's water meter sensor."""

    def __init__(self) -> None:
        """Construct WaterMeterSim water meter acquisition thread.
        """
        super().__init__(None)

    def init(self, topic: str = "", interval: float = 60) -> None:
        """Initialize thread for reading WaterMeterSim sensor and publishing
        the readings to Mqtt network.

        Args:
            topic (str, optional): Mqtt topic to publish the readings
            interval (float, optional): Update interval. Defaults to 60.
        """
        self._sensor_topic = topic
        self._interval = interval
        self.active_lpm: float = 1.0
        self.total_liter: float = 0.0

    @override
    def update_interval(self) -> float:
        return self._interval

    def publish_simulated_data(self) -> None:
        """Publish simulated watermeter readings
        """
        active_lpm = self.active_lpm
        self.total_liter += active_lpm
        ts = timestamp()
        msg: dict[str, float] = {
            "active_liter_lpm": active_lpm,
            "total_liter": self.total_liter,
            "ts": ts,
        }
        self.publish(self._sensor_topic, json.dumps(msg), qos=0, retain=False)


    @override
    def update(self) -> bool:
        super().update()
        self.publish_simulated_data()
        return True


class WaterMeterSim(JuhamThread):
    """Watermeter simulator sensor."""

    _WATERMETERSIM: str = "_watermetersim"
    workerThreadId = WaterMeterSimThread.get_class_id()
    update_interval = 30
    watermeter_topic : str = "watermeter"

    def __init__(
        self,
        name: str = "simulatedwatermeter",
        interval: float = 60.0,
    ) -> None:
        """Create Homewizard water meter sensor.

        Args:
            name (str, optional): name identifying the sensor. Defaults to 'simulatedwatermeter'.
            interval (float, optional): Frequency at which the watermeter is read. Defaults to None.
        """
        super().__init__(name)
        self.active_liter_lpm: float = -1
        self.update_ts: float = 0.0
        self.interval = self.update_interval
        if interval > 0.0:
            self.interval = interval
        self.sensor_topic = self.make_topic_name(self.watermeter_topic)

    

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        if msg.topic == self.sensor_topic:
            em = json.loads(msg.payload.decode())
            self.on_sensor(em)
        else:
            super().on_message(client, userdata, msg)

    def on_sensor(self, em: dict[str, Any]) -> None:
        """Placeholder, no need to process water meter data

        Args:
            em (dict): data from the sensor
        """
        pass

    @override
    def run(self) -> None:
        self.worker = cast(
            WaterMeterSimThread,
            MasterPiece.instantiate(WaterMeterSim.workerThreadId),
        )
        self.worker.init(self.sensor_topic, self.update_interval)
        super().run()

    @override
    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = super().to_dict()
        data[self._WATERMETERSIM] = {
            "topic": self.sensor_topic,
            "interval": self.interval,
        }
        return data

    @override
    def from_dict(self, data: Dict[str, Any]) -> None:
        super().from_dict(data)
        if self._WATERMETERSIM in data:
            for key, value in data[self._WATERMETERSIM].items():
                setattr(self, key, value)
