import json
import unittest
from unittest.mock import MagicMock, patch
from typing import Any, Dict

# adjust path if your module lives elsewhere
from juham_simulation.powermetersim import (
    PowerMeterSim,
    PowerMeterSimThread,
)
from masterpiece.mqtt import MqttMsg


class TestPowerMeterSimThread(unittest.TestCase):
    @patch("juham_simulation.powermetersim.timestamp", return_value=1000.0)
    def test_publish_active_power(self, mock_timestamp):
        # prepare a mock mqtt client and attach to thread instance
        mock_client = MagicMock()
        thread = PowerMeterSimThread()
        thread.mqtt_client = mock_client

        # set initial current_ts and class power
        thread.current_ts = 990.0  # previous timestamp
        PowerMeterSimThread.initialize(power_topic="test/power", power=200.0, interval=10.0)
        # ensure topic used by publish_active_power
        topic = PowerMeterSimThread._power_topic

        # call publish_active_power with timestamp() == 1000.0
        thread.publish_active_power(1000.0)

        # compute expected dt and payload
        dt = 1000.0 - 990.0  # 10.0
        expected = {
            "timestamp": 1000.0,
            "real_a": 200.0 * dt,
            "real_b": 200.0 * dt,
            "real_c": 200.0 * dt,
            "real_total": 3 * 200.0 * dt,
        }

        # Ensure client.publish called once with JSON payload
        mock_client.publish.assert_called_once()
        args, kwargs = mock_client.publish.call_args
        called_topic = args[0]
        called_payload = args[1]
        called_qos = args[2] if len(args) > 2 else kwargs.get("qos")
        called_retain = args[3] if len(args) > 3 else kwargs.get("retain")

        self.assertEqual(called_topic, topic)
        # payload is JSON string — parse and compare numeric values
        parsed = json.loads(called_payload)
        # floats might be large, compare numerically
        self.assertAlmostEqual(parsed["timestamp"], expected["timestamp"])
        self.assertAlmostEqual(parsed["real_a"], expected["real_a"])
        self.assertAlmostEqual(parsed["real_b"], expected["real_b"])
        self.assertAlmostEqual(parsed["real_c"], expected["real_c"])
        self.assertAlmostEqual(parsed["real_total"], expected["real_total"])
        self.assertEqual(called_qos, 1)
        self.assertTrue(called_retain)

    @patch("juham_simulation.powermetersim.timestamp", return_value=1234.5)
    def test_update_calls_publish(self, mock_timestamp):
        # Ensure update() calls publish_active_power internally
        mock_client = MagicMock()
        thread = PowerMeterSimThread()
        thread.mqtt_client = mock_client
        thread.current_ts = 1200.0
        PowerMeterSimThread.initialize(power_topic="p/t", power=50.0, interval=5.0)

        # call update which should call publish_active_power
        ok = thread.update()
        self.assertTrue(ok)
        mock_client.publish.assert_called_once()

class TestPowerMeterSim(unittest.TestCase):
    @patch("juham_simulation.powermetersim.Juham.instantiate")
    @patch("juham_simulation.powermetersim.JuhamThread.run", new_callable=MagicMock)
    def test_run_instantiates_worker_and_calls_super_run(self, mock_super_run, mock_instantiate):
        # prepare mock worker returned from instantiate
        mock_worker = MagicMock()
        mock_instantiate.return_value = mock_worker

        sim = PowerMeterSim(name="em", interval=12.0)
        sim.run()

        # instantiate called to create worker
        mock_instantiate.assert_called_once_with(PowerMeterSimThread.get_class_id())
        # super.run() should have been invoked (we patched it)
        mock_super_run.assert_called_once()

    def test_to_dict_and_from_dict(self):
        sim = PowerMeterSim("sensor", interval=15.0)
        d = sim.to_dict()

        # ensure powermetersim key present
        self.assertIn(sim._POWERMETERSIM, d)
        self.assertIn("power_topic", d[sim._POWERMETERSIM])

        # round-trip: modify dict and load back
        d2 = {
            "_class": "PowerMeterSim",
            "_version": 0,
            "_object": {"name": "sensor", "payload": None},
            "_base": {},
            sim._POWERMETERSIM: {"power_topic": "/some/topic"},
        }
        sim2 = PowerMeterSim()
        sim2.from_dict(d2)
        self.assertEqual(sim2.power_topic, "/some/topic")

    def test_on_message_calls_on_sensor(self):
        sim = PowerMeterSim("em", interval=10.0)
        with patch.object(sim, "on_sensor", MagicMock()) as mock_on_sensor:
            mock_msg = MagicMock(spec=MqttMsg)
            mock_msg.topic = sim.power_topic
            mock_msg.payload = json.dumps({"k": "v"}).encode()
            sim.on_message(None, None, mock_msg)
            mock_on_sensor.assert_called_once_with({"k": "v"})


if __name__ == "__main__":
    unittest.main()
