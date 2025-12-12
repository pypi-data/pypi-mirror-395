from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import numpy as np
from qiskit.primitives import (
    BaseEstimatorV2,
    PrimitiveJob,
    PrimitiveResult,
    PubResult,
)
from qiskit.primitives.containers import DataBin, EstimatorPubLike
from qiskit.primitives.containers.estimator_pub import EstimatorPub

from .provider import BlueQubitBackendV2

if TYPE_CHECKING:
    from collections.abc import Iterable

logger = logging.getLogger("bluequbit-python-sdk")


class BlueQubitEstimatorV2(BaseEstimatorV2):
    """
    Evaluates expectation values for provided quantum circuit and observable combinations.

    Qiskit Estimator V2 interface to BlueQubit cloud computation: https://docs.quantum.ibm.com/api/qiskit-ibm-runtime/qiskit_ibm_runtime.EstimatorV2
    Based on:
    - https://github.com/Qiskit/qiskit-ibm-runtime/blob/main/qiskit_ibm_runtime/estimator.py
    - https://github.com/Qiskit/qiskit-aer/blob/main/qiskit_aer/primitives/estimator_v2.py
    """

    def __init__(
        self,
        *,
        backend: BlueQubitBackendV2 | None = None,
        options: dict | None = None,
    ):
        self._options = options if options is not None else {}
        if backend is None:
            backend = BlueQubitBackendV2(**self._options.get("backend_options", {}))
        self._run_options = self._options.get("run_options", {})
        self._backend = backend
        self._warned_precision = False

    @property
    def options(self):
        """Return the options"""
        return self._options

    def run(
        self, pubs: Iterable[EstimatorPubLike], *, precision: float | None = None
    ) -> PrimitiveJob[PrimitiveResult[PubResult]]:
        if precision is not None and not self._warned_precision:
            logger.warning(
                "BlueQubit only supports float32 precision. The precision argument is going to be ignored."
            )
            self._warned_precision = True
        coerced_pubs = [EstimatorPub.coerce(pub, precision) for pub in pubs]
        job = PrimitiveJob(self._run, coerced_pubs)
        job._submit()  # noqa: SLF001
        return job

    def _run(self, pubs: list[EstimatorPub]) -> PrimitiveResult[PubResult]:
        return PrimitiveResult([self._run_pub(pub) for pub in pubs])

    def _run_pub(self, pub: EstimatorPub) -> PubResult:
        circuit = pub.circuit
        observables = pub.observables
        parameter_values = pub.parameter_values

        bound_circuits = parameter_values.bind_all(circuit)
        bc_circuits, bc_obs = np.broadcast_arrays(bound_circuits, observables)

        evs = np.zeros_like(bc_circuits, dtype=np.float64)

        for index in np.ndindex(*bc_circuits.shape):
            bound_circuit = bc_circuits[index]
            observable = bc_obs[index]
            precision = pub.precision

            pauli_sums = list(observable.items())
            job = self._backend.run(
                bound_circuit,
                pauli_sum=pauli_sums,  # type: ignore[arg-type]
                **self._run_options,
            )
            result = job.result()
            expectation_value = np.real_if_close(result.expectation_value)
            if precision != 0 and not np.isreal(expectation_value):
                raise ValueError(
                    "Given operator is not Hermitian and noise cannot be added."
                )
            evs[index] = expectation_value

        data = DataBin(evs=evs, shape=evs.shape)
        return PubResult(
            data,
            metadata={
                "target_precision": precision,
                "circuit_metadata": pub.circuit.metadata,
            },
        )
