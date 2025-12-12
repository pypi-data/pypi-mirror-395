import ast
import gzip
import json
import math
from pathlib import Path
from typing import Any

from qiskit import QuantumCircuit, transpile
from qiskit.transpiler import (
    CouplingMap,
    InstructionDurations,
    InstructionProperties,
    Target,
)

# Import BackendV1 for type hinting if available (Qiskit 1.x)
try:
    from qiskit.providers import BackendV1

    HAS_BACKEND_V1 = True
except ImportError:
    HAS_BACKEND_V1 = False


# Mock classes for Qiskit 1.x configuration and properties


class MockGateConfig:
    """Mock GateConfig for Qiskit 1.x BackendV1 compatibility."""

    def __init__(self, name: str, num_qubits: int, parameters: list[str] | None = None):
        self.name = name
        self.num_qubits = num_qubits
        self.parameters = parameters if parameters is not None else []
        self.qasm_def = None  # Not strictly required for transpiler, but common


class MockBackendConfiguration:
    def __init__(self, backend_data: dict):
        self.backend_name = backend_data["backend_name"]
        self.num_qubits = backend_data["num_qubits"]
        self.dt = backend_data.get("dt")
        self.max_shots = backend_data.get("max_shots", 100000)
        self.backend_version = "offline"
        self.simulator = False  # Assume it's a real device config

        # Filter basis gates to only include standard gates
        all_operations = backend_data.get(
            "basis_gates", backend_data["operation_names"]
        )
        standard_operations = {
            "sx",
            "x",
            "rz",
            "ecr",
            "id",
            "measure",
            "reset",
            "delay",
            "cx",
            "cz",
            "h",
            "y",
            "z",
            "s",
            "t",
            "sdg",
            "tdg",
            "rx",
            "ry",
            "u",
            "u1",
            "u2",
            "u3",
            "swap",
            "iswap",
        }
        self.basis_gates = [op for op in all_operations if op in standard_operations]

        # Populate coupling_map
        self.coupling_map = backend_data.get("coupling_map")
        if self.coupling_map and isinstance(self.coupling_map[0], tuple):
            # Convert tuples to lists for JSON compatibility if needed, but here we expect lists
            self.coupling_map = [list(c) for c in self.coupling_map]

        # Generate mock gate configs for the 'gates' attribute
        self.gates = []
        for gate_name in self.basis_gates:
            num_qubits = 1
            parameters: list[str] = []
            if gate_name in ["cx", "cz", "ecr", "swap", "iswap"]:
                num_qubits = 2
            elif gate_name in ["u", "u3"]:
                parameters = ["theta", "phi", "lambda"]
            elif gate_name == "u2":
                parameters = ["phi", "lambda"]
            elif gate_name == "u1":
                parameters = ["lambda"]
            elif gate_name in {"rz", "rx", "ry"}:
                parameters = ["theta"]

            self.gates.append(MockGateConfig(gate_name, num_qubits, parameters))

        # Add "measure" and "reset" if not already in basis_gates, as they are typically present
        if "measure" not in self.basis_gates:
            self.gates.append(MockGateConfig("measure", 1))
        if "reset" not in self.basis_gates:
            self.gates.append(MockGateConfig("reset", 1))


class MockBackendProperties:
    def __init__(self, backend_data: dict):
        self._data = backend_data

    def gate_error(
        self, gate: str, qubits: int | list[int] | tuple[int, ...]
    ) -> float | None:
        qubit_key = str(qubits) if isinstance(qubits, tuple) else str((qubits,))
        return (
            self._data.get("gate_errors", {})
            .get(gate, {})
            .get(qubit_key, {})
            .get("error")
        )

    def gate_length(
        self, gate: str, qubits: int | list[int] | tuple[int, ...]
    ) -> float | None:
        qubit_key = str(qubits) if isinstance(qubits, tuple) else str((qubits,))
        return (
            self._data.get("gate_errors", {})
            .get(gate, {})
            .get(qubit_key, {})
            .get("duration")
        )

    def readout_error(self, qubit: int) -> float | None:
        return (
            self._data.get("gate_errors", {})
            .get("measure", {})
            .get(f"({qubit},)", {})
            .get("error")
        )

    def t1(self, qubit: int) -> float | None:
        return self._data.get("qubit_properties", {}).get(str(qubit), {}).get("t1")

    def t2(self, qubit: int) -> float | None:
        return self._data.get("qubit_properties", {}).get(str(qubit), {}).get("t2")

    def is_qubit_operational(self, qubit: int) -> bool:
        """Check if a qubit is operational.
        Qiskit's ``BackendV2Converter`` requires this method.
        """
        return str(qubit) in self._data.get("qubit_properties", {})

    def qubit_property(self, qubit: int) -> dict | None:
        """Return the properties of a single qubit as a dictionary.

        Qiskit's ``BackendV2Converter`` requires this method and expects a dictionary
        with specific keys (e.g., ``"T1"``, ``"T2"``, etc.) and ``(value, unit)`` tuple values.
        """
        props = self._data.get("qubit_properties", {}).get(str(qubit))

        if props:
            # Return a dictionary formatted for Qiskit's converter
            return {
                "T1": (props.get("t1"), None),  # Map 't1' -> 'T1'
                "T2": (props.get("t2"), None),  # Map 't2' -> 'T2'
                "frequency": (props.get("frequency"), None),
            }
        return None

    def gate_property(self, name: str) -> dict:
        """Return the properties of a gate.

        Qiskit's ``BackendV2Converter`` requires this method.
        It expects a dictionary where keys are qubit tuples and
        values are dictionaries of properties (such as ``"error"`` and ``"duration"``).
        """
        gate_data = self._data.get("gate_errors", {}).get(name, {})
        if not gate_data:
            return {}

        properties_dict = {}
        for qubit_str, props in gate_data.items():
            # Convert string key "(q0,)" or "(q0, q1)" to tuple
            try:
                # Use ast.literal_eval to safely parse the tuple string
                qubit_tuple = ast.literal_eval(qubit_str)
            except (ValueError, SyntaxError):
                continue

            # Format properties for the converter: (value, unit)
            formatted_props = {
                "error": (props.get("error"), None),
                "duration": (props.get("duration"), None),
            }
            properties_dict[qubit_tuple] = formatted_props

        return properties_dict

    def is_gate_operational(self, name: str, qubits: tuple) -> bool:
        """Check if a gate is operational on specific qubits.

        Qiskit's ``BackendV2Converter`` requires this method.
        We define "operational" as "existing in the ``gate_errors`` data".
        """
        # Convert the qubit tuple back to the string key format
        qubit_key = str(qubits)
        gate_data = self._data.get("gate_errors", {}).get(name)

        # Return whether the gate exists and has an entry for this specific qubit_key
        return gate_data and qubit_key in gate_data


class QubitProperties:
    """Mock qubit properties class for offline data."""

    def __init__(self, t1, t2, frequency=None):
        self.t1 = t1
        self.t2 = t2
        self.frequency = frequency


class GateProperties:
    """Mock gate properties class for offline data."""

    def __init__(self, error, duration=None):
        self.error = error
        self.duration = duration


def build_target_from_data(backend_data: dict) -> Target:
    """Build a real Qiskit Target from saved backend data.
    This is much better than mocking all Target methods
    """
    # Create coupling map
    coupling_map = (
        CouplingMap(backend_data["coupling_map"])
        if backend_data.get("coupling_map")
        else None
    )

    # Filter basis gates to only include standard gates
    # Some operations like 'if_else', 'for_loop', 'while_loop', 'switch_case' are control flow, not gates
    all_operations = backend_data.get("basis_gates", backend_data["operation_names"])

    # List of known standard gates and operations
    standard_operations = {
        "sx",
        "x",
        "rz",
        "ecr",
        "id",
        "measure",
        "reset",
        "delay",
        "cx",
        "cz",
        "h",
        "y",
        "z",
        "s",
        "t",
        "sdg",
        "tdg",
        "rx",
        "ry",
        "u",
        "u1",
        "u2",
        "u3",
        "swap",
        "iswap",
    }

    # Filter to only standard operations
    basis_gates = [op for op in all_operations if op in standard_operations]

    # Create a Target using from_configuration
    # This gives us a real Target with all methods/attributes the transpiler needs
    target = Target.from_configuration(
        basis_gates=basis_gates,
        num_qubits=backend_data["num_qubits"],
        coupling_map=coupling_map,
        dt=backend_data.get("dt"),
    )

    # Note: The Target created above has generic properties.
    # We now populate it with detailed gate_errors data for the transpiler to use.
    if "gate_errors" in backend_data:
        for gate_name, gate_data in backend_data["gate_errors"].items():
            # Skip gates not in the target (e.g. non-standard ones we filtered out)
            if gate_name not in target:
                continue

            for qubit_str, props in gate_data.items():
                try:
                    # Parse qubit tuple string, e.g. "(0,)" or "(0, 1)"
                    qubits = ast.literal_eval(qubit_str)
                except (ValueError, SyntaxError):
                    continue

                error = props.get("error")
                duration = props.get("duration")

                if error is not None or duration is not None:
                    target.update_instruction_properties(
                        gate_name,
                        qubits,
                        InstructionProperties(duration=duration, error=error),
                    )

    return target


class GateErrorData:
    """Container for detailed gate error data for fidelity estimation.
    Separate from the Target to avoid interfering with transpilation.
    """

    def __init__(self, backend_data: dict):
        self._data = backend_data

        # Parse qubit properties for fidelity estimation
        self.qubit_properties = {}
        for qubit_str, props in backend_data["qubit_properties"].items():
            qubit = int(qubit_str)
            self.qubit_properties[qubit] = QubitProperties(
                t1=props["t1"], t2=props["t2"], frequency=props.get("frequency")
            )

        # Store operation names for reference
        control_flow_ops = {"if_else", "for_loop", "while_loop", "switch_case"}
        all_ops = backend_data["operation_names"]
        self.operation_names = [op for op in all_ops if op not in control_flow_ops]

    def __getitem__(self, gate_name: str):
        """Get gate data by name - for fidelity estimation."""
        return OfflineGateData(self._data["gate_errors"].get(gate_name, {}))

    def __contains__(self, gate_name: str):
        """Check if gate exists."""
        return gate_name in self._data["gate_errors"]


class OfflineGateData:
    """Mock gate data class for offline target."""

    def __init__(self, gate_data: dict):
        self._data = gate_data

    def get(self, qubits):
        """Get properties for specific qubit(s)."""
        qubit_key = str(qubits) if isinstance(qubits, tuple) else str((qubits,))
        if qubit_key in self._data:
            props = self._data[qubit_key]
            return GateProperties(error=props["error"], duration=props.get("duration"))
        return None

    def keys(self):
        """Get all qubit combinations for this gate."""
        return [ast.literal_eval(k) for k in self._data]


class OfflineBackend:
    """Mock backend class that provides the same interface as an IBM backend
    but uses offline calibration data from a ``.json.gz`` file.

    This class supports both fidelity estimation and offline transpilation.
    """

    def __init__(self, calibration_file: str):
        with gzip.open(calibration_file, "rt") as f:
            self._data = json.load(f)

        self._backend_name_str = self._data[
            "backend_name"
        ]  # Store name as internal string
        self.num_qubits = self._data["num_qubits"]

        # Use real Target for transpilation (no wrapper interference)
        self.target = build_target_from_data(self._data)

        # Store detailed gate error data separately for fidelity estimation
        self._gate_error_data = GateErrorData(self._data)

        # Filter operation_names to exclude control flow operations
        control_flow_ops = {"if_else", "for_loop", "while_loop", "switch_case"}
        all_ops = self._data["operation_names"]
        self.operation_names = [op for op in all_ops if op not in control_flow_ops]

        # Transpilation support
        if self._data.get("coupling_map"):
            self.coupling_map = CouplingMap(self._data["coupling_map"])
        else:
            # Fallback: fully connected (not recommended)
            print(
                f"WARNING: No coupling map found in {calibration_file}\n"
                "Using fully connected topology (may not match real backend)"
            )
            self.coupling_map = CouplingMap.from_full(self.num_qubits)

        # Basis gates for transpilation - use filtered operation_names
        self.basis_gates = self._data.get("basis_gates", self.operation_names)

        # Additional backend properties
        self.dt = self._data.get("dt")
        self.max_shots = self._data.get("max_shots", 100000)

        # Instruction durations (needed by transpiler)
        self.instruction_durations = InstructionDurations()

        # Backend version (for compatibility)
        self.backend_version = "offline"

        # Creation datetime
        self.creation_datetime = self._data.get("creation_datetime")

        # --- Qiskit 1.x compatibility additions ---
        if HAS_BACKEND_V1:
            self._options = None  # Required by BackendV2Converter
            self._configuration = MockBackendConfiguration(self._data)
            self._properties = MockBackendProperties(self._data)
            self._provider = None  # Required by BackendV2Converter

    @property
    def gate_error_data(self):
        """Access to gate error data for fidelity estimation."""
        return self._gate_error_data

    # Required for Qiskit 1.x BackendV2Converter
    def configuration(self):
        return self._configuration

    # Required for Qiskit 1.x BackendV2Converter
    def properties(self):
        return self._properties

    # Required for Qiskit 1.x BackendV2Converter to get backend name
    def name(self):
        return f"OfflineBackend(name={self._backend_name_str})"

    @property
    def provider(self):
        # Required for Qiskit 1.x BackendV2Converter
        return self._provider

    # Minimal BackendV1 interface requirements
    def __init_subclass__(cls, **kwargs):
        if HAS_BACKEND_V1 and not issubclass(cls, BackendV1):
            # This makes OfflineBackend compatible with BackendV1
            # without explicitly inheriting, avoiding MRO issues
            # if BackendV1 is not available.
            cls.__bases__ = (BackendV1, *cls.__bases__)
        super().__init_subclass__(**kwargs)


def load_backend(backend_source: str | Any, service=None) -> Any:
    """Load a backend from either a ``.json.gz`` file or a live IBM backend.

    :param backend_source: Either a path to a ``.json.gz`` file or a backend name string.
    :param service: ``QiskitRuntimeService`` instance (required if ``backend_source`` is a backend name).

    :returns: Backend object (either ``OfflineBackend`` or a live IBM backend).
    :rtype: object
    """

    if isinstance(backend_source, (str, Path)):
        backend_path = Path(backend_source)
        # Check if it's a JSON.GZ file
        if backend_path.suffix == ".gz" and backend_path.exists():
            print(f"Loading offline backend data from {backend_path}")
            return OfflineBackend(str(backend_path))
        # Assume it's a backend name, need service
        if service is None:
            raise ValueError(
                "service parameter required when loading live backend by name"
            )
        print(f"Loading live backend: {backend_source}")
        return service.backend(str(backend_source))
    # Assume it's already a backend object
    return backend_source


def calculate_circuit_fidelity_ibm_fez(circuit, backend, include_readout=True):
    """Estimate the fidelity of a quantum circuit based on backend gate fidelities.

    :param circuit: Transpiled quantum circuit.
    :param backend: IBM backend object (live or offline).
    :param include_readout: Whether to include readout errors in the estimate.

    :returns: A dictionary with fidelity estimates and a detailed breakdown, including:
            - ``fidelity_product``: Product method fidelity estimate (more accurate).
            - ``fidelity_linear``: Linear approximation fidelity estimate.
            - ``total_error``: Sum of all gate errors.
            - ``num_single_qubit_gates``: Count of single-qubit gates.
            - ``num_two_qubit_gates``: Count of two-qubit gates.
            - ``num_measurements``: Count of measurements.
            - ``breakdown``: Detailed breakdown by gate type.
    :rtype: dict
    """

    # For offline backends, use the separate gate error data
    # For live backends, use the target directly
    if hasattr(backend, "gate_error_data"):
        # Offline Backend (Custom GateErrorData structure)
        error_data = backend.gate_error_data
    else:
        # Live Backend (Standard Qiskit Target)
        error_data = backend.target

        # The Qiskit 'Target' object does not natively expose an 'operation_names' list,
        # which is required by the lookup logic below. We inject this attribute here
        # to ensure both Offline and Live objects expose a consistent API.
        if not hasattr(error_data, "operation_names"):
            error_data.operation_names = getattr(backend, "operation_names", [])

    # Track errors for each gate type
    gate_errors = []
    gate_breakdown: dict[str, list[dict[str, Any]]] = {
        "single_qubit": [],
        "two_qubit": [],
        "measurements": [],
    }

    # Analyze each instruction in the circuit
    for instruction_data in circuit.data:
        # Handle both old and new Qiskit API
        if hasattr(instruction_data, "operation"):
            instruction = instruction_data.operation
            qargs = instruction_data.qubits
        else:
            instruction, qargs, _ = instruction_data

        gate_name = instruction.name
        qubit_indices = tuple(circuit.find_bit(q).index for q in qargs)

        # Skip barriers and other non-gate operations
        if gate_name in ["barrier", "delay"]:
            continue

        # Handle measurement separately
        if gate_name == "measure":
            if include_readout:
                for qubit_tuple in [qubit_indices]:
                    gate_props = None

                    # 1. Try looking up using Target.get_instruction_properties (Live/V2 Backend)
                    if hasattr(error_data, "get_instruction_properties"):
                        # Use the dedicated lookup method for the Target object
                        props = error_data.get_instruction_properties(
                            gate_name, qubit_indices
                        )
                        if props is not None:
                            error = (
                                props.error.value if hasattr(props, "error") else None
                            )
                            duration = (
                                props.duration.value
                                if hasattr(props, "duration")
                                else None
                            )
                            if error is not None:
                                # Assuming GateProperties is defined elsewhere
                                gate_props = GateProperties(
                                    error=error, duration=duration
                                )

                    # 2. Fallback: Try looking up in OfflineBackend data structure
                    if (
                        gate_props is None
                        and hasattr(error_data, "__getitem__")
                        and "measure" in error_data
                    ):
                        gate_props = error_data["measure"].get(qubit_tuple)

                    if gate_props is not None and gate_props.error is not None:
                        error = gate_props.error
                        gate_errors.append(error)
                        gate_breakdown["measurements"].append(
                            {
                                "qubit": qubit_tuple[0],
                                "error": error,
                                "fidelity": 1 - error,
                            }
                        )
            continue

        # --- Handle Standard Gates ---
        gate_props = None

        # 1. Try looking up using Target.get_instruction_properties (Live/V2 Backend)
        if hasattr(error_data, "get_instruction_properties"):
            props = error_data.get_instruction_properties(gate_name, qubit_indices)
            if props is not None:
                error = props.error.value if hasattr(props, "error") else None
                duration = props.duration.value if hasattr(props, "duration") else None
                if error is not None:
                    gate_props = GateProperties(error=error, duration=duration)

        # 2. Fallback: Try looking up in OfflineBackend data structure
        elif (
            hasattr(error_data, "operation_names")
            and gate_name in error_data.operation_names
        ):
            gate_props = error_data[gate_name].get(qubit_indices)

        # 3. If found, record the error
        if gate_props is not None and gate_props.error is not None:
            error = gate_props.error
            gate_errors.append(error)

            # Categorize gate
            if len(qubit_indices) == 1:
                gate_breakdown["single_qubit"].append(
                    {
                        "gate": gate_name,
                        "qubit": qubit_indices[0],
                        "error": error,
                        "fidelity": 1 - error,
                    }
                )
            elif len(qubit_indices) == 2:
                gate_breakdown["two_qubit"].append(
                    {
                        "gate": gate_name,
                        "qubits": qubit_indices,
                        "error": error,
                        "fidelity": 1 - error,
                    }
                )

    # Calculate total fidelity using two methods

    # Method 1: Product of fidelities (exact for independent errors)
    total_fidelity_product = 1.0
    for error in gate_errors:
        total_fidelity_product *= 1 - error

    # Method 2: Sum of errors (linear approximation, valid for small errors)
    total_error_sum = sum(gate_errors)
    total_fidelity_linear = 1 - total_error_sum

    # Return comprehensive results
    return {
        "fidelity_product": total_fidelity_product,
        "fidelity_linear": total_fidelity_linear,
        "total_error": total_error_sum,
        "num_single_qubit_gates": len(gate_breakdown["single_qubit"]),
        "num_two_qubit_gates": len(gate_breakdown["two_qubit"]),
        "num_measurements": len(gate_breakdown["measurements"]),
        "breakdown": gate_breakdown,
    }


def get_fidelity_report_string(
    fidelity_result: dict, circuit=None, transpiled_circuit=None
):
    """Get a formatted report of the fidelity estimation as a string.

    :param fidelity_result: Result dictionary from ``estimate_circuit_fidelity()``.
    :param circuit: Original circuit (optional).
    :param transpiled_circuit: Transpiled circuit (optional).
    :returns: A string containing the formatted report.
    :rtype: str
    """

    report_string = ""

    report_string += "=" * 70 + "\n"
    report_string += "CIRCUIT FIDELITY ESTIMATION REPORT\n"
    report_string += "=" * 70 + "\n"

    if circuit is not None:
        report_string += "\nOriginal Circuit:\n"
        report_string += f"  Gates: {len(circuit.data)}\n"
        report_string += f"  Depth: {circuit.depth()}\n"
        report_string += f"  Qubits: {circuit.num_qubits}\n"

    if transpiled_circuit is not None:
        report_string += "\nTranspiled Circuit:\n"
        report_string += f"  Gates: {len(transpiled_circuit.data)}\n"
        report_string += f"  Depth: {transpiled_circuit.depth()}\n"
        report_string += f"  Qubits: {transpiled_circuit.num_qubits}\n"

    report_string += "\n" + "=" * 70 + "\n"
    report_string += "FIDELITY ESTIMATES:\n"
    report_string += "=" * 70 + "\n"
    report_string += f"\nEstimated circuit fidelity (product method): {fidelity_result['fidelity_product']:.6f}\n"
    report_string += f"Estimated circuit fidelity (linear approx):  {fidelity_result['fidelity_linear']:.6f}\n"
    report_string += f"Total error sum: {fidelity_result['total_error']:.6f}\n"

    report_string += "\nGate counts:\n"
    report_string += (
        f"  Single-qubit gates: {fidelity_result['num_single_qubit_gates']}\n"
    )
    report_string += f"  Two-qubit gates:    {fidelity_result['num_two_qubit_gates']}\n"
    report_string += f"  Measurements:       {fidelity_result['num_measurements']}\n"

    report_string += "\n" + "=" * 70 + "\n"
    report_string += "DETAILED GATE BREAKDOWN:\n"

    report_string += "=" * 70 + "\n"

    report_string += "\nSingle-Qubit Gates (first 10):\n"
    for i, gate in enumerate(fidelity_result["breakdown"]["single_qubit"][:10], 1):
        report_string += f"  {i:2d}. {gate['gate'].upper():4s} on qubit {gate['qubit']:3d} - error: {gate['error']:.6f}, fidelity: {gate['fidelity']:.6f}\n"
    if fidelity_result["num_single_qubit_gates"] > 10:
        report_string += (
            f"  ... and {fidelity_result['num_single_qubit_gates'] - 10} more\n"
        )

    report_string += "\nTwo-Qubit Gates (first 10):\n"
    for i, gate in enumerate(fidelity_result["breakdown"]["two_qubit"][:10], 1):
        report_string += (
            f"  {i:2d}. {gate['gate'].upper():4s} on qubits {gate['qubits']} - "
        )
        report_string += (
            f"error: {gate['error']:.6f}, fidelity: {gate['fidelity']:.6f}\n"
        )
    if fidelity_result["num_two_qubit_gates"] > 10:
        report_string += (
            f"  ... and {fidelity_result['num_two_qubit_gates'] - 10} more\n"
        )

    if fidelity_result["num_measurements"] > 0:
        report_string += "\nMeasurements:\n"
        for i, gate in enumerate(fidelity_result["breakdown"]["measurements"], 1):
            report_string += f"  {i:2d}. MEAS on qubit {gate['qubit']:3d} - "
            report_string += (
                f"error: {gate['error']:.6f}, fidelity: {gate['fidelity']:.6f}\n"
            )

    # Calculate error contribution by gate type for the product method (Logarithmic weight)
    f_single = 1.0
    for g in fidelity_result["breakdown"]["single_qubit"]:
        f_single *= 1.0 - g["error"]

    f_two = 1.0
    for g in fidelity_result["breakdown"]["two_qubit"]:
        f_two *= 1.0 - g["error"]

    f_meas = 1.0
    for g in fidelity_result["breakdown"]["measurements"]:
        f_meas *= 1.0 - g["error"]

    f_total = fidelity_result["fidelity_product"]

    if 0.0 < f_total < 1.0:
        log_total = math.log(f_total)
        share_single = (math.log(f_single) / log_total) * 100
        share_two = (math.log(f_two) / log_total) * 100
        share_meas = (math.log(f_meas) / log_total) * 100
    else:
        share_single = 0.0
        share_two = 0.0
        share_meas = 0.0

    report_string += "\n" + "=" * 70 + "\n"
    report_string += "ERROR CONTRIBUTION BY GATE TYPE (PRODUCT METHOD):\n"
    report_string += "=" * 70 + "\n"
    report_string += "This shows what the fidelity would be if ONLY that specific error type existed,\n"
    report_string += "and its relative contribution to the total fidelity decay.\n"
    report_string += "-" * 70 + "\n"
    report_string += f"\nSingle-qubit component:  {f_single:.6f} (Contributes {share_single:.1f}% to decay)\n"
    report_string += f"Two-qubit component:     {f_two:.6f} (Contributes {share_two:.1f}% to decay)\n"
    report_string += f"Measurement component:   {f_meas:.6f} (Contributes {share_meas:.1f}% to decay)\n"
    report_string += f"{'─' * 70}\n"
    report_string += f"Combined Product:        {f_total:.6f}\n"

    # Calculate error contribution by gate type for the linear approximation method
    single_error = sum(g["error"] for g in fidelity_result["breakdown"]["single_qubit"])
    two_error = sum(g["error"] for g in fidelity_result["breakdown"]["two_qubit"])
    meas_error = sum(g["error"] for g in fidelity_result["breakdown"]["measurements"])

    if fidelity_result["total_error"] > 0:
        report_string += "\n" + "=" * 70 + "\n"
        report_string += (
            "ERROR CONTRIBUTION BY GATE TYPE (LINEAR APPROXIMATION METHOD):\n"
        )
        report_string += "=" * 70 + "\n"
        report_string += f"\nSingle-qubit gates:  {single_error:.6f} ({single_error / fidelity_result['total_error'] * 100:.1f}%)\n"
        report_string += f"Two-qubit gates:     {two_error:.6f} ({two_error / fidelity_result['total_error'] * 100:.1f}%)\n"
        report_string += f"Measurements:        {meas_error:.6f} ({meas_error / fidelity_result['total_error'] * 100:.1f}%)\n"
        report_string += f"{'─' * 70}\n"
        report_string += (
            f"Total error sum:         {fidelity_result['total_error']:.6f} (100.0%)\n"
        )

    report_string += "\n" + "=" * 70 + "\n"
    report_string += "NOTES:\n"
    report_string += "=" * 70 + "\n"
    report_string += """
• The 'product method' is more accurate (multiplies 1-error for each gate)
• The 'linear approximation' simply sums errors (valid for small errors)
• For error rates < 5%, both methods give similar results
• This estimate assumes:
    - Gate errors are independent
    - No crosstalk between qubits
    - Coherence times >> gate durations
    - No state preparation errors
"""
    return report_string


def estimate_circuit_fidelity_ibm_fez(
    circuit: QuantumCircuit, ibm_token: str = "", verbose: bool = False
) -> float:
    """Estimate the fidelity of a quantum circuit on the IBM FEZ backend.

    :param circuit: The quantum circuit to estimate the fidelity of.
    :param ibm_token: The IBM Quantum token to use for the online mode.
    :param verbose: Whether to print verbose output.

    :returns: The estimated fidelity of the circuit as a float.
    :rtype: float
    """

    # Configuration
    ibm_instance = "crn:v1:bluemix:public:quantum-computing:us-east:a/373146ee8c834aa5a059a09701d8d31b:fd7f08b1-6d70-442e-bf8b-6df950815350::"
    backend_name = "ibm_fez"

    # Get the directory containing this module and construct the calibration file path
    module_dir = Path(__file__).parent
    offline_data_file = module_dir / "ibm_fez_calibration.json.gz"
    if not offline_data_file.exists():
        raise FileNotFoundError(f"Offline data file not found: {offline_data_file}")

    # Determine whether to use online or offline mode
    use_offline = not ibm_token

    if use_offline:
        if verbose:
            mode_info_string = ""
            mode_info_string += "=" * 70 + "\n"
            mode_info_string += "OFFLINE MODE: Using saved calibration data\n"
            mode_info_string += "=" * 70
            print(mode_info_string)
        backend = load_backend(offline_data_file)
        if verbose:
            print(f"Calibration data retrieved at: {backend.creation_datetime}")
    else:
        if verbose:
            mode_info_string = ""
            mode_info_string += "=" * 70 + "\n"
            mode_info_string += "ONLINE MODE: Connecting to IBM Quantum\n"
            mode_info_string += "=" * 70
            print(mode_info_string)

        try:
            from qiskit_ibm_runtime import QiskitRuntimeService
        except ImportError:
            raise ImportError(
                "qiskit_ibm_runtime is not installed. Please install it with `pip install qiskit-ibm-runtime`."
            ) from None

        service = QiskitRuntimeService(
            channel="ibm_cloud", token=ibm_token, instance=ibm_instance
        )
        backend = load_backend(backend_name, service)

    if verbose:
        # Handle backend.name being a method (Qiskit V1/OfflineBackend) or property (Qiskit V2)
        backend_info_string = ""
        b_name = backend.name() if callable(backend.name) else backend.name
        backend_info_string += f"Using backend: {b_name}\n\n"
        backend_info_string += f"\nThe circuit has {len(circuit.data)} gates\n"
        backend_info_string += f"\nTranspiling for {b_name}..."
        print(backend_info_string)

    # Transpile circuit (works both online and offline)
    tqc = transpile(circuit, backend=backend, optimization_level=3)
    if verbose:
        transpilation_info_string = ""
        transpilation_info_string += (
            f"Transpiled circuit has {len(tqc.data)} operations\n"
        )
        if use_offline:
            transpilation_info_string += (
                "✓ Transpilation completed using saved coupling map (offline mode)"
            )
        print(transpilation_info_string)

    # Estimate fidelity
    if verbose:
        print("\nEstimating circuit fidelity...\n")
    fidelity_result = calculate_circuit_fidelity_ibm_fez(
        tqc, backend, include_readout=True
    )

    # Print detailed report
    if verbose:
        report_string = get_fidelity_report_string(
            fidelity_result, circuit=circuit, transpiled_circuit=tqc
        )
        print(report_string)

    return fidelity_result["fidelity_product"]
