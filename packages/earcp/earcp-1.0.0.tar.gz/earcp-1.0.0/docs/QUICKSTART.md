# EARCP - Guide de Démarrage Rapide

**De zéro à votre premier ensemble EARCP en 5 minutes**

---

## Installation

```bash
pip install earcp
```

---

## Exemple Minimal (30 secondes)

```python
from earcp import EARCP

# 1. Définir des experts simples
class Expert:
    def __init__(self, factor):
        self.factor = factor
    def predict(self, x):
        return self.factor * x

# 2. Créer l'ensemble
experts = [Expert(1.0), Expert(2.0), Expert(0.5)]
ensemble = EARCP(experts=experts)

# 3. Utiliser
import numpy as np
for t in range(50):
    x = np.array([t * 0.1])
    target = np.array([2.0 * t * 0.1])  # Fonction cible

    pred, expert_preds = ensemble.predict(x)
    ensemble.update(expert_preds, target)

# 4. Résultats
print(f"Poids finaux: {ensemble.get_weights()}")
```

**C'est tout ! Vous venez de créer votre premier ensemble adaptatif.**

---

## Exemple Complet (5 minutes)

### Étape 1: Préparer vos données

```python
import numpy as np

# Données synthétiques
np.random.seed(42)
T = 200

def generate_data(t):
    x = t * 0.1
    y = 2*x + np.sin(x) + np.random.normal(0, 0.1)
    return x, y
```

### Étape 2: Créer des experts diversifiés

```python
# Expert linéaire
class LinearExpert:
    def __init__(self, slope, intercept):
        self.slope = slope
        self.intercept = intercept

    def predict(self, x):
        return self.slope * x + self.intercept

# Expert sinusoïdal
class SinExpert:
    def __init__(self, amplitude, frequency):
        self.amplitude = amplitude
        self.frequency = frequency

    def predict(self, x):
        return self.amplitude * np.sin(self.frequency * x)

# Créer plusieurs experts
experts = [
    LinearExpert(2.0, 0.0),
    LinearExpert(1.5, 0.5),
    SinExpert(1.0, 1.0),
]
```

### Étape 3: Configurer et entraîner EARCP

```python
from earcp import EARCP

# Initialiser avec configuration
ensemble = EARCP(
    experts=experts,
    beta=0.7,      # Balance performance/cohérence
    eta_s=5.0,     # Sensibilité
    w_min=0.05     # Poids minimum
)

# Entraînement en ligne
print("Entraînement...")
for t in range(T):
    x, target = generate_data(t)
    x = np.array([x])
    target = np.array([target])

    pred, expert_preds = ensemble.predict(x)
    ensemble.update(expert_preds, target)

    if (t + 1) % 50 == 0:
        weights = ensemble.get_weights()
        print(f"Étape {t+1}: Poids = {weights}")
```

### Étape 4: Analyser les résultats

```python
# Obtenir les diagnostics
diagnostics = ensemble.get_diagnostics()

print("\n=== RÉSULTATS FINAUX ===")
print(f"Poids finaux: {diagnostics['weights']}")
print(f"Pertes cumulatives: {diagnostics['cumulative_loss']}")

# Meilleur expert
best_expert = np.argmin(diagnostics['cumulative_loss'])
print(f"Meilleur expert: Expert {best_expert + 1}")

# Visualiser (optionnel)
from earcp.utils.visualization import plot_diagnostics
plot_diagnostics(diagnostics, save_path='results.png')
print("Visualisation sauvegardée dans 'results.png'")
```

---

## Avec scikit-learn (2 minutes supplémentaires)

```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from earcp import EARCP
from earcp.utils.wrappers import SklearnWrapper

# Créer des modèles sklearn
models = [
    Ridge(alpha=1.0),
    Lasso(alpha=0.5),
    DecisionTreeRegressor(max_depth=5),
    RandomForestRegressor(n_estimators=50)
]

# Entraîner sur vos données
for model in models:
    model.fit(X_train, y_train)

# Encapsuler pour EARCP
experts = [SklearnWrapper(model) for model in models]

# Créer l'ensemble
ensemble = EARCP(experts=experts, beta=0.7)

# Utiliser en mode en ligne
for x, y in zip(X_test, y_test):
    pred, expert_preds = ensemble.predict(x.reshape(1, -1))
    ensemble.update(expert_preds, y.reshape(-1, 1))

# Résultats
print(f"Poids finaux: {ensemble.get_weights()}")
```

---

## Configurations Prédéfinies

Utilisez des presets pour démarrer rapidement :

```python
from earcp import EARCP, get_preset_config

# Configuration focalisée sur la performance
config = get_preset_config('performance_focused')
ensemble = EARCP(experts=experts, config=config)

# Configuration focalisée sur la diversité
config = get_preset_config('diversity_focused')
ensemble = EARCP(experts=experts, config=config)

# Configuration équilibrée (recommandée)
config = get_preset_config('balanced')
ensemble = EARCP(experts=experts, config=config)
```

---

## Prochaines Étapes

1. **Explorez les exemples** : Consultez le dossier `examples/` pour plus de cas d'usage
2. **Lisez la documentation complète** : `docs/USAGE.md`
3. **Personnalisez** : Ajustez les paramètres pour votre cas d'usage
4. **Visualisez** : Utilisez les outils de visualisation pour comprendre le comportement

---

## Aide Rapide

### Paramètres Importants

| Paramètre | Effet | Quand l'ajuster |
|-----------|-------|-----------------|
| `beta` | Balance perf/cohérence | Pour favoriser performance (↑) ou diversité (↓) |
| `eta_s` | Sensibilité des poids | Pour mises à jour rapides (↑) ou douces (↓) |
| `w_min` | Poids minimum | Pour éviter l'exclusion d'experts (↑) |
| `alpha_P` | Lissage performance | Pour privilégier historique (↑) ou récent (↓) |

### Problèmes Courants

**Poids concentrés sur un expert :**
- Diminuer `eta_s` ou `beta`
- Augmenter `w_min`

**Poids trop uniformes :**
- Augmenter `eta_s`
- Augmenter `beta` (favoriser performance)

**Instabilité :**
- Augmenter `alpha_P` et `alpha_C`
- Diminuer `eta_s`

---

## Support

- **Documentation** : [docs/USAGE.md](USAGE.md)
- **Exemples** : `examples/`
- **Issues** : https://github.com/Volgat/earcp/issues
- **Email** : info@amewebstudio.com

---

**Vous êtes prêt à utiliser EARCP ! 🚀**

Copyright © 2025 Mike Amega
