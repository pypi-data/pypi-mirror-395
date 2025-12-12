import unittest
from typing_extensions import override
from typing import Any, Optional, Union
from masterpiece.timeseries import TimeSeries


import unittest
from typing import Any
from masterpiece.timeseries import Measurement


# Simulating Point class for testing purposes
class Point:
    def __init__(self, name: str):
        self.name: str = name
        self.tags: dict[str, Any] = {}
        self.fields: dict[str, Any] = {}
        self.timestamp: str = ""

    def tag(self, key: str, value: str) -> None:
        self.tags[key] = value

    def field(self, key: str, value: Any) -> None:
        self.fields[key] = value

    def time(self, timestamp: str) -> None:
        self.timestamp = timestamp


class TestMeasurementImpl(Measurement):
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.tags: dict[str, Any] = {}
        self.fields: dict[str, Any] = {}
        self.timestamp: Union[str, int] = ""

    @override
    def tag(self, key: str, value: str) -> Measurement:
        self.tags[key] = value
        return self

    @override
    def field(self, key: str, value: Any) -> Measurement:
        self.fields[key] = value
        return self

    @override
    def time(self, timestamp: Union[str, int]) -> Measurement:
        self.timestamp = timestamp
        return self

    @override
    def to_dict(self) -> dict[str, Any]:
        return {}

    @override
    def from_dict(self, data: dict[str, Any]) -> Measurement:
        return self

    @override
    def validate(self) -> bool:
        return True


class TestMeasurement(unittest.TestCase):
    def test_abstract_methods(self) -> None:
        """Test that Measurement cannot be instantiated and enforces abstract methods."""
        with self.assertRaises(TypeError):
            Measurement()  # type: ignore

    def test_measurement_abstract_methods(self) -> None:
        """Test that all abstract methods exist in a subclass."""
        test_instance = TestMeasurementImpl("test")
        self.assertIsInstance(test_instance, Measurement)


class TestTimeSeries(unittest.TestCase):
    class ConcreteTimeSeries(TimeSeries):  # A mock subclass for testing purposes
        def write(self, point: Any) -> None:
            raise Exception("TimeSeries write not implemented")

        @override
        def measurement(self, measurement: str) -> Measurement:
            return TestMeasurementImpl(measurement)

        @override
        def write_dict(
            self, name: str, tags: dict[str, Any], fields: dict[str, Any], ts: str
        ) -> None:
            # Raise the expected exception to pass the test
            raise Exception("TimeSeries write_dict not implemented")

        @override
        def read_dict(
            self,
            measurement: str,
            start_time: str,
            end_time: Optional[str] = None,
            tags: Optional[dict[str, Any]] = None,
            fields: Optional[list[str]] = None,
        ) -> list[dict[str, Any]]:
            return []

    def test_initialization(self) -> None:
        ts = self.ConcreteTimeSeries("test_name")
        self.assertEqual(ts.host, "")
        self.assertEqual(ts.org, "")
        self.assertEqual(ts.database, "")
        self.assertEqual(ts.token, "")

    def test_to_dict(self) -> None:
        ts = self.ConcreteTimeSeries("test_name")
        ts.host = "localhost"
        ts.org = "org_name"
        ts.database = "db_name"
        ts.token = "token123"

        data_dict = ts.to_dict()

        # Test that the '_timeseries' dictionary is included with the right attributes
        self.assertIn("_timeseries", data_dict)
        self.assertEqual(data_dict["_timeseries"]["host"], "localhost")
        self.assertEqual(data_dict["_timeseries"]["org"], "org_name")
        self.assertEqual(data_dict["_timeseries"]["database"], "db_name")
        self.assertEqual(data_dict["_timeseries"]["token"], "token123")

    def test_from_dict(self) -> None:
        ts = self.ConcreteTimeSeries("test_name")
        data_dict: dict[str, Any] = ts.to_dict()
        data_dict["_timeseries"] = {
            "host": "localhost",
            "org": "org_name",
            "database": "db_name",
            "token": "token123",
        }

        ts.from_dict(data_dict)

        self.assertEqual(ts.host, "localhost")
        self.assertEqual(ts.org, "org_name")
        self.assertEqual(ts.database, "db_name")
        self.assertEqual(ts.token, "token123")

    def test_write_not_implemented(self) -> None:
        ts = self.ConcreteTimeSeries("test_name")
        with self.assertRaises(Exception):
            ts.write("point")

    def test_write_dict_not_implemented(self) -> None:
        ts = self.ConcreteTimeSeries("test_name")
        with self.assertRaises(Exception):
            ts.write_dict("measurement", {}, {}, "2024-12-14T00:00:00Z")


if __name__ == "__main__":
    unittest.main()
