from functools import wraps

from qiskit.providers import JobError, JobStatus
from qiskit.providers import JobV1 as Job
from qiskit.result import Result

from bluequbit import job_metadata_constants


def requires_submit(func):
    """
    Decorator to ensure that a submit has been performed before
    calling the method.

    Args:
        func (callable): test function to be decorated.

    Returns:
        callable: the decorated function.
    """

    @wraps(func)
    def _wrapper(self, *args, **kwargs):
        if self._backend_job is None:
            raise JobError("Job not submitted yet!. You have to .submit() first!")
        return func(self, *args, **kwargs)

    return _wrapper


class BlueQubitQiskitJob(Job):
    def __init__(
        self,
        backend,
        job_id: str,
        fn,
        circuits,
        run_options=None,
    ):
        super().__init__(backend, job_id)
        self._job_id = job_id
        self._backend = backend
        self._backend_job = None
        self._circuits = circuits
        self._fn = fn
        self._run_options = run_options

    def submit(self):
        """Submit the job to the backend for execution."""
        if self._backend_job is not None:
            raise JobError("BlueQubit job already submitted!")
        self._backend_job = self._fn(self._circuits, self._run_options)

    @requires_submit
    def result(self) -> Result:
        """Return the results of the job."""
        if self._backend.execution_mode != "local":
            return self._backend.bq_client.wait(self._backend_job)
        return self._backend_job

    @requires_submit
    def cancel(self):
        """Attempt to cancel the job."""
        if self._backend.execution_mode == "local":
            raise JobError("Cannot cancel job in local mode")
        return self._backend.bq_client.cancel(self._backend_job)

    @requires_submit
    def status(self) -> JobStatus:
        """Return the status of the job, among the values of ``JobStatus``."""
        if self._backend.execution_mode == "local":
            return JobStatus.DONE
        job_status = [
            r.run_status for r in self._backend.bq_client.get(self._backend_job)
        ]
        if all(
            s in job_metadata_constants.JOB_RESULTS_READY_STATES for s in job_status
        ):
            return JobStatus.DONE
        if any(s in job_metadata_constants.JOB_NON_TERMINAL_STATES for s in job_status):
            return JobStatus.RUNNING
        return JobStatus.ERROR
