"""Optical Character Recognition based water meter
Note: tested and works, but needs more work to be reliable

"""

import json
import time
import cv2
import numpy as np
from typing import Any, Optional, Union, cast
from typing_extensions import override
import pytesseract  # type: ignore
from PIL import Image
from masterpiece.mqtt import Mqtt
from juham_core.timeutils import timestamp
from .webcamera import WebCameraThread, WebCamera


class WaterMeterThreadOCR(WebCameraThread):
    """Asynchronous thread for capturing and processing images of web camera."""

    # class attributes
    _watermeter_topic: str = ""
    _expected_image_size: int = 640 * 480
    _crop_x: int = 195
    _crop_y: int = 157
    _crop_width: int = 640
    _crop_height: int = 480
    _save_images: bool = True
    _num_digits: int = 5

    def __init__(self, client: Optional[Mqtt] = None):
        """Construct with the given mqtt client.

        Args:
            client (object, optional): MQTT client. Defaults to None.
        """
        super().__init__(client)
        self.mqtt_client: Optional[Mqtt] = client
        self.total_liter: float = 0.0
        self.active_liter_lpm: float = 0.0
        self._prev_time: float = (
            0.0  # for computing momentary consumption (liters per hour)
        )

    def init_watermeter_ocr(
        self,
        topic: str,
        interval: float,
        location: str,
        camera: int,
        crop_x: int,
        crop_y: int,
        crop_width: int,
        crop_height: int,
        save_images: bool,
        num_digits: int,
    ) -> None:
        """Initialize the  data acquisition thread

        Args:
            topic (str): mqtt topic to publish the acquired system info
            interval (float): update interval in seconds
            location (str): geographic location
            camera(int) : ordinal specifying the camera to be used (0, 1)
            crop_x, crop_y, crop_width, crop_height (int): crop box
            save_images (bool) : true to enable saving of captured images, for debugging
            num_digits (int) : number of digits in the watermeter
        """
        super().init(interval, location, camera)
        self._watermeter_topic = topic
        self._crop_x = crop_x
        self._crop_y = crop_y
        self._crop_width = crop_width
        self._crop_height = crop_height
        self._save_images = save_images
        self._num_digits = num_digits

    @override
    def update_interval(self) -> float:
        return self._interval

    @override
    def update(self) -> bool:
        captured_image = self.capture_image()
        if captured_image.size < self._expected_image_size:
            return False
        processed_image = self.process_image(captured_image)
        if processed_image.size < self._expected_image_size:
            return False

        value: float = self.recognize_text(processed_image)
        if value < self.total_liter:
            self.warning("Invalid watermeter reading {value} skipped")

        self.total_liter = value
        current_time: float = time.time()
        elapsed_seconds: float = current_time - self._prev_time
        self._prev_time = current_time
        liters_per_minute = value / (60 * elapsed_seconds)
        watermeter: dict[str, Union[float, str]] = {
            "location": self._location,
            "sensor": self.name,
            "total_liter": self.total_liter,
            "active_lpm": liters_per_minute,
            "ts": timestamp(),
        }

        msg = json.dumps(watermeter)
        self.publish(self._watermeter_topic, msg, qos=0, retain=False)
        self.debug(f"Watermeter published to {self._watermeter_topic}", msg)
        return True

    def evaluate_text(self, text: str) -> float:
        # make sure we got all the digits
        num_lines: int = len(text.splitlines())
        if num_lines != 2:
            print(f"{text} has invalid number of lines {num_lines}")
            return 0.0
        first_line = text.splitlines()[0]
        num_digits: int = len(first_line)

        if num_digits != self._num_digits:
            print(
                f"{text} has invalid number of digits {num_digits}, expected {self._num_digits}"
            )
            return 0.0
        try:
            num = float(first_line)
            self.debug(f"Evaluated string {first_line} as {num}")
            print(f"Evaluated string {first_line} as {num}")
            return num
        except ValueError:
            self.warning(f"Cannot evaluate string {first_line}")
            print(f"Cannot evaluated string {first_line}")

        return 0.0

    def recognize_text(self, greyscale_image: np.ndarray) -> float:
        """Recognize numerical digits from the given greyscale image.

        Args:
            greyscale_image (np.ndarray): image to be recognized

        Returns:
            float: recognized value.
        """

        # cv2.imwrite("full.jpg", greyscale_image)

        # Apply a mask to focus only on the digits
        mask = np.zeros_like(greyscale_image)
        cv2.rectangle(
            mask,
            (self._crop_x, self._crop_y),
            (self._crop_x + self._crop_width, self._crop_y + self._crop_height),
            255,
            -1,
        )  # White rectangle for the ROI
        masked_image = cv2.bitwise_and(greyscale_image, mask)
        # cv2.imwrite("masked.jpg", masked_image)

        # Crop the ROI for OCR
        cropped_roi = masked_image[
            self._crop_y : self._crop_y + self._crop_height,
            self._crop_x : self._crop_x + self._crop_width,
        ]

        # Step 1: Apply a Gaussian blur to smooth out small details
        blurred_image = cv2.GaussianBlur(cropped_roi, (5, 5), 0)

        # Step 2: Apply adaptive thresholding for better OCR
        thresholded_image = cv2.adaptiveThreshold(
            blurred_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )

        # Step 3: Use morphological operations to remove thin vertical lines
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        morph_image = cv2.morphologyEx(thresholded_image, cv2.MORPH_CLOSE, kernel)

        # Save the intermediate image for debugging
        # cv2.imwrite("preprocessed.jpg", morph_image)

        # Convert to PIL image for pytesseract
        pil_image = Image.fromarray(morph_image)

        # Perform OCR with digits only
        text = pytesseract.image_to_string(
            pil_image, config="--psm 6 -c tessedit_char_whitelist=0123456789"
        )

        return self.evaluate_text(text)


class WaterMeterOCR(WebCamera):
    """Constructs a data acquisition thread for reading system status
    info, e.g. available disk space and publishes the data to the watermeter topic.

    """

    _WATERMETER: str = "watermeter_ocr"
    _WATERMETER_ATTRS: list[str] = [
        "topic",
        "update_interval",
        "location",
        "crop_x",
        "crop_y",
        "crop_width",
        "crop_height",
        "save_images",
        "num_digits",
    ]

    _workerThreadId: str = WaterMeterThreadOCR.get_class_id()
    update_interval: float = 60
    topic = "watermeter"
    location = "home"
    camera: int = 0
    crop_x: int = 0
    crop_y: int = 0
    crop_width: int = 640
    crop_height: int = 480
    save_images: bool = True
    num_digits: int = 5

    def __init__(self, name="watermeter_ocr") -> None:
        """Constructs system status automation object for acquiring and publishing
        system info e.g. available memory and CPU loads.

        Args:
            name (str, optional): name of the object.
        """
        super().__init__(name)
        self.worker: Optional[WaterMeterThreadOCR] = None
        self.watermeter_topic: str = self.make_topic_name(self.topic)

    @override
    def run(self) -> None:
        # create, initialize and start the asynchronous thread for acquiring forecast

        self.worker = cast(
            WaterMeterThreadOCR, self.instantiate(WaterMeterOCR._workerThreadId)
        )
        self.worker.name = self.name

        self.worker.init_watermeter_ocr(
            self.watermeter_topic,
            self.update_interval,
            self.location,
            self.camera,
            self.crop_x,
            self.crop_y,
            self.crop_width,
            self.crop_height,
            self.save_images,
            self.num_digits,
        )
        super().run()

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()  # Call parent class method
        watermeter_data = {}
        for attr in self._WATERMETER_ATTRS:
            watermeter_data[attr] = getattr(self, attr)
        data[self._WATERMETER] = watermeter_data
        return data

    def from_dict(self, data: dict[str, Any]) -> None:
        super().from_dict(data)  # Call parent class method
        if self._WATERMETER in data:
            watermeter_data = data[self._WATERMETER]
            for attr in self._WATERMETER_ATTRS:
                setattr(self, attr, watermeter_data.get(attr, None))
