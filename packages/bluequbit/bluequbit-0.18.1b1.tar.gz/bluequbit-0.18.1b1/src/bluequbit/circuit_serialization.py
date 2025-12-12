import base64
import io
import pickle
import zlib


def is_a_qiskit_circuit(qc):
    return any(
        str(cls) == "<class 'qiskit.circuit.quantumcircuit.QuantumCircuit'>"
        for cls in type(qc).mro()
    )


def is_a_pennylane_circuit(qc):
    return str(type(qc)) == "<class 'dict'>" and any(
        str(cls) == "<class 'pennylane.tape.qscript.QuantumScript'>"
        for cls in type(qc.get("pennylane_circuit")).mro()
    )


def cirq_to_qasm2(circuit):
    import cirq
    from cirq import ops

    qubit_order = ops.QubitOrder.DEFAULT
    qubits = ops.QubitOrder.as_qubit_order(qubit_order).order_for(circuit.all_qubits())
    serialized = cirq.QasmOutput(
        operations=circuit.all_operations(),
        qubits=qubits,
        header="Generated from Cirq via BlueQubit",
        precision=10,
        version="2.0",
    )
    return str(serialized)


def encode_circuit(qc, use_cirq_qasm=False):
    """
    Encode a quantum circuit object from various quantum libraries to a
    portable format.
    """
    # We use the string representation of the object class so that we don't
    # have to require users to install Qiskit, Cirq, and Braket all at once.
    if isinstance(qc, dict) and "circuit_type" in qc:
        return qc
    circuit_type = str(type(qc))
    if circuit_type == "<class 'cirq.circuits.circuit.Circuit'>":
        if use_cirq_qasm:
            # We serialize to OQ2 string
            # https://quantumai.google/reference/python/cirq/QasmOutput
            serialized = cirq_to_qasm2(qc)
            return {"circuit_type": "Cirq_OQ2", "circuit": serialized}

        # We use Cirq-specific serialization method.
        import cirq

        # https://quantumai.google/cirq/build/interop
        serialized = cirq.to_json(qc)
        return {"circuit_type": "Cirq", "circuit": serialized}
    if circuit_type == "<class 'braket.circuits.circuit.Circuit'>":
        from braket.circuits.serialization import IRType

        serialized = qc.to_ir(IRType.OPENQASM).source
        return {"circuit_type": "Braket", "circuit": serialized}
    if is_a_qiskit_circuit(qc):
        from importlib.metadata import version

        from qiskit import qpy

        qiskit_version = version("qiskit")

        # https://qiskit.org/documentation/apidoc/qpy.html
        with io.BytesIO() as f:
            if qiskit_version[0] == "2":
                qpy.dump(qc, f, version=13)
            else:
                qpy.dump(qc, f)
            # Rewind back to the beginning of the "file".
            f.seek(0)
            serialized = f.read()
            # Convert to base64
            serialized = base64.b64encode(serialized)
            # Convert bytes to str
            serialized = serialized.decode("utf-8")
        return {"circuit_type": "Qiskit", "circuit": serialized}
    if is_a_pennylane_circuit(qc):
        return {
            "circuit_type": "Pennylane",
            "circuit": base64.b64encode(zlib.compress(pickle.dumps(qc))).decode(
                "utf-8"
            ),
        }
    raise TypeError("Unsupported circuit type", qc)


def encode_circuit_with_fallback(qc):
    # Temporary workaround: see https://trello.com/c/0SMvJuLV/266-productofsums-issue
    encoded = encode_circuit(qc)
    if encoded["circuit_type"] == "Cirq" and "ProductOfSums" in encoded["circuit"]:
        return encode_circuit(qc, use_cirq_qasm=True)
    return encoded


def decode_circuit(data):
    """
    Decode the output of encode_circuit.
    """
    if "circuit_type" not in data:
        raise Exception("Wrong data structure. 'circuit_type' must be present.")
    if "circuit" not in data:
        raise Exception("Wrong data structure. 'circuit' must be present.")
    circuit_type = data["circuit_type"]
    if circuit_type == "Cirq":
        import cirq

        return cirq.read_json(json_text=data["circuit"])
    if circuit_type == "Cirq_OQ2":
        from cirq.contrib.qasm_import import circuit_from_qasm

        return circuit_from_qasm(data["circuit"])
    if circuit_type == "Qiskit":
        from qiskit import qpy

        _bytes = str.encode(data["circuit"])
        _bytes = base64.b64decode(_bytes)
        with io.BytesIO(_bytes) as f:
            circuits = qpy.load(f)
            if len(circuits) != 1:
                raise Exception(
                    f"Unexpected number of circuits: {len(circuits)}. Must be 1."
                )
            return circuits[0]
    if circuit_type == "Pennylane":
        encoded_circuit = data["circuit"]
        decoded_bytes = base64.b64decode(encoded_circuit)
        circuit = pickle.loads(zlib.decompress(decoded_bytes))  # noqa: S301
        if isinstance(circuit, dict):
            pennylane_circuit = circuit.get("pennylane_circuit")
        else:
            raise TypeError(
                "the circuit must be dictionary containing pennylane_circuit"
            )
        return pennylane_circuit
    if circuit_type == "Braket":
        raise Exception("Braket decoding is not yet supported.")
    raise Exception("Unsupported circuit type", circuit_type)
