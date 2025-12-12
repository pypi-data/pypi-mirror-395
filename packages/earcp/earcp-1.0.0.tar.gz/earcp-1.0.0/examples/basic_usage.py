"""
Basic usage example for EARCP.

This example demonstrates how to use EARCP with simple synthetic experts
for a regression task.

Copyright (c) 2025 Mike Amega. All rights reserved.
"""

import numpy as np
from earcp import EARCP


# Define simple expert models
class LinearExpert:
    """Simple linear regression expert."""

    def __init__(self, slope, intercept):
        self.slope = slope
        self.intercept = intercept

    def predict(self, x):
        return self.slope * x + self.intercept


class PolynomialExpert:
    """Simple polynomial regression expert."""

    def __init__(self, coefficients):
        self.coefficients = coefficients

    def predict(self, x):
        result = 0
        for i, coef in enumerate(self.coefficients):
            result += coef * (x ** i)
        return result


class SinusoidalExpert:
    """Simple sinusoidal expert."""

    def __init__(self, amplitude, frequency, phase):
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase

    def predict(self, x):
        return self.amplitude * np.sin(self.frequency * x + self.phase)


def main():
    print("="*60)
    print("EARCP Basic Usage Example")
    print("="*60)

    # Create expert models
    experts = [
        LinearExpert(slope=2.0, intercept=1.0),
        PolynomialExpert(coefficients=[0, 1, 0.5]),
        SinusoidalExpert(amplitude=1.0, frequency=0.5, phase=0),
    ]

    print(f"\nNumber of experts: {len(experts)}")
    print("Expert types:", [type(e).__name__ for e in experts])

    # Initialize EARCP ensemble
    ensemble = EARCP(
        experts=experts,
        alpha_P=0.9,    # Performance smoothing
        alpha_C=0.85,   # Coherence smoothing
        beta=0.7,       # Performance-coherence balance
        eta_s=5.0,      # Sensitivity
        w_min=0.05      # Weight floor
    )

    print(f"\nInitial configuration:")
    print(f"  beta (performance/coherence balance): {ensemble.config.beta}")
    print(f"  eta_s (sensitivity): {ensemble.config.eta_s}")
    print(f"  w_min (weight floor): {ensemble.config.w_min}")
    print(f"\nInitial weights: {ensemble.get_weights()}")

    # Simulate online learning
    T = 100  # Number of time steps
    np.random.seed(42)

    print(f"\n{'='*60}")
    print(f"Running online learning for {T} time steps...")
    print(f"{'='*60}\n")

    for t in range(T):
        # Generate input (simulating sequential data)
        x = np.array([t * 0.1])

        # True target function (combination of linear and sinusoidal)
        true_target = 2.0 * x + np.sin(0.5 * x) + np.random.normal(0, 0.1)

        # Get ensemble prediction
        ensemble_pred, expert_preds = ensemble.predict(x)

        # Update ensemble
        metrics = ensemble.update(expert_preds, true_target)

        # Print progress every 20 steps
        if (t + 1) % 20 == 0:
            print(f"Step {t+1:3d}:")
            print(f"  Weights: {metrics['weights']}")
            print(f"  Performance scores: {metrics['performance_scores']}")
            print(f"  Coherence scores: {metrics['coherence_scores']}")
            print()

    # Final diagnostics
    print(f"{'='*60}")
    print("Final Results")
    print(f"{'='*60}\n")

    diagnostics = ensemble.get_diagnostics()
    print(f"Final weights: {diagnostics['weights']}")
    print(f"Final performance scores: {diagnostics['performance_scores']}")
    print(f"Final coherence scores: {diagnostics['coherence_scores']}")
    print(f"Cumulative losses: {diagnostics['cumulative_loss']}")

    # Best expert
    best_idx = np.argmin(diagnostics['cumulative_loss'])
    print(f"\nBest single expert: Expert {best_idx + 1} "
          f"({type(experts[best_idx]).__name__})")

    # Regret analysis
    from earcp.utils.metrics import compute_regret, theoretical_regret_bound

    ensemble_cum_loss = np.sum(ensemble.performance_tracker.get_loss_history())
    regret_metrics = compute_regret(
        diagnostics['cumulative_loss'],
        ensemble_cum_loss
    )

    print(f"\nRegret analysis:")
    print(f"  Regret: {regret_metrics['regret']:.4f}")
    print(f"  Relative regret: {regret_metrics['relative_regret']:.2%}")

    # Theoretical bound
    bound = theoretical_regret_bound(T, len(experts), beta=ensemble.config.beta)
    print(f"  Theoretical bound: {bound:.4f}")
    print(f"  Actual regret within bound: {regret_metrics['regret'] <= bound}")

    # Diversity analysis
    from earcp.utils.metrics import compute_diversity

    diversity = compute_diversity(diagnostics['weights_history'])
    print(f"\nDiversity metrics:")
    print(f"  Mean entropy: {diversity['mean_entropy']:.4f}")
    print(f"  Final entropy: {diversity['final_entropy']:.4f}")
    print(f"  Weight concentration (Gini): {diversity['weight_concentration']:.4f}")

    print(f"\n{'='*60}")
    print("Example completed successfully!")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
