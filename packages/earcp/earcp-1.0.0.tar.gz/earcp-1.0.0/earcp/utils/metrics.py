"""
Metrics and evaluation utilities for EARCP.

Copyright (c) 2025 Mike Amega. All rights reserved.
"""

import numpy as np
from typing import List, Dict, Any


def compute_regret(
    expert_cumulative_losses: np.ndarray,
    ensemble_cumulative_loss: float
) -> Dict[str, float]:
    """
    Compute regret metrics.

    Regret is the difference between ensemble performance and the best
    single expert in hindsight.

    Parameters
    ----------
    expert_cumulative_losses : np.ndarray
        Cumulative loss for each expert (shape: n_experts).
    ensemble_cumulative_loss : float
        Cumulative loss of the ensemble.

    Returns
    -------
    dict
        Dictionary with regret metrics:
        - 'regret': Absolute regret
        - 'relative_regret': Regret relative to best expert
        - 'best_expert_idx': Index of best expert
        - 'best_expert_loss': Loss of best expert
    """
    best_expert_idx = np.argmin(expert_cumulative_losses)
    best_expert_loss = expert_cumulative_losses[best_expert_idx]

    regret = ensemble_cumulative_loss - best_expert_loss
    relative_regret = regret / (best_expert_loss + 1e-10)

    return {
        'regret': float(regret),
        'relative_regret': float(relative_regret),
        'best_expert_idx': int(best_expert_idx),
        'best_expert_loss': float(best_expert_loss),
    }


def compute_diversity(weights_history: np.ndarray) -> Dict[str, float]:
    """
    Compute diversity metrics from weight history.

    Parameters
    ----------
    weights_history : np.ndarray
        Weight history (shape: T x n_experts).

    Returns
    -------
    dict
        Diversity metrics:
        - 'mean_entropy': Average entropy of weights
        - 'final_entropy': Entropy of final weights
        - 'weight_concentration': Gini coefficient of final weights
    """
    T, n_experts = weights_history.shape

    # Compute entropy at each time step
    entropies = []
    for t in range(T):
        weights = weights_history[t, :]
        weights = weights + 1e-10  # Avoid log(0)
        entropy = -np.sum(weights * np.log(weights))
        entropies.append(entropy)

    mean_entropy = np.mean(entropies)
    final_entropy = entropies[-1]

    # Normalize entropy
    max_entropy = np.log(n_experts)
    mean_entropy_normalized = mean_entropy / max_entropy
    final_entropy_normalized = final_entropy / max_entropy

    # Gini coefficient (concentration measure)
    final_weights = weights_history[-1, :]
    sorted_weights = np.sort(final_weights)
    n = len(sorted_weights)
    cumsum = np.cumsum(sorted_weights)
    gini = (2 * np.sum((np.arange(1, n + 1)) * sorted_weights)) / (n * cumsum[-1]) - (n + 1) / n

    return {
        'mean_entropy': float(mean_entropy_normalized),
        'final_entropy': float(final_entropy_normalized),
        'weight_concentration': float(gini),
    }


def evaluate_ensemble(
    predictions: np.ndarray,
    targets: np.ndarray,
    task_type: str = 'regression'
) -> Dict[str, float]:
    """
    Evaluate ensemble predictions.

    Parameters
    ----------
    predictions : np.ndarray
        Ensemble predictions.
    targets : np.ndarray
        True targets.
    task_type : str
        'regression' or 'classification'.

    Returns
    -------
    dict
        Evaluation metrics.
    """
    if task_type == 'regression':
        # Regression metrics
        mse = np.mean((predictions - targets) ** 2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(predictions - targets))

        # R-squared
        ss_res = np.sum((targets - predictions) ** 2)
        ss_tot = np.sum((targets - np.mean(targets)) ** 2)
        r2 = 1 - (ss_res / (ss_tot + 1e-10))

        return {
            'mse': float(mse),
            'rmse': float(rmse),
            'mae': float(mae),
            'r2': float(r2),
        }

    elif task_type == 'classification':
        # Classification metrics
        # Assume predictions are class labels or probabilities
        if predictions.ndim > 1 and predictions.shape[1] > 1:
            # Probabilities -> classes
            pred_classes = np.argmax(predictions, axis=1)
        else:
            pred_classes = predictions.flatten()

        if targets.ndim > 1 and targets.shape[1] > 1:
            true_classes = np.argmax(targets, axis=1)
        else:
            true_classes = targets.flatten()

        accuracy = np.mean(pred_classes == true_classes)

        # Per-class metrics
        unique_classes = np.unique(true_classes)
        precision_per_class = []
        recall_per_class = []

        for cls in unique_classes:
            tp = np.sum((pred_classes == cls) & (true_classes == cls))
            fp = np.sum((pred_classes == cls) & (true_classes != cls))
            fn = np.sum((pred_classes != cls) & (true_classes == cls))

            precision = tp / (tp + fp + 1e-10)
            recall = tp / (tp + fn + 1e-10)

            precision_per_class.append(precision)
            recall_per_class.append(recall)

        macro_precision = np.mean(precision_per_class)
        macro_recall = np.mean(recall_per_class)
        macro_f1 = 2 * macro_precision * macro_recall / (macro_precision + macro_recall + 1e-10)

        return {
            'accuracy': float(accuracy),
            'macro_precision': float(macro_precision),
            'macro_recall': float(macro_recall),
            'macro_f1': float(macro_f1),
        }

    else:
        raise ValueError(f"Unknown task_type: {task_type}")


def theoretical_regret_bound(T: int, M: int, beta: float = 1.0) -> float:
    """
    Compute theoretical regret bound for EARCP.

    For beta=1 (pure performance):
        Regret_T ≤ √(2T log M)

    For beta<1 (with coherence):
        Regret_T ≤ (1/beta) √(2T log M)

    Parameters
    ----------
    T : int
        Number of time steps.
    M : int
        Number of experts.
    beta : float
        Performance-coherence balance parameter.

    Returns
    -------
    float
        Theoretical regret upper bound.
    """
    if beta <= 0 or beta > 1:
        raise ValueError(f"beta must be in (0, 1], got {beta}")

    bound = (1.0 / beta) * np.sqrt(2 * T * np.log(M))
    return bound
