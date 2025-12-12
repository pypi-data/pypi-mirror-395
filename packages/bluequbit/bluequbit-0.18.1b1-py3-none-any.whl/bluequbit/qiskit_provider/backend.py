from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import TYPE_CHECKING

from qiskit.providers import BackendV2, Options

import bluequbit
from bluequbit.qiskit_provider.job import BlueQubitQiskitJob

if TYPE_CHECKING:
    from qiskit import QuantumCircuit
    from qiskit.result import Result


@dataclass
class BQDataBin:
    meas: Result


class BlueQubitBackendV2(BackendV2):
    def __init__(
        self,
        api_token: str | None = None,
        execution_mode=None,
    ):
        super().__init__()
        self.bq_client = bluequbit.init(
            api_token=api_token, execution_mode=execution_mode
        )
        self.execution_mode = self.bq_client.execution_mode

    @classmethod
    def _default_options(cls):
        return Options(
            shots=None,
            device="cpu",
            job_name=None,
            pauli_sum=None,
            options=None,
        )

    @property
    def max_circuits(self):
        return None

    @property
    def target(self):
        return None

    def run(
        self,
        circuits: QuantumCircuit | list[QuantumCircuit],
        **run_options,
    ):
        options = self._default_options().__dict__ | run_options

        job_id = str(uuid.uuid4())
        bq_job = BlueQubitQiskitJob(
            self,
            job_id=job_id,
            fn=self._execute,
            circuits=circuits,
            run_options=options,
        )
        bq_job.submit()
        return bq_job

    def _execute(self, circuits: QuantumCircuit | list[QuantumCircuit], options):
        jobs = self.bq_client.run(
            circuits,
            asynchronous=self.execution_mode == "cloud",
            **options,
        )
        return jobs
