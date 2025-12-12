from qiskit import QuantumCircuit

from .ibm_fez_fidelity_estimation import estimate_circuit_fidelity_ibm_fez
from .quantinuum_h2_fidelity_estimation import estimate_circuit_fidelity_quantinuum_h2


def estimate_circuit_fidelity(
    circuit: QuantumCircuit,
    device: str,
    token: str = "",
    verbose: bool = False,
) -> float:
    """Estimate the fidelity of a quantum circuit on a given device.

    :param circuit: The quantum circuit to estimate the fidelity of. Must be a valid
                    Qiskit ``QuantumCircuit`` object.
    :param device: The device to estimate the fidelity on. Can be ``"quantinuum.h2"`` or
                ``"ibm.fez"``.
    :param token: The token to use for the online mode. Only required for ``"ibm.fez"``.
    :param verbose: Whether to print verbose output.

    :returns: The estimated fidelity of the circuit as a float.
    :rtype: float

    :raises ValueError: If the device is invalid.
    """
    if device == "quantinuum.h2":
        return estimate_circuit_fidelity_quantinuum_h2(circuit, verbose)
    if device == "ibm.fez":
        return estimate_circuit_fidelity_ibm_fez(circuit, token, verbose)
    raise ValueError(f"Invalid device: {device}")
