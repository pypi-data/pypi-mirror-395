from qiskit.quantum_info import Pauli


def construct_pauli_from_idx_lists(
    idx_lists: list[list[int]], num_qubits: int
) -> Pauli:
    """Construct a Pauli operator from a list of Pauli X, Y, Z indices.
    idx_lists[0] is the list of indices for the X Pauli
    idx_lists[1] is the list of indices for the Y Pauli
    idx_lists[2] is the list of indices for the Z Pauli.
    The Pauli operator is the product of the Pauli operators at the indices in the lists.
    The Pauli operator is returned as a qiskit.quantum_info.Pauli object.

    :param idx_lists: list of lists of indices
    :type idx_lists: list[list[int]]
    :param num_qubits: number of qubits
    :type num_qubits: int

    :return: Pauli operator
    :rtype: qiskit.quantum_info.Pauli
    """
    paulis = ["I"] * num_qubits
    set_x = set(idx_lists[0])
    set_y = set(idx_lists[1])
    set_z = set(idx_lists[2])
    if len(set_x | set_y | set_z) != len(set_x) + len(set_y) + len(set_z):
        raise ValueError("idx_lists must not have overlapping indices")
    for i in set_x:
        paulis[i] = "X"
    for i in set_y:
        paulis[i] = "Y"
    for i in set_z:
        paulis[i] = "Z"
    return Pauli("".join(paulis))
