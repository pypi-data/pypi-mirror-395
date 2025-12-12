from math import ceil, log2

from qiskit import QuantumCircuit, QuantumRegister

from .draper_adder import DraperAdder


def multi_adder(m: int, n: int) -> QuantumCircuit:
    r"""A circuit that uses DraperAdder to perform in-place summation of :math:`m` qubit registers,
    each having :math:`n` qubits. The total sum will be in the last register, which should have extra
    qubits, initially at state :math:`|0\rangle`, to store the total maximum possible sum.

    :param m: The number of qubit registers, which must be at least 2
    :param n: The number of qubits in each register. It must be the same for all registers
    :raises ValueError: If ``m`` is lower than 2 or if ``n`` is lower than 1
    :return: circuit that performs summation of ``m`` registers

    :Example:

        Construct a circuit with m = 4 registers and n = 3 qubits for each. Set up the registers to be uniformly random
        numbers in their value range \(0-7\) and measure their sum.

        .. code-block:: python

            import bluequbit
            from bluequbit.library import multi_adder
            from qiskit import QuantumCircuit
            from math import ceil, log2

            m = 4
            n = 3
            num_sum_qubits = int(ceil(log2(m * (2**n - 1) + 0.5)))
            num_qubits = m * n + num_sum_qubits - n
            qc = QuantumCircuit(num_qubits, num_sum_qubits)
            qc.h(range(m * n))
            qc = qc.compose(multi_adder(m, n))
            qc.measure(range(num_qubits-num_sum_qubits, num_qubits), range(num_sum_qubits))

            bq = bluequbit.init("YOUR_TOKEN_HERE")
            result = bq.run(qc)
            print(result.get_counts())

    """
    if m < 2:
        raise ValueError("m must be at least 2")
    if n < 1:
        raise ValueError("n must be at least 1")

    max_reg_value = 2**n - 1
    max_sum = m * max_reg_value
    num_sum_qubits = ceil(log2(max_sum + 0.5))

    # create the registers
    q_registers = [QuantumRegister(n, name=f"q{i}") for i in range(m - 1)]
    last_qreg = QuantumRegister(num_sum_qubits, name=f"q{m - 1}")

    # build summation circuit
    sum_qc = QuantumCircuit(*q_registers, last_qreg)

    current_num_qubits = n
    current_max_value = 2**n
    current_max_sum = 2 * max_reg_value
    for qreg in q_registers:
        if current_max_sum < current_max_value:  # no need for a new qubit
            if (
                current_max_sum + max_reg_value < current_max_value
                and qreg != q_registers[-1]
            ):  # if next one is fixed
                sum_qc.append(
                    DraperAdder(
                        n, current_num_qubits, include_qft=False, include_iqft=False
                    ),
                    qreg[:] + last_qreg[:current_num_qubits],
                )
            else:  # if the next adder has kind="half"
                sum_qc.append(
                    DraperAdder(n, current_num_qubits, include_qft=False),
                    qreg[:] + last_qreg[:current_num_qubits],
                )
        else:  # add one qubit
            current_num_qubits += 1
            current_max_value *= 2
            if (
                current_max_sum + max_reg_value < current_max_value
                and qreg != q_registers[-1]
            ):  # if next one is fixed
                sum_qc.append(
                    DraperAdder(
                        n, current_num_qubits - 1, kind="half", include_iqft=False
                    ),
                    qreg[:] + last_qreg[:current_num_qubits],
                )
            else:  # if the next adder has kind="half"
                sum_qc.append(
                    DraperAdder(n, current_num_qubits - 1, kind="half"),
                    qreg[:] + last_qreg[:current_num_qubits],
                )
        current_max_sum += max_reg_value

    return sum_qc
