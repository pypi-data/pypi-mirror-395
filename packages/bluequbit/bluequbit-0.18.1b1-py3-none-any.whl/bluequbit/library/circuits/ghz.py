from qiskit import QuantumCircuit


def ghz(n: int = 3) -> QuantumCircuit:
    r"""Return circuit that produces the generalized Greenberger-Horne-Zeilinger \(GHZ\) state with n qubits
    defined by:

    .. math::

        |{\rm GHZ} \rangle = \frac{|0 \rangle ^{\otimes n} + |1 \rangle ^{\otimes n}}{\sqrt{2}} , n > 2

    If the argument `n` isn't passed in, the default 3 is used.

    :param n: The number of qubits \(default is 3\). Valid choices are integers greater than 2.
            If you want ``n = 2``, use ``bell_pair`` function from ``bluequbit.library``
    :raises ValueError: if ``n`` is lower than 3
    :return: GHZ circuit
    """
    if n < 3:
        raise ValueError("n must be at least 3")
    ghz_qc = QuantumCircuit(n)
    ghz_qc.h(0)
    ghz_qc.cx(0, range(1, n))
    return ghz_qc
