from qiskit import QuantumCircuit

BELL_STATES = ("00+11", "00-11", "01+10", "01-10")


def bell_pair(state: str = "00+11") -> QuantumCircuit:
    r"""Return circuit that produces a Bell state.
    If the argument `state` isn't passed in, the default "00+11" string is used.

    :param state: The state string describing a Bell state \(default is "00+11"\).
            Valid choices are ``"00+11", "00-11", "01+10", "01-10"``, which correspond to
            :math:`|\Phi^+\rangle, |\Phi^-\rangle, |\Psi^+\rangle` and :math:`|\Psi^-\rangle` Bell states respectively
    :raises ValueError: If state is not one of the 4 valid strings
    :return: Circuit producing a Bell state
    """
    if state not in BELL_STATES:
        raise ValueError('input state must be "00+11", "00-11", "01+10" or "01-10"')
    n = BELL_STATES.index(state)
    bell_state_qc = QuantumCircuit(2)
    if n & 1:
        bell_state_qc.x(0)
    if n & 2:
        bell_state_qc.x(1)
    bell_state_qc.h(0)
    bell_state_qc.cx(0, 1)
    if n == 3:
        bell_state_qc.swap(0, 1)
    return bell_state_qc
