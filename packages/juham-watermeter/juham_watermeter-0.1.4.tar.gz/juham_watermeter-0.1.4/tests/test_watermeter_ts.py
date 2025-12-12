import unittest
from unittest.mock import MagicMock, patch
import json

from masterpiece.mqtt import MqttMsg
from juham_watermeter.watermeter_ts import WaterMeterTs 


class TestWaterMeterTs(unittest.TestCase):

    def setUp(self):
        self.wm = WaterMeterTs("test_wm")

        # Mock write_point and error
        self.wm.write_point = MagicMock()
        self.wm.error = MagicMock()

        # Patch epoc2utc
        epoc_patch = patch("juham_watermeter.watermeter_ts.epoc2utc", return_value="utc-ts")
        self.addCleanup(epoc_patch.stop)
        epoc_patch.start()

    # ---------------------------------------------------------
    # CONNECT
    # ---------------------------------------------------------
    def test_on_connect_success(self):
        self.wm.subscribe = MagicMock()

        self.wm.on_connect(None, None, None, rc=0)

        self.wm.subscribe.assert_called_once_with(self.wm.watermeter_topic)

    def test_on_connect_failure_no_subscribe(self):
        self.wm.subscribe = MagicMock()

        self.wm.on_connect(None, None, None, rc=5)

        self.wm.subscribe.assert_not_called()

    # ---------------------------------------------------------
    # MESSAGE DISPATCH
    # ---------------------------------------------------------
    def test_on_message_correct_topic_calls_record(self):
        em = {"sensor": "s1", "location": "kitchen", "ts": 123, "total_liter": 100, "active_lpm": 2.1}
        msg = MagicMock(spec=MqttMsg)
        msg.topic = self.wm.watermeter_topic
        msg.payload = json.dumps(em).encode()

        self.wm.record = MagicMock()
        self.wm.on_message(None, None, msg)

        self.wm.record.assert_called_once_with(em)

    def test_on_message_other_topic_calls_super(self):
        msg = MagicMock(spec=MqttMsg)
        msg.topic = "other/topic"
        msg.payload = b"{}"

        with patch.object(self.wm.__class__.__bases__[0], "on_message") as mock_super:
            self.wm.on_message(None, None, msg)
            mock_super.assert_called_once_with(None, None, msg)

    # ---------------------------------------------------------
    # RECORD
    # ---------------------------------------------------------
    def test_record_leak_suspected(self):
        info = {
            "sensor": "s1",
            "location": "basement",
            "leak_suspected": True,
            "ts": 123456
        }

        self.wm.record(info)

        self.wm.write_point.assert_called_once_with(
            "watermeter",
            {"sensor": "s1", "location": "basement"},
            {"leak_suspected": True, "ts": 123456},
            "utc-ts"
        )

    def test_record_active_lpm(self):
        info = {
            "sensor": "s1",
            "location": "bathroom",
            "total_liter": 500,
            "active_lpm": 3.2,
            "ts": 999
        }

        self.wm.record(info)

        self.wm.write_point.assert_called_once_with(
            "watermeter",
            {"sensor": "s1", "location": "bathroom"},
            {"total_liter": 500, "active_lpm": 3.2, "ts": 999},
            "utc-ts"
        )

    def test_record_error_handling(self):
        info = {
            "sensor": "s1",
            "location": "home",
            "ts": 555,
            "leak_suspected": True
        }

        # Force failure
        self.wm.write_point.side_effect = Exception("boom")

        self.wm.record(info)

        self.wm.error.assert_called_once()
        self.assertIn("boom", self.wm.error.call_args[0][0])

    # ---------------------------------------------------------
    # SERIALIZATION
    # ---------------------------------------------------------
    def test_to_dict_and_from_dict_roundtrip(self):
        original = self.wm.to_dict()

        new = WaterMeterTs("wm2")
        new.from_dict(original)

        # Only check attributes that should be persisted
        self.assertEqual(new.topic, self.wm.topic)


if __name__ == "__main__":
    unittest.main()
