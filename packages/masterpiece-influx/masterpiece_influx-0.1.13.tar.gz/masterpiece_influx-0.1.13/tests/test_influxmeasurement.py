import unittest
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
from masterpiece_influx.influx_measurement import InfluxMeasurement


class TestInfluxMeasurement(unittest.TestCase):
    def setUp(self) -> None:
        """Set up common test data for InfluxMeasurement."""
        self.measurement_name = "temperature"
        self.tags = {"location": "office", "sensor": "sensor1"}
        self.fields = {"value": 22.5}
        self.timestamp = "2024-12-16T12:00:00Z"

    def test_influx_measurement_initialization(self) -> None:
        """Test the initialization of InfluxMeasurement."""
        measurement = InfluxMeasurement(
            self.measurement_name,
            tags=self.tags,
            fields=self.fields,
            timestamp=self.timestamp,
        )
        self.assertEqual(measurement.name, self.measurement_name)
        self.assertEqual(measurement.tags, self.tags)
        self.assertEqual(measurement.fields, self.fields)
        self.assertEqual(measurement.timestamp, self.timestamp)

    def test_to_dict(self) -> None:
        """Test the to_dict method of InfluxMeasurement."""
        measurement = InfluxMeasurement(
            self.measurement_name,
            tags=self.tags,
            fields=self.fields,
            timestamp=self.timestamp,
        )
        expected_dict = {
            "measurement": self.measurement_name,
            "tags": self.tags,
            "fields": self.fields,
            "timestamp": self.timestamp,
        }
        self.assertEqual(measurement.to_dict(), expected_dict)

    def test_from_dict(self) -> None:
        """Test the from_dict method of InfluxMeasurement."""
        data = {
            "measurement": self.measurement_name,
            "tags": self.tags,
            "fields": self.fields,
            "timestamp": self.timestamp,
        }
        measurement = InfluxMeasurement("dummy")
        measurement.from_dict(data)
        self.assertEqual(measurement.name, self.measurement_name)
        self.assertEqual(measurement.tags, self.tags)
        self.assertEqual(measurement.fields, self.fields)
        self.assertEqual(measurement.timestamp, self.timestamp)

    def test_validate_valid_measurement(self) -> None:
        """Test the validate method for a valid measurement."""
        measurement = InfluxMeasurement(
            self.measurement_name,
            tags=self.tags,
            fields=self.fields,
            timestamp=self.timestamp,
        )
        self.assertTrue(measurement.validate())

    def test_validate_invalid_measurement(self) -> None:
        """Test the validate method for an invalid measurement."""
        measurement = InfluxMeasurement(self.measurement_name)
        with self.assertRaises(ValueError):
            measurement.validate()


if __name__ == "__main__":
    unittest.main()
