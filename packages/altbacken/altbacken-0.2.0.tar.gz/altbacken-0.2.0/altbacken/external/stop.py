from altbacken.core.annealing import AnnealingState


class TemperatureThreshold:
    """
    Represents a temperature threshold for an annealing process.

    This class is used to determine whether a given annealing state's
    temperature has fallen below a specified threshold. It helps in controlling
    the termination criteria for algorithms based on simulated annealing
    techniques.

    Attributes:
        threshold (float): Specifies the non-negative temperature value used
            as the limit for comparison.
    """
    def __init__(self, threshold: float):
        if threshold < 0:
            raise ValueError("Threshold must be non-negative")
        self.threshold = threshold

    def __call__(self, state: AnnealingState) -> bool:
        return state.temperature < self.threshold


class IterationThreshold:
    """Represents a stopping criterion based on a threshold iteration count.

    This class is used to determine whether a process, such as an optimization
    algorithm, should stop based on the current iteration surpassing a predefined
    iteration threshold. It can be utilized as a callable object in these scenarios.

    Attributes:
        threshold (int): The iteration count threshold. The process stops
            when the current iteration reaches or exceeds this value.
    """
    def __init__(self, threshold: int):
        if threshold <= 0:
            raise ValueError("Threshold must be positive")
        self.threshold = threshold

    def __call__(self, state: AnnealingState) -> bool:
        return state.iteration >= self.threshold