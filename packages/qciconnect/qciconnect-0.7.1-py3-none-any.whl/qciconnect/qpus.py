"""The Qpu class represents a quantum circuit processing unit (real device or simulator)."""
import itertools
import re
import textwrap
from pprint import pprint

from pydantic import ValidationError as PydanticValidationError
from tabulate import tabulate
from typeguard import typechecked

from qciconnect.exceptions import QciConnectClientError

from .client import BackendJob, QciConnectClient
from .result_handling import BackendResult, FutureBackendResult


class Qpu:
    """The `Qpu` class encapsulates access to a quantum processing unit (QPU).
    Use its methods to query properties and submit quantum circuits for execution.

    To view a QPU's properties and current status, call the show method.
    Programmatically, access its attributes directly:

    :`alias`:               The name of the QPU that is used for programmatic access
    :`manufacturer`:        The manufacturer of the QPU.
    :`qubit_count`:         The number of qubits in the QPU.
    :`technology`:          The QPU's base technology, like trapped ions, NV centers etc.
    :`native_gate_set`:     The set of gates that are natively supported by hardware.
    :`accepted_gate_set`:   The set of gates that are accepted by the hardware.
                            This can be a superset of the  native gate set.
    :`status`:              The current status of the QPU, e.g., online, calibration, etc.
    :`gate_fidelities`:     A dictionary of gate names to their fidelities.
    :`qubit_connectivity`:  A dictionary representing the connectivity of qubits.
    :`description`:         A detailed description of the QPU.
    :`base_coupling_list`:  A list of tuples representing the coupling between
                            qubits that are supported by all native gates simultaneously.
    """
    def __init__(
        self,
        identifier: int,
        name: str,
        manufacturer: str,
        qubit_count: int,
        status: str,
        non_standard_gate_definitions_available: bool,
        qubit_connectivity: dict,
        technology: str,
        gate_set: dict,
        gate_fidelities: dict,
        access_for_current_user: bool,
        description: str,
        base_coupling_list: list,
        client: QciConnectClient,
    ):
        """Constructs a Qpu object.

        Args:
        :`identifier`:          Unique identifier of the quantum circuit processing unit.
        :`name`:                Name of the quantum circuit processing unit.
        :`manufacturer`:        Manufacturer of the quantum circuit processing unit.
        :`qubit_count`:         Number of qubits available on the QPU.
        :`status`:              Current operational status.
        :`non_standard_gate_definitions_available`: Is a respective file available.
        :`qubit_connectivity`:  Information on which qubits can interact
        :`technology`:          Base technology (ion trap, superconducting, etc.).
        :`gate_set`:            Native and/or accepted gate set of the QPU.
        :`gate_fidelities`:     Information on fidelities of supported gates (per qubit if available)
        :`access_for_current_user`: Is the current user allowed to use this QPU
        :`description`:         Vendor-provided high-level info in the QPU
        :`base_coupling_list`:  list of qubits that support all accepted gates
        :`client`:              Instance of QciConnectClient - QCI Connect RestAPI client.

        """ # noqa: E501
        self._id = identifier
        self._name = name
        self._alias = name.lower()\
            .replace(" ", "_")\
            .replace("-", "_")\
            .replace("(", "")\
            .replace(")", "")
        self._manufacturer = manufacturer
        self._qubit_count = qubit_count
        self._status = status
        self._non_standard_gate_definitions_available = non_standard_gate_definitions_available
        self._technology = technology
        self._gate_set = gate_set
        self._gate_fidelities = gate_fidelities
        self._accepted_gate_set = {}
        self._native_gate_set = {}
        self._access_for_current_user = access_for_current_user
        self._description = description
        self._qubit_connectivity = Qpu._clean_qubit_connectivity(qubit_connectivity, qubit_count)
        self._base_coupling_list = base_coupling_list
        self._client = client

        if self._gate_fidelities and 'gate_fidelity_data' in self._gate_fidelities:
            self._gate_fidelities = self._gate_fidelities['gate_fidelity_data']
        else:
            self._gate_fidelities = {}

        self._clean_data_for_show()

    # make these properties accessible as read-only
    name = property(lambda self: self._name)
    alias = property(lambda self: self._alias)
    technology = property(lambda self: self._technology)
    status = property(lambda self: self._status)
    manufacturer = property(lambda self: self._manufacturer)
    qubit_count = property(lambda self: self._qubit_count)
    gate_fidelities = property(lambda self: self._gate_fidelities)
    gate_set = property(lambda self: self._gate_set)
    accepted_gate_set = property(lambda self: self._accepted_gate_set)
    native_gate_set = property(lambda self: self._native_gate_set)
    description = property(lambda self: self._description)
    qubit_connectivity = property(lambda self: self._qubit_connectivity)
    base_coupling = property(lambda self: self._base_coupling_list)

    @staticmethod
    def _clean_qubit_connectivity(raw_connectivity, qubit_count):
        """Bring connectivity to unified format, i.e. a connectivity list."""
        qubit_connectivity = {}
        if raw_connectivity is not None:
            for gate, gate_info in raw_connectivity.items():
                connectivity_list = []
                if gate_info['all_to_all_connectivity']:
                    for i, j in itertools.product(range(qubit_count), range(qubit_count)):
                        if i == j:
                            continue
                        connectivity_list.append([i, j])
                else:
                    connectivity_list = gate_info['coupling_list']

                qubit_connectivity[gate] = connectivity_list
        return qubit_connectivity

    def _clean_data_for_show(self):
        """Remove whitespace and line breaks from description. Provide gate set attributes."""
        if self._gate_set is not None:
            if "accepted_gate_set" in self._gate_set:
                self._accepted_gate_set = self._gate_set["accepted_gate_set"]
            if "native_gate_set" in self._gate_set:
                self._native_gate_set = self._gate_set["native_gate_set"]

        if self._description is not None:
            self._description = self._description.replace("\n", "")
            self._description = re.sub(r'\s+', ' ', self._description)


    @typechecked
    def submit(
        self,
        circuit: str,
        primitive: str,
        shots: int = 10000,
        wait_for_results: bool = True,
        name: str = "Hequate QPU Job",
        comment: str = "Issued via API",
        qpu_options: dict | None = None,
    ) -> FutureBackendResult | BackendResult | None:
        """To execute a quantum circuit on a QPU, use the submit method with the specified parameters:

        :`circuit`:             Quantum circuit to be executed (OpenQASM 3 string)
        :`primitive`:           Way of execution. Possible values: "sampling" or "quantum_state"
        :`shots`:               Number of runs/executions.
        :`wait_for_results`:    wait for the backend to finished the submitted job. Default: True
        :`comment`:             Optional string to further describe the job
        :`qpu_options`:         Additional options for the QPU.

        Depending on the value of `wait_for_results`, the method either returns:
        - `BackendResult` which is measurement data with a bunch of meta data or
        - `FutureBackendResult` which is a promise to later return a `BackendResult`

        Example:
            circuit = 'OPENQASM 3.0; include \"qelib1.inc\"; qreg q[2]; creg c[2]; h q[0]; ...'
            promise = qpu.submit(circuit, "sampling", 100, wait_for_results=False)
            result = promise.result()

        """ # noqa: E501
        if qpu_options is None:
            qpu_options = {}
        try:
            job = BackendJob(
                self._id,
                circuit,
                primitive,
                name=name,
                shots=shots,
                comment=comment,
                qpu_options=qpu_options
            )
        except (PydanticValidationError, ValueError) as e:
            print(e)
            return None

        if wait_for_results:
            try:
                result = self._client.submit_backend_job_and_wait(job)
                if result.last_qpu_result is None:
                    print("Job failed(?) - no result data available.")
                    return None
            except (QciConnectClientError, PydanticValidationError) as e:
                print(e)
                return None
            return BackendResult.from_qpu_task_result(result.last_qpu_result)
        else:
            try:
                job_id = self._client.submit_backend_job(job)
            except (QciConnectClientError, PydanticValidationError) as e:
                print(e)
                return None
            return FutureBackendResult(job_id, self._client)


    def __str__(self) -> str:
        """Returns a string representation of the QPU with its alias, qubit count, and status."""
        return f"Name: {self._alias}, #Qubits: {self.qubit_count}, Status: {self._status}"

    def get_qpu_info(self) -> list[str]:
        """Returns list containing QPU alias, #qubits, and status."""
        return [self._alias,
                str(self.qubit_count),
                self._status,
                self._technology,
                str(self._access_for_current_user)]

    def __dir__(self):
        """Returns a list of attributes and methods of the specific Qpu  (w/o dunders)."""
        method_list = []
        for attr in dir(self):
            if not attr.startswith("__"):
                method_list.append(attr)
        return method_list

    def show(self):
        """Prints a description of the QPU."""
        title = f"{self._name} by {self._manufacturer}"
        print(title)
        print("=" * len(title))
        print()
        print(textwrap.fill(self._description, width=80))
        print()
        print(f"Accessible to me: {self._access_for_current_user}")
        print()
        print(f"Technology: {self._technology}, Status: {self._status}")
        print()
        self._print_gate_sets()

        self._print_connectivity()

        self._print_gate_info()

    def _print_gate_sets(self):
        if self.accepted_gate_set is not None:
            print(
                textwrap.fill(f"Accepted gate set: {", ".join(self.accepted_gate_set)}", width=80))
            print()
        if self.native_gate_set is not None:
            print(textwrap.fill(f"Native gate set: {", ".join(self.native_gate_set)}", width=80))
            print()

    def _print_connectivity(self):
        print("Coupling information\n====================", end="\n\n")
        if self._base_coupling_list is None:
            print("No connectivity information available.", end="\n\n")
            return

        print("Base coupling:")
        self._plot_connectivity(self.qubit_count, self._base_coupling_list)
        print()
        for gate, connectivity_list in self.qubit_connectivity.items():
            if connectivity_list and len(connectivity_list) > 0:
                print(f"Gate connectivity: {gate}")
                self._plot_connectivity(self.qubit_count, connectivity_list)
                print()

    def _plot_connectivity(self, qubit_count, coupling_list):
        if not self.qubit_connectivity:
            print("No connectivity information available.")
            return

        if coupling_list and len(coupling_list[0]) > 2:
            pprint(coupling_list)
        else:
            for i, j in itertools.product(range(qubit_count), range(qubit_count)):
                if [i, j] in coupling_list:
                    print("* ", end="")
                else:
                    print("- ", end="")

                if j == self.qubit_count - 1:
                    print()

    def _print_gate_info(self):
        some_info_available = False
        if self._gate_fidelities is not None:
            print("Fidelities\n==========", end="\n\n")
            if 'comment' in self._gate_fidelities and\
                    self._gate_fidelities['comment'] is not None:
                some_info_available = True
                print(textwrap.fill(self._gate_fidelities['comment'], width=80))
                print()

            if self._gate_fidelities and 'gate_fidelity_data' in self._gate_fidelities:
                for gate, gate_info in self._gate_fidelities['gate_fidelity_data'].items():
                    print(f"Gate: {gate}")
                    if 'fidelity_description' in gate_info and \
                            gate_info['fidelity_description'] is not None:
                        some_info_available = True
                        print(textwrap.fill(f"Gate fidelity description: "
                                            f"{gate_info['fidelity_description']}", width=80))
                    if 'mean_fidelity' in gate_info and \
                            gate_info['mean_fidelity'] is not None:
                        some_info_available = True
                        print(textwrap.fill(f"Mean fidelity: {gate_info['mean_fidelity']}",
                                            width=80))
                    elif 'individual_fidelities' in gate_info and \
                            gate_info['individual_fidelities'] is not None:
                        some_info_available = True
                        count = len(gate_info['individual_fidelities'])
                        total = sum(gate_info['individual_fidelities'])
                        if count != 0:
                            print(textwrap.fill(f"Mean fidelity: {total / count}",
                                           width=80))
                    else:
                        print("Mean fidelity: not available", end="\n\n")
                    print()

        if not some_info_available:
            print("No fidelity information available.")

class QpuByAlias:
    """The `client.qpus` object provides an attribute for each available quantum processing unit (QPU),
    named after its alias.

    Interactively, use autocompletion or the `show` method to list available QPUs:

        client.qpus.show()

        Alias                    Qubits  Status       Technology             Accessible to me
        ---------------------  --------  -----------  ---------------------  ------------------
        qsea_i_digital_twin          10  idle         digital_twin           True
        dedalo                       64  coming_soon  photons                True
        qsea_ii                      20  coming_soon  trapped_ions           True
        comiqc                       50  coming_soon  solid_state_spins      True
    
    Programmatically, list and get access to QPUs (in this example QSea I Digital Twin)
    as follows:

        qpu_aliases = client.qpus.aliases() # list of available QPUs
        favorite_qpu = client.qpus["qsea_i_digital_twin"] 
        favorite_qpu = client.qpus.qsea_i_digital_twin # this is equivalent to the previous line

    """ # noqa: E501

    def __init__(self, client: QciConnectClient):
        """Constructs a dict of QPUs available on the platform (indexed by their aliases).

        Args:
        :`qpu_list`:    list of QPUTable objects.
        :`client`:      Instance of QciConnectClient - QCI Connect RestAPI client.

        """
        self._client = client
        self._update_qpu_dict()

    def _update_qpu_dict(self):
        qpu_list = self._client.get_available_qpus()
        self._qpus = {}
        for qpu_entry in qpu_list:
            qpu = Qpu(
                identifier=qpu_entry["qpu_id"],
                name=qpu_entry["name"],
                manufacturer=qpu_entry["manufacturer"],
                qubit_count=qpu_entry["number_of_qubits_available"],
                status=qpu_entry["status"],
                non_standard_gate_definitions_available=\
                    qpu_entry["non_standard_gate_definitions_available"],
                qubit_connectivity=qpu_entry["qubit_connectivity"],
                technology=qpu_entry["technology"],
                gate_set=qpu_entry["gate_set"],
                gate_fidelities=qpu_entry["gate_fidelities"],
                access_for_current_user=qpu_entry["access_for_current_user"],
                description=qpu_entry["description"],
                base_coupling_list=qpu_entry["base_coupling_list"],
                client=self._client,
            )
            self._qpus[qpu._alias] = qpu

    def __getattr__(self, name) -> Qpu | None:
        """Returns a Qpu object if it exists, otherwise None."""
        try:
            return self._qpus.__getitem__(name)
        except KeyError as e:
            print(e)
            return None

    def __dir__(self):
        """Returns a list of QPUs and other attributes."""
        extended_key_list = list(self._qpus.keys()) + list(super().__dir__())
        return extended_key_list

    def show(self):
        """Prints table of available QPUs including their qubit counts and status."""
        self._update_qpu_dict()
        all_qpu_info = []
        for qpu in self._qpus.values():
            all_qpu_info.append(qpu.get_qpu_info())

        print(tabulate(all_qpu_info,
                       headers=["Alias",
                                "Qubits",
                                "Status",
                                "Technology",
                                "Accessible to me"]))


