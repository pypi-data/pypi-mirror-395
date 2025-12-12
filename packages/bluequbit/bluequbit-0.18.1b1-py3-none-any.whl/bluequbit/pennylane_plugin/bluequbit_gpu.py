from .bluequbit_device import BluequbitDevice


class BluequbitGPU(BluequbitDevice):
    """BluequbitGPU device for PennyLane. This device is used to run Pennylane circuits on BlueQubit platform using a
    gpu device and is similar to using lightning.gpu on your local device. It requires a BlueQubit token, which
    you can get from your BlueQubit account. This device is not free to use, so make sure the cost is appropriate for
    you.

    .. warning::

            To use this plugin, you must have pennylane>=0.39 version installed. It requires
            Python 3.9, but we would recommend using Python 3.10 . Make sure your Python version
            is not older.

    Args:
        wires (int, Iterable[Number, str]): Number of subsystems represented by the device,
            or iterable that contains unique labels for the subsystems as numbers (i.e., ``[-1, 0, 2]``)
            or strings (``['auxiliary', 'q1', 'q2']``). Default 1 if not specified.
        token (str, None): Your BlueQubit token. This is an optional keyword argument that defaults to None.
            If None, the token will be retrieved from the BLUEQUBIT_API_TOKEN environment variable.
    """

    short_name = "bluequbit.gpu"

    def __init__(self, wires, *args, token=None, **kwargs):
        super().__init__(wires, *args, token=token, **kwargs)
        self._device = "pennylane.gpu"
