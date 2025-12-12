"""
Example demonstrating EARCP visualization utilities.

This example shows how to visualize ensemble behavior and diagnostics.

Copyright (c) 2025 Mike Amega. All rights reserved.
"""

import numpy as np
import matplotlib.pyplot as plt
from earcp import EARCP, get_preset_config
from earcp.utils.visualization import (
    plot_weights,
    plot_performance,
    plot_diagnostics,
    plot_regret
)


# Define simple expert models
class ExponentialExpert:
    def __init__(self, rate):
        self.rate = rate

    def predict(self, x):
        return np.exp(-self.rate * x)


class PowerLawExpert:
    def __init__(self, exponent):
        self.exponent = exponent

    def predict(self, x):
        return x ** self.exponent


class PeriodicExpert:
    def __init__(self, period):
        self.period = period

    def predict(self, x):
        return np.cos(2 * np.pi * x / self.period)


class RandomWalkExpert:
    def __init__(self):
        self.value = 0.5

    def predict(self, x):
        self.value += np.random.normal(0, 0.1)
        self.value = np.clip(self.value, 0, 1)
        return self.value


def main():
    print("="*60)
    print("EARCP Visualization Example")
    print("="*60)

    # Create experts
    experts = [
        ExponentialExpert(rate=0.1),
        PowerLawExpert(exponent=0.5),
        PeriodicExpert(period=20),
        RandomWalkExpert(),
    ]

    expert_names = [
        'Exponential Decay',
        'Power Law',
        'Periodic',
        'Random Walk'
    ]

    print(f"\nExperts: {expert_names}")

    # Use preset configuration
    config = get_preset_config('balanced')

    # Initialize ensemble
    ensemble = EARCP(
        experts=experts,
        config=config,
        track_diagnostics=True
    )

    print(f"\nUsing preset config: 'balanced'")
    print(f"  beta={config.beta}, eta_s={config.eta_s}")

    # Simulate online learning
    T = 200
    np.random.seed(42)

    print(f"\nRunning online learning for {T} steps...")

    # True target: mixture of behaviors
    def true_function(t):
        x = t * 0.1
        return (
            0.3 * np.exp(-0.1 * x) +
            0.3 * (x ** 0.5) +
            0.4 * np.cos(2 * np.pi * x / 20) +
            np.random.normal(0, 0.05)
        )

    for t in range(T):
        x = np.array([t * 0.1])
        target = np.array([true_function(t)])

        # Predict and update
        ensemble_pred, expert_preds = ensemble.predict(x)
        ensemble.update(expert_preds, target)

    print("Learning completed!")

    # Get diagnostics
    diagnostics = ensemble.get_diagnostics()

    # Visualization
    print("\nGenerating visualizations...")

    # 1. Plot weights evolution
    print("  - Weights evolution")
    plot_weights(
        diagnostics['weights_history'],
        expert_names=expert_names,
        save_path='weights_evolution.png'
    )

    # 2. Plot performance and coherence
    print("  - Performance and coherence scores")
    plot_performance(
        diagnostics['performance_history'],
        diagnostics['coherence_history'],
        expert_names=expert_names,
        save_path='performance_coherence.png'
    )

    # 3. Plot comprehensive diagnostics
    print("  - Comprehensive diagnostics")
    plot_diagnostics(
        diagnostics,
        expert_names=expert_names,
        save_path='diagnostics.png'
    )

    # 4. Plot regret analysis
    print("  - Regret analysis")
    ensemble_cum_loss = np.sum(ensemble.performance_tracker.get_loss_history())
    plot_regret(
        diagnostics['cumulative_loss'],
        ensemble_cum_loss,
        expert_names=expert_names,
        save_path='regret_analysis.png'
    )

    print("\nVisualizations saved:")
    print("  - weights_evolution.png")
    print("  - performance_coherence.png")
    print("  - diagnostics.png")
    print("  - regret_analysis.png")

    # Print summary
    print("\n" + "="*60)
    print("Summary")
    print("="*60)

    print("\nFinal weights:")
    for name, weight in zip(expert_names, diagnostics['weights']):
        print(f"  {name:20s}: {weight:.4f}")

    print("\nCumulative losses:")
    for name, loss in zip(expert_names, diagnostics['cumulative_loss']):
        print(f"  {name:20s}: {loss:.4f}")

    best_idx = np.argmin(diagnostics['cumulative_loss'])
    print(f"\nBest expert: {expert_names[best_idx]}")

    from earcp.utils.metrics import compute_regret

    regret_metrics = compute_regret(
        diagnostics['cumulative_loss'],
        ensemble_cum_loss
    )
    print(f"\nRegret: {regret_metrics['regret']:.4f}")
    print(f"Relative regret: {regret_metrics['relative_regret']:.2%}")

    print("\n" + "="*60)
    print("Example completed successfully!")
    print("="*60)


if __name__ == "__main__":
    main()
