"""Web camera with basic image processing features."""

import cv2
import numpy as np
from typing import Any, Optional
from typing_extensions import override
from masterpiece.mqtt import Mqtt
from masterpiece import MasterPieceThread
from juham_core import JuhamThread
from juham_core.timeutils import timestamp


class WebCameraThread(MasterPieceThread):
    """Asynchronous thread for capturing and processing images of web camera."""

    # class attributes
    _interval: float = 60  # seconds
    _location = "unknown"
    _camera: int = 0  # e.g. 0 built-in, 1 external camera
    _expected_image_size: int = 640 * 480

    def __init__(self, client: Optional[Mqtt] = None):
        """Construct with the given mqtt client.  Initializes minimal 1x1 image
        with timestamp 0.0, which are updated to actual image size and timestamp
        with each captured image, for sub classes to process.

        Args:
            client (object, optional): MQTT client. Defaults to None.
        """
        super().__init__(client)
        self.mqtt_client: Optional[Mqtt] = client
        self.image: np.ndarray = np.zeros((1, 1, 3), dtype=np.uint8)
        self.image_timestamp: float = 0.0

    def init(
        self,
        interval: float,
        location: str,
        camera: int,
    ) -> None:
        """Initialize the  data acquisition thread

        Args:
            interval (float): update interval in seconds
            location (str): geographic location
            camera(int) : ordinal specifying the camera to be used (0, 1)

        """
        self._interval = interval
        self._location = location
        self._camera = camera

    def capture_image(self) -> np.ndarray:
        """
        Captures an image from the webcam and returns the image as a numpy array.

        Returns:
            np.ndarray: The captured image in the form of a NumPy array.
        """
        # Initialize the webcam (0 for the built-in camera or 1 for the USB webcam)
        cap = cv2.VideoCapture(self._camera)

        # Check if the webcam is opened correctly
        if not cap.isOpened():
            self.error(f"Could not access the camera {self._camera}.")
            return np.zeros(
                (1, 1, 3), dtype=np.uint8
            )  # Return an empty array if the camera isn't accessible

        # Capture a frame
        try:
            ret, frame = cap.read()
            if not ret:
                self.error("Could not capture image.")
                frame = np.zeros(
                    (1, 1, 3), dtype=np.uint8
                )  # Return 1x1 array if capture failed
        finally:
            cap.release()
        return frame  # Return the captured image

    def process_image(self, image: np.ndarray) -> np.ndarray:
        """
        Processes the captured image by converting it to grayscale and applying thresholding.

        Args:
            image (np.ndarray): The input image to process.

        Returns:
            np.ndarray: The processed image after grayscale conversion and thresholding.
        """
        if image.size < self._expected_image_size:  # Check if the image is empty
            self.error("Received an empty image for processing.")
            return image

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return gray

    def enhance_contrast(self, image: np.ndarray) -> np.ndarray:
        """
        Enhances the contrast of a grayscale image while suppressing noise.

        Args:
            image (np.ndarray): The input grayscale image.

        Returns:
            np.ndarray: The contrast-enhanced image with reduced noise amplification.
        """
        if image.ndim != 2:  # Ensure the image is grayscale
            self.error("Contrast enhancement requires a grayscale image.")
            return image

        # Apply a slight Gaussian blur to reduce noise before enhancing contrast
        blurred = cv2.GaussianBlur(image, (3, 3), 0)

        # Apply CLAHE with conservative parameters to avoid over-enhancement
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        contrast_enhanced = clahe.apply(blurred)

        return contrast_enhanced

    @override
    def update_interval(self) -> float:
        return self._interval

    @override
    def update(self) -> bool:
        self.image = self.capture_image()
        self.image_timestamp = timestamp()
        return self.image.size == self._expected_image_size


class WebCamera(JuhamThread):
    """Base class for web camera."""

    _WEBCAMERA: str = "webcamera"
    _WEBCAMERA_ATTRS: list[str] = ["location", "camera"]

    _workerThreadId: str = WebCameraThread.get_class_id()
    location = "home"
    camera: int = 0

    def __init__(self, name="webcam") -> None:
        """Constructs system status automation object for acquiring and publishing
        system info e.g. available memory and CPU loads.

        Args:
            name (str, optional): name of the object.
        """
        super().__init__(name)
        self.worker: Optional[WebCameraThread] = None

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()  # Call parent class method
        webcam_data = {}
        for attr in self._WEBCAMERA_ATTRS:
            webcam_data[attr] = getattr(self, attr)
        data[self._WEBCAMERA] = webcam_data
        return data

    def from_dict(self, data: dict[str, Any]) -> None:
        super().from_dict(data)  # Call parent class method
        if self._WEBCAMERA in data:
            webcam_data = data[self._WEBCAMERA]
            for attr in self._WEBCAMERA_ATTRS:
                setattr(self, attr, webcam_data.get(attr, None))
