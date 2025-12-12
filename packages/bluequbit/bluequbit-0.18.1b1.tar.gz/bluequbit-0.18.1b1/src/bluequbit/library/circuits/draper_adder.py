# Qiskit notice begins here
# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
# Qiskit notice ends here

# This file has been modified based on:
# https://github.com/Qiskit/qiskit/blob/main/qiskit/circuit/library/arithmetic/adders/draper_qft_adder.py
# Changes made:
# - The class has been renamed from DraperQFTAdder to DraperAdder
# - Modified to support addition of registers with different sizes, instead of equally sized registers
# - Changed the base class from Adder to QuantumCircuit, because Adder is for equally sized registers
# - Added arguments for the sizes of each register. The second one is optional and equal to the first by default
# - Added two arguments  that allow to remove QFT and IQFT parts of the circuit
# - Changed the name of the circuit to this form: "DraperAdder_m_n_kind_int(include_qft)_int(include_iqft))"
# - Changed the docstring to adjust the style and correspond to the modifications


"""Compute the sum of two qubit registers using QFT."""

from __future__ import annotations

import numpy as np
from qiskit.circuit import QuantumRegister
from qiskit.circuit.library.basis_change import QFT
from qiskit.circuit.quantumcircuit import QuantumCircuit


class DraperAdder(QuantumCircuit):
    r"""A circuit that uses QFT to perform in-place addition on two qubit registers.

    For registers with :math:`m` and :math:`n` qubits, where :math:`m \leq n`, the QFT adder can perform addition modulo
    :math:`2^n` (with ``kind="fixed"``) or ordinary addition by adding a carry qubits (with
    ``kind="half"``). It also provides options to omit ``QFT`` or ``IQFT`` parts of DraperAdder through
    ``include_qft`` and ``include_iqft`` arguments.

    The name of the circuit is in the form "DraperAdder_m_n_kind_int(include_qft)_int(include_iqft)",
    e.g. DraperAdder_3_5_half_1_0

    :param m: The number of qubits in the first input register for
            state :math:`|a\rangle`. The second input
            registers must have at least as many qubits as the first one (m<=n).
    :param n: The number of qubits in the second input register for
            state :math:`|b\rangle`. The second input
            registers must have at least as many qubits as the first one (m<=n).
            If ``n`` is not provided it will be equal to ``m`` by default.
    :param kind: The kind of adder, can be ``'half'`` for a half adder or
            ``'fixed'`` for a fixed-sized adder. A half adder contains a carry-out to represent
            the most-significant bit, but the fixed-sized adder doesn't and hence performs
            addition modulo ``2 ** num_state_qubits``.
    :param name: The name of the circuit object \(default is "DraperAdder"\). The other parameters will be added to
        this name as described above
    :param include_qft: If ``False``, the ``QFT`` part is not added to the circuit
    :param include_iqft: If ``False``, the ``IQFT`` part is not added to the circuit
    :raises ValueError: If ``m`` is lower than 1 or if ``m > n``


    As an example, a non-fixed_point QFT adder circuit that performs addition on two 2-qubit sized
    registers is as follows:

    .. parsed-literal::

         a_0:   ─────────■──────■────────────────────────■────────────────
                         │      │                        │
         a_1:   ─────────┼──────┼────────■──────■────────┼────────────────
                ┌──────┐ │P(π)  │        │      │        │       ┌───────┐
         b_0:   ┤0     ├─■──────┼────────┼──────┼────────┼───────┤0      ├
                │      │        │P(π/2)  │P(π)  │        │       │       │
         b_1:   ┤1 qft ├────────■────────■──────┼────────┼───────┤1 iqft ├
                │      │                        │P(π/2)  │P(π/4) │       │
        cout_0: ┤2     ├────────────────────────■────────■───────┤2      ├
                └──────┘                                         └───────┘

    **References:**

    [1] T. G. Draper, Addition on a Quantum Computer, 2000.
    `arXiv:quant-ph/0008033 <https://arxiv.org/pdf/quant-ph/0008033.pdf>`_

    [2] Ruiz-Perez et al., Quantum arithmetic with the Quantum Fourier Transform, 2017.
    `arXiv:1411.5949 <https://arxiv.org/pdf/1411.5949.pdf>`_

    [3] Vedral et al., Quantum Networks for Elementary Arithmetic Operations, 1995.
    `arXiv:quant-ph/9511018 <https://arxiv.org/pdf/quant-ph/9511018.pdf>`_

    """

    def __init__(
        self,
        m: int,
        n: int | None = None,
        kind: str = "fixed",
        name: str = "DraperAdder",
        include_qft: bool = True,
        include_iqft: bool = True,
    ) -> None:
        if n is None:
            n = m

        if kind == "full":
            raise ValueError(
                "The DraperAdder only supports 'half' and 'fixed' as ``kind``."
            )

        if m < 1:
            raise ValueError(
                "The number of qubits in the first register must be at least 1."
            )

        if m > n:
            raise ValueError(
                "The first register must not have more qubits than the second (m <= n)"
            )

        name += f"_{m}_{n}_{kind}_{int(include_qft)}_{int(include_iqft)}"
        super().__init__(name=name)

        qr_a = QuantumRegister(m, name="a")
        qr_b = QuantumRegister(n, name="b")
        qr_list = [qr_a, qr_b]

        if kind == "half":
            qr_z = QuantumRegister(1, name="cout")
            qr_list.append(qr_z)

        # add registers
        self.add_register(*qr_list)

        # define register containing the sum and number of qubits for QFT circuit
        qr_sum = qr_b[:] if kind == "fixed" else qr_b[:] + qr_z[:]
        num_qubits_qft = n if kind == "fixed" else n + 1

        circuit = QuantumCircuit(*self.qregs, name=name)

        # build QFT adder circuit
        if include_qft:
            circuit.append(QFT(num_qubits_qft, do_swaps=False).to_gate(), qr_sum[:])

        for j in range(m):
            for k in range(n - j):
                lam = np.pi / (2**k)
                circuit.cp(lam, qr_a[j], qr_b[j + k])

        if kind == "half":
            for j in range(m):
                lam = np.pi / (2 ** (j + 1 + n - m))
                circuit.cp(lam, qr_a[m - j - 1], qr_z[0])

        if include_iqft:
            circuit.append(
                QFT(num_qubits_qft, do_swaps=False).inverse().to_gate(), qr_sum[:]
            )

        self.append(circuit.to_gate(), self.qubits)
