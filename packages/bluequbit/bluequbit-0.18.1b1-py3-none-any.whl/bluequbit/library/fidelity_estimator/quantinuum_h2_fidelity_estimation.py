from qiskit import QuantumCircuit, transpile

# --- H2 Fidelity Constants (Typical) ---
# Based on "Typical" column in Table 1
INFIDELITY_1Q_TYPICAL = 3e-5
FIDELITY_1Q_TYPICAL = 1.0 - INFIDELITY_1Q_TYPICAL

INFIDELITY_2Q_TYPICAL = 1e-3
FIDELITY_2Q_TYPICAL = 1.0 - INFIDELITY_2Q_TYPICAL

INFIDELITY_SPAM_TYPICAL = 1e-3
FIDELITY_SPAM_TYPICAL = 1.0 - INFIDELITY_SPAM_TYPICAL

# --- H2 Fidelity Constants (Min) ---
# Based on "Max" column in Table 1
INFIDELITY_1Q_MAX = 2e-4
FIDELITY_1Q_MIN = 1.0 - INFIDELITY_1Q_MAX

INFIDELITY_2Q_MAX = 2e-3
FIDELITY_2Q_MIN = 1.0 - INFIDELITY_2Q_MAX

INFIDELITY_SPAM_MAX = 5e-3
FIDELITY_SPAM_MIN = 1.0 - INFIDELITY_SPAM_MAX


def calculate_circuit_fidelity_quantinuum_h2(
    circuit: QuantumCircuit, include_readout=True, mode: str = "typical"
) -> dict:
    """Calculate the fidelity estimation of a quantum circuit on the Quantinuum H2.

    This calculation is simple and assumes all-to-all connectivity. It does
    not transpile the circuit; it only counts the gates in the provided
    transpiled circuit. It does not account for memory errors.

    :param circuit: The transpiled quantum circuit to estimate the fidelity of.
    :param include_readout: Whether to include SPAM errors in the estimate.
    :param mode: The fidelity mode to use: ``"typical"`` (default) or ``"min"``.

    :returns: A dictionary with fidelity estimates and gate counts.
    :rtype: dict
    """
    num_1q_gates = 0
    num_2q_gates = 0
    num_measurements = 0

    # Analyze each instruction in the circuit
    for instruction_data in circuit.data:
        # Handle both old (tuple) and new (InstructionData) Qiskit API
        if hasattr(instruction_data, "operation"):
            instruction = instruction_data.operation
            qargs = instruction_data.qubits
        else:
            instruction, qargs, _ = instruction_data

        gate_name = instruction.name
        num_qubits = len(qargs)

        # Skip non-gate operations
        if gate_name in ["barrier", "delay"]:
            continue

        # Categorize operation
        if gate_name == "measure":
            num_measurements += 1
        elif num_qubits == 1:
            num_1q_gates += 1
        elif num_qubits == 2:
            num_2q_gates += 1
        # We can ignore 3+ qubit gates
        # as they would be decomposed during transpilation.

    # --- Select Fidelities Based on Mode ---
    if mode.lower() == "min":
        infidelity_1q = INFIDELITY_1Q_MAX
        fidelity_1q = FIDELITY_1Q_MIN
        infidelity_2q = INFIDELITY_2Q_MAX
        fidelity_2q = FIDELITY_2Q_MIN
        infidelity_spam = INFIDELITY_SPAM_MAX
        fidelity_spam = FIDELITY_SPAM_MIN
        mode_name = "Min"
    else:
        # Default to typical
        infidelity_1q = INFIDELITY_1Q_TYPICAL
        fidelity_1q = FIDELITY_1Q_TYPICAL
        infidelity_2q = INFIDELITY_2Q_TYPICAL
        fidelity_2q = FIDELITY_2Q_TYPICAL
        infidelity_spam = INFIDELITY_SPAM_TYPICAL
        fidelity_spam = FIDELITY_SPAM_TYPICAL
        mode_name = "Typical"

    # --- Calculate Fidelity ---

    # Method 1: Product of fidelities (more accurate)
    fidelity_product = 1.0
    fidelity_product *= fidelity_1q**num_1q_gates
    fidelity_product *= fidelity_2q**num_2q_gates
    if include_readout:
        # Apply SPAM fidelity for each measurement operation
        fidelity_product *= fidelity_spam**num_measurements

    # Method 2: Linear approximation (sum of errors)
    total_error = 0.0
    total_error += num_1q_gates * infidelity_1q
    total_error += num_2q_gates * infidelity_2q
    if include_readout:
        total_error += num_measurements * infidelity_spam

    fidelity_linear = 1.0 - total_error

    return {
        "fidelity_product": fidelity_product,
        "fidelity_linear": fidelity_linear,
        "total_error": total_error,
        "num_single_qubit_gates": num_1q_gates,
        "num_two_qubit_gates": num_2q_gates,
        "num_measurements": num_measurements,
        # Pass back info for the report
        "mode": mode_name,
        "infidelity_1q": infidelity_1q,
        "fidelity_1q": fidelity_1q,
        "infidelity_2q": infidelity_2q,
        "fidelity_2q": fidelity_2q,
        "infidelity_spam": infidelity_spam,
        "fidelity_spam": fidelity_spam,
    }


def get_fidelity_report_string_quantinuum_h2(
    fidelity_result: dict, circuit: QuantumCircuit, original_circuit: QuantumCircuit
) -> str:
    """Get a formatted report string of the H2 fidelity estimation.

    :param fidelity_result: Result dictionary from ``calculate_circuit_fidelity_quantinuum_h2``.
    :param circuit: Transpiled quantum circuit.
    :param original_circuit: Original quantum circuit.

    :returns: A formatted report string.
    :rtype: str
    """
    report_string = ""
    report_string += "=" * 70 + "\n"
    report_string += "QUANTINUUM H2 FIDELITY ESTIMATION REPORT\n"
    report_string += "=" * 70 + "\n"

    report_string += "\nOriginal Circuit:\n"
    report_string += f"  Gates (total): {len(original_circuit.data)}\n"
    report_string += f"  Depth:         {original_circuit.depth()}\n"
    report_string += f"  Qubits:        {original_circuit.num_qubits}\n"

    report_string += "\nTranspiled Circuit:\n"
    report_string += f"  Gates (total): {len(circuit.data)}\n"
    report_string += f"  Depth:         {circuit.depth()}\n"
    report_string += f"  Qubits:        {circuit.num_qubits}\n"

    # Get mode and fidelities from the result dict
    mode_name = fidelity_result.get("mode", "Typical")
    fidelity_1q = fidelity_result["fidelity_1q"]
    infidelity_1q = fidelity_result["infidelity_1q"]
    fidelity_2q = fidelity_result["fidelity_2q"]
    infidelity_2q = fidelity_result["infidelity_2q"]
    fidelity_spam = fidelity_result["fidelity_spam"]
    infidelity_spam = fidelity_result["infidelity_spam"]

    report_string += f"\nFidelity Estimates (based on {mode_name} fidelities):\n"
    report_string += (
        f"  Fidelity (product method): {fidelity_result['fidelity_product']:.6f}\n"
    )
    report_string += (
        f"  Fidelity (linear approx):  {fidelity_result['fidelity_linear']:.6f}\n"
    )
    report_string += f"  Total error sum:        {fidelity_result['total_error']:.6f}\n"

    report_string += "\nGate Counts (from transpiled circuit):\n"
    report_string += (
        f"  Single-qubit gates: {fidelity_result['num_single_qubit_gates']}\n"
    )
    report_string += f"  Two-qubit gates:    {fidelity_result['num_two_qubit_gates']}\n"
    report_string += f"  Measurements:       {fidelity_result['num_measurements']}\n"

    report_string += "\n" + "=" * 70 + "\n"
    report_string += "NOTES:\n"
    report_string += "=" * 70 + "\n"
    report_string += "• Assumes all-to-all connectivity (no connectivity constraints during transpilation). \n"
    report_string += (
        "• Transpiled to 'u' (general 1Q) and 'cx' (general 2Q proxy) gates.\n"
    )
    report_string += f"• Uses '{mode_name}' fidelities from H2 data sheet: \n"
    report_string += (
        f"  - 1Q Fidelity: {fidelity_1q:.6f} (Error: {infidelity_1q:.1e})\n"
    )
    report_string += (
        f"  - 2Q Fidelity: {fidelity_2q:.6f} (Error: {infidelity_2q:.1e})\n"
    )
    report_string += (
        f"  - SPAM Fidelity: {fidelity_spam:.6f} (Error: {infidelity_spam:.1e})\n"
    )
    report_string += "• This estimate does not account for memory errors. \n"
    report_string += "• This estimate does not account for crosstalk between qubits. \n"
    return report_string


def estimate_circuit_fidelity_quantinuum_h2(
    circuit: QuantumCircuit, verbose: bool = False, mode: str = "typical"
) -> float:
    """Estimate the fidelity of a quantum circuit on the Quantinuum H2.

    :param circuit: The quantum circuit to estimate the fidelity of.
    :param verbose: Whether to print the detailed fidelity report.
    :param mode: The fidelity mode to use: ``"typical"`` (default) or ``"min"``.

    :returns: The estimated fidelity of the circuit as a float.
    :rtype: float
    """
    if verbose:
        run_info_string = "=" * 70 + "\n"
        run_info_string += "Running Quantinuum H2 Fidelity Estimator\n"
        run_info_string += f"Input circuit has {len(circuit.data)} operations\n"
        run_info_string += f"Calculating using '{mode}' infidelity values.\n"
        run_info_string += (
            "Estimating fidelity (transpiling to 'u' and 'cx' gates)...\n"
        )
        run_info_string += "=" * 70
        print(run_info_string)

    # Transpile to 'u' (general 1Q) and 'cx' (general 2Q proxy)
    transpiled_circuit = transpile(
        circuit, basis_gates=["u", "cx"], optimization_level=3
    )

    # Estimate fidelity from the transpiled circuit
    fidelity_result = calculate_circuit_fidelity_quantinuum_h2(
        transpiled_circuit, include_readout=True, mode=mode
    )

    # Print detailed report if requested
    if verbose:
        report_string = get_fidelity_report_string_quantinuum_h2(
            fidelity_result, circuit=transpiled_circuit, original_circuit=circuit
        )
        print(report_string)

    return fidelity_result["fidelity_product"]
