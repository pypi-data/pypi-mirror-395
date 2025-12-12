"""
Main EARCP ensemble model.

Copyright (c) 2025 Mike Amega. All rights reserved.
"""

import numpy as np
from typing import List, Optional, Dict, Any, Tuple, Union
import warnings

from ..config import EARCPConfig
from ..core.performance_tracker import PerformanceTracker
from ..core.coherence_metrics import CoherenceMetrics
from ..core.ensemble_weighting import EnsembleWeighting


class EARCP:
    """
    EARCP: Ensemble Auto-Régulé par Cohérence et Performance

    A self-regulating ensemble that dynamically weights heterogeneous expert
    models based on both performance and inter-model coherence.

    Parameters
    ----------
    experts : list
        List of expert models. Each must implement a predict(x) method.
    config : EARCPConfig, optional
        Configuration object. If None, uses default configuration.
    **kwargs
        Additional configuration parameters (overrides config).

    Attributes
    ----------
    n_experts : int
        Number of expert models.
    weights : np.ndarray
        Current expert weights.
    t : int
        Current time step.

    Examples
    --------
    >>> from earcp import EARCP
    >>> experts = [model1, model2, model3]
    >>> ensemble = EARCP(experts, beta=0.7, eta_s=5.0)
    >>> for t in range(T):
    ...     pred, expert_preds = ensemble.predict(state)
    ...     target = get_target(pred)
    ...     ensemble.update(expert_preds, target)
    """

    def __init__(
        self,
        experts: List[Any],
        config: Optional[EARCPConfig] = None,
        **kwargs
    ):
        # Initialize configuration
        if config is None:
            config = EARCPConfig(**kwargs)
        else:
            # Override config with kwargs
            config_dict = config.to_dict()
            config_dict.update(kwargs)
            config = EARCPConfig(**config_dict)

        self.config = config
        self.experts = experts
        self.n_experts = len(experts)

        # Validate experts
        self._validate_experts()

        # Set random seed if specified
        if config.random_state is not None:
            np.random.seed(config.random_state)

        # Initialize core components
        self.performance_tracker = PerformanceTracker(
            n_experts=self.n_experts,
            alpha=config.alpha_P,
            loss_fn=config.loss_fn,
            epsilon=config.epsilon
        )

        self.coherence_metrics = CoherenceMetrics(
            n_experts=self.n_experts,
            alpha=config.alpha_C,
            agreement_fn=config.coherence_fn,
            mode=config.prediction_mode,
            epsilon=config.epsilon
        )

        self.weighting = EnsembleWeighting(
            n_experts=self.n_experts,
            beta=config.beta,
            eta_s=config.eta_s,
            w_min=config.w_min,
            normalize=config.normalize_weights,
            epsilon=config.epsilon
        )

        # State
        self.t = 0
        self.weights = self.weighting.get_weights()

        # Diagnostics
        self.diagnostics = {
            'weights_history': [],
            'performance_history': [],
            'coherence_history': [],
            'ensemble_predictions': [],
        } if config.track_diagnostics else None

    def _validate_experts(self):
        """Validate that experts have required interface."""
        if self.n_experts < 2:
            raise ValueError(
                f"Need at least 2 experts, got {self.n_experts}"
            )

        for i, expert in enumerate(self.experts):
            if not hasattr(expert, 'predict'):
                raise ValueError(
                    f"Expert {i} must have a predict() method"
                )

    def predict(
        self,
        x: Union[np.ndarray, Any],
        return_expert_predictions: bool = True
    ) -> Union[np.ndarray, Tuple[np.ndarray, List[np.ndarray]]]:
        """
        Make ensemble prediction.

        Parameters
        ----------
        x : array-like
            Input to predict on.
        return_expert_predictions : bool
            Whether to return individual expert predictions.

        Returns
        -------
        prediction : np.ndarray
            Weighted ensemble prediction.
        expert_predictions : list of np.ndarray, optional
            Individual expert predictions (if return_expert_predictions=True).
        """
        # Get predictions from all experts
        expert_predictions = []
        for expert in self.experts:
            pred = expert.predict(x)
            # Ensure numpy array
            if not isinstance(pred, np.ndarray):
                pred = np.array(pred)
            expert_predictions.append(pred)

        # Weighted combination
        ensemble_prediction = self._combine_predictions(expert_predictions)

        # Store for diagnostics
        if self.diagnostics is not None:
            self.diagnostics['ensemble_predictions'].append(
                ensemble_prediction.copy()
            )

        if return_expert_predictions:
            return ensemble_prediction, expert_predictions
        else:
            return ensemble_prediction

    def _combine_predictions(
        self,
        predictions: List[np.ndarray]
    ) -> np.ndarray:
        """
        Combine expert predictions using current weights.

        Parameters
        ----------
        predictions : list of np.ndarray
            Predictions from each expert.

        Returns
        -------
        np.ndarray
            Weighted ensemble prediction.
        """
        # Stack predictions
        pred_array = np.array(predictions)  # Shape: (n_experts, ...)

        # Weighted sum
        # Reshape weights for broadcasting
        weights_expanded = self.weights.reshape(-1, *([1] * (pred_array.ndim - 1)))
        ensemble_pred = np.sum(weights_expanded * pred_array, axis=0)

        return ensemble_pred

    def update(
        self,
        expert_predictions: List[np.ndarray],
        target: np.ndarray
    ) -> Dict[str, Any]:
        """
        Update ensemble based on observed target.

        Parameters
        ----------
        expert_predictions : list of np.ndarray
            Predictions from each expert (from last predict() call).
        target : np.ndarray
            True target values.

        Returns
        -------
        dict
            Metrics from this update step.
        """
        # Update performance scores
        performance_scores = self.performance_tracker.update(
            expert_predictions,
            target
        )

        # Update coherence scores
        coherence_scores = self.coherence_metrics.update(expert_predictions)

        # Update weights
        self.weights = self.weighting.update_weights(
            performance_scores,
            coherence_scores
        )

        # Increment time step
        self.t += 1

        # Store diagnostics
        if self.diagnostics is not None:
            self.diagnostics['weights_history'].append(self.weights.copy())
            self.diagnostics['performance_history'].append(
                performance_scores.copy()
            )
            self.diagnostics['coherence_history'].append(
                coherence_scores.copy()
            )

        # Return metrics
        return {
            'weights': self.weights.copy(),
            'performance_scores': performance_scores,
            'coherence_scores': coherence_scores,
            'time_step': self.t,
        }

    def get_weights(self) -> np.ndarray:
        """Get current expert weights."""
        return self.weights.copy()

    def get_diagnostics(self) -> Dict[str, Any]:
        """
        Get comprehensive diagnostics.

        Returns
        -------
        dict
            Diagnostics including weights, scores, and histories.
        """
        diag = {
            'weights': self.weights.copy(),
            'performance_scores': self.performance_tracker.get_scores(),
            'coherence_scores': self.coherence_metrics.get_scores(),
            'time_step': self.t,
        }

        if self.diagnostics is not None:
            diag.update({
                'weights_history': np.array(
                    self.diagnostics['weights_history']
                ),
                'performance_history': np.array(
                    self.diagnostics['performance_history']
                ),
                'coherence_history': np.array(
                    self.diagnostics['coherence_history']
                ),
                'cumulative_loss': self.performance_tracker.get_cumulative_loss(),
            })

        return diag

    def reset(self):
        """Reset ensemble to initial state."""
        self.performance_tracker.reset()
        self.coherence_metrics.reset()
        self.weighting.reset()
        self.weights = self.weighting.get_weights()
        self.t = 0

        if self.diagnostics is not None:
            self.diagnostics = {
                'weights_history': [],
                'performance_history': [],
                'coherence_history': [],
                'ensemble_predictions': [],
            }

    def save_state(self, filepath: str):
        """
        Save ensemble state to file.

        Parameters
        ----------
        filepath : str
            Path to save state.
        """
        import pickle

        state = {
            'config': self.config.to_dict(),
            'weights': self.weights,
            'performance_scores': self.performance_tracker.get_scores(),
            'coherence_scores': self.coherence_metrics.get_scores(),
            'time_step': self.t,
            'diagnostics': self.diagnostics,
        }

        with open(filepath, 'wb') as f:
            pickle.dump(state, f)

    def load_state(self, filepath: str):
        """
        Load ensemble state from file.

        Parameters
        ----------
        filepath : str
            Path to load state from.
        """
        import pickle

        with open(filepath, 'rb') as f:
            state = pickle.load(f)

        # Restore state
        self.weights = state['weights']
        self.t = state['time_step']
        self.diagnostics = state['diagnostics']

        # Restore component states
        self.performance_tracker.P = state['performance_scores']
        self.coherence_metrics.C = state['coherence_scores']
        self.weighting.weights = state['weights']

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"EARCP(n_experts={self.n_experts}, "
            f"beta={self.config.beta}, "
            f"eta_s={self.config.eta_s}, "
            f"t={self.t})"
        )

    def __str__(self) -> str:
        """User-friendly string representation."""
        return (
            f"EARCP Ensemble\n"
            f"  Experts: {self.n_experts}\n"
            f"  Time step: {self.t}\n"
            f"  Weights: {self.weights}\n"
            f"  Config: beta={self.config.beta}, "
            f"eta_s={self.config.eta_s}"
        )
