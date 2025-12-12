"""
Basic tests for EARCP library.

Copyright (c) 2025 Mike Amega. All rights reserved.
"""

import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from earcp import EARCP, EARCPConfig, get_preset_config


# Simple expert for testing
class SimpleExpert:
    def __init__(self, coefficient):
        self.coefficient = coefficient

    def predict(self, x):
        return self.coefficient * x


def test_basic_initialization():
    """Test basic EARCP initialization."""
    print("Test 1: Basic initialization...")

    experts = [SimpleExpert(1.0), SimpleExpert(2.0), SimpleExpert(0.5)]
    ensemble = EARCP(experts=experts)

    assert ensemble.n_experts == 3
    assert len(ensemble.get_weights()) == 3
    assert np.allclose(ensemble.get_weights(), [1/3, 1/3, 1/3])

    print("  ✓ Initialization successful")
    print(f"  ✓ Initial weights: {ensemble.get_weights()}")


def test_predict_update():
    """Test prediction and update cycle."""
    print("\nTest 2: Predict and update...")

    experts = [SimpleExpert(1.0), SimpleExpert(2.0), SimpleExpert(0.5)]
    ensemble = EARCP(experts=experts, beta=0.7, eta_s=5.0)

    # Single prediction
    x = np.array([1.0])
    pred, expert_preds = ensemble.predict(x)

    assert pred is not None
    assert len(expert_preds) == 3
    print(f"  ✓ Prediction: {pred}")
    print(f"  ✓ Expert predictions: {[p for p in expert_preds]}")

    # Update
    target = np.array([1.5])
    metrics = ensemble.update(expert_preds, target)

    assert 'weights' in metrics
    assert 'performance_scores' in metrics
    assert 'coherence_scores' in metrics

    print(f"  ✓ Updated weights: {metrics['weights']}")


def test_online_learning():
    """Test online learning over multiple steps."""
    print("\nTest 3: Online learning (100 steps)...")

    experts = [SimpleExpert(1.0), SimpleExpert(2.0), SimpleExpert(1.5)]
    ensemble = EARCP(experts=experts, beta=0.7)

    # Target function: y = 1.5 * x
    T = 100
    for t in range(T):
        x = np.array([t * 0.1])
        target = 1.5 * x

        pred, expert_preds = ensemble.predict(x)
        ensemble.update(expert_preds, target)

    final_weights = ensemble.get_weights()
    print(f"  ✓ Final weights: {final_weights}")

    # Expert 3 (coefficient=1.5) should have highest weight
    best_expert = np.argmax(final_weights)
    print(f"  ✓ Best expert: Expert {best_expert + 1} (coefficient={experts[best_expert].coefficient})")

    assert best_expert == 2, "Expert with coefficient 1.5 should have highest weight"


def test_config():
    """Test configuration."""
    print("\nTest 4: Configuration...")

    # Custom config
    config = EARCPConfig(
        alpha_P=0.9,
        alpha_C=0.85,
        beta=0.7,
        eta_s=5.0,
        w_min=0.05
    )

    experts = [SimpleExpert(1.0), SimpleExpert(2.0)]
    ensemble = EARCP(experts=experts, config=config)

    assert ensemble.config.beta == 0.7
    assert ensemble.config.eta_s == 5.0
    print("  ✓ Custom configuration applied")

    # Preset config
    config_preset = get_preset_config('balanced')
    ensemble2 = EARCP(experts=experts, config=config_preset)

    print(f"  ✓ Preset config 'balanced': beta={config_preset.beta}")


def test_diagnostics():
    """Test diagnostics tracking."""
    print("\nTest 5: Diagnostics...")

    experts = [SimpleExpert(1.0), SimpleExpert(2.0)]
    ensemble = EARCP(experts=experts, track_diagnostics=True)

    # Run some steps
    for t in range(10):
        x = np.array([t * 0.1])
        target = np.array([t * 0.15])

        pred, expert_preds = ensemble.predict(x)
        ensemble.update(expert_preds, target)

    diagnostics = ensemble.get_diagnostics()

    assert 'weights' in diagnostics
    assert 'weights_history' in diagnostics
    assert 'performance_history' in diagnostics
    assert 'coherence_history' in diagnostics
    assert len(diagnostics['weights_history']) == 10

    print("  ✓ Diagnostics tracking working")
    print(f"  ✓ History length: {len(diagnostics['weights_history'])}")


def test_reset():
    """Test ensemble reset."""
    print("\nTest 6: Reset...")

    experts = [SimpleExpert(1.0), SimpleExpert(2.0)]
    ensemble = EARCP(experts=experts)

    # Run some steps
    for t in range(10):
        x = np.array([t * 0.1])
        target = np.array([t * 0.15])
        pred, expert_preds = ensemble.predict(x)
        ensemble.update(expert_preds, target)

    weights_before = ensemble.get_weights().copy()

    # Reset
    ensemble.reset()

    weights_after = ensemble.get_weights()
    assert np.allclose(weights_after, [0.5, 0.5])
    assert ensemble.t == 0

    print("  ✓ Reset successful")
    print(f"  ✓ Weights before reset: {weights_before}")
    print(f"  ✓ Weights after reset: {weights_after}")


def test_metrics():
    """Test utility metrics."""
    print("\nTest 7: Utility metrics...")

    from earcp.utils.metrics import compute_regret, compute_diversity

    # Create diagnostic data
    expert_losses = np.array([10.0, 8.0, 12.0])
    ensemble_loss = 9.0

    regret = compute_regret(expert_losses, ensemble_loss)

    assert 'regret' in regret
    assert 'best_expert_idx' in regret
    assert regret['best_expert_idx'] == 1  # Expert with loss=8.0

    print(f"  ✓ Regret: {regret['regret']:.4f}")
    print(f"  ✓ Best expert: {regret['best_expert_idx']}")

    # Diversity
    weights_history = np.random.rand(50, 3)
    weights_history = weights_history / weights_history.sum(axis=1, keepdims=True)

    diversity = compute_diversity(weights_history)

    assert 'mean_entropy' in diversity
    assert 'final_entropy' in diversity
    assert 0 <= diversity['mean_entropy'] <= 1

    print(f"  ✓ Mean entropy: {diversity['mean_entropy']:.4f}")


def run_all_tests():
    """Run all tests."""
    print("="*60)
    print("EARCP Library Tests")
    print("="*60)

    try:
        test_basic_initialization()
        test_predict_update()
        test_online_learning()
        test_config()
        test_diagnostics()
        test_reset()
        test_metrics()

        print("\n" + "="*60)
        print("✓ ALL TESTS PASSED!")
        print("="*60)
        return True

    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
