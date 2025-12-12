"""This module uses https requests to communicate with QCIConnect platform.

Its main class QciConnectClient provides methods to query several REST endpoints.
"""

import json
import time

import httpx
from hequate_common.models import (
    CompilerTaskBase,
    JobResult,
    JobSubmission,
    Primitive,
    QPUOptions,
    QPUTaskBase,
)

from .exceptions import QciConnectClientError
from .token_managers import DummyTokenManager, QciConnectTokenManager


class CompilerJob:
    """Class used to hand over the compile jobs to QciConnectClient."""

    def __init__(self, compiler_id: int, compilation_pass: str, options: dict, circuits: dict):
        """Constructor of CompilerJob class."""
        self.task = CompilerTaskBase(
            compiler_id=compiler_id, compilation_pass=compilation_pass, options=options
        )
        self.circuits = circuits


class BackendJob:
    """Class used to hand over the qpu jobs to QciConnectClient."""

    def __init__(
        self,
        backend_id: int,
        circuit: str,
        primitive: str,
        name: str = "Hequate Client Job",
        comment: str = "Issued via API",
        shots: int = 10000,
        qpu_options: dict | None=None,
    ):
        """Initializer of BackendJob class.

        Arguments:
            backend_id: ID that uniquely identifies the backend to be used
            circuit: a string that comprises an OpenQASM 3 circuit.
            primitive: "sampling" or "quantum_state"
            name: Optional name of the job
            comment: Optional string further describing the job
            shots: number of shots
            qpu_options: Additional options for the QPU
        """
        if qpu_options is None:
            qpu_options = {"coupling_map": None, "basis_gates": None}
        self.name = name
        self.comment = comment
        self.circuit = circuit
        self.task = QPUTaskBase(
            qpu_id=backend_id,
            total_shots=shots,
            primitive=Primitive(primitive),
            qpu_options=QPUOptions(**qpu_options),
        )

API_VERSION = "/v1"
class QciConnectClient:
    """Client for QCI Connect frontend RestAPI.

    Handles http get/put/post requests to retrieve available compilers/QPUs
    and to submit jobs to these resources.

    Attributes:
        _server_address: Address of the platform.
        _token_manager: Authorization token manager.
    """

    def __init__(self, /, 
        server_address: str, *, 
        username: str | None = None, password: str | None = None, token: str | None = None):
        """Constructs QciConnectClient object.

        Args:
            server_address: Address of the platform.
            username: username for authentication.
            password: password for authentication.
            token: personal access token created on QCI Connect website
        """
        self._username = username
        self._password = password
        self._token = token
        self.server_address = (
            server_address  # setting this also creates a TokenManager object
        )

        if isinstance(self._token_manager, DummyTokenManager):
            self._init_endpoints("")
        else:
            self._init_endpoints(API_VERSION)

    @property
    def server_address(self) -> str:
        """Returns the current server address."""
        return self._server_address

    @server_address.setter
    def server_address(self, value: str):
        """Sets the server address.

        Args:
            value: Server address.
        """
        value = value.rstrip("/")
        self._server_address = value
        if self._username is None and self._password is None and self._token is None:
            self._token_manager = DummyTokenManager()
        elif self._username is not None and self._password is not None:
            raise QciConnectClientError("Using username/password is no longer  supported. Generate "
                                        "a personal access token via the web interface.")
        elif self._username is None and self._password is None and self._token is not None:
            self._token_manager = QciConnectTokenManager(self._token)
        elif self._username is not None and \
             self._password is not None and \
             self._token is not None:
             raise QciConnectClientError("Using username/password together with personal "
                "access token is not supported. If possible, use token only.")
        else:
            raise QciConnectClientError("Error determining the token manager to be used.")

    def _init_endpoints(self, api_version):
        """Initialize API endpoints."""
        self._endpoints = {
            "JOB_LIST_ENDPOINT": "/api" + api_version + "/job/",
            "JOB_SUBMIT_ENDPOINT": "/api" + api_version + "/job/submit",
            "JOB_RESULT_ENDPOINT": "/api" + api_version + "/result/",
            "COMPILER_LIST_ENDPOINT": "/api" + api_version + "/compiler/all",
            "QPU_LIST_ENDPOINT": "/api" + api_version + "/qpu/all",
            "TAC_STATUS_ENDPOINT": "/api" + api_version + "/terms_and_conditions/status",
            "PRIVACY_NOTICE_ENDPOINT": "/api" + api_version + "/privacy_notice/status",
        }

    def _handle_http_status_error(self, errh):
        """Handles HTTP errors.

        Args:
            errh: HTTP error to be handled.
        """
        error_dict = json.loads(errh.response.text)
        if errh.response.status_code == 301:
            # Handle the 301 status code
            raise QciConnectClientError(
                 'Received a 301 status code. '
                f'The requested resource has been permanently moved: "{error_dict["detail"]}"'
            )
        elif errh.response.status_code == 401:
            # Handle the 401 status code
            raise QciConnectClientError(
                 'Received a 401 status code. '
                f'The request was unauthorized: "{error_dict["detail"]}"'
            )
        elif errh.response.status_code == 403:
            # Handle the 403 status code
            raise QciConnectClientError(
                 'Received a 403 status code. '
                f'The request was forbidden: "{error_dict["detail"]}"'
            )
        else:
            # Handle other HTTP errors - print information about the error in a nicely formatted way
            error_detail = error_dict["detail"]
            raise QciConnectClientError(
                f"HTTP Error ({errh.response.status_code}) occurred: {error_detail}"
            )

    def _post(self, request: dict) -> None | str:
        """Sends a post request to the platform and returns the respective job ID.

        Args:
            request: JSON request as a dict.

        Returns: job ID.
        """
        headers = {"Content-Type": "application/json", "Connection": "keep-alive"}
        headers = self._token_manager.add_auth_header(headers)

        with httpx.Client(follow_redirects=False, verify=True, timeout=None) as client:
            try:
                post_response = client.post(
                    f"{self._server_address}{self._endpoints['JOB_SUBMIT_ENDPOINT']}", 
                    json=request,
                    headers=headers
                )
                post_response.raise_for_status()
                job_id = post_response.json()
                print(f"Job submitted with ID: {job_id}")
                return str(job_id)
            except httpx.RequestError as e:
                raise QciConnectClientError(
                    f"A RequestError occurred while sending a post-request to URL: "
                    f"{e.request.url} - {e}"
                ) from e
            except httpx.HTTPStatusError as e:
                self._handle_http_status_error(e)

    def _job_id_to_result_endpoint(self, job_id: str) -> str:
        """Converts a job ID to the respective result endpoint.

        Args:
            job_id: Job ID to be converted.

        Returns: URL to the respective result endpoint.
        """
        return f"{self._server_address}{self._endpoints['JOB_RESULT_ENDPOINT']}{job_id}"

    def _job_id_to_job_endpoint(self, job_id: str) -> str:
        """Converts a job ID to the respective result endpoint.

        Args:
            job_id: Job ID to be converted.

        Returns: URL to the respective result endpoint.
        """
        return f"{self._server_address}{self._endpoints['JOB_LIST_ENDPOINT']}{job_id}"

    def _get(self, get_url: str) -> dict | list[dict]:
        """Sends a get request for a given URL.

        Args:
            get_url: URL to which a get request is sent.

        Returns: JSON response in form of a dict.
        """
        headers = {"Content-Type": "application/json", "Connection": "keep-alive"}
        headers = self._token_manager.add_auth_header(headers)

        with httpx.Client(follow_redirects=False, verify=True, timeout=None) as client:
            try:
                get_response = client.get(get_url, headers=headers)
                get_response.raise_for_status()
                payload = get_response.json()
                return payload # noqa: TRY300
            except httpx.HTTPStatusError as errh:
                self._handle_http_status_error(errh)
            except httpx.ConnectError as e:
                raise QciConnectClientError(f"Can't connect to server {get_url}") from e
            except httpx.RequestError as e:
                raise QciConnectClientError(
                    f"A RequestError occurred while sending a get-request to URL: "
                    f"{e.request.url} - {e}."
                ) from e
            except Exception as e:
                # Handle other exceptions
                raise QciConnectClientError(f"An error occurred: {e}") from e

    def _sanitize_circuit(self, circuit: str) -> str:
        """Sanitizes the circuit.

        Args:
            circuit: Circuit to be sanitized.

        Returns: Sanitized circuit.
        """
        if type(circuit) is not str:
            raise QciConnectClientError("Circuit must be a string.")

        circuit = circuit.replace("OPENQASM 2.0;", "")
        circuit = circuit.replace('include "qelib1.inc";', 'include "stdgates.inc";')

        return circuit

    def submit_compiler_job(self, compiler_job: CompilerJob):
        """Submits a compiler job.

        Args:
            compiler_job: Quantum circuit(s) and information about the compiler pass to be used.

        Returns: id identifying the job just submitted.
        """
        circuit = next(iter(compiler_job.circuits.values()))
        circuit = self._sanitize_circuit(circuit)

        request = JobSubmission(
            circuit=circuit,
            name="Hequate Client Compile Job",
            comment="Issued via API",
            tasks=[compiler_job.task],
        )

        job_id = self._post(request.model_dump())
        return job_id

    def _has_job_finished(self, response: dict) -> bool:
        """Interprets the status message.

        Args:
            response: dictionary that contains status message to be interpreted.
        """
        if response["status"] == "SUCCESS":
            print("Job was successful.")
            return True
        elif response["status"] == "FAILURE":
            try:
                print(f"{response['status_message']}")
            except KeyError:
                print("Job failed.")
            return True
        else:
            print("Job is not finished yet.")
            return False

    def get_job_status(self, job_id: str) -> str:
        """Gets the status of a job.

        Args:
            job_id: id of job which status shall be returned.

        Returns: string telling the status of the job.
        """
        endpoint_url = self._job_id_to_result_endpoint(job_id)
        response = self._get(endpoint_url)
        return response["status"]

    def get_job(self, job_id: str) -> dict:
        """Queries the job endpoint to return the info on a specific job.

        Args:
            job_id: UID that defines the job to be queried.

        Returns:
            dict with information on the given job
        """
        endpoint_url = self._job_id_to_job_endpoint(job_id)
        return self._get(endpoint_url)

    def retrieve_result(self, job_id: str) -> JobResult | None:
        """Retrieves the result of a job by its job ID.

        Args:
            job_id: string with the job's UID

        Returns:
            JobResult object
        """
        endpoint_url = self._job_id_to_result_endpoint(job_id)
        response = self._get(endpoint_url)
        if self._has_job_finished(response):
            result = JobResult.model_validate(response)
            return result
        else:
            return None

    def wait_and_call_method(self, timeout, method, *params):
        """Calls `method` every 5 seconds until it returns not None or timeout is exceeded.

        Args:
            timeout: timeout in seconds. An exception is raised when the `method` does not
                     return a value in that time.
            method: the function or method to be called
            params: parameters for the function or method to be called.

        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            result = method(*params)
            if result is not None:
                return result
            time.sleep(5)
        raise QciConnectClientError("Timeout occurred while waiting for job result.")

    def submit_compiler_job_and_wait(self, compiler_job: CompilerJob, timeout=3600) -> JobResult:
        """Submits a compiler job and waits for the result.

        Args:
            compiler_job: Quantum circuit(s) and information about the compiler pass to be used.
            timeout: Timeout in seconds.

        Returns: JobResult which is compiled quantum circuit(s) and a bunch of meta information.
        """
        job_id = self.submit_compiler_job(compiler_job)
        result = self.wait_and_call_method(timeout, self.retrieve_result, job_id)
        return result

    def submit_backend_job(self, backend_job: BackendJob) -> str:
        """Submits a quantum circuit processing job.

        Args:
            backend_job: Quantum circuit and information about the QPU it should run on (and how).

        Returns: id identifying the job just submitted.
        """
        circuit = self._sanitize_circuit(backend_job.circuit)

        request = JobSubmission(
            circuit=circuit,
            primitive=backend_job.task.primitive,
            name=backend_job.name,
            comment=backend_job.comment,
            tasks=[backend_job.task],
        )

        job_id = self._post(request.model_dump())
        return job_id

    def submit_backend_job_and_wait(
        self, backend_job: BackendJob, timeout: int = 3600
    ) -> JobResult:
        """Submits a quantum circuit processing job and waits for the result.

        Args:
            backend_job: Quantum circuit and information about the QPU it should run on (and how).
            timeout: Timeout in seconds.

        Returns: JobResult which is measurement data and a bunch of meta information.
        """
        job_id = self.submit_backend_job(backend_job)
        result = self.wait_and_call_method(timeout, self.retrieve_result, job_id)
        return result

    def get_available_compilers(self) -> list:
        """Retrieves list of compilers available on the platform."""
        endpoint_url = f"{self._server_address}{self._endpoints['COMPILER_LIST_ENDPOINT']}"
        return self._get(endpoint_url)

    def get_available_qpus(self) -> list[dict]:
        """Retrieves list of QPUs available on the platform."""
        endpoint_url = f"{self._server_address}{self._endpoints['QPU_LIST_ENDPOINT']}"
        result = self._get(endpoint_url)
        return result

    def get_jobs(self) -> list[dict]:
        """Retrieves list of jobs available in the platform database."""
        endpoint_url = f"{self._server_address}{self._endpoints['JOB_LIST_ENDPOINT']}"
        return self._get(endpoint_url)

    def get_tac_status(self) -> bool:
        """Retrieves status of terms and conditions acceptance."""
        endpoint_url = f"{self._server_address}{self._endpoints['TAC_STATUS_ENDPOINT']}"
        return self._get(endpoint_url)

    def get_privacy_notice_status(self) -> bool:
        """Retrieves status of privacy notice acceptance."""
        endpoint_url = f"{self._server_address}{self._endpoints['PRIVACY_NOTICE_ENDPOINT']}"
        return self._get(endpoint_url)
