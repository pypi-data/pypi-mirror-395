"""
Coherence metrics for measuring expert agreement.

Copyright (c) 2025 Mike Amega. All rights reserved.
"""

import numpy as np
from typing import List, Optional, Callable
from scipy.spatial.distance import cosine
from scipy.stats import pearsonr


class CoherenceMetrics:
    """
    Computes coherence (agreement) between expert predictions.

    Coherence measures how well experts agree with each other, promoting
    diversity while maintaining ensemble quality.

    Parameters
    ----------
    n_experts : int
        Number of expert models.
    alpha : float
        Exponential smoothing factor for coherence (0 < alpha < 1).
    agreement_fn : callable, optional
        Custom agreement function agreement(pred_i, pred_j) -> [0, 1].
    mode : str
        Type of predictions: 'regression', 'classification', 'auto'.
    epsilon : float
        Numerical stability constant.
    """

    def __init__(
        self,
        n_experts: int,
        alpha: float = 0.85,
        agreement_fn: Optional[Callable] = None,
        mode: str = 'auto',
        epsilon: float = 1e-10
    ):
        self.n_experts = n_experts
        self.alpha = alpha
        self.epsilon = epsilon
        self.mode = mode

        # Agreement function
        if agreement_fn is not None:
            self.agreement_fn = agreement_fn
        else:
            self._infer_agreement_fn(mode)

        # Initialize coherence scores
        self.C = np.ones(n_experts) * 0.5  # Start neutral
        self.coherence_history = []
        self.initialized = False

    def _infer_agreement_fn(self, mode: str):
        """Infer agreement function based on mode."""
        if mode == 'regression' or mode == 'auto':
            self.agreement_fn = self._regression_agreement
        elif mode == 'classification':
            self.agreement_fn = self._classification_agreement
        else:
            raise ValueError(f"Unknown mode: {mode}")

    def _regression_agreement(
        self,
        pred_i: np.ndarray,
        pred_j: np.ndarray
    ) -> float:
        """
        Agreement for regression (cosine similarity).

        Parameters
        ----------
        pred_i, pred_j : np.ndarray
            Predictions from two experts.

        Returns
        -------
        float
            Agreement score in [0, 1].
        """
        # Flatten predictions
        pred_i = pred_i.flatten()
        pred_j = pred_j.flatten()

        # Avoid division by zero
        if np.linalg.norm(pred_i) < self.epsilon or \
           np.linalg.norm(pred_j) < self.epsilon:
            return 0.5

        # Cosine similarity
        similarity = 1 - cosine(pred_i, pred_j)

        # Map to [0, 1]
        return (similarity + 1) / 2

    def _classification_agreement(
        self,
        pred_i: np.ndarray,
        pred_j: np.ndarray
    ) -> float:
        """
        Agreement for classification (accuracy of agreement).

        Parameters
        ----------
        pred_i, pred_j : np.ndarray
            Predicted class labels or probabilities.

        Returns
        -------
        float
            Agreement score in [0, 1].
        """
        # If probabilities, convert to classes
        if pred_i.ndim > 1 and pred_i.shape[1] > 1:
            pred_i = np.argmax(pred_i, axis=1)
        if pred_j.ndim > 1 and pred_j.shape[1] > 1:
            pred_j = np.argmax(pred_j, axis=1)

        # Compute agreement
        agreement = np.mean(pred_i == pred_j)
        return float(agreement)

    def update(self, predictions: List[np.ndarray]) -> np.ndarray:
        """
        Update coherence scores based on expert predictions.

        Parameters
        ----------
        predictions : list of np.ndarray
            Predictions from each expert model.

        Returns
        -------
        np.ndarray
            Updated coherence scores (shape: n_experts).
        """
        if len(predictions) != self.n_experts:
            raise ValueError(
                f"Expected {self.n_experts} predictions, "
                f"got {len(predictions)}"
            )

        # Compute pairwise agreements
        current_coherence = np.zeros(self.n_experts)

        for i in range(self.n_experts):
            agreements = []
            for j in range(self.n_experts):
                if i != j:
                    agreement = self.agreement_fn(predictions[i], predictions[j])
                    agreements.append(agreement)

            # Average agreement with other experts
            if agreements:
                current_coherence[i] = np.mean(agreements)

        # Store for diagnostics
        self.coherence_history.append(current_coherence.copy())

        # Exponential smoothing
        if not self.initialized:
            self.C = current_coherence
            self.initialized = True
        else:
            self.C = self.alpha * self.C + (1 - self.alpha) * current_coherence

        return self.C.copy()

    def get_scores(self) -> np.ndarray:
        """Get current coherence scores."""
        return self.C.copy()

    def get_coherence_matrix(
        self,
        predictions: List[np.ndarray]
    ) -> np.ndarray:
        """
        Compute full coherence matrix between all expert pairs.

        Parameters
        ----------
        predictions : list of np.ndarray
            Predictions from each expert.

        Returns
        -------
        np.ndarray
            Coherence matrix (shape: n_experts x n_experts).
        """
        matrix = np.eye(self.n_experts)

        for i in range(self.n_experts):
            for j in range(i + 1, self.n_experts):
                agreement = self.agreement_fn(predictions[i], predictions[j])
                matrix[i, j] = agreement
                matrix[j, i] = agreement

        return matrix

    def get_history(self) -> np.ndarray:
        """Get coherence history (shape: T x n_experts)."""
        return np.array(self.coherence_history)

    def reset(self):
        """Reset coherence tracking."""
        self.C = np.ones(self.n_experts) * 0.5
        self.coherence_history = []
        self.initialized = False


class DiversityMetrics:
    """
    Additional diversity metrics for ensemble analysis.
    """

    @staticmethod
    def disagreement_measure(predictions: List[np.ndarray]) -> float:
        """
        Compute overall disagreement (diversity) among experts.

        Parameters
        ----------
        predictions : list of np.ndarray
            Predictions from all experts.

        Returns
        -------
        float
            Disagreement measure in [0, 1].
        """
        n_experts = len(predictions)
        if n_experts < 2:
            return 0.0

        # Compute pairwise distances
        distances = []
        for i in range(n_experts):
            for j in range(i + 1, n_experts):
                pred_i = predictions[i].flatten()
                pred_j = predictions[j].flatten()
                dist = np.linalg.norm(pred_i - pred_j)
                distances.append(dist)

        # Average distance normalized
        avg_distance = np.mean(distances)
        return min(avg_distance, 1.0)

    @staticmethod
    def entropy_measure(weights: np.ndarray) -> float:
        """
        Compute entropy of weight distribution (diversity indicator).

        Parameters
        ----------
        weights : np.ndarray
            Expert weights.

        Returns
        -------
        float
            Normalized entropy in [0, 1].
        """
        # Avoid log(0)
        weights = weights + 1e-10
        weights = weights / weights.sum()

        # Shannon entropy
        entropy = -np.sum(weights * np.log(weights))

        # Normalize by maximum entropy
        max_entropy = np.log(len(weights))
        if max_entropy > 0:
            return entropy / max_entropy
        return 0.0
