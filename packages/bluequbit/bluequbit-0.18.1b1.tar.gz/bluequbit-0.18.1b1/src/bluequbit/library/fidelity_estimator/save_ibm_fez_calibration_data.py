"""
Script to fetch and save IBM FEZ Quantum backend calibration data to ``.json.gz``.

This script connects to IBM Quantum using your token and saves all the
necessary backend calibration data (gate fidelities, measurement errors, etc.)
to a ``.json.gz`` file. This data can then be used for offline fidelity estimation
without requiring an IBM token.
"""

import gzip
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from qiskit_ibm_runtime import QiskitRuntimeService


def extract_backend_data(backend) -> dict[str, Any]:
    """Extract all necessary calibration and transpilation data from a backend.

    :param backend: IBM backend object.

    :returns: Dictionary containing all backend calibration and transpilation data.
    :rtype: dict
    """
    creation_datetime = datetime.now(timezone.utc).isoformat()

    target = backend.target

    # Extract gate error data
    gate_errors: dict[str, dict[str, dict[str, Any]]] = {}
    for gate_name in target.operation_names:
        if gate_name in target:
            gate_errors[gate_name] = {}
            for qubits in target[gate_name]:
                if qubits is not None:
                    props = target[gate_name][qubits]

                    # Skip if props is None (can happen for some gates)
                    if props is None:
                        continue

                    # Convert tuple to string for JSON serialization
                    qubit_key = (
                        str(qubits) if isinstance(qubits, tuple) else str((qubits,))
                    )

                    # Handle duration - could be float or object with .magnitude attribute
                    duration = None
                    if props.duration is not None:
                        if hasattr(props.duration, "magnitude"):
                            duration = props.duration.magnitude
                        else:
                            duration = props.duration

                    gate_errors[gate_name][qubit_key] = {
                        "error": props.error,
                        "duration": duration,
                    }

    # Extract qubit properties (T1, T2, frequency, etc.)
    qubit_properties = {}
    for qubit in range(backend.num_qubits):
        if target.qubit_properties and target.qubit_properties[qubit]:
            props = target.qubit_properties[qubit]
            qubit_properties[str(qubit)] = {
                "t1": props.t1,
                "t2": props.t2,
                "frequency": props.frequency if hasattr(props, "frequency") else None,
            }

    # Extract coupling map (critical for transpilation)
    coupling_map = []
    if hasattr(backend, "coupling_map") and backend.coupling_map:
        # Convert EdgeList to regular Python list for JSON serialization
        coupling_map = list(backend.coupling_map.get_edges())

    # Extract basis gates
    basis_gates = list(target.operation_names)

    # Extract backend configuration details
    dt = None
    if hasattr(backend, "dt"):
        dt = backend.dt

    max_shots = None
    if hasattr(backend, "max_shots"):
        max_shots = backend.max_shots

    # Create comprehensive backend data structure
    backend_data = {
        "creation_datetime": creation_datetime,
        "backend_name": backend.name,
        "num_qubits": backend.num_qubits,
        "gate_errors": gate_errors,
        "qubit_properties": qubit_properties,
        "operation_names": list(target.operation_names),
        # Transpilation data
        "coupling_map": coupling_map,
        "basis_gates": basis_gates,
        "dt": dt,
        "max_shots": max_shots,
    }

    return backend_data


def save_backend_data(backend, output_file: str | None = None):
    """Save backend calibration data to a JSON file.

    :param backend: IBM backend object.
    :param output_file: Path to the output JSON file (default: ``{backend_name}_calibration.json``).
    """
    if output_file is None:
        output_file = f"{backend.name}_calibration.json.gz"

    print(f"Extracting calibration data from {backend.name}...")
    backend_data = extract_backend_data(backend)

    # Save to JSON
    print(f"Saving to {output_file}...")
    with gzip.open(output_file, "wt") as f:
        json.dump(backend_data, f, indent=2)

    print(f"✓ Successfully saved backend data to {output_file}")
    print(f"  Backend: {backend_data['backend_name']}")
    print(f"  Qubits: {backend_data['num_qubits']}")
    print(f"  Operations: {len(backend_data['operation_names'])}")
    print(f"  Coupling map edges: {len(backend_data['coupling_map'])}")
    print(f"  File size: {Path(output_file).stat().st_size / 1024:.2f} KB")
    print(f"  Creation datetime: {backend_data['creation_datetime']}")
    print("\n✓ Saved data includes:")
    print("  - Gate fidelities and errors")
    print("  - Qubit properties (T1, T2, frequency)")
    print("  - Coupling map (for transpilation)")
    print("  - Basis gates and backend configuration")
    print("  - Creation datetime")


def main():
    """Main function to connect to IBM Quantum and save backend data.

    This function connects to IBM Quantum using the provided token and instance,
    retrieves the backend data, and saves it to a ``.json.gz`` file.
    """
    # Configuration - Replace with your credentials
    ibm_token = ""  # Your IBM Quantum token
    ibm_instance = "crn:v1:bluemix:public:quantum-computing:us-east:a/373146ee8c834aa5a059a09701d8d31b:fd7f08b1-6d70-442e-bf8b-6df950815350::"
    backend_name = "ibm_fez"

    if not ibm_token:
        print("ERROR: Please set your ibm_token in the script")
        return

    print("=" * 70)
    print("IBM FEZ Quantum Backend Data Saver")
    print("=" * 70)
    print()

    # Connect to IBM Quantum
    print("Connecting to IBM Quantum...")
    service = QiskitRuntimeService(
        channel="ibm_cloud", token=ibm_token, instance=ibm_instance
    )

    # Get backend
    print(f"Getting backend: {backend_name}...")
    backend = service.backend(backend_name)

    # Save data
    save_backend_data(backend)

    print()
    print("=" * 70)
    print("Done! You can now use this file for offline fidelity estimation.")
    print("=" * 70)


if __name__ == "__main__":
    main()
