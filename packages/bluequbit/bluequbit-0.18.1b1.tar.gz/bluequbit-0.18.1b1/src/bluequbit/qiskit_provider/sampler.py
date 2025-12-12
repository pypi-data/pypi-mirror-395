from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np
from qiskit.primitives import (
    BaseSamplerV2,
    PrimitiveJob,
    PrimitiveResult,
    SamplerPubResult,
)
from qiskit.primitives.containers.sampler_pub import SamplerPub

from .provider import BlueQubitBackendV2

if TYPE_CHECKING:
    from collections.abc import Iterable

    from qiskit.circuit import QuantumCircuit
    from qiskit.primitives.containers import SamplerPubLike
    from qiskit.result import Result


@dataclass
class BQDataBin:
    meas: Result


class BlueQubitSamplerV2(BaseSamplerV2):
    """
    Qiskit SamplerV2 interface to BlueQubit cloud computation.
    """

    def __init__(
        self,
        *,
        backend: BlueQubitBackendV2 | None = None,
        backend_options: dict | None = None,
        run_options: dict | None = None,
    ):
        """
        Args:
            backend: The backend to run the primitive on.
            options: The options to specify the BlueQubit device type.
                For now, if you specify ``seed_simulator`` for deterministic output,
        """
        self._backend_options = backend_options if backend_options is not None else {}
        if backend is None:
            backend = BlueQubitBackendV2(**self._backend_options)

        self._backend = backend
        self._run_options = run_options if run_options is not None else {}

    def run(
        self, pubs: Iterable[SamplerPubLike], *, shots: int | None = None
    ) -> PrimitiveJob[PrimitiveResult[SamplerPubResult]]:
        if shots is None:
            shots = self._options.default_shots
        coerced_pubs = [SamplerPub.coerce(pub, shots) for pub in pubs]
        job = PrimitiveJob(self._run, coerced_pubs)
        job._submit()  # noqa: SLF001
        return job

    def _run(self, pubs: list[SamplerPub]) -> PrimitiveResult[SamplerPubResult]:
        pub_dict = defaultdict(list)
        # consolidate pubs with the same number of shots
        for i, pub in enumerate(pubs):
            pub_dict[pub.shots].append(i)

        results = [None] * len(pubs)
        for shots, lst in pub_dict.items():
            # run pubs with the same number of shots at once
            pub_results = self._run_pubs([pubs[i] for i in lst], shots)
            # reconstruct the result of pubs
            for i, pub_result in zip(lst, pub_results, strict=True):
                results[i] = pub_result
        return PrimitiveResult(results)

    def _run_pubs(self, pubs: list[SamplerPub], shots: int) -> list[SamplerPubResult]:
        """Compute results for pubs that all require the same value of ``shots``."""
        # prepare circuits
        bound_circuits = [pub.parameter_values.bind_all(pub.circuit) for pub in pubs]
        flatten_circuits: list[QuantumCircuit] = []
        for circuits in bound_circuits:
            flatten_circuits.extend(np.ravel(circuits).tolist())

        # run circuits
        job = self._backend.run(flatten_circuits, shots=shots, **self._run_options)
        results = job.result()

        pub_result = [
            SamplerPubResult(BQDataBin(meas=results[i])) for i in range(len(results))
        ]
        return pub_result
