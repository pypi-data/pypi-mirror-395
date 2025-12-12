import json
import time
from typing import Any
import unittest
from unittest.mock import MagicMock, patch

from juham_simulation.motionsim import MotionSim, MotionSimThread   # adjust import as needed
from juham_core import Juham


class TestMotionSimThread(unittest.TestCase):

    def setUp(self):
        self.thread = MotionSimThread(topic="test/topic", interval=42)
        self.thread.publish = MagicMock()

    def test_initialization(self):
        self.assertEqual(self.thread.sensor_topic, "test/topic")
        self.assertEqual(self.thread.interval, 42)

    def test_update_interval(self):
        self.assertEqual(self.thread.update_interval(), 42)

    def test_update_publishes_valid_json(self):
        self.assertTrue(self.thread.update())

        self.thread.publish.assert_called_once()
        topic, payload, qos, retain = self.thread.publish.call_args[0]

        self.assertEqual(topic, "test/topic")
        self.assertEqual(qos, 1)
        self.assertTrue(retain)

        data = json.loads(payload)
        self.assertIn("tmp", data)
        self.assertIn("sensor", data)
        self.assertIn("unixtime", data)

        self.assertEqual(data["tmp"]["value"], 22.5)
        self.assertTrue(data["sensor"]["vibration"])
        self.assertFalse(data["sensor"]["motion"])
        self.assertIsInstance(data["unixtime"], int)

    def test_unixtime_is_current(self):
        now = int(time.time())
        self.thread.update()

        payload = self.thread.publish.call_args[0][1]
        data = json.loads(payload)

        # allow small race condition tolerance
        self.assertLess(abs(data["unixtime"] - now), 3)


class TestMotionSim(unittest.TestCase):

    def test_to_dict(self):
        sim = MotionSim(name="motionsimtest", topic="abc/def", interval=10)
        d = sim.to_dict()

        self.assertIn("_MotionSim", d)
        self.assertEqual(d["_MotionSim"]["motion_topic"], sim.sensor_topic)

    def test_from_dict(self):
        sim = MotionSim()
        data : dict[str, Any] = {
            "_class": MotionSim.get_class_id(),
            "_version": 0,
            "_object": {"name": "sensor", "payload": None},
            "_base": {},
            "_MotionSim": {"motion_topic": "new/topic"},
        }

        sim.from_dict(data)

        # Check the updated attribute
        self.assertEqual(sim.motion_topic, "new/topic")

    


if __name__ == "__main__":
    unittest.main()
