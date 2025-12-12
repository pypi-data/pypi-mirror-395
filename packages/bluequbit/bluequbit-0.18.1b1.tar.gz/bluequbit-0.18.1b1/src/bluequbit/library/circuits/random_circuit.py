# wrapper for random_circuit to have docstring in the desired style
from qiskit import QuantumCircuit
from qiskit.circuit.random import random_circuit as original_random_circuit


def random_circuit(
    num_qubits,
    depth,
    max_operands=4,
    measure=False,
    conditional=False,
    reset=False,
    seed=None,
) -> QuantumCircuit:
    r"""Generate random circuit of arbitrary size and form.

    This function will generate a random circuit by randomly selecting gates
    from the set of standard gates in :mod:`qiskit.extensions`. For example:

    .. plot::
       :include-source:

       from qiskit.circuit.random import random_circuit

       circ = random_circuit(2, 2, measure=True)
       circ.draw(output='mpl')

    :param num_qubits: number of quantum wires
    :param depth: layers of operations (i.e. critical path length)
    :param max_operands: maximum qubit operands of each gate (between 1 and 4)
    :param measure: if True, measure all qubits at the end
    :param conditional: if True, insert middle measurements and conditionals
    :param reset: if True, insert middle resets
    :param seed: sets random seed (optional)
    :raises CircuitError: when invalid options given
    :return: constructed circuit
    """
    return original_random_circuit(
        num_qubits,
        depth,
        max_operands=max_operands,
        measure=measure,
        conditional=conditional,
        reset=reset,
        seed=seed,
    )
