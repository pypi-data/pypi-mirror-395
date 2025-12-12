"""Provides Result object containing result related data for hanling in Celery."""

from datetime import datetime, timedelta
from typing import Any

from qciconnect_conversion.json_conversion import JSONDateTimeConverter, JSONNumpyConverter
from sqlmodel import SQLModel


class ResultForCelery(SQLModel):
    """Contains all result data, meta data that should be fetched by orchestrator.

    Args:
        SQLModel: Class inherits from SQLModel
    """

    data: Any | None
    result_metadata: dict[str, Any] | None
    compiled_circuit: str | None
    start_date: datetime
    end_date: datetime
    status: str | None
    status_message: str | None
    total_run_time: timedelta

    def __init__(self, **data) -> None:
        """Initializes Result with all relevant data."""
        super().__init__(**data)

    def _convert_data(self, data_nparray: Any) -> Any:
        data = JSONNumpyConverter.nparray_to_json_list(data_nparray)
        return data

    def convert_to_json_for_celery(self) -> Any:
        """Converts Result object to JSON.

        Returns:
            JSON: JSON equivalent of result.
        """
        result_dict = {
            "meta_data": self.result_metadata,
            "compiled_circuit": self.compiled_circuit,
            "start_date_time": JSONDateTimeConverter.datetime_to_json_datetime(self.start_date),
            "end_date_time": JSONDateTimeConverter.datetime_to_json_datetime(self.end_date),
            "total_run_time": JSONDateTimeConverter.timedelta_to_json(self.total_run_time),
            "status": self.status,
            "status_message": self.status_message,
            "data": self._convert_data(self.data),
        }
        result_json = JSONNumpyConverter.dict_to_json(result_dict)
        return result_json
