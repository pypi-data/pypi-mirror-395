r"""
The "bluequbit.device" device is the base device for Bluequbit Pennylane plugin used to run Pennylane circuits on
BlueQubit platform
"""

# ruff: noqa: ARG002

from __future__ import annotations

import base64
import pickle
import zlib
from collections import defaultdict
from typing import TYPE_CHECKING, ClassVar

from pennylane import numpy as np
from pennylane.devices import QubitDevice
from pennylane.ops.qubit.attributes import diagonal_in_z_basis

import bluequbit.exceptions
from bluequbit import BQClient
from bluequbit.job_metadata_constants import QUEUED_CPU_JOBS_LIMIT

if TYPE_CHECKING:
    from collections.abc import Callable


class BluequbitDevice(QubitDevice):
    """BluequbitDevice device for PennyLane. This device is not directly used but serves as the base class
    for BluequbitCPU and BluequbitGPU subclasses. However, most functionality of the plugin is implemented
    inside this class. The plugin is used to run Pennylane circuits on BlueQubit platform. It requires a
    BlueQubit token, which you can get from your BlueQubit account.

    .. warning::

            To use this plugin, you must have pennylane>=0.39 version installed. It requires
            Python 3.9, but we would recommend using Python 3.10 . Make sure your Python version
            is not older.

    Args:
        wires (int, Iterable[Number, str]): Number of subsystems represented by the device,
            or iterable that contains unique labels for the subsystems as numbers (i.e., ``[-1, 0, 2]``)
            or strings (``['auxiliary', 'q1', 'q2']``). Default 1 if not specified.
        token (str, None): Your BlueQubit token. This is an optional keyword argument that defaults to None.
            If None, the token will be retrieved from the BLUEQUBIT_API_TOKEN environment variable.
    """

    name = "Bluequbit PennyLane plugin"
    short_name = "bluequbit.device"
    pennylane_requires = ">=0.39"
    version = "0.0.1"
    author = "Bluequbit"

    operations: ClassVar[set[str]] = {
        "Identity",
        "Snapshot",
        "BasisState",
        "StatePrep",
        "QubitStateVector",
        "QubitUnitary",
        "ControlledQubitUnitary",
        "MultiControlledX",
        "DiagonalQubitUnitary",
        "SpecialUnitary",
        "PauliX",
        "PauliY",
        "PauliZ",
        "MultiRZ",
        "Hadamard",
        "S",
        "Adjoint(S)",
        "T",
        "Adjoint(T)",
        "SX",
        "Adjoint(SX)",
        "CNOT",
        "SWAP",
        "ISWAP",
        "PSWAP",
        "Adjoint(ISWAP)",
        "SISWAP",
        "Adjoint(SISWAP)",
        "SQISW",
        "CSWAP",
        "Toffoli",
        "CY",
        "CZ",
        "CCZ",
        "CH",
        "PhaseShift",
        "ControlledPhaseShift",
        "CPhase",
        "RX",
        "RY",
        "RZ",
        "Rot",
        "CRX",
        "CRY",
        "CRZ",
        "CRot",
        "IsingXX",
        "IsingYY",
        "IsingZZ",
        "IsingXY",
        "SingleExcitation",
        "SingleExcitationPlus",
        "SingleExcitationMinus",
        "DoubleExcitation",
        "DoubleExcitationPlus",
        "DoubleExcitationMinus",
        "QubitCarry",
        "QubitSum",
        "OrbitalRotation",
        "QFT",
        "ECR",
    }

    observables: ClassVar[set[str]] = {
        "PauliX",
        "PauliY",
        "PauliZ",
        "Hadamard",
        "Hermitian",
        "Identity",
        "Projector",
        "SparseHamiltonian",
        "Hamiltonian",
        "Sum",
        "SProd",
        "Prod",
        "Exp",
    }

    def __init__(self, wires, *args, token=None, **kwargs):
        default_kwargs = {
            "shots": None,
            "analytic": None,
            "r_dtype": np.float64,
            "c_dtype": np.complex128,
        }
        kwargs = {**default_kwargs, **kwargs}

        self._operation_calls = defaultdict(int)
        super().__init__(
            wires,
            shots=kwargs["shots"],
            r_dtype=kwargs["r_dtype"],
            c_dtype=kwargs["c_dtype"],
            analytic=kwargs["analytic"],
        )
        self._debugger = None

        # Create the initial state. The state will always be None.
        self._state = self._create_basis_state(0)
        self._pre_rotated_state = self._state

        self._apply_ops: dict[str, Callable] = {
            "PauliX": self._apply_x,
            "PauliY": self._apply_y,
            "PauliZ": self._apply_z,
            "Hadamard": self._apply_hadamard,
            "S": self._apply_s,
            "T": self._apply_t,
            "SX": self._apply_sx,
            "CNOT": self._apply_cnot,
            "SWAP": self._apply_swap,
            "CZ": self._apply_cz,
            "Toffoli": self._apply_toffoli,
        }

        self._device = "bluequbit.device"
        self._token = token

        try:
            self._bq = BQClient(self._token)
        except bluequbit.exceptions.BQUnauthorizedAccessError:
            raise ValueError(
                "BlueQubit authentication failed. Please provide a valid API token when creating the PennyLane device "
                "using the 'token' parameter (e.g., dev = qml.device('bluequbit.cpu', wires=1, token='<your-token>')) "
                "or set the BLUEQUBIT_API_TOKEN environment variable. "
                "You can find your API token at https://app.bluequbit.io."
            ) from None

    # pylint: disable=arguments-differ
    def apply(self, operations, *args, **kwargs):
        for op in operations:
            self._apply_operation(self._state, op)

    def _apply_operation(self, state, operation):
        self._operation_calls[operation.name] += 1

        if operation.name in self._apply_ops:
            return self._apply_ops[operation.name](state, axes=None)

        wires = operation.wires
        if operation in diagonal_in_z_basis:
            return self._apply_diagonal_unitary(state, None, wires)
        if len(wires) <= 2:
            # Einsum is faster for small gates
            return self._apply_unitary_einsum(state, None, wires)
        return self._apply_unitary(state, None, wires)

    def _apply_x(self, state, axes, **kwargs):
        return [0.0]

    def _apply_y(self, state, axes, **kwargs):
        return [0.0]

    def _apply_z(self, state, axes, **kwargs):
        return [0.0]

    def _apply_hadamard(self, state, axes, **kwargs):
        return [0.0]

    def _apply_s(self, state, axes, inverse=False):
        return [0.0]

    def _apply_t(self, state, axes, inverse=False):
        return [0.0]

    def _apply_sx(self, state, axes, inverse=False):
        return [0.0]

    def _apply_cnot(self, state, axes, **kwargs):
        return [0.0]

    def _apply_swap(self, state, axes, **kwargs):
        return [0.0]

    def _apply_cz(self, state, axes, **kwargs):
        return [0.0]

    def _apply_toffoli(self, state, axes, **kwargs):
        return [0.0]

    def _apply_phase(self, state, axes, parameters, inverse=False):
        return [0.0]

    def expval(self, observable, shot_range=None, bin_size=None):
        return [0.0]

    def var(self, observable, shot_range=None, bin_size=None):
        return [0.0]

    @classmethod
    def capabilities(cls):
        capabilities = super().capabilities().copy()
        capabilities.update(
            model="qubit",
            supports_inverse_operations=True,
            supports_analytic_computation=True,
            supports_broadcasting=False,
            returns_state=True,
            passthru_devices={},
        )
        return capabilities

    @staticmethod
    def _create_basis_state(index):  # noqa: ARG004
        return [0.0]

    @property
    def state(self):
        return [0.0]

    def density_matrix(self, wires):
        return [0.0]

    def _apply_state_vector(self, state, device_wires):
        return [0.0]

    def _apply_basis_state(self, state, wires):
        return [0.0]

    def _apply_unitary(self, state, mat, wires):
        return [0.0]

    def _apply_unitary_einsum(self, state, mat, wires):
        return [0.0]

    def _apply_diagonal_unitary(self, state, phases, wires):
        return [0.0]

    def reset(self):
        self._operation_calls = defaultdict(int)

    def analytic_probability(self, wires=None):
        return [0.0]

    def generate_samples(self):
        """Returns the computational basis samples generated for all wires.
        In the _qubit_device.py, the function calls for analytic_probability for its operations.
        """
        return self.analytic_probability()

    def sample(self, observable, shot_range=None, bin_size=None, counts=False):
        return [0.0]

    def operation_calls(self):
        """Statistics of operation calls"""
        return self._operation_calls

    def execute(self, circuit, **kwargs):
        data = {"circuit": {"pennylane_circuit": circuit}, "method": "execute"}
        result = self._run_bluequbit(data)
        return result

    def batch_execute(self, circuits, **kwargs):
        if type(circuits) is tuple:
            circuits = list(circuits)
        if len(circuits) == 1:
            res = [self.execute(circuits[0])]
        elif len(circuits) > QUEUED_CPU_JOBS_LIMIT:
            raise ValueError(
                f"Cannot run more than {QUEUED_CPU_JOBS_LIMIT} jobs in batch mode"
            )
        else:
            circuit_batch = [{"pennylane_circuit": c} for c in circuits]
            data = {"circuit": circuit_batch, "method": "batch"}
            res = self._run_bluequbit(data)
        return res

    @staticmethod
    def _decode_pennylane_result(result):
        encoded_result = result._pennylane_result  # noqa: SLF001
        decoded_result = base64.b64decode(encoded_result)
        return pickle.loads(zlib.decompress(decoded_result))  # noqa: S301

    def _run_bluequbit(self, data):
        device = data.get("device", self._device)

        result = self._bq.run(
            circuits=data.get("circuit"), device=device, shots=self.shots
        )
        print(result)

        if isinstance(result, list):
            batch_result = [
                self._decode_pennylane_result(single_result) for single_result in result
            ]
            return batch_result
        return self._decode_pennylane_result(result)

    def adjoint_jacobian(self, tape, starting_state=None, use_device_state=False):
        data = {
            "circuit": {"pennylane_circuit": tape},
            "method": "adjoint_jacobian",
            "device": self._device + ".adjoint",
        }
        result = self._run_bluequbit(data)
        return result
