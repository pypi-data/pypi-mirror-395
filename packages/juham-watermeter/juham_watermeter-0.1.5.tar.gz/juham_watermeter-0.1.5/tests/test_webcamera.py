import unittest
from unittest.mock import patch, MagicMock
import numpy as np
import cv2

from typing import Any
from juham_watermeter.webcamera import WebCameraThread


class TestWebCameraThread(unittest.TestCase):
    def setUp(self) -> None:
        self.cam = WebCameraThread()

    def test_init_sets_defaults(self) -> None:
        self.assertEqual(self.cam._interval, 60)
        self.assertEqual(self.cam._location, "unknown")
        self.assertEqual(self.cam._camera, 0)
        self.assertEqual(self.cam.image.shape, (1, 1, 3))
        self.assertEqual(self.cam.image_timestamp, 0.0)

    def test_init_method_sets_values(self) -> None:
        self.cam.init(30.0, "office", 1)
        self.assertEqual(self.cam._interval, 30.0)
        self.assertEqual(self.cam._location, "office")
        self.assertEqual(self.cam._camera, 1)

    @patch("cv2.VideoCapture")
    def test_capture_image_successful(self, mock_VideoCapture: MagicMock) -> None:
        mock_cap = MagicMock()
        mock_frame = np.ones((480, 640, 3), dtype=np.uint8)
        mock_cap.isOpened.return_value = True
        mock_cap.read.return_value = (True, mock_frame)
        mock_VideoCapture.return_value = mock_cap

        result = self.cam.capture_image()
        self.assertEqual(result.shape, mock_frame.shape)

    @patch("cv2.VideoCapture")
    def test_capture_image_camera_unavailable(
        self, mock_VideoCapture: MagicMock
    ) -> None:
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = False
        mock_VideoCapture.return_value = mock_cap

        result = self.cam.capture_image()
        self.assertTrue(np.array_equal(result, np.zeros((1, 1, 3), dtype=np.uint8)))

    @patch("cv2.VideoCapture")
    def test_capture_image_read_failure(self, mock_VideoCapture: MagicMock) -> None:
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.read.return_value = (False, None)
        mock_VideoCapture.return_value = mock_cap

        result = self.cam.capture_image()
        self.assertTrue(np.array_equal(result, np.zeros((1, 1, 3), dtype=np.uint8)))

    def test_process_image_with_empty_input(self) -> None:
        result = self.cam.process_image(np.zeros((1, 1, 3), dtype=np.uint8))
        self.assertEqual(result.shape, (1, 1, 3))

    def test_process_image_grayscale_conversion(self) -> None:
        dummy_img = np.ones((480, 640, 3), dtype=np.uint8) * 255
        self.cam._expected_image_size = dummy_img.size
        result = self.cam.process_image(dummy_img)
        self.assertEqual(result.ndim, 2)  # grayscale image

    def test_enhance_contrast_on_invalid_input(self) -> None:
        # Input is not grayscale
        dummy_img = np.ones((480, 640, 3), dtype=np.uint8)
        result = self.cam.enhance_contrast(dummy_img)
        self.assertTrue((result == dummy_img).all())

    def test_enhance_contrast_output_shape(self) -> None:
        gray_img = np.ones((480, 640), dtype=np.uint8) * 100
        result = self.cam.enhance_contrast(gray_img)
        self.assertEqual(result.shape, gray_img.shape)
        self.assertEqual(result.dtype, gray_img.dtype)

    def test_update_interval_returns_correct_value(self) -> None:
        self.cam._interval = 42.0
        self.assertEqual(self.cam.update_interval(), 42.0)

    @patch("juham_watermeter.webcamera.timestamp", return_value=123.456)
    @patch.object(
        WebCameraThread,
        "capture_image",
        return_value=np.ones((480, 640, 3), dtype=np.uint8),
    )
    def test_update_method(self, mock_capture, mock_timestamp):
        self.cam._expected_image_size = 480 * 640 * 3
        result = self.cam.update()
        self.assertTrue(result)
        self.assertEqual(self.cam.image.shape, (480, 640, 3))
        self.assertEqual(self.cam.image_timestamp, 123.456)


if __name__ == "__main__":
    unittest.main()
