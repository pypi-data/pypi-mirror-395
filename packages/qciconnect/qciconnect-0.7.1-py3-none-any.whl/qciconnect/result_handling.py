"""Module for handling results from QciConnectClient."""
import contextlib
import json

import numpy as np
from hequate_common.models import CompilerTaskResult, QPUTaskResult

from .client import QciConnectClient
from .exceptions import ResultError
from .utils import timestamp_to_datetime


class CompilerResult:
    """Result of a compile job.

    Attributes:
    :`compiled_circuits`: list of compiled circuits.

    """

    _compiler_task_result: CompilerTaskResult
    compiled_circuits: list

    def __getattr__(self, attribute):
        """Redirects retrieval of attributes to _compiler_task_result and hides pydantic noise.

        Args:
        :`attribute`: Name of attribute to get.

        Returns: attribute.

        """
        if attribute != "compiled_circuits":
            return getattr(self._compiler_task_result, attribute)
        else:
            return self.compiled_circuits

    def __dir__(self):
        """Fixes autocompletion and hides pydantic noise."""
        dir_output = list(self._compiler_task_result.model_fields_set)
        dir_output.append("compiled_circuits")
        dir_output.remove("compiled_circuit")
        return dir_output

    @classmethod
    def from_compiler_task_result(cls, result: CompilerTaskResult):
        """Creates `CompilerResult` from `CompilerTaskResult`.

        Args:
        :`result`: compiler task result to create compiler result from.

        Returns: Compiler result

        """
        compiler_result = cls()
        compiler_result._compiler_task_result = result
        if isinstance(result.compiled_circuit, list):
            compiler_result.compiled_circuits = result.compiled_circuit
        else:
            compiler_result.compiled_circuits = [result.compiled_circuit]
        return compiler_result


class BackendResult:
    """On successful execution of a QPU task, a `BackendResult` is returned.

    Attributes:
    :`data`:            Measurement data - can be a list of bit strings or state vector.
    :`meta_data`:       Metadata of the result.
    :`status_message`:  Status message of the job.
    :`status`:          Status of the job. Can be "SUCCESS", "FAILURE", "RUNNING" or "PENDING"(?)
    :`start_date_time`: Start time of the job. 
    :`end_date_time`:   End time of the job.
    :`total_runtime`:   Total runtime of the job.

    """

    _qpu_task_result: QPUTaskResult

    def __getattr__(self, attribute):
        """Redirects retrieval of attributes to `_qpu_task_result` and hides pydantic noise.

        Args:
        :`attribute`: Name of attribute to get.

        Returns: attribute.

        """
        return getattr(self._qpu_task_result, attribute)

    def __dir__(self):
        """Fixes autocompletion and hides pydantic noise."""
        return list(self._qpu_task_result.model_fields_set)

    @classmethod
    def from_qpu_task_result(cls, result: QPUTaskResult):
        """Creates `BackendResult` from `QPUTaskResult`.

        Args:
        :`result`: QPU task result to create backend result from.

        Returns: backend result

        """
        backend_result = cls()
        backend_result._qpu_task_result = result

        if isinstance(backend_result._qpu_task_result.data, str):
            backend_result._qpu_task_result.data = json.loads(backend_result._qpu_task_result.data)

        if type(backend_result._qpu_task_result.data) is dict:
            # See whether the data is a dictionary of real valued numpy arrays
            # (e.g. for "sampling" primitive)
            with contextlib.suppress(Exception):
                backend_result._qpu_task_result.data = {
                    key: np.ndarray(value)
                    for key, value in backend_result._qpu_task_result.data.items()
                }

            # Otherwise, convert to complex numbers
            # (e.g. necessary for "quantum_state" primitive)
            with contextlib.suppress(Exception):
                backend_result._qpu_task_result.data = {
                    key: complex(value)
                    for key, value in backend_result._qpu_task_result.data.items()
                }

        elif type(backend_result._qpu_task_result.data) is list:
            with contextlib.suppress(Exception):
                backend_result._qpu_task_result.data = np.ndarray(
                    backend_result._qpu_task_result.data
                )

        else:
            raise ResultError(
                f"Unexpected data type of backend_result._qpu_task_result.data: "
                f"{type(backend_result._qpu_task_result.data)}"
            )

        try:
            backend_result._qpu_task_result.start_date_time = timestamp_to_datetime(
                backend_result._qpu_task_result.start_date_time
            )
            backend_result._qpu_task_result.end_date_time = timestamp_to_datetime(
                backend_result._qpu_task_result.end_date_time
            )
        except Exception: # noqa: BLE001
            pass

        return backend_result


class FutureResult:
    """The `FutureResult` object can be used to poll/retrieve the result of a job."""

    def __init__(self, job_id: str, client: QciConnectClient):
        """Initialize the FutureResult object."""
        self._client = client
        self._job_id = job_id
        self._result = None
        self.update()

    @property
    def job_id(self) -> str:
        """Returns the job ID of the job."""
        return self._job_id

    @property
    def status(self) -> str:
        """Returns the current status of the job. Updates status and result if necessary."""
        if not self._result:
            self.update()
        return self._status

    def update(self):
        """Updates status of the job and retrieves result if job has finished."""
        self._status = self._client.get_job_status(self._job_id)
        self._result = self._client.retrieve_result(self._job_id)


class FutureBackendResult(FutureResult):
    """If a QPU task is submitted with `wait_for_result == False`, a `FutureBackendResult` is returned instead of a `BackendResult`.

    The `FutureBackendResult` is a promise that can be used to poll and later retrieve the
    result of an job. It has the following attributes:

    :`job_id`: Job ID of the submitted job.
    :`status`: Indicates current status of the job.

    The `update` method updates status of the job and retrieves result if job has finished.

    """ #noqa: E501
    @property
    def result(self) -> BackendResult | None:
        """The `result` method returns `BackendResult` if ready, `None` otherwise."""
        if not self._result:
            self.update()
        if self._result:
            return BackendResult.from_qpu_task_result(self._result.last_qpu_result)
        return None


class FutureCompilerResult(FutureResult):
    """Future result for compiler tasks."""
    @property
    def result(self) -> CompilerResult | None:
        """Updates future and returns `CompilerResult` if ready.

        Returns: BackendResult object.

        """
        if not self._result:
            self.update()
        if self._result:
            return CompilerResult.from_compiler_task_result(self._result.last_compiler_result)
        return None


class Results(dict):
    """The dictionary-like `Results` class serves as history of past results.

    The results dictionary is indexed by job ID, so you can access a past result as follows:

        result = client.results["job_id"]

    Depending on the type of the job, the `result` object is either a `BackendResult` or a
    `CompilerResult`.
    """
    def __init__(self, client: QciConnectClient):
        """Initialize the Results object with a `QciConnectClient` instance."""
        super().__init__(self)
        self._client = client

    def __dir__(self):
        """Update the results dictionary with the latest jobs from the server."""
        self._update_results()
        return super().__dir__()

    def _update_results(self):
        super().clear()
        jobs = self._client.get_jobs()
        for job in jobs:
            self._update_result(job)

    def _update_result(self, job):
        if job["status"] == "SUCCESS":
            job_id = job["job_id"]
            if job["last_compiler_task"] is not None:
                super().__setitem__(job_id, CompilerResult)
            if job["last_qpu_task"] is not None:
                super().__setitem__(job_id, BackendResult)

    def __getitem__(self, key: str) -> BackendResult | CompilerResult | None:
        """Get the result for a given job ID."""
        if key not in self:
            job = self._client.get_job(key)
            job["job_id"] = key
            self._update_result(job)
        if key not in self:
            return None

        if super().__getitem__(key) == BackendResult:
            super().__setitem__(
                key,
                BackendResult.from_qpu_task_result(
                    self._client.retrieve_result(key).last_qpu_result
                ),
            )
        elif super().__getitem__(key) == CompilerResult:
            super().__setitem__(
                key,
                CompilerResult.from_compiler_task_result(
                    self._client.retrieve_result(key).last_compiler_result
                ),
            )
        return super().__getitem__(key)

    def refresh(self):
        """Call the `refresh` method, when you need to refresh the results dictionary with the latest results from the server.
        """ #noqa: E501
        self._update_results()
