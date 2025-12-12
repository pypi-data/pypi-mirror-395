import unittest
import pandas as pd
from unittest.mock import MagicMock
from typing import Any, Dict, List, Optional
from influxdb_client_3 import InfluxDBClient3, Point
from masterpiece_influx.influx import Influx


class TestInflux(unittest.TestCase):
    def setUp(self) -> None:
        # Mocking InfluxDBClient3 and its methods
        self.mock_influx_client = MagicMock(spec=InfluxDBClient3)

        # Create an instance of Influx, replacing the actual InfluxDBClient3 with the mock
        self.influx = Influx(name="test_influx")
        self.influx.influx_client = (
            self.mock_influx_client
        )  # Replacing the real influx client

    def test_write(self) -> None:
        # Test for the write method
        point = MagicMock(spec=Point)  # Mocking the Point object

        # Call the write method
        self.influx.write(point)

        # Ensure that the InfluxDBClient3 write method was called with the correct arguments
        self.influx.influx_client.write.assert_called_once_with(record=point)

    def test_write_dict(self) -> None:
        # Test for the write_dict method
        name = "test_measurement"
        tags = {"tag1": "value1"}
        fields = {"field1": 100}
        ts = "2024-12-14T12:00:00Z"

        # Call the write_dict method
        self.influx.write_dict(name, tags, fields, ts)

        # Prepare the expected point dictionary
        expected_point = {
            "measurement": name,
            "tags": tags,
            "fields": fields,
            "time": ts,
        }

        # Ensure that the InfluxDBClient3 write method was called with the correct arguments
        self.influx.influx_client.write.assert_called_once_with(record=expected_point)

    def test_read_dict(self) -> None:
        # Test for the read_dict method
        measurement = "test_measurement"
        start_time = "2024-12-01T00:00:00Z"
        end_time = "2024-12-14T00:00:00Z"
        tags = {"tag1": "value1"}
        fields = ["field1"]

        # Mock the query result
        mock_result = [
            MagicMock()
        ]  # Replace with a proper mock or actual expected result
        self.mock_influx_client.query.return_value = mock_result

        # Call the read_dict method
        result = self.influx.read_dict(measurement, start_time, end_time, tags, fields)

        # Ensure the query method was called with the correct query string
        expected_query = (
            f"SELECT {', '.join(fields)} FROM {measurement} WHERE time >= '{start_time}' "
            f"AND time <= '{end_time}' AND tag1 = 'value1' ORDER BY time"
        )
        self.influx.influx_client.query.assert_called_once_with(expected_query)

        # Ensure the result is as expected
        self.assertEqual(result, [dict(mock_result[0])])

    def test_read_dict_no_end_time(self) -> None:
        # Test for the read_dict method when end_time is None
        measurement = "test_measurement"
        start_time = "2024-12-01T00:00:00Z"
        tags = {"tag1": "value1"}
        fields = ["field1"]

        # Mock the query result
        mock_result = [MagicMock()]
        self.mock_influx_client.query.return_value = mock_result

        # Call the read_dict method
        result = self.influx.read_dict(
            measurement, start_time, tags=tags, fields=fields
        )

        # Ensure the query method was called with the correct query string
        expected_query = (
            f"SELECT {', '.join(fields)} FROM {measurement} WHERE time >= '{start_time}' "
            f"AND tag1 = 'value1' ORDER BY time"
        )
        self.influx.influx_client.query.assert_called_once_with(expected_query)

        # Ensure the result is as expected
        self.assertEqual(result, [dict(mock_result[0])])

    def test_read_dict_exception(self) -> None:
        # Test for the read_dict method when an exception is raised
        self.mock_influx_client.query.side_effect = Exception("Query failed")

        with self.assertRaises(Exception) as context:
            self.influx.read_dict("test_measurement", "2024-12-01T00:00:00Z")

        self.assertEqual(str(context.exception), "Failed to read data: Query failed")

    def test_read_last_value(self):
        measurement = "test_measurement"
        tags = {"tag1": "value1"}
        fields = ["field1"]

        # Mock a realistic DataFrame
        df = pd.DataFrame([{"time": "2025-01-01T12:00:00Z", "field1": 42}])
        self.mock_influx_client.query.return_value = df

        result = self.influx.read_last_value(measurement, tags=tags, fields=fields)

        expected_query = (
            f"SELECT field1 FROM {measurement} WHERE tag1 = 'value1' "
            f"AND field1 IS NOT NULL ORDER BY time DESC LIMIT 1"
        )
        self.influx.influx_client.query.assert_called_once_with(expected_query)

        self.assertEqual(result, {"time": "2025-01-01T12:00:00Z", "field1": 42})

    def test_read_last_value_fields_only(self):
        measurement = "test_m"

        df = pd.DataFrame([{"time": "X", "field1": 123}])
        self.mock_influx_client.query.return_value = df

        result = self.influx.read_last_value(measurement, fields=["field1"])

        expected_query = (
            "SELECT field1 FROM test_m WHERE field1 IS NOT NULL "
            "ORDER BY time DESC LIMIT 1"
        )

        self.influx.influx_client.query.assert_called_once_with(expected_query)
        self.assertEqual(result, {"time": "X", "field1": 123})

    def test_read_last_value_empty_dataframe(self):
        measurement = "test_m"
        df = pd.DataFrame([])  # empty df

        self.mock_influx_client.query.return_value = df
        result = self.influx.read_last_value(measurement)

        expected_query = (
            "SELECT * FROM test_m ORDER BY time DESC LIMIT 1"
        )

        self.influx.influx_client.query.assert_called_once_with(expected_query)
        self.assertEqual(result, {})

    def test_read_last_value_exception(self):
        measurement = "test_m"

        self.mock_influx_client.query.side_effect = Exception("Query failed")

        result = self.influx.read_last_value(measurement)
        self.assertEqual(result, {})

    def test_read_last_value_no_result(self) -> None:
        # Test for the read_last_value method with no query result
        measurement = "test_measurement"
        fields = ["field1"]

        # Mock the query result to be empty
        self.mock_influx_client.query.return_value = []

        # Call the read_last_value method
        result = self.influx.read_last_value(measurement, fields=fields)

        # Ensure the query method was called with the correct query string
        expected_query = f"SELECT {', '.join(fields)} FROM {measurement} WHERE field1 IS NOT NULL ORDER BY time DESC LIMIT 1"
        self.influx.influx_client.query.assert_called_once_with(expected_query)

        # Ensure the result is an empty dictionary
        self.assertEqual(result, {})


if __name__ == "__main__":
    unittest.main()
