import unittest
from unittest.mock import MagicMock, patch
import json
from typing import Any, Dict
from masterpiece.mqtt import MqttMsg
from juham_simulation.watermetersim import WaterMeterSim, WaterMeterSimThread


class TestWaterMeterSimThread(unittest.TestCase):

    @patch("juham_simulation.watermetersim.timestamp", return_value=1234567890)
    def test_publish_simulated_data(self, mock_timestamp) -> None:
        # Create the thread
        thread = WaterMeterSimThread()
        thread.init("test/topic", 60)

        # Set known values
        thread.active_lpm = 5.5
        thread.total_liter = 1000.0

        # Patch publish() to track calls
        thread.publish = MagicMock()

        # Publish
        thread.publish_simulated_data()

        expected_payload = json.dumps({
            "active_liter_lpm": 5.5,
            "total_liter": 1005.5,
            "ts": 1234567890
        })

        thread.publish.assert_called_once_with("test/topic", expected_payload, qos=0, retain=False)

    def test_update_calls_publish(self):
        thread = WaterMeterSimThread()
        thread.init("topic", 60)
        thread.publish_simulated_data = MagicMock()
        thread.update()  # calls super().update() + publish_simulated_data
        thread.publish_simulated_data.assert_called_once()


class TestWaterMeterSim(unittest.TestCase):

    @patch("masterpiece.MasterPiece.instantiate")
    def test_run_starts_worker(self, mock_instantiate):
        # Mock a worker thread
        mock_worker = MagicMock()
        mock_instantiate.return_value = mock_worker

        sensor = WaterMeterSim("sensor", 30)
        sensor.run()

        mock_instantiate.assert_called_once_with(WaterMeterSim.workerThreadId)
        mock_worker.init.assert_called_once_with(sensor.sensor_topic, sensor.interval)
        mock_worker.start.assert_called_once()  # from super().run()

    def test_to_dict_and_from_dict(self):
        sensor = WaterMeterSim("sensor",  42)
        d = sensor.to_dict()
        self.assertIn("_watermetersim", d)
        self.assertEqual(d["_watermetersim"]["topic"], sensor.sensor_topic)
        self.assertEqual(d["_watermetersim"]["interval"], sensor.interval)

        # Modify dict and reload
        d["_watermetersim"]["interval"] = 99
        sensor.from_dict(d)
        self.assertEqual(sensor.interval, 99)

    def test_on_message_routes_to_on_sensor(self):
        sensor = WaterMeterSim("sensor",  30)
        with patch.object(sensor, "on_sensor") as mock_on_sensor:
            mock_msg = MagicMock(spec=MqttMsg)
            mock_msg.topic = sensor.sensor_topic
            mock_msg.payload = json.dumps({"value": 42}).encode()

            sensor.on_message(None, None, mock_msg)
            mock_on_sensor.assert_called_once_with({"value": 42})

    def test_on_message_calls_super_for_other_topics(self):
        sensor = WaterMeterSim("sensor", 30)
        with patch.object(sensor, "on_sensor") as mock_on_sensor, \
             patch("juham_simulation.watermetersim.JuhamThread.on_message") as mock_super:
            mock_msg = MagicMock(spec=MqttMsg)
            mock_msg.topic = "other/topic"
            mock_msg.payload = b"{}"

            sensor.on_message(None, None, mock_msg)
            mock_on_sensor.assert_not_called()
            mock_super.assert_called_once_with(None, None, mock_msg)


    @patch("juham_simulation.watermetersim.timestamp", side_effect=[1, 2, 3, 4])
    def test_cumulative_water_consumption(self, mock_timestamp):
        """Test that total_liter accumulates correctly over multiple updates."""
        thread = WaterMeterSimThread()
        thread.init("topic", interval=1.0)
        thread.active_lpm = 2.5  # constant flow rate

        # Patch publish so we can inspect payloads
        thread.publish = MagicMock()

        # Simulate 4 updates
        for _ in range(4):
            thread.publish_simulated_data()

        # Total should be 4 * 2.5 = 10.0
        self.assertAlmostEqual(thread.total_liter, 10.0)

        # Also check the last payload
        expected_payload = json.dumps({
            "active_liter_lpm": 2.5,
            "total_liter": 10.0,
            "ts": 4
        })
        thread.publish.assert_called_with("topic", expected_payload, qos=0, retain=False)

        # Optionally check all intermediate calls
        self.assertEqual(thread.publish.call_count, 4)


if __name__ == "__main__":
    unittest.main()
