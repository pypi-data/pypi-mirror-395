from . import job_metadata_constants

AUTH_ERROR_MESSAGE = (
    "BlueQubit client was not authorized. For full functionality please specify an API token to init(<your-api-token>) or have API"
    " token set in BLUEQUBIT_API_TOKEN environment variable. You can"
    " find your API token once you log in to https://app.bluequbit.io"
)


class BQError(Exception):
    def __init__(self, message="Unknown Error Message"):
        super().__init__(message)
        self.message = message


class BQSDKUsageError(BQError):
    def __init__(self, message):
        super().__init__(message)


class BQUnauthorizedAccessError(BQError):
    def __init__(self, request_id):
        super().__init__(AUTH_ERROR_MESSAGE + f". Request ID: {request_id}")
        self.request_id = request_id


class BQJobStatevectorNotAvailableError(BQError):
    def __init__(self, job_id, num_qubits, shots, pauli_sum):
        message = "Statevector is not available."
        if shots is not None and shots != 0:
            message += " Job run with shots > 0. Please use .get_counts() instead."
        elif num_qubits > job_metadata_constants.MAX_QUBITS_WITH_STATEVEC:
            message += f" Job has too many, {num_qubits}, qubits."
        elif pauli_sum is not None:
            message += " Observables are provided."
        super().__init__(message)
        self.job_id = job_id
        self.num_qubits = num_qubits


class BQJobNotCompleteError(BQError):
    def __init__(self, job_id, run_status, error_message):
        super().__init__(
            f"Job {job_id} finished with status: {run_status}. {error_message}",
        )
        self.job_id = job_id
        self.run_status = run_status
        self.error_message = error_message


class BQJobHasNotFinishedYetError(BQError):
    def __init__(self, job_id, run_status):
        super().__init__(
            f"Job {job_id} has not finished yet. Current status: {run_status}.",
        )
        self.job_id = job_id
        self.run_status = run_status


class BQJobCouldNotCancelError(BQError):
    def __init__(self, job_id, run_status, error_message):
        super().__init__(
            f"Couldn't cancel job {job_id}. Finished status is {run_status}."
            f" {error_message}",
        )
        self.job_id = job_id
        self.run_status = run_status


class BQBatchJobsLimitExceededError(BQError):
    def __init__(self, num):
        super().__init__(
            "Batch operations job count limit exceeded. The maximum is"
            f" {job_metadata_constants.MAXIMUM_NUMBER_OF_BATCH_JOBS}, but {num} was"
            " used."
        )
        self.num = num


class BQJobsLimitExceededError(BQError):
    def __init__(self, num):
        super().__init__(
            "Maximum number of batch jobs to run is "
            f" {job_metadata_constants.MAXIMUM_NUMBER_OF_JOBS_FOR_RUN}, but {num} was"
            " used."
        )
        self.num = num


class BQCPUJobsLimitExceededError(BQError):
    def __init__(self, num):
        super().__init__(
            "Maximum free CPU jobs limit is "
            f" {job_metadata_constants.QUEUED_CPU_JOBS_LIMIT}, but {num} was"
            " used."
        )
        self.num = num


class BQAPIError(BQError):
    def __init__(self, http_status_code, error_message, request_id):
        super().__init__(
            f"{error_message.strip()}. HTTP response status code: {http_status_code}. Request ID: {request_id}",
        )
        self.http_status_code = http_status_code
        self.error_message = error_message
        self.request_id = request_id


class BQJobInvalidDeviceTypeError(BQError):
    def __init__(self, device):
        super().__init__(
            f"Invalid device type {device}. Must be one of"
            f" {', '.join(job_metadata_constants.DEVICE_TYPES)}."
        )


class BQJobExceedsSerializedCircuitSizeLimitError(BQError):
    def __init__(self, size):
        super().__init__(
            f"Circuit size is {size} bytes which exceeds {job_metadata_constants.MAXIMUM_SERIALIZED_CIRCUIT_SIZE / 1_000_000:.0f} MB limit."
        )


class BQJobsMalformedShotsError(BQError):
    def __init__(self, shots, device, max_shots):
        super().__init__(
            f"Malformed number of shots: {shots} or exceeds limit of"
            f" {max_shots} for {device} device."
        )
