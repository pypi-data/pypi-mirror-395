"""Web camera based optical watermeter based on differences between subsequent frames. 

"""

import json
import os
import subprocess
import tempfile
import time
import cv2
import numpy as np
from typing import Any, Optional, Union, cast
from typing_extensions import override
from masterpiece.mqtt import Mqtt

from juham_core.timeutils import timestamp
from .webcamera import WebCameraThread, WebCamera


class WaterMeterThreadImgDiff(WebCameraThread):
    """Asynchronous thread for capturing and processing images of web camera.
    Uploads three images to sftp server for inspection: the original watermeter
    image, the image holding differences between the last captured watermeter image,
    and  processed image with noise eliminated, and differences scaled up for maximum
    image contrast: white pixels represent areas. The more white pixels, the bigger the
    water consumption.
    """

    # class attributes
    _watermeter_topic: str = ""
    _expected_image_size: int = 640 * 480
    _save_images: bool = True
    _calibration_factor: float = 1000.0  # img diff to liters
    _max_change_area: float = 0.1  # difference can't be greater than this
    ftp_site: str = ""
    ftp_user: str = ""
    ftp_pw: str = ""

    def __init__(self, client: Optional[Mqtt] = None):
        """Construct with the given mqtt client.

        Args:
            client (object, optional): MQTT client. Defaults to None.
        """
        super().__init__(client)
        self.sensor_name = "watermeter_imgdiff"
        self.mqtt_client: Optional[Mqtt] = client
        self.total_liter: float = 0.0
        self.active_liter_lpm: float = 0.0
        self._prev_image: np.ndarray = np.zeros((1, 1, 3), dtype=np.uint8)
        self._prev_image_initialized = False
        self._prev_time: float = 0.0

        # total cumulative diff between two consequtive images
        self._wm_start_seconds: float = 0.0

        # temp filenames for saving the original and processed images, for debugging purposes
        self._temp_filename1: str = ""
        self._temp_filename2: str = ""

    def init_watermeter_imgdiff(
        self,
        interval: float,
        location: str,
        camera: int,
        topic: str,
        save_images: bool,
    ) -> None:
        """Initialize the  data acquisition thread

        Args:
            topic (str): mqtt topic to publish the acquired system info
            interval (float): update interval in seconds
            location (str): geographic location
            camera(int) : ordinal specifying the camera to be used (0, 1)
            save_images (bool) : true to enable saving of captured images, for debugging
        """
        super().init(interval, location, camera)
        self._watermeter_topic = topic
        self._save_images = save_images
        # temp filenames for saving the original and processed images, for debugging purposes
        tmpdir: str = tempfile.mkdtemp()
        self._temp_filename1 = os.path.join(tmpdir, f"{self.sensor_name}_wm_1.png")
        self._temp_filename2 = os.path.join(tmpdir, f"{self.sensor_name}_wm_2.png")

    def upload_image(self, file: str, img: np.ndarray) -> None:
        """Save the image to the given file and upload the file to the FTP server.

        Args:
            file (str): The filename where the image will be saved.
            img (np.ndarray): The image to be saved and uploaded.
        """
        # Save the image to the specified file
        cv2.imwrite(file, img)

        try:
            # Upload the file to the FTP server
            self.upload_file(file)

            # If the upload is successful, remove the file
            os.remove(file)

        except Exception as e:
            # Handle any errors that occurred during upload
            self.error(f"Error during file upload: {e}")

    def compare_images(
        self,
        np_prev: np.ndarray,
        np_current: np.ndarray,
        threshold: int = 20,
    ) -> float:
        """
        Compares two images and returns a float value representing the level of differences.

        Parameters:
            np_prev (np.ndarray): The previous image.
            np_current (np.ndarray): The current image.
            threshold (int): Threshold value to filter noise in the difference image.

        Returns:
            float: A value between 0.0 and 1.0 indicating the level of difference.
                0.0 means identical, 1.0 means maximally different.
        """
        # Ensure both images are the same size and type
        if np_prev.shape != np_current.shape:
            self.error("Images have different shapes or dimensions.")
            return -1.0  # Error value for different shapes

        # Step 1: Calculate the absolute difference between the two images
        diff_image = cv2.absdiff(np_prev, np_current)

        # Step 2: Filter small differences (noise) using a binary threshold
        _, binary_diff = cv2.threshold(diff_image, threshold, 255, cv2.THRESH_BINARY)

        # Step 3: Calculate the proportion of changed pixels
        change_area: float = np.count_nonzero(binary_diff) / binary_diff.size

        if change_area > 0.0:
            print(f"Waterflow detected {change_area}, uploading")
            self.upload_images(np_current, binary_diff)

        # Return a value between 0.0 (identical) and 1.0 (maximally different)
        return min(max(change_area, 0.0), 1.0)

    def upload_file(self, filename: str) -> None:
        """Upload the given filename to the ftp server, if the server is configured.

        Args:
            filename (str): _description_
        """
        if len(self.ftp_site) > 0 and len(self.ftp_user) > 0 and len(self.ftp_pw) > 0:

            # Build the curl command for uploading the file
            curl_command = [
                "curl",
                f"-u{self.ftp_user}:{self.ftp_pw}",
                "--retry",
                "3",
                "--retry-delay",
                "5",
                "-T",
                filename,
                self.ftp_site,
            ]

            # Execute the curl command
            try:
                subprocess.run(curl_command, check=True)
            except subprocess.CalledProcessError as e:
                self.error(f"Error during image upload: {e}")

    def upload_images(self, np_watermeter: np.ndarray, np_diff: np.ndarray) -> None:
        """Upload captured grayscale watermeter image, and the diff image to ftp site

        Parameters:
            np_watermeter (np.ndarray): Watermeter image in grayscale
            np_diff (np.ndarray): The diff image reflecting consumed water
        """
        self.upload_image(self._temp_filename1, np_watermeter)
        self.upload_image(self._temp_filename2, np_diff)

    @override
    def update(self) -> bool:
        change_area: float = -1
        captured_image = self.capture_image()
        if captured_image.size < self._expected_image_size:
            return False
        grayscale_image = self.process_image(captured_image)
        if grayscale_image.size < self._expected_image_size:
            return False
        processed_image = self.enhance_contrast(grayscale_image)
        if processed_image.size < self._expected_image_size:
            return False

        if self._prev_image.size == self._expected_image_size:
            change_area = self.compare_images(self._prev_image, processed_image)
        else:
            self._prev_image = processed_image
            return True

        lpm: float = 0.0

        if change_area > 0.0:
            # to capture even the smallest leaks, update the previous image
            # only when difference is found
            self._prev_image = processed_image
            wm_elapsed_seconds: float = time.time() - self._wm_start_seconds
            self._wm_start_seconds = time.time()

            # image change_area factor to consumed water in liters
            liters = change_area * self._calibration_factor

            # update cumulative water consumption
            self.total_liter += liters / 1000.0

            # scale liters to flow (liters per minute)
            lpm = liters / (wm_elapsed_seconds / 60.0)

        watermeter: dict[str, Union[float, str]] = {
            "location": self._location,
            "sensor": self.sensor_name,
            "total_liter": self.total_liter,
            "active_lpm": lpm,
            "ts": timestamp(),
        }

        msg = json.dumps(watermeter)
        self.publish(self._watermeter_topic, msg, qos=0, retain=False)
        return True


class WaterMeterImgDiff(WebCamera):
    """WebCamera based optical watermeter. Needs a low-cost web camera and a spot
    light to illuminate the watermeter. Captures images with specified interval (the default
    is 1 minute) and computes a factor that represents the level of difference, 0.0 being no
    differences and 1.0 corresponding to the maximum difference (all pixels different with
    maximum contrast e.g. 0 vs 255).
    The more two consequtive images differ, the higher the water consumption. Cannot give any absolute water consumption
    measurements as liters, but suits well for leak detection purposes - the greater
    the difference the creater the water consumption.

    """

    _WATERMETER: str = "watermeter_imgdiff"
    _WATERMETER_ATTRS: list[str] = [
        "topic",
        "update_interval",
        "location",
        "camera",
        "save_images",
    ]

    _workerThreadId: str = WaterMeterThreadImgDiff.get_class_id()
    update_interval: float = 60 * 10 # 10 minutes
    topic = "watermeter"
    location = "home"
    camera: int = 0
    save_images: bool = True

    def __init__(self, name="watermeter_imgdiff") -> None:
        """Constructs system status automation object for acquiring and publishing
        system info e.g. available memory and CPU loads.

        Args:
            name (str, optional): name of the object.
        """
        super().__init__(name)
        self.worker: Optional[WaterMeterThreadImgDiff] = None
        self.watermeter_topic: str = self.make_topic_name(self.topic)

    @override
    def initialize(self) -> None:
        # let the super class to initialize database first so that we can read it
        super().initialize()

        # read the latest known value from
        last_value: dict[str, float] = self.read_last_value(
            "watermeter",
            {"sensor": self.name, "location": self.location},
            ["total_liter"],
        )
        worker: WaterMeterThreadImgDiff = cast(WaterMeterThreadImgDiff, self.worker)
        if "total_liter" in last_value:
            worker.total_liter = last_value["total_liter"]
            self.info(f"Total liters {worker.total_liter} read from the database")
        else:
            self.warning("no previous database value for total_liter found")

    @override
    def run(self) -> None:
        # create, initialize and start the asynchronous thread for acquiring forecast

        self.worker = cast(
            WaterMeterThreadImgDiff, self.instantiate(WaterMeterImgDiff._workerThreadId)
        )
        self.worker.sensor_name = self.name

        self.worker.init_watermeter_imgdiff(
            self.update_interval,
            self.location,
            self.camera,
            self.watermeter_topic,
            self.save_images,
        )
        super().run()

    @override
    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()  # Call parent class method
        watermeter_data = {}
        for attr in self._WATERMETER_ATTRS:
            watermeter_data[attr] = getattr(self, attr)
        data[self._WATERMETER] = watermeter_data
        return data

    @override
    def from_dict(self, data: dict[str, Any]) -> None:
        super().from_dict(data)  # Call parent class method
        if self._WATERMETER in data:
            watermeter_data = data[self._WATERMETER]
            for attr in self._WATERMETER_ATTRS:
                setattr(self, attr, watermeter_data.get(attr, None))
