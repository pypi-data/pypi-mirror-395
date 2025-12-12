from __future__ import annotations

import contextlib

from . import exceptions, job_metadata_constants
from .bluequbit_client import BQClient
from .bluequbit_logger import init_logger
from .estimate_result import EstimateResult
from .job_result import JobResult

with contextlib.suppress(ImportError):
    from .qiskit_provider.backend import BlueQubitBackendV2
    from .qiskit_provider.estimator import BlueQubitEstimatorV2
    from .qiskit_provider.provider import BlueQubitProvider
    from .qiskit_provider.sampler import BlueQubitSamplerV2

from .version import __version__

with contextlib.suppress(ImportError):
    from .__init__private import *  # noqa: F403

__all__ = [
    "BQClient",
    "BlueQubitBackendV2",
    "BlueQubitEstimatorV2",
    "BlueQubitProvider",
    "BlueQubitSamplerV2",
    "EstimateResult",
    "JobResult",
    "__version__",
    "exceptions",
    "job_metadata_constants",
]

logger = init_logger()


def init(api_token: str | None = None, execution_mode: str | None = None) -> BQClient:
    """Returns :class:`BQClient` instance for managing jobs on BlueQubit platform.

    :param api_token: API token of the user. If ``None``, the token will be looked
                      in the environment variable BLUEQUBIT_API_TOKEN.
    :param execution_mode: Execution mode. Can be ``"cloud"``, ``"local"`` or ``None``.
                           If ``None``, the environment variable
                           BLUEQUBIT_EXECUTION_MODE will be used if set, otherwise
                           ``"cloud"`` will be used.
    """
    return BQClient(api_token, execution_mode)
