"""
Wrappers for integrating external models with EARCP.

Copyright (c) 2025 Mike Amega. All rights reserved.
"""

import numpy as np
from typing import Any


class SklearnWrapper:
    """
    Wrapper for scikit-learn models to make them compatible with EARCP.

    Parameters
    ----------
    model : sklearn estimator
        Scikit-learn model with fit() and predict() methods.
    """

    def __init__(self, model: Any):
        self.model = model

    def predict(self, x: np.ndarray) -> np.ndarray:
        """
        Make prediction.

        Parameters
        ----------
        x : np.ndarray
            Input features.

        Returns
        -------
        np.ndarray
            Predictions.
        """
        pred = self.model.predict(x)
        if not isinstance(pred, np.ndarray):
            pred = np.array(pred)
        return pred

    def fit(self, X: np.ndarray, y: np.ndarray):
        """Fit the underlying model."""
        return self.model.fit(X, y)

    def __getattr__(self, name: str):
        """Delegate attribute access to underlying model."""
        return getattr(self.model, name)


class TorchWrapper:
    """
    Wrapper for PyTorch models to make them compatible with EARCP.

    Parameters
    ----------
    model : torch.nn.Module
        PyTorch model.
    device : str
        Device to run model on ('cpu' or 'cuda').
    """

    def __init__(self, model: Any, device: str = 'cpu'):
        try:
            import torch
        except ImportError:
            raise ImportError(
                "PyTorch is required for TorchWrapper. "
                "Install with: pip install torch"
            )

        self.model = model
        self.device = device
        self.model.to(device)
        self.model.eval()
        self.torch = torch

    def predict(self, x: np.ndarray) -> np.ndarray:
        """
        Make prediction.

        Parameters
        ----------
        x : np.ndarray
            Input features.

        Returns
        -------
        np.ndarray
            Predictions.
        """
        # Convert to tensor
        if not isinstance(x, self.torch.Tensor):
            x = self.torch.from_numpy(x).float()

        x = x.to(self.device)

        # Forward pass
        with self.torch.no_grad():
            output = self.model(x)

        # Convert back to numpy
        if isinstance(output, self.torch.Tensor):
            output = output.cpu().numpy()

        return output

    def __getattr__(self, name: str):
        """Delegate attribute access to underlying model."""
        return getattr(self.model, name)


class KerasWrapper:
    """
    Wrapper for Keras/TensorFlow models to make them compatible with EARCP.

    Parameters
    ----------
    model : keras.Model
        Keras model.
    """

    def __init__(self, model: Any):
        self.model = model

    def predict(self, x: np.ndarray) -> np.ndarray:
        """
        Make prediction.

        Parameters
        ----------
        x : np.ndarray
            Input features.

        Returns
        -------
        np.ndarray
            Predictions.
        """
        pred = self.model.predict(x, verbose=0)
        if not isinstance(pred, np.ndarray):
            pred = np.array(pred)
        return pred

    def __getattr__(self, name: str):
        """Delegate attribute access to underlying model."""
        return getattr(self.model, name)


class CallableWrapper:
    """
    Wrapper for simple callable functions.

    Parameters
    ----------
    predict_fn : callable
        Function that takes input and returns predictions.
    """

    def __init__(self, predict_fn: callable):
        self.predict_fn = predict_fn

    def predict(self, x: np.ndarray) -> np.ndarray:
        """
        Make prediction.

        Parameters
        ----------
        x : np.ndarray
            Input features.

        Returns
        -------
        np.ndarray
            Predictions.
        """
        pred = self.predict_fn(x)
        if not isinstance(pred, np.ndarray):
            pred = np.array(pred)
        return pred
