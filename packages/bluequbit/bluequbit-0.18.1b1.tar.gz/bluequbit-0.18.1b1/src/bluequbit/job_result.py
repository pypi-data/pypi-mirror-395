from __future__ import annotations

import base64
import datetime
import json
import zlib
from io import BytesIO

import numpy as np
import packaging
from dateutil.parser import parse

from . import job_metadata_constants
from .exceptions import (
    BQJobHasNotFinishedYetError,
    BQJobNotCompleteError,
    BQJobStatevectorNotAvailableError,
    BQSDKUsageError,
)
from .http_utils import request_retriable
from .version import __version__

SDK_VERSION = packaging.version.parse(__version__)


class JobResult:
    """This class contains information from a job run on quantum hardware or
    quantum simulators. Mainly it contains the resulting statevector from the
    run. It might contain only partial information, such as job ID,
    when :func:`BQClient.run` is called with ``asynchronous=True``."""

    def __init__(self, data, _backend_connection=None):
        super().__init__()

        self._backend_connection = _backend_connection

        #: str: job id
        self.job_id = data.get("job_id")

        #: str: batch id
        self.batch_id = data.get("batch_id")

        #: str: job run status, can be one of ``"FAILED_VALIDATION"`` | ``"PENDING"`` |
        #       ``"QUEUED"`` | ``"RUNNING"`` | ``"TERMINATED"`` | ``"CANCELED"`` |
        #       ``"NOT_ENOUGH_FUNDS"`` | ``"COMPLETED"``
        self.run_status = data.get("run_status")

        #: str: job name
        self.job_name = data.get("job_name")

        #: str: run device
        self.device = data.get("device")

        #: dict: device parameters used in circuit execution
        self.device_options = data.get("device_options")

        #: int: estimated runtime in milliseconds
        self.estimated_runtime = data.get("estimated_runtime_ms")

        #: float: estimated cost in US dollars
        self.estimated_cost = data.get("estimated_cost")
        if self.estimated_cost is not None:
            self.estimated_cost /= 100.0

        #: datetime: job creation date in UTC timezone
        self.created_on = parse(data.get("created_on"))

        self._results_path = data.get("results_path")

        self._top_100k_results = None

        #: dict: top 128 results
        self.top_128_results = data.get("top_128")

        self._pennylane_result = data.get("pennylane_result")

        #: int: number of qubits
        self.num_qubits = data.get("num_qubits")

        #: int: number of used qubits
        self.num_qubits_used = data.get("num_qubits_used", self.num_qubits)

        #: dict[str, Any]: tags, a JSON serializable dictionary.
        self.tags = data.get("tags")

        #: list[tuple[str, float]]: expectation value
        self.pauli_sum = data.get("pauli_sum")

        #: float | list[float]: expectation value
        self.expectation_value = data.get("expectation_value")

        self.run_start = data.get("run_start")
        if self.run_start is not None:
            self.run_start = parse(self.run_start)

        self.run_end = data.get("run_end")
        if self.run_end is not None:
            self.run_end = parse(self.run_end)

        #: int: job queue time in milliseconds
        self.queue_time_ms = None
        if self.run_start is not None:
            self.queue_time_ms = int(
                (self.run_start - self.created_on) / datetime.timedelta(milliseconds=1)
            )

        #: int: job runtime in milliseconds
        self.run_time_ms = None
        if self.run_start is not None and self.run_end is not None:
            self.run_time_ms = round(
                (self.run_end - self.run_start) / datetime.timedelta(milliseconds=1)
            )

        #: str: error message if failed
        self.error_message = data.get("error_message")

        #: float: job cost in US dollars
        self.cost = data.get("cost")
        if self.cost is not None:
            self.cost /= 100.0

        #: bool: if statevector available
        self.has_statevector = data.get("has_statevector")

        # This is present by default only on results by _run_circuit_local.
        self._statevector = data.get("state_vector")

        #: Cirq, Qiskit, dict: original circuit
        self.circuit = data.get("qc_unprocessed")
        if self.circuit is not None:
            self.circuit = json.loads(
                zlib.decompress(base64.b64decode(self.circuit)).decode()
            )

        self.sdk_version = data.get("sdk_version")
        if self.sdk_version is not None:
            self.sdk_version = packaging.version.parse(self.sdk_version)

        #: int: number of shots specified during the job submission
        self.shots = data.get("shots")

    def get_statevector(self) -> np.ndarray:
        """Return statevector of the job. If the statevector is too large then throws exception.

        :rtype: NumPy array
        """
        if self.run_status in job_metadata_constants.JOB_NON_TERMINAL_STATES:
            raise BQJobHasNotFinishedYetError(self.job_id, self.run_status)
        if not self.ok:
            raise BQJobNotCompleteError(
                self.job_id, self.run_status, self.error_message
            )
        if self.num_qubits_used > job_metadata_constants.MAX_QUBITS_WITH_STATEVEC:
            raise BQJobStatevectorNotAvailableError(
                self.job_id, self.num_qubits_used, self.shots, self.expectation_value
            )
        if self.has_statevector is False:
            raise BQJobStatevectorNotAvailableError(
                self.job_id, self.num_qubits_used, self.shots, self.expectation_value
            )

        if self._statevector is None:
            response = request_retriable("GET", self._results_path + "statevector.txt")
            self._statevector = np.loadtxt(
                BytesIO(response.content), dtype=np.complex128
            )

        return self._statevector

    def get_counts(self) -> None | dict[str, float]:
        """
        If shots argument in bq.run() was not None, return a number of samples
        from the measurements, otherwise, measurement probabilities of the
        computation result, without any statistical fluctuation are returned. In both
        cases only top 131072 (2^17) results are returned.
        """
        if self.top_128_results is not None and len(self.top_128_results) < 128:
            return self.top_128_results
        if self.run_status in job_metadata_constants.JOB_NON_TERMINAL_STATES:
            raise BQJobHasNotFinishedYetError(self.job_id, self.run_status)
        if not self.ok:
            raise BQJobNotCompleteError(
                self.job_id, self.run_status, self.error_message
            )
        if self._top_100k_results is None:
            response = request_retriable("GET", self._results_path + "metadata.json")
            # in case of old jobs that have hybrid_code_result as not None we didn't upload metadata.json
            if response.ok:
                self._top_100k_results = json.loads(response.content).get("counts")
            else:
                raise BQSDKUsageError("Counts are not available for this job")

        return self._top_100k_results

    @property
    def ok(self) -> bool:  # pylint: disable=invalid-name
        """``True``, if job's current run status is ``"COMPLETED"``,
        else ``False``."""

        return self.run_status == "COMPLETED"

    def __repr__(self):
        jr_repr = f"Job ID: {self.job_id}"
        if self.batch_id is not None:
            jr_repr += f" (batch ID: {self.batch_id})"
        if self.job_name is not None:
            jr_repr += f", name: {self.job_name}"
        jr_repr += f", device: {self.device}"
        jr_repr += f", run status: {self.run_status}"
        jr_repr += (
            f", created on: {self.created_on.replace(microsecond=0, tzinfo=None)} UTC"
        )
        if (
            self.run_status in ["PENDING", "QUEUED", "RUNNING"]
            and self.estimated_runtime is not None
        ):
            jr_repr += f", estimated runtime: {self.estimated_runtime} ms"
            jr_repr += f", estimated cost: ${self.estimated_cost:.2f}"
        if self.cost is not None:
            jr_repr += f", cost: ${self.cost:.2f}"
        if self.run_time_ms is not None:
            jr_repr += f", run time: {self.run_time_ms} ms"
        if self.queue_time_ms is not None:
            jr_repr += f", queue time: {self.queue_time_ms} ms"
        if self.num_qubits is not None:
            jr_repr += f", num qubits: {self.num_qubits}"
        if self.num_qubits_used != self.num_qubits:
            jr_repr += f", num qubits used: {self.num_qubits_used}"
        if self.shots is not None:
            jr_repr += f", shots: {self.shots}"
        if self.error_message is not None:
            jr_repr += f", error_message: {self.error_message}"
        return jr_repr
