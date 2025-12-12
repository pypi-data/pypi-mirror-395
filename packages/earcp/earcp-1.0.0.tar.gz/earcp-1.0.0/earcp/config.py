"""
Configuration module for EARCP.

Copyright (c) 2025 Mike Amega. All rights reserved.
"""

from dataclasses import dataclass, field
from typing import Optional, Callable, Dict, Any
import numpy as np


@dataclass
class EARCPConfig:
    """
    Configuration for EARCP ensemble.

    Parameters
    ----------
    alpha_P : float, default=0.9
        Exponential smoothing factor for performance tracking (0 < alpha_P < 1).
        Higher values give more weight to historical performance.

    alpha_C : float, default=0.85
        Exponential smoothing factor for coherence tracking (0 < alpha_C < 1).
        Higher values give more weight to historical coherence.

    beta : float, default=0.7
        Balance between performance and coherence (0 <= beta <= 1).
        beta = 1: Pure performance-based weighting
        beta = 0: Pure coherence-based weighting
        beta in (0,1): Hybrid approach (recommended)

    eta_s : float, default=5.0
        Learning rate / sensitivity parameter for weight updates.
        Higher values make weights more sensitive to score differences.

    w_min : float, default=0.05
        Minimum weight floor to prevent expert starvation.
        Must satisfy: w_min <= 1/M where M is number of experts.

    loss_fn : callable, optional
        Custom loss function L(y_pred, y_true) -> [0, 1].
        If None, uses squared error for regression or 0-1 loss for classification.

    coherence_fn : callable, optional
        Custom coherence function agreement(pred_i, pred_j) -> [0, 1].
        If None, uses default based on prediction type.

    prediction_mode : str, default='auto'
        Type of predictions: 'regression', 'classification', 'auto'.
        'auto' infers from prediction shape.

    epsilon : float, default=1e-10
        Numerical stability constant.

    normalize_weights : bool, default=True
        Whether to normalize weights to sum to 1.

    track_diagnostics : bool, default=True
        Whether to track detailed diagnostics (weights history, scores, etc.).

    random_state : int, optional
        Random seed for reproducibility.
    """

    # Core parameters
    alpha_P: float = 0.9
    alpha_C: float = 0.85
    beta: float = 0.7
    eta_s: float = 5.0
    w_min: float = 0.05

    # Custom functions
    loss_fn: Optional[Callable[[np.ndarray, np.ndarray], float]] = None
    coherence_fn: Optional[Callable[[np.ndarray, np.ndarray], float]] = None

    # Modes
    prediction_mode: str = 'auto'

    # Numerical stability
    epsilon: float = 1e-10

    # Behavior flags
    normalize_weights: bool = True
    track_diagnostics: bool = True

    # Reproducibility
    random_state: Optional[int] = None

    def __post_init__(self):
        """Validate configuration parameters."""
        self._validate()

    def _validate(self):
        """Validate configuration values."""
        # Validate smoothing factors
        if not 0 < self.alpha_P < 1:
            raise ValueError(f"alpha_P must be in (0, 1), got {self.alpha_P}")
        if not 0 < self.alpha_C < 1:
            raise ValueError(f"alpha_C must be in (0, 1), got {self.alpha_C}")

        # Validate beta
        if not 0 <= self.beta <= 1:
            raise ValueError(f"beta must be in [0, 1], got {self.beta}")

        # Validate eta_s
        if self.eta_s <= 0:
            raise ValueError(f"eta_s must be positive, got {self.eta_s}")

        # Validate w_min
        if not 0 <= self.w_min < 1:
            raise ValueError(f"w_min must be in [0, 1), got {self.w_min}")

        # Validate epsilon
        if self.epsilon <= 0:
            raise ValueError(f"epsilon must be positive, got {self.epsilon}")

        # Validate prediction mode
        valid_modes = ['auto', 'regression', 'classification']
        if self.prediction_mode not in valid_modes:
            raise ValueError(
                f"prediction_mode must be one of {valid_modes}, "
                f"got {self.prediction_mode}"
            )

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'alpha_P': self.alpha_P,
            'alpha_C': self.alpha_C,
            'beta': self.beta,
            'eta_s': self.eta_s,
            'w_min': self.w_min,
            'prediction_mode': self.prediction_mode,
            'epsilon': self.epsilon,
            'normalize_weights': self.normalize_weights,
            'track_diagnostics': self.track_diagnostics,
            'random_state': self.random_state,
        }

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'EARCPConfig':
        """Create configuration from dictionary."""
        return cls(**config_dict)

    def copy(self) -> 'EARCPConfig':
        """Create a copy of this configuration."""
        return EARCPConfig(**self.to_dict())


# Preset configurations for common use cases
PRESET_CONFIGS = {
    'default': EARCPConfig(),

    'performance_focused': EARCPConfig(
        beta=0.95,
        eta_s=10.0,
        alpha_P=0.95,
    ),

    'diversity_focused': EARCPConfig(
        beta=0.5,
        eta_s=3.0,
        alpha_C=0.9,
    ),

    'balanced': EARCPConfig(
        beta=0.7,
        eta_s=5.0,
        alpha_P=0.9,
        alpha_C=0.85,
    ),

    'conservative': EARCPConfig(
        alpha_P=0.95,
        alpha_C=0.9,
        eta_s=3.0,
        w_min=0.1,
    ),

    'aggressive': EARCPConfig(
        alpha_P=0.8,
        alpha_C=0.75,
        eta_s=8.0,
        w_min=0.01,
    ),
}


def get_preset_config(preset_name: str) -> EARCPConfig:
    """
    Get a preset configuration.

    Parameters
    ----------
    preset_name : str
        Name of the preset: 'default', 'performance_focused',
        'diversity_focused', 'balanced', 'conservative', 'aggressive'.

    Returns
    -------
    EARCPConfig
        The preset configuration.
    """
    if preset_name not in PRESET_CONFIGS:
        raise ValueError(
            f"Unknown preset '{preset_name}'. "
            f"Available presets: {list(PRESET_CONFIGS.keys())}"
        )
    return PRESET_CONFIGS[preset_name].copy()
