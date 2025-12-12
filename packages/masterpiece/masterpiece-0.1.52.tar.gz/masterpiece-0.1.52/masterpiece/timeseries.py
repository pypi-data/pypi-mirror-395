from typing import Any, Optional, Union
from typing_extensions import override
from .masterpiece import MasterPiece

from abc import ABC, abstractmethod
from typing import Dict, Any


class Measurement(ABC):
    """Abstract base class for measurement structures."""

    def __init(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the measurement into a dictionary format.
        Used for writing to storage or transferring data.
        """
        pass

    @abstractmethod
    def from_dict(self, data: Dict[str, Any]) -> "Measurement":
        """
        Populate the measurement fields from a dictionary.
        """
        pass

    @abstractmethod
    def validate(self) -> bool:
        """
        Validate the measurement data.
        Return True if valid, otherwise raise an exception or return False.
        """
        pass

    @abstractmethod
    def tag(self, tag: str, value: str) -> "Measurement":
        """
        Add a tag to the measurement and return self for method chaining.
        """
        raise Exception("tag not implemented")

    @abstractmethod
    def field(self, field: str, value: Union[int, float, str, bool]) -> "Measurement":
        """
        Add a field to the measurement and return self for method chaining.
        """
        raise Exception("field not implemented")

    @abstractmethod
    def time(self, timestamp: Union[str, int]) -> "Measurement":
        """
        Set the timestamp for the measurement and return self for method chaining.
        """
        raise Exception("time not implemented")


class TimeSeries(MasterPiece):
    """An abstract base class for time series database interactions.

    This class defines a standardized interface for reading and writing time series data.
    It serves as a foundation for implementing support for specific time series databases,
    abstracting low-level details and enabling consistent access patterns.

    Subclasses must implement the `write_dict` and `read_dict` methods to provide
    database-specific functionality.

    """

    token: str = ""
    org: str = ""
    host: str = ""
    database: str = ""

    def __init__(self, name: str) -> None:
        super().__init__(name)

    def write(self, point: Measurement) -> None:
        """Write record to database table.

        Args:
            point (Any): The data point to be written to the database.

        Raises:
            Exception: If not implemented in the subclass.
        """
        raise Exception("write not implemented")

    def write_dict(
        self, name: str, tags: dict[str, Any], fields: dict[str, Any], ts: str
    ) -> None:
        """Write record to the database table.

        Args:
            name (str): The name of the measurement.
            tags (dict[str, Any]): Tags (indexed keys) for filtering the data.
            fields (dict[str, Any]): Measurement data fields.
            ts (str): The timestamp for the measurement.

        Returns:
            None

        Raises:
            Exception: If the write method is not implemented in the subclass.
        """
        raise Exception("TimeSeries write_dict not implemented")

    def read_dict(
        self,
        measurement: str,
        start_time: str,
        end_time: Optional[str] = None,
        tags: Optional[dict[str, Any]] = None,
        fields: Optional[list[str]] = None,
    ) -> list[dict[str, Any]]:
        """Reads records from the database using SQL.

        Args:
            measurement (str): The name of the measurement (table) to query.
            start_time (str): The start time for the query (ISO8601 format).
            end_time (Optional[str]): The end time for the query (ISO8601 format). Defaults to None.
            tags (Optional[dict[str, Any]]): Tags to filter the data (as WHERE conditions). Defaults to None.
            fields (Optional[list[str]]): Specific fields to include in the result. Defaults to None.

        Returns:
            list[dict[str, Any]]: A list of records matching the query.

        Raises:
            Exception: If reading from the database fails.
        """
        raise Exception("TimeSeries read_dict not implemented")

    def read_last_value(
        self,
        measurement: str,
        tags: Optional[dict[str, Any]] = None,
        fields: Optional[list[str]] = None,
    ) -> dict[str, Any]:
        """Reads the last value from the database.

        Args:
            measurement (str): The name of the measurement (table) to query.
            tags (Optional[dict[str, Any]]): Tags to filter the data (as WHERE conditions). Defaults to None.
            fields (Optional[list[str]]): Specific fields to include in the result. Defaults to None.

        Returns:
            list[dict[str, Any]]: A list of records matching the query.

        Raises:
            Exception: If reading from the database fails.
        """
        raise Exception("TimeSeries read_last_value not implemented")

    def read_point(
        self,
        measurement: str,
        start_time: str,
        end_time: Optional[str] = None,
        tags: Optional[dict[str, Any]] = None,
        fields: Optional[list[str]] = None,
    ) -> list[Measurement]:
        """Reads records from the database and returns them as Point objects.

        Args:
            measurement (str): The name of the measurement (table) to query.
            start_time (str): The start time for the query (ISO8601 format).
            end_time (Optional[str]): The end time for the query (ISO8601 format). Defaults to None.
            tags (Optional[Dict[str, Any]]): Tags to filter the data (as WHERE conditions). Defaults to None.
            fields (Optional[list[str]]): Specific fields to include in the result. Defaults to None.

        Returns:
            List[Point]: A list of Point objects matching the query.

        Raises:
            Exception: If reading from the database fails.
        """
        raise Exception("TimeSeries read_point not implemented")

    @abstractmethod
    def measurement(self, measurement: str) -> Measurement:
        """Create new measurement.

        Args:
            measurement (str): The name of the measurement (table) to query.

        Returns:
            Measurement

        Raises:
            NotImplementedError: If this method is not implemented by the subclass.
        """
        raise NotImplementedError("Measurement not implemented")

    @override
    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = super().to_dict()
        data["_timeseries"] = {}
        attributes = ["host", "org", "database", "token"]
        for attr in attributes:
            if getattr(self, attr) != getattr(type(self), attr):
                data["_timeseries"][attr] = getattr(self, attr)
        return data

    @override
    def from_dict(self, data_dict: dict[str, Any]) -> None:
        super().from_dict(data_dict)
        for key, value in data_dict["_timeseries"].items():
            setattr(self, key, value)
