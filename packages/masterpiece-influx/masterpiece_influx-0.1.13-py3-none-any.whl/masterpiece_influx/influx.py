from typing import Any, Optional
from typing_extensions import override
from influxdb_client_3 import InfluxDBClient3, Point
from masterpiece.timeseries import TimeSeries, Measurement
from masterpiece_influx.influx_measurement import InfluxMeasurement


class Influx(TimeSeries):
    """InfluxDB V3 implementation of a time series database for MasterPiece.

    This class provides an interface for interacting with an InfluxDB V3 time series
    database. The `host`, `token`, `org`, and `database` attributes are inherited
    from the `TimeSeries` superclass and can be initialized through the configuration
    system or overridden via constructor parameters.

    Attributes:
        host (str): Hostname of the InfluxDB server.
        token (str): Authentication token for InfluxDB.
        org (str): Organization name for InfluxDB.
        database (str): Database name for InfluxDB.
        influx_client (InfluxDBClient3): The client instance used for database operations.

    Example:
        Creating a custom instance with specific parameters:

        .. code-block:: python

            db = Influx(
                host="example.com",
                token="my-token",
                org="my-org",
                database="my-db"
            )
    """

    def __init__(
        self,
        name: str = "influx",
        host: Optional[str] = None,
        token: Optional[str] = None,
        org: Optional[str] = None,
        database: Optional[str] = None,
    ) -> None:
        """Construct InfluxDB v3 client for writing and reading time series.
        If the constructor parameters are not given, then the default class attribute
        values defined by the `TimeSeries` super class are used.

        Args:
            name (str, optional): Name of the object to be created. Defaults to "influx".
            host (Optional[str], optional): Hostname of the InfluxDB server. Defaults to class attribute.
            token (Optional[str], optional): Authentication token for InfluxDB. Defaults to class attribute.
            org (Optional[str], optional): Organization name for InfluxDB. Defaults to class attribute.
            database (Optional[str], optional): Database name for InfluxDB. Defaults to class attribute.
        """
        super().__init__(name)

        # Use constructor parameters if provided, otherwise fall back to class attributes
        self.host = host if host is not None else self.host
        self.token = token if token is not None else self.token
        self.org = org if org is not None else self.org
        self.database = database if database is not None else self.database

        # Initialize the InfluxDB client
        self.influx_client = InfluxDBClient3(
            host=self.host,
            token=self.token,
            org=self.org,
            database=self.database,
        )

    @override
    def write(self, point: Point) -> None:
        self.influx_client.write(record=point)

    @override
    def write_dict(
        self, name: str, tags: dict[str, Any], fields: dict[str, Any], ts: str
    ) -> None:
        point: dict[str, Any] = {
            "measurement": name,
            "tags": tags,
            "fields": fields,
            "time": ts,
        }
        self.influx_client.write(record=point)

    @override
    def read_dict(
        self,
        measurement: str,
        start_time: str,
        end_time: Optional[str] = None,
        tags: Optional[dict[str, Any]] = None,
        fields: Optional[list[str]] = None,
    ) -> list[dict[str, Any]]:
        try:
            # Select specific fields or all fields
            fields_query = ", ".join(fields) if fields else "*"

            # Construct the base SQL query
            query = (
                f"SELECT {fields_query} FROM {measurement} WHERE time >= '{start_time}'"
            )
            if end_time:
                query += f" AND time <= '{end_time}'"

            # Add tag filters
            if tags:
                tag_conditions = " AND ".join(
                    f"{key} = '{value}'" for key, value in tags.items()
                )
                query += f" AND {tag_conditions}"

            # Order by time
            query += " ORDER BY time"

            # Execute the query
            result = self.influx_client.query(query)

            # Convert the result to a list of dictionaries
            records = []
            for row in result:
                records.append(dict(row))

            return records

        except Exception as e:
            raise Exception(f"Failed to read data: {e}")

    @override
    def read_last_value(
        self,
        measurement: str,
        tags: Optional[dict[str, Any]] = None,
        fields: Optional[list[str]] = None,
    ) -> dict[str, Any]:
        try:
            fields_query = ", ".join(fields) if fields else "*"
            query = f"SELECT {fields_query} FROM {measurement}"

            if tags:
                tag_conditions = " AND ".join(
                    f"{key} = '{value}'" for key, value in tags.items()
                )
                query += f" WHERE {tag_conditions}"

            if fields:
                not_null_conditions = " AND ".join(
                    f"{field} IS NOT NULL" for field in fields
                )
                query += (
                    f" AND {not_null_conditions}"
                    if tags
                    else f" WHERE {not_null_conditions}"
                )

            query += " ORDER BY time DESC LIMIT 1"

            print(f"Constructed Query: {query}")

            df = self.influx_client.query(query)  # Pandas DataFrame

            if df is None or df.empty:
                return {}

            return df.iloc[0].to_dict()

        except Exception as e:
            print(f"Query execution failed: {e}")
            return {}

    @override
    def read_point(
        self,
        measurement: str,
        start_time: str,
        end_time: Optional[str] = None,
        tags: Optional[dict[str, Any]] = None,
        fields: Optional[list[str]] = None,
    ) -> list[Any]:

        try:
            # Select specific fields or all fields
            fields_query = ", ".join(fields) if fields else "*"

            # Construct the base SQL query
            query = (
                f"SELECT {fields_query} FROM {measurement} WHERE time >= '{start_time}'"
            )
            if end_time:
                query += f" AND time <= '{end_time}'"

            # Add tag filters
            if tags:
                tag_conditions = " AND ".join(
                    f"{key} = '{value}'" for key, value in tags.items()
                )
                query += f" AND {tag_conditions}"

            # Order by time
            query += " ORDER BY time"

            # Execute the query
            result = self.influx_client.query(query)

            # Convert the result to a list of Point objects
            points = []
            for row in result:
                point = Point(measurement)
                for key, value in row.items():
                    if key == "time":
                        point.time(value)
                    elif isinstance(value, (int, float)):
                        point.field(key, value)
                    else:
                        point.tag(key, value)
                points.append(point)

            return points

        except Exception as e:
            raise Exception(f"Failed to read data as Points: {e}")

    @override
    def measurement(self, measurement: str) -> Measurement:
        return InfluxMeasurement(measurement)
