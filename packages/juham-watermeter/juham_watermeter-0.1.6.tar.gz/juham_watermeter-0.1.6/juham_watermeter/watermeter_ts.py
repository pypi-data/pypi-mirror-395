"""Water meter time series recorder

"""

import json

from typing import Any
from typing_extensions import override
from masterpiece.mqtt import MqttMsg

from juham_core.timeutils import epoc2utc
from juham_core import JuhamTs


class WaterMeterTs(JuhamTs):
    """Watermeter timeseries recorder. Listens the watermeter MQTT topic
    and writes the measurements to timeseries database.

    """

    _WATERMETER: str = "watermeter_ts"
    _WATERMETER_ATTRS: list[str] = [
        "topic",
    ]

    topic = "watermeter"  # topic to listen

    def __init__(self, name="watermeter_ts") -> None:
        """Watermeter recorder, for listening watermeter MQTT topic and saving
        measurements to timeseries database.

        Args:
            name (str, optional): name of the object.
        """
        super().__init__(name)
        self.watermeter_topic: str = self.make_topic_name(self.topic)

    @override
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.watermeter_topic)

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        if msg.topic == self.watermeter_topic:
            em = json.loads(msg.payload.decode())
            self.record(em)
        else:
            super().on_message(client, userdata, msg)

    def record(self, info: dict[str, float]) -> None:
        """Writes system info to the time series database

        Args:
            ts (float): utc time
            em (dict): water meter message
        """

        try:
            if "leak_suspected" in info:
                self.write_point(
                    "watermeter",
                    {"sensor": info["sensor"], "location": info["location"]},
                    {
                        "leak_suspected": info["leak_suspected"],
                        "ts": info["ts"],
                    },
                    epoc2utc(info["ts"]),
                )
            elif "active_lpm" in info:
                self.write_point(
                    "watermeter",
                    {"sensor": info["sensor"], "location": info["location"]},
                    {
                        "total_liter": info["total_liter"],
                        "active_lpm": info["active_lpm"],
                        "ts": info["ts"],
                    },
                    epoc2utc(info["ts"]),
                )
        except Exception as e:
            self.error(f"Writing memory to influx failed {str(e)}")

    @override
    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()  # Call super class method
        watermeter_data = {}
        for attr in self._WATERMETER_ATTRS:
            watermeter_data[attr] = getattr(self, attr)
        data[self._WATERMETER] = watermeter_data
        return data

    @override
    def from_dict(self, data: dict[str, Any]) -> None:
        super().from_dict(data)  # Call super class method
        if self._WATERMETER in data:
            watermeter_data = data[self._WATERMETER]
            for attr in self._WATERMETER_ATTRS:
                setattr(self, attr, watermeter_data.get(attr, None))
