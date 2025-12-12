from __future__ import annotations

import importlib.util
import logging
import os
import time
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

from . import job_metadata_constants
from .circuit_serialization import encode_circuit_with_fallback, is_a_qiskit_circuit
from .computation_local import run_circuit_cirq, run_circuit_qiskit
from .exceptions import (
    BQJobNotCompleteError,
    BQSDKUsageError,
)
from .host_info import check_local_gpu_availability
from .job_result import JobResult
from .tools import format_pauli_sum

if TYPE_CHECKING:
    from collections.abc import Callable

logger = logging.getLogger("bluequbit-python-sdk")

_warning_no_deqart_internal_shown = False
_local_execution_mode_used = False


def run_circuits_local(
    circuits,
    device: str,
    *,
    job_name: str | None = None,
    shots: int | None = None,
    pauli_sum: Any | None = None,
    options: dict | None = None,
    tags: dict[str, Any] | None = None,
):
    global _warning_no_deqart_internal_shown  # noqa: PLW0603
    global _local_execution_mode_used  # noqa: PLW0603

    if not _local_execution_mode_used:
        os.environ["BLUEQUBIT_DEQART_INTERNAL_ANALYSIS_LOGGER_NAME"] = (
            "bluequbit-python-sdk"
        )
        _local_execution_mode_used = True

    # GPU availability check and fallback to CPU
    original_device = device
    if "gpu" in device:
        gpu_available = check_local_gpu_availability()
        if not gpu_available:
            device = job_metadata_constants.DEVICE_FALLBACK_MAPPING.get(device, device)
            logger.warning(
                f"NVIDIA GPU not detected locally. Falling back from '{original_device}' to '{device}' device."
            )

    # if changing device options, please change backend jobs.py new_single_job() code
    device_options = {}
    options = options or {}
    if "mps" in device:
        device_options["mps_bond_dimension"] = options.get(
            "mps_bond_dimension", job_metadata_constants.MPS_DEFAULT_BOND_DIMENSION
        )
        device_options["mps_truncation_threshold"] = options.get(
            "mps_truncation_threshold",
            job_metadata_constants.MPS_DEFAULT_TRUNCATION_THRESHOLD,
        )
    if "pauli-path" in device:
        pps_truncation_threshold = options.get("pauli_path_truncation_threshold")
        if pps_truncation_threshold is None:
            pps_truncation_threshold = 0.0
        device_options["pauli_path_truncation_threshold"] = pps_truncation_threshold
        pps_transpilation_level = options.get("pauli_path_circuit_transpilation_level")
        if pps_transpilation_level is None:
            pps_transpilation_level = (
                job_metadata_constants.PAULI_PATH_DEFAULT_TRANSPILATION_LEVEL
            )
        device_options["pauli_path_circuit_transpilation_level"] = (
            pps_transpilation_level
        )
        if "gpu" in device:
            pps_gpu_weight_cutoff = options.get("pauli_path_weight_cutoff")
            device_options["pauli_path_weight_cutoff"] = pps_gpu_weight_cutoff
    options = device_options

    created_on = time.time()
    if pauli_sum is not None:
        pauli_sum = format_pauli_sum(pauli_sum)

    def _format_result(r):
        def to_str_time(x):
            return (
                datetime.fromtimestamp(x, tz=timezone.utc)
                .astimezone()
                .strftime("%Y-%m-%d %H:%M:%S.%f")
            )

        r["created_on"] = to_str_time(created_on)
        r["run_start"] = to_str_time(r["run_start"])
        r["run_end"] = to_str_time(r["run_end"])
        r["has_statevector"] = "state_vector" in r
        r["run_status"] = "COMPLETED"
        r["job_name"] = job_name
        r["shots"] = shots
        r["pauli_sum"] = pauli_sum
        r["device_options"] = options
        r["tags"] = tags
        res = JobResult(r)
        res._top_100k_results = r.get("counts")  # noqa: SLF001
        return res

    first_circuit = circuits[0] if isinstance(circuits, list) else circuits
    if importlib.util.find_spec("deqart_internal") is not None:
        # os.environ["BLUEQUBIT_PPS_USE_PARALLEL_COMPUTE"] = "1"
        from deqart_internal.analysis import estimate_and_validate
        from deqart_internal.computation import run_circuit

        logger.debug("Using local deqart_internal")

        def _run_and_format_result(circuit):
            encoded_circuit = encode_circuit_with_fallback(circuit)
            encoded_circuit["hybrid_code_snippet"] = None
            encoded_circuit["pauli_sum"] = pauli_sum
            encoded_circuit["shots"] = shots
            encoded_circuit["seed"] = None
            if options is not None:
                encoded_circuit["options"] = options
            (
                estimate_result,
                deqart_circuit,
                validation_result,
                validation_ok,
                _,
            ) = estimate_and_validate(
                encoded_circuit,
                False,
                device,
                execution_mode="local",
                decoded_circuit=circuit,
            )
            if not validation_ok:
                raise BQJobNotCompleteError(
                    "local",
                    "FAILED_VALIDATION",
                    validation_result,
                )
            r = run_circuit(deqart_circuit)
            jr = _format_result(r)
            jr.num_qubits_used = estimate_result["num_qubits_used"]
            jr.num_qubits = estimate_result["num_qubits"]
            jr.circuit = encoded_circuit
            jr.job_id = "local"
            return jr

        if isinstance(circuits, list):
            zero_fill_count = len(str(len(circuits) - 1))
            jrs = [_run_and_format_result(c) for c in circuits]
            for i, jr in enumerate(jrs):
                jr.batch_id = "local"
                if job_name is not None:
                    jr.job_name = f"{job_name}_{str(i).zfill(zero_fill_count)}"
            return jrs

        return _run_and_format_result(circuits)
    if not _warning_no_deqart_internal_shown:
        logger.warning("Using local execution mode without deqart_internal")
        _warning_no_deqart_internal_shown = True
    fn: Callable
    if is_a_qiskit_circuit(first_circuit):
        fn = run_circuit_qiskit
    elif str(type(first_circuit)) == "<class 'cirq.circuits.circuit.Circuit'>":
        fn = run_circuit_cirq
    else:
        error_msg = f"Circuit type not yet supported for {first_circuit}"
        raise BQSDKUsageError(error_msg) from None

    if isinstance(circuits, list):
        jrs = [_format_result(fn(c, shots=shots)) for c in circuits]
        for i, jr in enumerate(jrs):
            jr.batch_id = "localn"
            jr.job_id = "localn"
            if job_name is not None:
                jr.job_name = f"{job_name}_{str(i).zfill(len(str(len(circuits) - 1)))}"
            jr.num_qubits = len(circuits[i].qubits)
            jr.num_qubits_used = jr.num_qubits
        return jrs

    jr = _format_result(fn(circuits, shots=shots))
    jr.num_qubits = len(circuits.qubits)
    jr.num_qubits_used = jr.num_qubits
    jr.job_name = job_name
    jr.job_id = "localn"
    return jr
