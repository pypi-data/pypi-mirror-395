from __future__ import annotations

from .backend import BlueQubitBackendV2


class BlueQubitProvider:
    """A Qiskit provider for accessing BlueQubit backend.

    :param api_token: API token of the user. If ``None``, the token will be looked
                      in the environment variable BLUEQUBIT_API_TOKEN.
    """

    def __init__(self, api_token: str | None = None):
        super().__init__()
        self.api_token = api_token

    def get_backend(self, execution_mode: str | None = None):
        """
        :param execution_mode: Execution mode. Can be ``"cloud"``, ``"local"`` or ``None``.
                           If ``None``, the environment variable
                           BLUEQUBIT_EXECUTION_MODE will be used if set, otherwise
                           ``"cloud"`` will be used.
        """
        return BlueQubitBackendV2(
            api_token=self.api_token, execution_mode=execution_mode
        )
