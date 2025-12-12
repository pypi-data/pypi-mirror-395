# EARCP - Guide d'Utilisation Complet

**Ensemble Auto-Régulé par Cohérence et Performance**

Copyright © 2025 Mike Amega. Tous droits réservés.

---

## Table des Matières

1. [Installation](#installation)
2. [Démarrage Rapide](#démarrage-rapide)
3. [Concepts Fondamentaux](#concepts-fondamentaux)
4. [Configuration](#configuration)
5. [Utilisation Avancée](#utilisation-avancée)
6. [Intégration avec les Frameworks ML](#intégration-avec-les-frameworks-ml)
7. [Visualisation et Diagnostics](#visualisation-et-diagnostics)
8. [Cas d'Utilisation](#cas-dutilisation)
9. [API Reference](#api-reference)
10. [FAQ](#faq)

---

## Installation

### Installation Standard

```bash
pip install earcp
```

### Installation depuis les sources

```bash
git clone https://github.com/Volgat/earcp.git
cd earcp
pip install -e .
```

### Installation avec dépendances optionnelles

```bash
# Avec support PyTorch
pip install earcp[torch]

# Avec support scikit-learn
pip install earcp[sklearn]

# Installation complète
pip install earcp[full]
```

### Dépendances

**Obligatoires:**
- numpy >= 1.20.0
- scipy >= 1.7.0
- matplotlib >= 3.3.0

**Optionnelles:**
- torch >= 1.9.0 (pour TorchWrapper)
- scikit-learn >= 0.24.0 (pour SklearnWrapper)

---

## Démarrage Rapide

### Exemple Minimal

```python
from earcp import EARCP

# Définir des modèles experts (tout modèle avec une méthode .predict())
class SimpleExpert:
    def __init__(self, coefficient):
        self.coefficient = coefficient

    def predict(self, x):
        return self.coefficient * x

# Créer des experts
experts = [
    SimpleExpert(1.0),
    SimpleExpert(2.0),
    SimpleExpert(0.5),
]

# Initialiser l'ensemble EARCP
ensemble = EARCP(
    experts=experts,
    beta=0.7,      # Balance performance/cohérence
    eta_s=5.0,     # Sensibilité des poids
    w_min=0.05     # Poids minimum
)

# Boucle d'apprentissage en ligne
for t in range(100):
    # Obtenir une prédiction
    x = data[t]
    prediction, expert_predictions = ensemble.predict(x)

    # Observer la cible réelle
    target = get_target(prediction)

    # Mettre à jour les poids
    metrics = ensemble.update(expert_predictions, target)
```

### Exemple Complet avec Données Réelles

```python
import numpy as np
from earcp import EARCP

# Générer des données synthétiques
np.random.seed(42)
T = 200  # Nombre d'étapes

# Fonction cible
def target_function(t):
    x = t * 0.1
    return 2*x + np.sin(x) + np.random.normal(0, 0.1)

# Définir des experts avec différentes stratégies
class LinearExpert:
    def __init__(self, slope, intercept):
        self.slope = slope
        self.intercept = intercept

    def predict(self, x):
        return self.slope * x + self.intercept

class SinusoidalExpert:
    def __init__(self, amplitude, frequency):
        self.amplitude = amplitude
        self.frequency = frequency

    def predict(self, x):
        return self.amplitude * np.sin(self.frequency * x)

# Créer les experts
experts = [
    LinearExpert(slope=2.0, intercept=0.5),
    LinearExpert(slope=1.5, intercept=1.0),
    SinusoidalExpert(amplitude=1.0, frequency=1.0),
]

# Initialiser EARCP
ensemble = EARCP(experts=experts, beta=0.7, eta_s=5.0)

# Apprentissage en ligne
for t in range(T):
    x = np.array([t * 0.1])
    target = np.array([target_function(t)])

    # Prédiction et mise à jour
    pred, expert_preds = ensemble.predict(x)
    metrics = ensemble.update(expert_preds, target)

    if (t + 1) % 50 == 0:
        print(f"Étape {t+1}: Poids = {metrics['weights']}")

# Obtenir les diagnostics finaux
diagnostics = ensemble.get_diagnostics()
print(f"\nPoids finaux: {diagnostics['weights']}")
print(f"Pertes cumulatives: {diagnostics['cumulative_loss']}")
```

---

## Concepts Fondamentaux

### Architecture EARCP

EARCP combine dynamiquement les prédictions de plusieurs modèles experts en utilisant un **mécanisme de pondération à double signal** :

1. **Performance (P)** : Mesure la qualité des prédictions de chaque expert
2. **Cohérence (C)** : Mesure l'accord entre les experts

#### Algorithme Principal

À chaque étape *t*, EARCP :

1. **Collecte les prédictions** de M experts : p₁,ₜ, ..., p_M,ₜ

2. **Calcule les scores de performance** :
   ```
   P_i,t = α_P · P_i,t-1 + (1 - α_P) · (-ℓ_i,t)
   ```

3. **Calcule la cohérence** :
   ```
   C_i,t = (1/(M-1)) · Σⱼ≠ᵢ Agreement(i,j)
   ```

4. **Combine les signaux** :
   ```
   s_i,t = β · P_i,t + (1 - β) · C_i,t
   ```

5. **Met à jour les poids** :
   ```
   w_i,t ∝ exp(η_s · s_i,t) avec contrainte w_i ≥ w_min
   ```

### Paramètres Clés

| Paramètre | Description | Valeur par défaut | Plage typique |
|-----------|-------------|-------------------|---------------|
| `alpha_P` | Lissage exponentiel de la performance | 0.9 | [0.8, 0.95] |
| `alpha_C` | Lissage exponentiel de la cohérence | 0.85 | [0.75, 0.95] |
| `beta` | Balance performance/cohérence | 0.7 | [0.5, 1.0] |
| `eta_s` | Sensibilité des poids | 5.0 | [1.0, 10.0] |
| `w_min` | Poids minimum | 0.05 | [0.01, 1/M] |

#### Interprétation de Beta

- **β = 1.0** : Pondération basée uniquement sur la performance (similaire à Hedge)
- **β = 0.5** : Balance égale entre performance et cohérence
- **β = 0.0** : Pondération basée uniquement sur la cohérence (favorise la diversité)

Recommandation : Commencer avec **β = 0.7** pour un bon équilibre.

---

## Configuration

### Utiliser EARCPConfig

```python
from earcp import EARCP, EARCPConfig

# Créer une configuration personnalisée
config = EARCPConfig(
    alpha_P=0.9,
    alpha_C=0.85,
    beta=0.7,
    eta_s=5.0,
    w_min=0.05,
    prediction_mode='regression',  # ou 'classification'
    track_diagnostics=True,
    random_state=42
)

# Utiliser la configuration
ensemble = EARCP(experts=experts, config=config)
```

### Configurations Prédéfinies

```python
from earcp import get_preset_config

# Configurations disponibles:
# - 'default': Configuration standard
# - 'performance_focused': Privilégie la performance (β=0.95)
# - 'diversity_focused': Privilégie la diversité (β=0.5)
# - 'balanced': Équilibre optimal (β=0.7)
# - 'conservative': Mise à jour prudente
# - 'aggressive': Mise à jour rapide

config = get_preset_config('performance_focused')
ensemble = EARCP(experts=experts, config=config)
```

### Fonctions de Perte Personnalisées

```python
def custom_loss(y_pred, y_true):
    """Fonction de perte personnalisée retournant une valeur dans [0, 1]."""
    mse = np.mean((y_pred - y_true) ** 2)
    return np.tanh(mse)  # Normaliser à [0, 1]

config = EARCPConfig(loss_fn=custom_loss)
ensemble = EARCP(experts=experts, config=config)
```

### Fonctions de Cohérence Personnalisées

```python
def custom_coherence(pred_i, pred_j):
    """Fonction de cohérence personnalisée retournant une valeur dans [0, 1]."""
    correlation = np.corrcoef(pred_i.flatten(), pred_j.flatten())[0, 1]
    return (correlation + 1) / 2  # Mapper [-1, 1] à [0, 1]

config = EARCPConfig(coherence_fn=custom_coherence)
ensemble = EARCP(experts=experts, config=config)
```

---

## Utilisation Avancée

### Sauvegarder et Charger l'État

```python
# Sauvegarder l'état de l'ensemble
ensemble.save_state('ensemble_checkpoint.pkl')

# Charger l'état
ensemble.load_state('ensemble_checkpoint.pkl')
```

### Réinitialiser l'Ensemble

```python
# Réinitialiser à l'état initial
ensemble.reset()
```

### Modifier les Paramètres Dynamiquement

```python
# Ajuster beta pendant l'exécution
ensemble.weighting.set_beta(0.8)

# Ajuster la sensibilité
ensemble.weighting.set_eta_s(7.0)
```

### Accéder aux Composants Internes

```python
# Obtenir les scores de performance
perf_scores = ensemble.performance_tracker.get_scores()

# Obtenir les scores de cohérence
coh_scores = ensemble.coherence_metrics.get_scores()

# Obtenir la matrice de cohérence complète
coh_matrix = ensemble.coherence_metrics.get_coherence_matrix(expert_predictions)
```

### Utilisation Multi-Objectifs

```python
from earcp.core.performance_tracker import MultiObjectivePerformanceTracker

# Créer un tracker multi-objectifs
tracker = MultiObjectivePerformanceTracker(
    n_experts=3,
    n_objectives=2,
    objective_weights=[0.6, 0.4]  # Pondération des objectifs
)

# Mettre à jour avec plusieurs cibles
tracker.update(
    predictions=[pred1, pred2, pred3],
    targets=[target_obj1, target_obj2]
)
```

---

## Intégration avec les Frameworks ML

### Avec scikit-learn

```python
from sklearn.linear_model import Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from earcp import EARCP
from earcp.utils.wrappers import SklearnWrapper

# Créer et entraîner des modèles sklearn
models = [
    Ridge(alpha=1.0),
    Lasso(alpha=0.5),
    RandomForestRegressor(n_estimators=100)
]

# Entraîner les modèles
for model in models:
    model.fit(X_train, y_train)

# Encapsuler pour EARCP
experts = [SklearnWrapper(model) for model in models]

# Créer l'ensemble
ensemble = EARCP(experts=experts, beta=0.7)

# Utilisation
for x, y in zip(X_test, y_test):
    pred, expert_preds = ensemble.predict(x.reshape(1, -1))
    ensemble.update(expert_preds, y.reshape(1, -1))
```

### Avec PyTorch

```python
import torch
import torch.nn as nn
from earcp import EARCP
from earcp.utils.wrappers import TorchWrapper

# Définir des modèles PyTorch
class SimpleNN(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        return self.layers(x)

# Créer des modèles
models = [SimpleNN(input_dim=10) for _ in range(3)]

# Encapsuler pour EARCP
experts = [TorchWrapper(model, device='cpu') for model in models]

# Créer l'ensemble
ensemble = EARCP(experts=experts)
```

### Avec TensorFlow/Keras

```python
from tensorflow import keras
from earcp import EARCP
from earcp.utils.wrappers import KerasWrapper

# Créer des modèles Keras
def create_model():
    model = keras.Sequential([
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

models = [create_model() for _ in range(3)]

# Entraîner les modèles
for model in models:
    model.fit(X_train, y_train, epochs=10, verbose=0)

# Encapsuler pour EARCP
experts = [KerasWrapper(model) for model in models]

# Créer l'ensemble
ensemble = EARCP(experts=experts)
```

### Wrapper pour Fonctions Personnalisées

```python
from earcp.utils.wrappers import CallableWrapper

# Définir une fonction de prédiction simple
def my_predictor(x):
    return np.mean(x) * 2.5

# Encapsuler
expert = CallableWrapper(my_predictor)

# Utiliser dans EARCP
experts = [expert, other_expert_1, other_expert_2]
ensemble = EARCP(experts=experts)
```

---

## Visualisation et Diagnostics

### Obtenir les Diagnostics

```python
# Obtenir les diagnostics complets
diagnostics = ensemble.get_diagnostics()

# Contenu disponible :
# - 'weights': Poids actuels
# - 'performance_scores': Scores de performance actuels
# - 'coherence_scores': Scores de cohérence actuels
# - 'time_step': Étape temporelle actuelle
# - 'weights_history': Historique des poids (si track_diagnostics=True)
# - 'performance_history': Historique des performances
# - 'coherence_history': Historique de la cohérence
# - 'cumulative_loss': Perte cumulative par expert
```

### Visualisations

```python
from earcp.utils.visualization import (
    plot_weights,
    plot_performance,
    plot_diagnostics,
    plot_regret
)

# Évolution des poids
plot_weights(
    diagnostics['weights_history'],
    expert_names=['Expert 1', 'Expert 2', 'Expert 3'],
    save_path='weights.png'
)

# Performance et cohérence
plot_performance(
    diagnostics['performance_history'],
    diagnostics['coherence_history'],
    expert_names=['Expert 1', 'Expert 2', 'Expert 3'],
    save_path='performance.png'
)

# Diagnostics complets
plot_diagnostics(
    diagnostics,
    expert_names=['Expert 1', 'Expert 2', 'Expert 3'],
    save_path='diagnostics.png'
)

# Analyse de regret
ensemble_cum_loss = np.sum(ensemble.performance_tracker.get_loss_history())
plot_regret(
    diagnostics['cumulative_loss'],
    ensemble_cum_loss,
    expert_names=['Expert 1', 'Expert 2', 'Expert 3'],
    save_path='regret.png'
)
```

### Métriques d'Évaluation

```python
from earcp.utils.metrics import (
    compute_regret,
    compute_diversity,
    evaluate_ensemble,
    theoretical_regret_bound
)

# Calculer le regret
regret_metrics = compute_regret(
    expert_cumulative_losses=diagnostics['cumulative_loss'],
    ensemble_cumulative_loss=ensemble_cum_loss
)
print(f"Regret: {regret_metrics['regret']:.4f}")
print(f"Regret relatif: {regret_metrics['relative_regret']:.2%}")

# Calculer la diversité
diversity = compute_diversity(diagnostics['weights_history'])
print(f"Entropie moyenne: {diversity['mean_entropy']:.4f}")

# Borne théorique du regret
bound = theoretical_regret_bound(T=1000, M=3, beta=0.7)
print(f"Borne théorique: {bound:.4f}")

# Évaluer l'ensemble
eval_metrics = evaluate_ensemble(
    predictions=ensemble_predictions,
    targets=true_targets,
    task_type='regression'  # ou 'classification'
)
print(f"RMSE: {eval_metrics['rmse']:.4f}")
print(f"R²: {eval_metrics['r2']:.4f}")
```

---

## Cas d'Utilisation

### 1. Prédiction de Séries Temporelles

```python
# Experts avec différentes fenêtres temporelles
class MovingAverageExpert:
    def __init__(self, window_size):
        self.window = window_size
        self.history = []

    def predict(self, x):
        self.history.append(x)
        if len(self.history) > self.window:
            self.history.pop(0)
        return np.mean(self.history)

experts = [
    MovingAverageExpert(window_size=5),
    MovingAverageExpert(window_size=10),
    MovingAverageExpert(window_size=20),
]

ensemble = EARCP(experts=experts, beta=0.7)
```

### 2. Apprentissage par Renforcement

```python
# Combiner différents agents RL
class DQNAgent:
    def predict(self, state):
        # Retourne les Q-values
        return self.model(state)

agents = [dqn_agent_1, dqn_agent_2, policy_gradient_agent]
ensemble = EARCP(experts=agents, beta=0.8)

# Dans la boucle d'entraînement
state = env.reset()
action_values, expert_values = ensemble.predict(state)
action = np.argmax(action_values)

next_state, reward, done, _ = env.step(action)

# Mise à jour avec la cible Q-learning
target = reward + gamma * np.max(next_action_values)
ensemble.update(expert_values, target)
```

### 3. Classification Multi-Classes

```python
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

# Créer des classifieurs
classifiers = [
    LogisticRegression(),
    SVC(probability=True),
    RandomForestClassifier()
]

# Entraîner
for clf in classifiers:
    clf.fit(X_train, y_train)

# Créer l'ensemble
experts = [SklearnWrapper(clf) for clf in classifiers]
ensemble = EARCP(
    experts=experts,
    prediction_mode='classification'
)
```

### 4. Prédiction Financière

```python
# Experts avec différentes stratégies
class TrendFollower:
    def predict(self, features):
        # Stratégie momentum
        return features['price'] * (1 + features['momentum'])

class MeanReversion:
    def predict(self, features):
        # Stratégie retour à la moyenne
        return features['mean'] + 0.5 * (features['mean'] - features['price'])

experts = [TrendFollower(), MeanReversion(), ARIMAModel(), LSTMModel()]
ensemble = EARCP(experts=experts, beta=0.75)
```

---

## API Reference

### Classe EARCP

```python
class EARCP(experts, config=None, **kwargs)
```

**Paramètres:**
- `experts` (list): Liste de modèles experts avec méthode `.predict()`
- `config` (EARCPConfig, optional): Objet de configuration
- `**kwargs`: Paramètres de configuration supplémentaires

**Méthodes:**

#### `predict(x, return_expert_predictions=True)`
Fait une prédiction d'ensemble.

**Retourne:**
- `prediction` (np.ndarray): Prédiction pondérée
- `expert_predictions` (list): Prédictions individuelles (optionnel)

#### `update(expert_predictions, target)`
Met à jour l'ensemble après observation de la cible.

**Retourne:**
- `metrics` (dict): Métriques de cette étape

#### `get_weights()`
Retourne les poids actuels des experts.

#### `get_diagnostics()`
Retourne les diagnostics complets.

#### `reset()`
Réinitialise l'ensemble à l'état initial.

#### `save_state(filepath)`
Sauvegarde l'état de l'ensemble.

#### `load_state(filepath)`
Charge l'état de l'ensemble.

### Classe EARCPConfig

```python
class EARCPConfig(
    alpha_P=0.9,
    alpha_C=0.85,
    beta=0.7,
    eta_s=5.0,
    w_min=0.05,
    loss_fn=None,
    coherence_fn=None,
    prediction_mode='auto',
    epsilon=1e-10,
    normalize_weights=True,
    track_diagnostics=True,
    random_state=None
)
```

---

## FAQ

### Q: Combien d'experts minimum/maximum ?

**R:** Minimum 2 experts. Testé jusqu'à 50+ experts. Performance optimale avec 3-10 experts.

### Q: EARCP fonctionne-t-il avec des modèles pré-entraînés ?

**R:** Oui ! Utilisez les wrappers (`SklearnWrapper`, `TorchWrapper`, etc.) pour intégrer n'importe quel modèle pré-entraîné.

### Q: Comment choisir beta ?

**R:**
- **β = 0.7-0.8** : Bon point de départ (recommandé)
- **β > 0.8** : Si vous avez confiance en vos experts
- **β < 0.7** : Si vous voulez favoriser la diversité

### Q: Quelle est la complexité temporelle ?

**R:** O(M²) par étape, où M est le nombre d'experts (principalement dû au calcul de cohérence).

### Q: EARCP supporte-t-il l'apprentissage par batch ?

**R:** EARCP est conçu pour l'apprentissage en ligne séquentiel. Pour du batch, appelez `update()` pour chaque échantillon.

### Q: Comment gérer des experts très déséquilibrés ?

**R:** Ajustez `w_min` pour garantir un poids minimum à tous les experts, ou utilisez `eta_s` plus faible pour des mises à jour plus douces.

### Q: Peut-on utiliser EARCP pour du clustering ?

**R:** Oui, si vos experts produisent des assignations de clusters ou des probabilités d'appartenance.

---

## Support et Contact

**Auteur:** Mike Amega
**Email:** info@amewebstudio.com
**GitHub:** https://github.com/Volgat/earcp
**Issues:** https://github.com/Volgat/earcp/issues

---

## Citation

```bibtex
@article{amega2025earcp,
  title={EARCP: Ensemble Auto-Régulé par Cohérence et Performance},
  author={Amega, Mike},
  year={2025},
  url={https://github.com/Volgat/earcp}
}
```

---

**Copyright © 2025 Mike Amega. Tous droits réservés.**
