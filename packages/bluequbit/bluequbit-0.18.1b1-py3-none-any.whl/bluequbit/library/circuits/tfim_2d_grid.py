from qiskit import QuantumCircuit
from qiskit.circuit import Parameter


def tfim_2d_grid(
    n_rows: int,
    n_cols: int,
    trotter_steps: int,
) -> QuantumCircuit:
    """
    Create a parametric circuit for the transverse-field Ising model (TFIM) on a 2D
    grid with alternating RX and RZZ layers, representing Trotter evolution steps.

    Args:
        n_rows: Number of rows in the 2D grid.
        n_cols: Number of columns in the 2D grid.
        trotter_steps: Number of Trotter steps (alternating RZZ/RX layer pairs).

    Returns:
        A parametric QuantumCircuit with parameters for RZZ and RX gates.
    """
    n_qubits = n_rows * n_cols
    qc = QuantumCircuit(n_qubits)

    # Build grid connectivity with open boundary conditions
    grid_connectivity = []
    for r in range(n_rows):
        for c in range(n_cols):
            qubit = r * n_cols + c
            if c < n_cols - 1:
                grid_connectivity.append((qubit, r * n_cols + c + 1))
            if r < n_rows - 1:
                grid_connectivity.append((qubit, (r + 1) * n_cols + c))

    # Create Trotter steps with alternating RX and RZZ layers
    for step in range(trotter_steps):
        # RX layer on all qubits
        for i in range(n_qubits):
            param = Parameter(f"θ_rx_{step}_{i}")
            qc.rx(param, i)

        # RZZ layer on grid connectivity
        for i, j in grid_connectivity:
            param = Parameter(f"θ_rzz_{step}_{i}_{j}")
            qc.rzz(param, i, j)

    return qc
