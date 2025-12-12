from __future__ import annotations

import datetime
import json
import logging
import zlib

import dateutil.parser

from bluequbit.circuit_serialization import encode_circuit_with_fallback
from bluequbit.exceptions import (
    BQError,
    BQJobExceedsSerializedCircuitSizeLimitError,
)
from bluequbit.job_metadata_constants import MAXIMUM_SERIALIZED_CIRCUIT_SIZE
from bluequbit.tools import format_pauli_sum

logger = logging.getLogger("bluequbit-python-sdk")

_SINGLE_REQUEST_LIMIT = 100


def search_jobs(
    _connection,
    run_status=None,
    created_later_than=None,
    job_ids=None,
    batch_id=None,
    *,
    need_qc_unprocessed=False,
):
    if created_later_than is None:
        parsed_created_later_than = None
    elif isinstance(created_later_than, str):
        parsed_created_later_than_datetime = dateutil.parser.parse(created_later_than)
        if parsed_created_later_than_datetime.tzinfo is None:
            logger.warning(
                "created_later_than is a str object without timezone info, assuming UTC"
                " timezone"
            )
            parsed_created_later_than_datetime = (
                parsed_created_later_than_datetime.replace(tzinfo=datetime.timezone.utc)
            )
        parsed_created_later_than = parsed_created_later_than_datetime.isoformat()
    elif isinstance(created_later_than, datetime.datetime):
        if created_later_than.tzinfo is None:
            raise BQError(
                "created_later_than is a datetime object without timezone info"
            )
        parsed_created_later_than = created_later_than.isoformat()
    else:
        raise BQError(
            "created_later_than should be None, str, or datetime.datetime object"
        )

    params = {
        "limit": _SINGLE_REQUEST_LIMIT,
        "run_status": run_status,
        "created_later_than": parsed_created_later_than,
        "job_ids": job_ids,
        "batch_id": batch_id,
        "need_qc_unprocessed": str(need_qc_unprocessed),
        # "need_top_128": True,
    }
    result_dict: dict = {"data": []}
    while True:
        response = _connection.send_request(req_type="GET", path="/jobs", params=params)
        response = response.json()

        results = response["data"]
        result_dict["data"] += results
        result_dict["total_count"] = response["total_count"]

        if len(results) < _SINGLE_REQUEST_LIMIT:
            break

        params["offset"] = len(result_dict["data"])
    return result_dict


def submit_jobs(
    _connection,
    circuits,
    device,
    job_name=None,
    shots=None,
    pauli_sum=None,
    options=None,
    tags=None,
    *,
    estimate_only=False,
    asynchronous=False,
):
    encoded_circuits: dict | list[dict]
    if isinstance(circuits, list):
        encoded_circuits = [
            encode_circuit_with_fallback(circuit) for circuit in circuits
        ]
        if pauli_sum is not None:
            for ec in encoded_circuits:
                ec["pauli_sum"] = format_pauli_sum(pauli_sum)
        if options is not None:
            for ec in encoded_circuits:
                ec["options"] = options
    else:
        encoded_circuits = encode_circuit_with_fallback(circuits)
        assert isinstance(encoded_circuits, dict)
        if pauli_sum is not None:
            encoded_circuits["pauli_sum"] = format_pauli_sum(pauli_sum)
        if options is not None:
            encoded_circuits["options"] = options

    params = {
        "estimate_only": estimate_only,
        "circuit": encoded_circuits,
        "job_name": job_name,
        "device": device,
        "shots": shots,
        "asynchronous": asynchronous,
        "tags": tags,
    }
    data_str = json.dumps(params)
    data = data_str.encode()
    data_size = len(data)
    if data_size > MAXIMUM_SERIALIZED_CIRCUIT_SIZE:
        raise BQJobExceedsSerializedCircuitSizeLimitError(data_size)

    if data_size > 2000:
        data = zlib.compress(data)
        headers = {"content-encoding": "gzip"}
    else:
        headers = {"content-type": "application/json"}
    response = _connection.send_request(
        req_type="POST", path="/jobs", data=data, headers=headers
    )
    return response.json()["data"]


def cancel_jobs(_connection, job_ids):
    response = _connection.send_request(
        req_type="PATCH", path="/jobs", json_req={"job_ids": job_ids, "cancel": True}
    )
    return response.json()["data"]
