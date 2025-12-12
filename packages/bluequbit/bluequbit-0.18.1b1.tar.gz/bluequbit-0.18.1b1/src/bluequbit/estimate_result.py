class EstimateResult:  # pylint: disable=too-few-public-methods
    """This class contains information about the estimated runtime/cost that
    will be incurred from running the given circuit on the given quantum
    machine/simulator. `WARNING:` this is just an estimate, the actual runtime/cost
    may be less or more."""

    def __init__(self, data):
        self.device = data.get("device")

        #: int: estimated runtime in milliseconds
        self.estimated_runtime = data.get("estimate_ms")

        #: float: estimated cost in US dollars
        self.estimated_cost = data.get("estimated_cost")
        if self.estimated_cost is not None:
            self.estimated_cost /= 100.0

        #: int: number of qubits
        self.num_qubits = data.get("num_qubits")

        #: str: warning message
        self.warning_message = data.get("warning_message")

        #: str: error message if available
        self.error_message = data.get("error_message")

    def __repr__(self):
        if self.error_message is not None:
            return f"Estimation failed due to error: {self.error_message}."
        return (
            f"Estimated: runtime: {self.estimated_runtime} ms, cost:"
            f" ${self.estimated_cost:.2f}. {self.warning_message}"
        )
