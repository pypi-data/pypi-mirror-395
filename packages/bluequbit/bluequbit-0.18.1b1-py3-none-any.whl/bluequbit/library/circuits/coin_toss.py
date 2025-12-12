from qiskit import QuantumCircuit


def coin_toss(n: int = 1) -> QuantumCircuit:
    r"""Return circuit that performs n coin tosses
    If the argument `n` isn't passed in, the default 1 is used.

    :param n: The number of coin tosses \(default is 1\). Valid choices are positive integers
    :raises ValueError: If ``n`` is lower than 1
    :return: Circuit performing ``n`` coin tosses
    """
    if n < 1:
        raise ValueError("n must be a positive integer")
    coin_toss_qc = QuantumCircuit(n)
    coin_toss_qc.h(range(n))
    return coin_toss_qc
