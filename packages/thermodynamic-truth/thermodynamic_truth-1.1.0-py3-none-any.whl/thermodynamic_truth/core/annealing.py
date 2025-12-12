"""
Thermodynamic Annealing for Consensus

Implements simulated annealing with parallel tempering for consensus convergence.
This is the core algorithm that drives the system toward low-energy, high-coherence states.
"""

import numpy as np
from typing import List, Tuple, Optional, Callable
import time
from .state import ConsensusState, ThermodynamicEnsemble


class AnnealingSchedule:
    """
    Defines the temperature schedule for simulated annealing.

    The schedule determines how temperature decreases over time,
    controlling the exploration-exploitation tradeoff.
    """

    def __init__(
        self,
        T_initial: float = 10.0,
        T_final: float = 0.01,
        schedule_type: str = "exponential",
        alpha: float = 0.95,
    ):
        """
        Initialize annealing schedule.

        Args:
            T_initial: Initial temperature (high for exploration)
            T_final: Final temperature (low for exploitation)
            schedule_type: Type of schedule ('exponential', 'linear', 'logarithmic')
            alpha: Cooling rate for exponential schedule
        """
        self.T_initial = T_initial
        self.T_final = T_final
        self.schedule_type = schedule_type
        self.alpha = alpha
        self.current_step = 0

    def get_temperature(self, step: Optional[int] = None) -> float:
        """
        Get temperature at given step.

        Args:
            step: Annealing step (uses current_step if None)

        Returns:
            Temperature at this step
        """
        if step is None:
            step = self.current_step

        if self.schedule_type == "exponential":
            # T(k) = T_0 * alpha^k
            T = self.T_initial * (self.alpha**step)
            return max(T, self.T_final)

        elif self.schedule_type == "linear":
            # T(k) = T_0 - k * (T_0 - T_f) / max_steps
            # Assume max_steps = 100 for linear
            max_steps = 100
            T = self.T_initial - step * (self.T_initial - self.T_final) / max_steps
            return max(T, self.T_final)

        elif self.schedule_type == "logarithmic":
            # T(k) = T_0 / log(k + 2)
            T = self.T_initial / np.log(step + 2)
            return max(T, self.T_final)

        else:
            return self.T_initial

    def step(self) -> float:
        """
        Advance to next step and return new temperature.

        Returns:
            New temperature
        """
        self.current_step += 1
        return self.get_temperature()

    def reset(self):
        """Reset schedule to initial state."""
        self.current_step = 0


class ParallelTempering:
    """
    Parallel tempering (replica exchange) for enhanced sampling.

    Runs multiple replicas at different temperatures and exchanges them
    to escape local minima. This is inspired by UAP maneuver simulations.
    """

    def __init__(self, n_replicas: int = 4, T_min: float = 0.1, T_max: float = 10.0):
        """
        Initialize parallel tempering.

        Args:
            n_replicas: Number of temperature replicas
            T_min: Minimum temperature (cold chain)
            T_max: Maximum temperature (hot chain)
        """
        self.n_replicas = n_replicas
        self.T_min = T_min
        self.T_max = T_max

        # Create geometric temperature ladder
        self.temperatures = np.geomspace(T_min, T_max, n_replicas)

        # Track which ensemble is at which temperature
        self.replica_assignments = list(range(n_replicas))

    def compute_exchange_probability(self, E_i: float, E_j: float, T_i: float, T_j: float) -> float:
        """
        Compute Metropolis-Hastings acceptance probability for replica exchange.

        P(exchange) = min(1, exp(-(1/T_i - 1/T_j)(E_j - E_i)))

        Args:
            E_i: Energy of replica i
            E_j: Energy of replica j
            T_i: Temperature of replica i
            T_j: Temperature of replica j

        Returns:
            Exchange acceptance probability
        """
        beta_i = 1.0 / (T_i + 1e-10)
        beta_j = 1.0 / (T_j + 1e-10)

        delta = (beta_i - beta_j) * (E_j - E_i)

        if delta <= 0:
            return 1.0
        else:
            return np.exp(-delta)

    def attempt_exchange(
        self, ensembles: List[ThermodynamicEnsemble]
    ) -> List[ThermodynamicEnsemble]:
        """
        Attempt replica exchanges between adjacent temperatures.

        Args:
            ensembles: List of ensembles at different temperatures

        Returns:
            Ensembles after exchange attempts
        """
        if len(ensembles) != self.n_replicas:
            return ensembles

        # Try exchanges between adjacent replicas
        for i in range(self.n_replicas - 1):
            j = i + 1

            # Get energies
            E_i = ensembles[i].compute_free_energy()
            E_j = ensembles[j].compute_free_energy()

            # Get temperatures
            T_i = self.temperatures[i]
            T_j = self.temperatures[j]

            # Compute exchange probability
            p_exchange = self.compute_exchange_probability(E_i, E_j, T_i, T_j)

            # Attempt exchange
            if np.random.rand() < p_exchange:
                # Swap ensembles
                ensembles[i], ensembles[j] = ensembles[j], ensembles[i]

        return ensembles

    def get_cold_chain(self, ensembles: List[ThermodynamicEnsemble]) -> ThermodynamicEnsemble:
        """
        Get the coldest (lowest temperature) ensemble.

        This is the one we use for consensus.

        Args:
            ensembles: List of ensembles

        Returns:
            Cold chain ensemble
        """
        return ensembles[0]


class ThermodynamicAnnealer:
    """
    Main annealing engine for thermodynamic consensus.

    Combines simulated annealing with parallel tempering to converge
    to consensus states with minimal free energy.
    """

    def __init__(
        self,
        schedule: Optional[AnnealingSchedule] = None,
        use_parallel_tempering: bool = True,
        n_replicas: int = 4,
    ):
        """
        Initialize annealer.

        Args:
            schedule: Annealing schedule (creates default if None)
            use_parallel_tempering: Whether to use parallel tempering
            n_replicas: Number of replicas for parallel tempering
        """
        self.schedule = schedule or AnnealingSchedule()
        self.use_parallel_tempering = use_parallel_tempering

        if use_parallel_tempering:
            self.tempering = ParallelTempering(
                n_replicas=n_replicas, T_min=self.schedule.T_final, T_max=self.schedule.T_initial
            )
        else:
            self.tempering = None

        self.convergence_history = []

    def anneal_step(
        self, ensemble: ThermodynamicEnsemble, temperature: float
    ) -> ThermodynamicEnsemble:
        """
        Perform one annealing step on an ensemble.

        This reweights states according to Boltzmann distribution at given temperature.

        Args:
            ensemble: Current ensemble
            temperature: Current temperature

        Returns:
            Updated ensemble
        """
        if len(ensemble.states) == 0:
            return ensemble

        # Update ensemble temperature
        ensemble.temperature = temperature

        # Compute Boltzmann weights
        beta = 1.0 / (temperature + 1e-10)
        weights = ensemble.compute_boltzmann_weights(beta)

        # Resample states according to weights (importance sampling)
        n_states = len(ensemble.states)
        indices = np.random.choice(n_states, size=n_states, p=weights, replace=True)

        # Create resampled ensemble
        resampled_states = [ensemble.states[i] for i in indices]

        new_ensemble = ThermodynamicEnsemble(
            states=resampled_states,
            temperature=temperature,
            boltzmann_constant=ensemble.boltzmann_constant,
        )

        return new_ensemble

    def converge(
        self,
        ensemble: ThermodynamicEnsemble,
        max_steps: int = 100,
        convergence_threshold: float = 1e-3,
    ) -> Tuple[ThermodynamicEnsemble, dict]:
        """
        Run annealing until convergence.

        Args:
            ensemble: Initial ensemble
            max_steps: Maximum annealing steps
            convergence_threshold: Variance threshold for convergence

        Returns:
            Tuple of (converged_ensemble, metrics)
        """
        self.schedule.reset()
        self.convergence_history = []

        current_ensemble = ensemble
        start_time = time.time()

        for step in range(max_steps):
            # Get current temperature
            T = self.schedule.get_temperature(step)

            # Perform annealing step
            current_ensemble = self.anneal_step(current_ensemble, T)

            # Compute metrics
            variance = current_ensemble.compute_variance()
            entropy = current_ensemble.compute_entropy()
            free_energy = current_ensemble.compute_free_energy()

            # Record history
            self.convergence_history.append(
                {
                    "step": step,
                    "temperature": T,
                    "variance": variance,
                    "entropy": entropy,
                    "free_energy": free_energy,
                }
            )

            # Check convergence
            if variance < convergence_threshold:
                break

            # Advance schedule
            self.schedule.step()

        elapsed_time = time.time() - start_time

        # Compile metrics
        metrics = {
            "steps": step + 1,
            "final_variance": variance,
            "final_entropy": entropy,
            "final_free_energy": free_energy,
            "convergence_time": elapsed_time,
            "converged": variance < convergence_threshold,
            "history": self.convergence_history,
        }

        return current_ensemble, metrics

    def converge_with_tempering(
        self,
        ensemble: ThermodynamicEnsemble,
        max_steps: int = 100,
        exchange_interval: int = 10,
        convergence_threshold: float = 1e-3,
    ) -> Tuple[ThermodynamicEnsemble, dict]:
        """
        Run annealing with parallel tempering.

        Args:
            ensemble: Initial ensemble
            max_steps: Maximum annealing steps
            exchange_interval: Steps between replica exchanges
            convergence_threshold: Variance threshold for convergence

        Returns:
            Tuple of (converged_ensemble, metrics)
        """
        if not self.use_parallel_tempering or self.tempering is None:
            return self.converge(ensemble, max_steps, convergence_threshold)

        # Create replicas at different temperatures
        replicas = []
        for T in self.tempering.temperatures:
            replica = ThermodynamicEnsemble(
                states=ensemble.states.copy(),
                temperature=T,
                boltzmann_constant=ensemble.boltzmann_constant,
            )
            replicas.append(replica)

        start_time = time.time()
        self.convergence_history = []

        for step in range(max_steps):
            # Anneal each replica at its temperature
            for i, replica in enumerate(replicas):
                T = self.tempering.temperatures[i]
                replicas[i] = self.anneal_step(replica, T)

            # Attempt replica exchanges
            if step % exchange_interval == 0:
                replicas = self.tempering.attempt_exchange(replicas)

            # Get cold chain for monitoring
            cold_chain = self.tempering.get_cold_chain(replicas)
            variance = cold_chain.compute_variance()
            entropy = cold_chain.compute_entropy()

            # Record history
            self.convergence_history.append(
                {
                    "step": step,
                    "variance": variance,
                    "entropy": entropy,
                }
            )

            # Check convergence
            if variance < convergence_threshold:
                break

        elapsed_time = time.time() - start_time

        # Get final cold chain
        final_ensemble = self.tempering.get_cold_chain(replicas)

        metrics = {
            "steps": step + 1,
            "final_variance": final_ensemble.compute_variance(),
            "final_entropy": final_ensemble.compute_entropy(),
            "convergence_time": elapsed_time,
            "converged": variance < convergence_threshold,
            "history": self.convergence_history,
            "n_replicas": self.tempering.n_replicas,
        }

        return final_ensemble, metrics
