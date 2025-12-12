import unittest

from juham_watermeter.watermeter_imgdiff import WaterMeterImgDiff


class TestWaterMeterImgDiff(unittest.TestCase):
    """Unit tests for `WaterMeterImgDiff`."""

    def test_get_classid(self):
        """Assert that the meta-class driven class initialization works."""
        classid = WaterMeterImgDiff.get_class_id()
        self.assertEqual("WaterMeterImgDiff", classid)


if __name__ == "__main__":
    unittest.main()
