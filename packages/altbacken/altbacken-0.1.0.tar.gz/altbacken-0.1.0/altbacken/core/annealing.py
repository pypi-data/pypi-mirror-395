from collections.abc import Callable, Generator
from dataclasses import dataclass
from typing import Protocol
from random import random as builtin_random

from altbacken.core.neighbourhood import Neighbourhood


@dataclass
class AnnealingState[T]:
    """
    Represents the state of the simulated annealing process.

    This class contains information about the current state of the process,
    including details about the iteration, temperature, and solutions
    (both current and best). It is designed to encapsulate and track the
    progress of the annealing algorithm, allowing for monitoring and analysis.

    Attributes:
        iteration (int): The current iteration number of the annealing process.
        temperature (float): The current temperature in the annealing schedule.
        current_solution (T): The solution being evaluated at the current step.
        current_value (float): The evaluation value of the current solution.
        best_solution (T): The best solution found so far.
        best_value (float): The evaluation value of the best solution found so far.
    """
    iteration: int
    temperature: float
    current_solution: T
    current_value: float
    best_solution: T
    best_value: float


class StopCondition[T](Protocol):
    """
    Protocol that defines a stop condition for an annealing process.

    This protocol is used to determine whether a simulated annealing process
    should terminate, based on the current state of the annealing procedure.
    Implementations of this protocol must define the __call__ method to evaluate
    the termination condition.

    Attributes:
        None
    """
    def __call__(self, state: AnnealingState[T]) -> bool:
        """
        Callable object to determine the termination condition of an annealing process.

        This function evaluates whether the annealing process should terminate upon
        being called with the current state. The decision logic is embedded within the
        function implementation, based on the properties and status of the provided
        current state.

        Args:
            state (AnnealingState[T]): The current state of the annealing process,
                providing the necessary information to evaluate the termination
                condition.

        Returns:
            bool: A boolean indicating whether the annealing process should terminate.
        """

type FitnessFunction[T] = Callable[[T], float]
type TemperatureFunction = Callable[[], Generator[float]]
type EnergyFunction = Callable[[float, float, float], float]
type RandomNumberGenerator = Callable[[], float]

class SimulatedAnnealing[T]:
    """
    SimulatedAnnealing class represents the simulated annealing optimization algorithm.

    This class performs optimization based on the simulated annealing technique, which iteratively
    explores a solution space to find a globally optimal solution for a given problem. The process relies
    on various components, such as temperature scheduling, fitness evaluation, neighborhood exploration,
    stop conditions, and energy functions to simulate the annealing process for optimization problems.

    Attributes:
        fitness (FitnessFunction[T]): A function that evaluates the fitness of a solution.
        temperature (TemperatureFunction): A generator function that determines the temperature at each iteration.
        neighbourhood (Neighbourhood[T]): A function that generates a neighboring solution for the current solution.
        stop_condition (StopCondition[T]): A function that determines when to stop the annealing process.
        energy (EnergyFunction): A function that computes the probability of transitioning between solutions.
        random (RandomNumberGenerator): A random number generator function, defaults to a built-in generator.
    """
    def __init__(
            self,
            fitness: FitnessFunction[T],
            temperature: TemperatureFunction,
            neighbourhood: Neighbourhood[T],
            stop_condition: StopCondition[T],
            energy: EnergyFunction,
            random: RandomNumberGenerator = builtin_random
    ):
        self._fitness: FitnessFunction[T] = fitness
        self._temperature: TemperatureFunction = temperature
        self._neighbourhood: Neighbourhood[T] = neighbourhood
        self._stop_condition: StopCondition[T] = stop_condition
        self._energy: EnergyFunction = energy
        self._random: RandomNumberGenerator = random


    def simulate(self, initial: T) -> tuple[T, float]:
        """
        Simulates an optimization process using a predefined algorithm.

        This method performs an iterative optimization process through a simulated
        annealing approach. A neighborhood function generates potential solutions,
        and fitness values are evaluated to determine solution quality. The process
        continues until a stopping condition is satisfied or a temperature generator
        is exhausted.

        Args:
            initial (T): The initial solution to start the optimization process.

        Returns:
            tuple[T, float]: A tuple containing the best solution found and its
            corresponding fitness value.

        Raises:
            StopIteration: If the temperature generator is exhausted before meeting
            the stopping condition.
        """
        temperatures: Generator[float] = self._temperature()
        initial_value: float = self._fitness(initial)
        state: AnnealingState[T] = AnnealingState(0, next(temperatures), initial, initial_value, initial, initial_value)
        while not self._stop_condition(state):
            state.iteration += 1
            try:
                state.temperature = next(temperatures)
            except StopIteration:
                return state.best_solution, state.best_value
            x: T = self._neighbourhood(state.current_solution)
            y: float = self._fitness(x)
            if y < state.best_value:
                state.best_value = y
                state.best_solution = x
                state.current_value = y
                state.current_solution = x
            elif self._phase_out(state.best_value, y, state.temperature):
                state.current_value = y
                state.current_solution = x
            state.iteration += 1
        return state.best_solution, state.best_value

    def _phase_out(self, current_value: float, new_value: float, current_temperature: float) -> bool:
        return self._random() < self._energy(current_value, new_value, current_temperature)