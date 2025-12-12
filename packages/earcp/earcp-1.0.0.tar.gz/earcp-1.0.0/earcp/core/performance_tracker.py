"""
Performance tracking for expert models.

Copyright (c) 2025 Mike Amega. All rights reserved.
"""

import numpy as np
from typing import List, Dict, Optional, Callable


class PerformanceTracker:
    """
    Tracks and smooths performance metrics for expert models.

    Maintains exponentially weighted moving averages of individual expert losses
    and computes performance scores.

    Parameters
    ----------
    n_experts : int
        Number of expert models.
    alpha : float
        Exponential smoothing factor (0 < alpha < 1).
    loss_fn : callable, optional
        Loss function L(y_pred, y_true) -> [0, 1].
    epsilon : float
        Numerical stability constant.
    """

    def __init__(
        self,
        n_experts: int,
        alpha: float = 0.9,
        loss_fn: Optional[Callable] = None,
        epsilon: float = 1e-10
    ):
        self.n_experts = n_experts
        self.alpha = alpha
        self.loss_fn = loss_fn or self._default_loss
        self.epsilon = epsilon

        # Initialize performance scores
        self.P = np.zeros(n_experts)
        self.losses = []
        self.initialized = False

    def _default_loss(self, y_pred: np.ndarray, y_true: np.ndarray) -> float:
        """
        Default loss function (squared error normalized to [0,1]).

        Parameters
        ----------
        y_pred : np.ndarray
            Predicted values.
        y_true : np.ndarray
            True values.

        Returns
        -------
        float
            Loss value in [0, 1].
        """
        # Squared error
        se = np.mean((y_pred - y_true) ** 2)
        # Normalize to [0, 1] using bounded sigmoid
        return np.tanh(se)

    def update(
        self,
        predictions: List[np.ndarray],
        target: np.ndarray
    ) -> np.ndarray:
        """
        Update performance scores based on new predictions.

        Parameters
        ----------
        predictions : list of np.ndarray
            Predictions from each expert model.
        target : np.ndarray
            True target values.

        Returns
        -------
        np.ndarray
            Updated performance scores (shape: n_experts).
        """
        if len(predictions) != self.n_experts:
            raise ValueError(
                f"Expected {self.n_experts} predictions, "
                f"got {len(predictions)}"
            )

        # Compute losses for each expert
        current_losses = np.array([
            self.loss_fn(pred, target) for pred in predictions
        ])

        # Store for diagnostics
        self.losses.append(current_losses.copy())

        # Initialize P if first update
        if not self.initialized:
            self.P = -current_losses
            self.initialized = True
        else:
            # Exponential smoothing: P_t = alpha * P_{t-1} + (1 - alpha) * (-loss_t)
            self.P = self.alpha * self.P + (1 - self.alpha) * (-current_losses)

        return self.P.copy()

    def get_scores(self) -> np.ndarray:
        """Get current performance scores."""
        return self.P.copy()

    def get_loss_history(self) -> np.ndarray:
        """Get history of losses (shape: T x n_experts)."""
        return np.array(self.losses)

    def get_cumulative_loss(self) -> np.ndarray:
        """Get cumulative loss for each expert."""
        if not self.losses:
            return np.zeros(self.n_experts)
        return np.sum(self.get_loss_history(), axis=0)

    def reset(self):
        """Reset performance tracking."""
        self.P = np.zeros(self.n_experts)
        self.losses = []
        self.initialized = False


class MultiObjectivePerformanceTracker(PerformanceTracker):
    """
    Extended performance tracker supporting multiple objectives.

    Useful for multi-task learning or multi-objective optimization.
    """

    def __init__(
        self,
        n_experts: int,
        n_objectives: int,
        alpha: float = 0.9,
        loss_fns: Optional[List[Callable]] = None,
        objective_weights: Optional[np.ndarray] = None,
        epsilon: float = 1e-10
    ):
        super().__init__(n_experts, alpha, None, epsilon)
        self.n_objectives = n_objectives

        # Loss functions for each objective
        self.loss_fns = loss_fns or [self._default_loss] * n_objectives

        # Weights for combining objectives
        if objective_weights is None:
            self.objective_weights = np.ones(n_objectives) / n_objectives
        else:
            self.objective_weights = np.array(objective_weights)
            self.objective_weights /= self.objective_weights.sum()

        # Per-objective performance scores
        self.P_objectives = np.zeros((n_experts, n_objectives))

    def update(
        self,
        predictions: List[np.ndarray],
        targets: List[np.ndarray]
    ) -> np.ndarray:
        """
        Update with multiple objectives.

        Parameters
        ----------
        predictions : list of np.ndarray
            Predictions from each expert.
        targets : list of np.ndarray
            True targets for each objective.

        Returns
        -------
        np.ndarray
            Combined performance scores.
        """
        if len(targets) != self.n_objectives:
            raise ValueError(
                f"Expected {self.n_objectives} targets, got {len(targets)}"
            )

        # Update each objective
        for obj_idx in range(self.n_objectives):
            losses = np.array([
                self.loss_fns[obj_idx](pred, targets[obj_idx])
                for pred in predictions
            ])

            if not self.initialized:
                self.P_objectives[:, obj_idx] = -losses
            else:
                self.P_objectives[:, obj_idx] = (
                    self.alpha * self.P_objectives[:, obj_idx] +
                    (1 - self.alpha) * (-losses)
                )

        self.initialized = True

        # Combine objectives
        self.P = self.P_objectives @ self.objective_weights

        return self.P.copy()
