import json
import unittest
from unittest.mock import MagicMock, patch
from typing import Any, Dict
from masterpiece.mqtt import MqttMsg

from juham_simulation.temperaturesim import TemperatureSim, TemperatureSimThread


class TestTemperatureSimThread(unittest.TestCase):

    @patch("juham_simulation.temperaturesim.datetime")
    def test_update_publishes_data(self, mock_datetime):
        # Mock the timestamp to a fixed value
        mock_datetime.now.return_value.timestamp.return_value = 1234567890

        thread = TemperatureSimThread()
        thread.init("test/topic", 10, 60)
        thread.temp = 50

        # Patch the publish method
        thread.publish = MagicMock()

        thread.update()

        # Retrieve the published message
        args, kwargs = thread.publish.call_args
        topic, msg_json = args
        msg = json.loads(msg_json)

        self.assertEqual(topic, "test/topic")
        self.assertEqual(msg["method"], "NotifyStatus")
        self.assertAlmostEqual(msg["params"]["temperature:100"]["tC"], 50)
        self.assertAlmostEqual(msg["params"]["temperature:101"]["tC"], 50 * 0.9)
        self.assertAlmostEqual(msg["params"]["temperature:102"]["tC"], 50 * 0.8)
        self.assertAlmostEqual(msg["params"]["temperature:103"]["tC"], 50 * 0.7)
        self.assertEqual(msg["params"]["ts"], 1234567890)


class TestTemperatureSim(unittest.TestCase):

    @patch("juham_core.Juham.instantiate")
    def test_run_starts_worker(self, mock_instantiate):
        mock_worker = MagicMock()
        mock_instantiate.return_value = mock_worker

        sim = TemperatureSim("sensor", "test/topic", 60)
        sim.run()

        self.assertIsNotNone(sim.worker)
        self.assertEqual(sim.worker, mock_worker)
        # Worker run() or start() should be called via superclass run
        self.assertTrue(mock_worker.start.called or mock_worker.run.called)

    def test_to_dict_and_from_dict(self):
        sim = TemperatureSim("sensor", "test/topic", 60)

        # Add a dummy attribute used in to_dict
        sim.temperature_topic = "dummy/topic"

        d = sim.to_dict()
        self.assertIn("_temperaturesim", d)
        self.assertEqual(d["_temperaturesim"]["temperature_topic"], "dummy/topic")

        sim2 = TemperatureSim()
        sim2.from_dict(d)
        self.assertEqual(sim2.temperature_topic, "dummy/topic")


if __name__ == "__main__":
    unittest.main()
