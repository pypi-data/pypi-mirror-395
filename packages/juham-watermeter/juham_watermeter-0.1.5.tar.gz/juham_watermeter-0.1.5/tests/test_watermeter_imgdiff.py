import unittest
from unittest.mock import MagicMock, patch, call
import numpy as np
import cv2

from juham_watermeter.watermeter_imgdiff import WaterMeterThreadImgDiff


class TestWaterMeterThreadImgDiff(unittest.TestCase):

    def setUp(self):
        # We provide a fake mqtt client
        self.client = MagicMock()
        self.wm = WaterMeterThreadImgDiff(client=self.client)

        # Disable actual FTP upload
        self.wm.upload_file = MagicMock()

        # Provide required fields
        self.wm._temp_filename1 = "/tmp/f1.png"
        self.wm._temp_filename2 = "/tmp/f2.png"
        self.wm._expected_image_size = 640 * 480

    # ------------------------------------------------------------------
    # compare_images()
    # ------------------------------------------------------------------
    def test_compare_images_different_size_returns_error(self):
        img1 = np.zeros((10, 10, 3), dtype=np.uint8)
        img2 = np.zeros((20, 20, 3), dtype=np.uint8)

        result = self.wm.compare_images(img1, img2)
        self.assertEqual(result, -1.0)

    @patch("juham_watermeter.watermeter_imgdiff.cv2.threshold")
    @patch("juham_watermeter.watermeter_imgdiff.cv2.absdiff")
    def test_compare_images_identical(self, mock_absdiff, mock_threshold):
        img = np.zeros((480, 640, 3), dtype=np.uint8)

        diff = np.zeros_like(img)
        mock_absdiff.return_value = diff
        mock_threshold.return_value = (None, diff)

        r = self.wm.compare_images(img, img)
        self.assertEqual(r, 0.0)

    @patch("juham_watermeter.watermeter_imgdiff.cv2.threshold")
    @patch("juham_watermeter.watermeter_imgdiff.cv2.absdiff")
    def test_compare_images_detects_change_and_triggers_upload(self, mock_absdiff, mock_threshold):
        # Prepare non-zero difference
        img_prev = np.zeros((480, 640, 3), dtype=np.uint8)
        img_now = np.ones((480, 640, 3), dtype=np.uint8) * 255

        diff = np.ones_like(img_prev)
        mock_absdiff.return_value = diff
        mock_threshold.return_value = (None, diff)

        self.wm.upload_images = MagicMock()

        r = self.wm.compare_images(img_prev, img_now)

        self.assertGreater(r, 0.0)
        self.wm.upload_images.assert_called_once()

    # ------------------------------------------------------------------
    # upload_images()
    # ------------------------------------------------------------------
    @patch("juham_watermeter.watermeter_imgdiff.cv2.imwrite")
    @patch("juham_watermeter.watermeter_imgdiff.os.remove")
    def test_upload_images_saves_and_uploads_and_removes(
        self, mock_remove, mock_imwrite
    ):
        img = np.zeros((10, 10), dtype=np.uint8)

        self.wm.upload_images(img, img)

        # cv2.imwrite called for both temp files
        mock_imwrite.assert_has_calls(
            [call(self.wm._temp_filename1, img), call(self.wm._temp_filename2, img)],
            any_order=True,
        )

        # upload_file called twice
        self.assertEqual(self.wm.upload_file.call_count, 2)

        # remove files afterward
        mock_remove.assert_has_calls(
            [call(self.wm._temp_filename1), call(self.wm._temp_filename2)],
            any_order=True,
        )

    # ------------------------------------------------------------------
    # update()
    # ------------------------------------------------------------------
    @patch.object(WaterMeterThreadImgDiff, "enhance_contrast")
    @patch.object(WaterMeterThreadImgDiff, "process_image")
    @patch.object(WaterMeterThreadImgDiff, "capture_image")
    def test_update_runs_and_publishes(
        self, mock_capture, mock_process, mock_enhance
    ):
        # Valid images
        good_img = np.zeros((480, 640, 3), dtype=np.uint8)
        good_gray = np.zeros((480, 640), dtype=np.uint8)

        mock_capture.return_value = good_img
        mock_process.return_value = good_gray
        mock_enhance.return_value = good_gray

        # First call: no previous image yet
        r = self.wm.update()
        self.assertTrue(r)

        # Now previous image exists, simulate a tiny diff
        self.wm._prev_image = good_gray
        self.wm.publish = MagicMock()

        r = self.wm.update()
        self.assertTrue(r)

        # publish() must have been called once
        self.wm.publish.assert_called_once()

    @patch.object(WaterMeterThreadImgDiff, "enhance_contrast")
    @patch.object(WaterMeterThreadImgDiff, "process_image")
    @patch.object(WaterMeterThreadImgDiff, "capture_image")
    def test_update_small_change_updates_total_water(
        self, mock_capture, mock_process, mock_enhance
    ):
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        gray = np.zeros((480, 640), dtype=np.uint8)

        mock_capture.return_value = img
        mock_process.return_value = gray
        mock_enhance.return_value = gray

        # Initialize previous image
        self.wm._prev_image = gray

        # Force compare_images to return stable 0.1
        self.wm.compare_images = MagicMock(return_value=0.1)

        self.wm.publish = MagicMock()

        before = self.wm.total_liter

        self.wm.update()

        after = self.wm.total_liter

        # change_area > 0 => total_liter must increase
        self.assertGreater(after, before)
        self.wm.publish.assert_called_once()


if __name__ == "__main__":
    unittest.main()
