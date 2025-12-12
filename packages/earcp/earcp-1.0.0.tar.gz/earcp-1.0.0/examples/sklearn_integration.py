"""
Example of EARCP with scikit-learn models.

This example shows how to use EARCP with standard sklearn models
for a classification task.

Copyright (c) 2025 Mike Amega. All rights reserved.
"""

import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

from earcp import EARCP
from earcp.utils.wrappers import SklearnWrapper
from earcp.utils.metrics import evaluate_ensemble


def main():
    print("="*60)
    print("EARCP with scikit-learn Integration")
    print("="*60)

    # Generate synthetic classification dataset
    print("\nGenerating synthetic dataset...")
    X, y = make_classification(
        n_samples=1000,
        n_features=20,
        n_informative=15,
        n_redundant=5,
        n_classes=3,
        random_state=42
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    print(f"Features: {X.shape[1]}")
    print(f"Classes: {len(np.unique(y))}")

    # Create and train sklearn models
    print("\nTraining expert models...")

    sklearn_models = {
        'Logistic Regression': LogisticRegression(random_state=42),
        'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=5),
        'Random Forest': RandomForestClassifier(n_estimators=50, random_state=42),
        'SVM': SVC(probability=True, random_state=42),
        'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5),
    }

    # Train each model
    for name, model in sklearn_models.items():
        model.fit(X_train, y_train)
        train_acc = model.score(X_train, y_train)
        test_acc = model.score(X_test, y_test)
        print(f"  {name:25s} - Train: {train_acc:.4f}, Test: {test_acc:.4f}")

    # Wrap models for EARCP
    experts = [SklearnWrapper(model) for model in sklearn_models.values()]
    expert_names = list(sklearn_models.keys())

    # Create EARCP ensemble
    print("\nInitializing EARCP ensemble...")
    ensemble = EARCP(
        experts=experts,
        alpha_P=0.9,
        alpha_C=0.85,
        beta=0.7,
        eta_s=5.0,
        w_min=0.05,
        prediction_mode='classification'
    )

    print(f"Initial weights: {ensemble.get_weights()}")

    # Online learning on training set
    print("\n" + "="*60)
    print("Online learning phase...")
    print("="*60 + "\n")

    # Shuffle training data for online learning
    indices = np.random.permutation(len(X_train))

    for i, idx in enumerate(indices):
        x_sample = X_train[idx:idx+1]
        y_sample = y_train[idx]

        # Get predictions
        ensemble_pred, expert_preds = ensemble.predict(x_sample)

        # Convert predictions to class probabilities if needed
        processed_preds = []
        for pred in expert_preds:
            if pred.ndim == 1 or pred.shape[1] == 1:
                # Convert to one-hot
                n_classes = len(np.unique(y_train))
                one_hot = np.zeros((len(pred), n_classes))
                one_hot[np.arange(len(pred)), pred.astype(int)] = 1
                processed_preds.append(one_hot)
            else:
                processed_preds.append(pred)

        # Create target one-hot
        n_classes = len(np.unique(y_train))
        target_one_hot = np.zeros((1, n_classes))
        target_one_hot[0, y_sample] = 1

        # Update ensemble
        metrics = ensemble.update(processed_preds, target_one_hot)

        # Print progress
        if (i + 1) % 200 == 0:
            print(f"Sample {i+1:4d}/{len(indices)}:")
            print(f"  Weights: {metrics['weights']}")

    # Evaluate on test set
    print("\n" + "="*60)
    print("Evaluation on test set")
    print("="*60 + "\n")

    test_predictions = []
    for x_sample in X_test:
        ensemble_pred, _ = ensemble.predict(x_sample.reshape(1, -1))
        test_predictions.append(ensemble_pred)

    test_predictions = np.array(test_predictions).squeeze()

    # Evaluate
    eval_metrics = evaluate_ensemble(
        test_predictions,
        y_test,
        task_type='classification'
    )

    print("Ensemble performance:")
    print(f"  Accuracy: {eval_metrics['accuracy']:.4f}")
    print(f"  Macro Precision: {eval_metrics['macro_precision']:.4f}")
    print(f"  Macro Recall: {eval_metrics['macro_recall']:.4f}")
    print(f"  Macro F1: {eval_metrics['macro_f1']:.4f}")

    # Final diagnostics
    print("\n" + "="*60)
    print("Final diagnostics")
    print("="*60 + "\n")

    diagnostics = ensemble.get_diagnostics()
    print("Final weights:")
    for name, weight in zip(expert_names, diagnostics['weights']):
        print(f"  {name:25s}: {weight:.4f}")

    print("\nPerformance scores:")
    for name, score in zip(expert_names, diagnostics['performance_scores']):
        print(f"  {name:25s}: {score:.4f}")

    print("\nCoherence scores:")
    for name, score in zip(expert_names, diagnostics['coherence_scores']):
        print(f"  {name:25s}: {score:.4f}")

    # Diversity analysis
    from earcp.utils.metrics import compute_diversity

    diversity = compute_diversity(diagnostics['weights_history'])
    print(f"\nDiversity metrics:")
    print(f"  Mean entropy: {diversity['mean_entropy']:.4f}")
    print(f"  Final entropy: {diversity['final_entropy']:.4f}")

    print("\n" + "="*60)
    print("Example completed successfully!")
    print("="*60)


if __name__ == "__main__":
    main()
