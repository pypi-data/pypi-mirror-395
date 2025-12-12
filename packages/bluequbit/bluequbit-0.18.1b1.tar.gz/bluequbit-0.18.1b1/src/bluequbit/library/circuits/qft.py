# wrapper for QFT to have docstring in the desired style
from __future__ import annotations

from qiskit.circuit.library import QFT as OriginalQFT  # noqa: N811


class QFT(OriginalQFT):
    r"""Quantum Fourier Transform Circuit.

    The Quantum Fourier Transform (QFT) on :math:`n` qubits is the operation

    .. math::

        |j\rangle \mapsto \frac{1}{2^{n/2}} \sum_{k=0}^{2^n - 1} e^{2\pi ijk / 2^n} |k\rangle

    The circuit that implements this transformation can be implemented using Hadamard gates
    on each qubit, a series of controlled-U1 (or Z, depending on the phase) gates and a
    layer of Swap gates. The layer of Swap gates can in principle be dropped if the QFT appears
    at the end of the circuit, since then the re-ordering can be done classically. They
    can be turned off using the ``do_swaps`` attribute.

    :param num_qubits: The number of qubits on which the QFT acts.
    :param approximation_degree: The degree of approximation (0 for no approximation).
    :param do_swaps: Whether to include the final swaps in the QFT.
    :param inverse: If True, the inverse Fourier transform is constructed.
    :param insert_barriers: If True, barriers are inserted as visualization improvement.
    :param name: The name of the circuit.

    For 4 qubits, the circuit that implements this transformation is:

    .. plot::

       from qiskit.circuit.library import QFT
       from qiskit.tools.jupyter.library import _generate_circuit_library_visualization
       circuit = QFT(4)
       _generate_circuit_library_visualization(circuit)

    The inverse QFT can be obtained by calling the ``inverse`` method on this class.
    The respective circuit diagram is:

    .. plot::

       from qiskit.circuit.library import QFT
       from qiskit.tools.jupyter.library import _generate_circuit_library_visualization
       circuit = QFT(4).inverse()
       _generate_circuit_library_visualization(circuit)

    One method to reduce circuit depth is to implement the QFT approximately by ignoring
    controlled-phase rotations where the angle is beneath a threshold. This is discussed
    in more detail in https://arxiv.org/abs/quant-ph/9601018 or
    https://arxiv.org/abs/quant-ph/0403071.

    Here, this can be adjusted using the ``approximation_degree`` attribute: the smallest
    ``approximation_degree`` rotation angles are dropped from the QFT. For instance, a QFT
    on 5 qubits with approximation degree 2 yields (the barriers are dropped in this example):

    .. plot::

       from qiskit.circuit.library import QFT
       from qiskit.tools.jupyter.library import _generate_circuit_library_visualization
       circuit = QFT(5, approximation_degree=2)
       _generate_circuit_library_visualization(circuit)

    """

    def __init__(
        self,
        num_qubits: int | None = None,
        approximation_degree: int = 0,
        do_swaps: bool = True,
        inverse: bool = False,
        insert_barriers: bool = False,
        name: str | None = None,
    ) -> None:
        super().__init__(
            num_qubits, approximation_degree, do_swaps, inverse, insert_barriers, name
        )
