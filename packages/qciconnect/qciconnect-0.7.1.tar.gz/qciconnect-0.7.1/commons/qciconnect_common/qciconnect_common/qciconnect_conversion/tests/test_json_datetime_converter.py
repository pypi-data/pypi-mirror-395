"""Unit tests for JSONDateTimeConverter class."""

from datetime import UTC, datetime, timedelta

import pytest
from qciconnect_common.qciconnect_conversion.json_conversion import JSONDateTimeConverter

conv = JSONDateTimeConverter()


class TestJSONDateTimeConverter:
    """Tests for JSONDateTimeConverter class."""

    @pytest.mark.parametrize(
        ("datetime_input", "datetime_json_input"),
        [
            (
                datetime(2020, 2, 2),
                "2020-02-02T00:00:00.000000",
            ),
            (
                datetime(2020, 2, 2, hour=1, minute=2, second=3),
                "2020-02-02T01:02:03.000000",
            ),
            (
                datetime(2020, 2, 29, hour=1, minute=2, second=3, microsecond=4),
                "2020-02-29T01:02:03.000004",
            ),
            (
                datetime(2020, 2, 29, hour=1, minute=2, second=3, microsecond=4, tzinfo=UTC),
                "2020-02-29T01:02:03.000004",
            ),
        ],
    )
    def test_datetime_to_json_datetime(self, datetime_input: datetime, datetime_json_input: str):
        """Test conversion of Python datetime object to JSON compatible string.

        Args:
            datetime_input (datetime): Python datetime input.
            datetime_json_input (str): Expected JSON compatible output.
        """
        converted_input = conv.datetime_to_json_datetime(datetime_input)
        assert converted_input == datetime_json_input

    @pytest.mark.parametrize(
        ("timedelta_input", "timedelta_json_input"),
        [
            (
                timedelta(microseconds=1),
                "1e-06",
            ),
            (
                timedelta(milliseconds=1),
                "0.001",
            ),
            (
                timedelta(seconds=1),
                "1.0",
            ),
            (
                timedelta(minutes=1),
                "60.0",
            ),
            (
                timedelta(hours=1),
                "3600.0",
            ),
            (
                timedelta(days=1),
                "86400.0",
            ),
            (
                timedelta(weeks=1),
                "604800.0",
            ),
        ],
    )
    def test_timedelta_to_json(self, timedelta_input: timedelta, timedelta_json_input: str):
        """Test conversion of Python datetime.timedelta to JSON compatible value in seconds.

        Args:
            timedelta_input (_type_): Python datetime.timedelta input.
            timedelta_json_input (str): JSON compatible float (as string).
        """
        converted_input = conv.timedelta_to_json(timedelta_input)
        assert converted_input == timedelta_json_input
