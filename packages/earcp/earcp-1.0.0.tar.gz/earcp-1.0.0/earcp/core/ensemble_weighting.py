"""
Ensemble weighting mechanism for EARCP.

Copyright (c) 2025 Mike Amega. All rights reserved.
"""

import numpy as np
from typing import Optional


class EnsembleWeighting:
    """
    Computes and maintains expert weights based on performance and coherence.

    Implements the core EARCP weighting algorithm:
    1. Combine performance P and coherence C scores
    2. Apply softmax-like transformation with sensitivity
    3. Enforce weight floor to prevent expert starvation

    Parameters
    ----------
    n_experts : int
        Number of expert models.
    beta : float
        Balance between performance and coherence (0 <= beta <= 1).
    eta_s : float
        Learning rate / sensitivity parameter.
    w_min : float
        Minimum weight floor.
    normalize : bool
        Whether to normalize weights to sum to 1.
    epsilon : float
        Numerical stability constant.
    """

    def __init__(
        self,
        n_experts: int,
        beta: float = 0.7,
        eta_s: float = 5.0,
        w_min: float = 0.05,
        normalize: bool = True,
        epsilon: float = 1e-10
    ):
        self.n_experts = n_experts
        self.beta = beta
        self.eta_s = eta_s
        self.w_min = w_min
        self.normalize = normalize
        self.epsilon = epsilon

        # Validate w_min
        if w_min > 1.0 / n_experts:
            raise ValueError(
                f"w_min ({w_min}) must be <= 1/M ({1.0/n_experts}) "
                f"for M={n_experts} experts"
            )

        # Initialize weights uniformly
        self.weights = np.ones(n_experts) / n_experts
        self.weight_history = []

    def update_weights(
        self,
        performance_scores: np.ndarray,
        coherence_scores: np.ndarray
    ) -> np.ndarray:
        """
        Update expert weights based on performance and coherence.

        Parameters
        ----------
        performance_scores : np.ndarray
            Performance scores P (shape: n_experts).
        coherence_scores : np.ndarray
            Coherence scores C (shape: n_experts).

        Returns
        -------
        np.ndarray
            Updated weights (shape: n_experts).
        """
        if len(performance_scores) != self.n_experts:
            raise ValueError(
                f"Expected {self.n_experts} performance scores, "
                f"got {len(performance_scores)}"
            )
        if len(coherence_scores) != self.n_experts:
            raise ValueError(
                f"Expected {self.n_experts} coherence scores, "
                f"got {len(coherence_scores)}"
            )

        # Step 1: Combine performance and coherence
        # s_i = beta * P_i + (1 - beta) * C_i
        combined_scores = (
            self.beta * performance_scores +
            (1 - self.beta) * coherence_scores
        )

        # Step 2: Apply softmax transformation with sensitivity
        # w_i ∝ exp(eta_s * s_i)
        # Use log-sum-exp trick for numerical stability
        max_score = np.max(combined_scores)
        exp_scores = np.exp(self.eta_s * (combined_scores - max_score))
        raw_weights = exp_scores / (np.sum(exp_scores) + self.epsilon)

        # Step 3: Apply weight floor
        # w_i = max(w_i, w_min)
        floored_weights = np.maximum(raw_weights, self.w_min)

        # Step 4: Renormalize if needed
        if self.normalize:
            self.weights = floored_weights / (np.sum(floored_weights) + self.epsilon)
        else:
            self.weights = floored_weights

        # Store for diagnostics
        self.weight_history.append(self.weights.copy())

        return self.weights.copy()

    def get_weights(self) -> np.ndarray:
        """Get current weights."""
        return self.weights.copy()

    def get_weight_history(self) -> np.ndarray:
        """Get weight history (shape: T x n_experts)."""
        return np.array(self.weight_history)

    def reset(self):
        """Reset to uniform weights."""
        self.weights = np.ones(self.n_experts) / self.n_experts
        self.weight_history = []

    def set_beta(self, beta: float):
        """Update beta parameter."""
        if not 0 <= beta <= 1:
            raise ValueError(f"beta must be in [0, 1], got {beta}")
        self.beta = beta

    def set_eta_s(self, eta_s: float):
        """Update sensitivity parameter."""
        if eta_s <= 0:
            raise ValueError(f"eta_s must be positive, got {eta_s}")
        self.eta_s = eta_s


class AdaptiveEnsembleWeighting(EnsembleWeighting):
    """
    Extended weighting with adaptive parameters.

    Automatically adjusts beta and eta_s based on ensemble performance.
    """

    def __init__(
        self,
        n_experts: int,
        beta: float = 0.7,
        eta_s: float = 5.0,
        w_min: float = 0.05,
        normalize: bool = True,
        epsilon: float = 1e-10,
        adapt_beta: bool = True,
        adapt_eta: bool = False,
        adaptation_rate: float = 0.01
    ):
        super().__init__(n_experts, beta, eta_s, w_min, normalize, epsilon)

        self.adapt_beta = adapt_beta
        self.adapt_eta = adapt_eta
        self.adaptation_rate = adaptation_rate

        # Track performance for adaptation
        self.ensemble_loss_history = []

    def update_weights(
        self,
        performance_scores: np.ndarray,
        coherence_scores: np.ndarray,
        ensemble_loss: Optional[float] = None
    ) -> np.ndarray:
        """
        Update weights with optional parameter adaptation.

        Parameters
        ----------
        performance_scores : np.ndarray
            Performance scores.
        coherence_scores : np.ndarray
            Coherence scores.
        ensemble_loss : float, optional
            Current ensemble loss for adaptation.

        Returns
        -------
        np.ndarray
            Updated weights.
        """
        # Adapt parameters if ensemble loss provided
        if ensemble_loss is not None and len(self.ensemble_loss_history) > 10:
            self._adapt_parameters(ensemble_loss)

        if ensemble_loss is not None:
            self.ensemble_loss_history.append(ensemble_loss)

        # Standard weight update
        return super().update_weights(performance_scores, coherence_scores)

    def _adapt_parameters(self, current_loss: float):
        """
        Adapt beta and/or eta_s based on performance trends.

        Parameters
        ----------
        current_loss : float
            Current ensemble loss.
        """
        if len(self.ensemble_loss_history) < 10:
            return

        # Compute recent loss trend
        recent_losses = self.ensemble_loss_history[-10:]
        loss_trend = np.mean(np.diff(recent_losses))

        # Adapt beta: if loss increasing, focus more on performance
        if self.adapt_beta:
            if loss_trend > 0:  # Loss increasing
                self.beta = min(1.0, self.beta + self.adaptation_rate)
            else:  # Loss decreasing or stable
                self.beta = max(0.3, self.beta - self.adaptation_rate)

        # Adapt eta_s: adjust sensitivity based on loss variance
        if self.adapt_eta:
            loss_variance = np.var(recent_losses)
            if loss_variance > 0.01:  # High variance
                self.eta_s = max(1.0, self.eta_s - self.adaptation_rate * 10)
            else:  # Low variance
                self.eta_s = min(10.0, self.eta_s + self.adaptation_rate * 10)
