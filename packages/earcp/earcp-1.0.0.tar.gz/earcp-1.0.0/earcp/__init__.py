"""
EARCP: Ensemble Auto-Régulé par Cohérence et Performance
A Self-Regulating Coherence-Aware Ensemble Architecture

Author: Mike Amega
Copyright (c) 2025 Mike Amega. All rights reserved.
Prior Art Date: November 13, 2025
"""

__version__ = "1.0.0"
__author__ = "Mike Amega"
__email__ = "info@amewebstudio.com"

from .models.earcp_model import EARCP
from .core.ensemble_weighting import EnsembleWeighting
from .core.coherence_metrics import CoherenceMetrics
from .core.performance_tracker import PerformanceTracker
from .config import EARCPConfig, get_preset_config

__all__ = [
    'EARCP',
    'EARCPConfig',
    'get_preset_config',
    'EnsembleWeighting',
    'CoherenceMetrics',
    'PerformanceTracker',
]
