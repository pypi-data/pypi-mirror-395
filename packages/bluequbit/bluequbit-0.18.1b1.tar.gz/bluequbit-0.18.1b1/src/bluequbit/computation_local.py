from __future__ import annotations

import time
from typing import TYPE_CHECKING, Any

from .exceptions import BQSDKUsageError

if TYPE_CHECKING:
    from qiskit import QuantumCircuit

MAX_QUBITS_WITH_STATEVEC = 16


def run_circuit_qiskit(qc: QuantumCircuit, shots: int | None = None):
    from qiskit import transpile
    from qiskit.circuit import Measure
    from qiskit.quantum_info import Statevector
    from qiskit_aer import Aer

    qiskit_backend = Aer.get_backend("aer_simulator")
    transpiled = transpile(qc, qiskit_backend, routing_method="none")
    transpiled.remove_final_measurements()

    has_measurements = any(isinstance(instr, Measure) for instr, _, _ in qc.data)
    output: dict[str, Any] = {
        "has_measurements": has_measurements,
    }
    if has_measurements or (shots is not None and shots > 0):
        if has_measurements and shots is None:
            raise BQSDKUsageError(
                "You have to specify shots when there are measurements."
            )
        run_start = time.time()
        sv = Statevector(transpiled)
        run_end = time.time()
        output["counts"] = sv.probabilities_dict()
    elif shots is None or shots == 0:
        run_start = time.time()
        sv = Statevector(transpiled)
        run_end = time.time()
        output["counts"] = sv.probabilities_dict()
        num_qubits = len(transpiled.qubits)
        if num_qubits <= MAX_QUBITS_WITH_STATEVEC:
            output["state_vector"] = sv
    else:
        raise BQSDKUsageError(
            f"Wrong configuration for bq.run with device=local: has_measurements={has_measurements}, shots={shots}"
        )
    output["run_start"] = run_start
    output["run_end"] = run_end
    return output


def run_circuit_cirq(circuit, shots: int | None = None):
    simulator: cirq.Simulator | qsimcirq.QSimSimulator
    try:
        # Prefer qsim whenever possible
        import qsimcirq

        simulator = qsimcirq.QSimSimulator()
    except ImportError:
        import cirq

        simulator = cirq.Simulator()

    has_measurements = circuit.has_measurements()
    output = {
        "has_measurements": has_measurements,
    }
    if has_measurements and shots is None:
        raise BQSDKUsageError("You have to specify shots when there are measurements.")
    run_start = time.time()
    result = simulator.simulate(circuit)
    run_end = time.time()
    output["state_vector"] = result.final_state_vector
    output["counts"] = result.final_state_vector * result.final_state_vector.conj()
    output["run_start"] = run_start
    output["run_end"] = run_end
    return output
