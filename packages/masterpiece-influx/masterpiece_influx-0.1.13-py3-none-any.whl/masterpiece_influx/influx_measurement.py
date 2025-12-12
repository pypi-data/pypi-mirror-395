from typing import Any, Optional
from influxdb_client_3 import Point
from masterpiece.timeseries import Measurement

from typing import Optional, Any, Union, Dict
from influxdb_client_3 import Point


class InfluxMeasurement(Point, Measurement):
    """
    Concrete implementation of the Measurement class for InfluxDB.
    Supports both dictionary-based and fluent interface initialization.
    """

    def __init__(
        self,
        measurement_name: str,
        tags: Optional[dict[str, str]] = None,
        fields: Optional[dict[str, Any]] = None,
        timestamp: Optional[str] = None,
    ) -> None:
        """
        Initialize an InfluxMeasurement object.
        """
        super().__init__(measurement_name)
        self.tags = tags or {}
        self.fields = fields or {}
        self.timestamp = timestamp
        self.name = measurement_name

        # Add tags and fields to the Point object
        for tag, value in self.tags.items():
            self.tag(tag, value)

        for field, value in self.fields.items():
            self.field(field, value)

        if self.timestamp:
            self.time(self.timestamp)

    def tag(self, tag: str, value: str) -> "InfluxMeasurement":
        """
        Add a tag to the measurement and return self for method chaining.
        """
        super().tag(tag, value)  # Call the Point method
        self.tags[tag] = value
        return self

    def field(
        self, field: str, value: Union[int, float, str, bool]
    ) -> "InfluxMeasurement":
        """
        Add a field to the measurement and return self for method chaining.
        """
        super().field(field, value)  # Call the Point method
        self.fields[field] = value
        return self

    def time(self, timestamp: Union[str, int]) -> "InfluxMeasurement":
        """
        Set the timestamp for the measurement and return self for method chaining.
        """
        super().time(timestamp)  # Call the Point method
        self.timestamp = timestamp
        return self

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the InfluxMeasurement to a dictionary.
        """
        return {
            "measurement": self.name,
            "tags": self.tags,
            "fields": self.fields,
            "timestamp": self.timestamp,
        }

    def from_dict(self, data: Dict[str, Any]) -> "InfluxMeasurement":
        """
        Populate the InfluxMeasurement from a dictionary.
        """
        self.name = data["measurement"]
        self.tags = data.get("tags", {})
        self.fields = data.get("fields", {})
        self.timestamp = data.get("timestamp")

        for tag, value in self.tags.items():
            self.tag(tag, value)

        for field, value in self.fields.items():
            self.field(field, value)

        if self.timestamp:
            self.time(self.timestamp)

        return self

    def validate(self) -> bool:
        """
        Validate the measurement data.
        - Ensure it has at least one field (InfluxDB requires fields).
        - Validate that tags and fields are dictionaries.
        """
        if not self.fields:
            raise ValueError("InfluxMeasurement must have at least one field.")
        if not isinstance(self.tags, dict) or not isinstance(self.fields, dict):
            raise TypeError("Tags and fields must be dictionaries.")
        return True
