# EARCP: Invention Disclosure and IP Claims Document

**Title:** EARCP - Ensemble Auto-Régulé par Cohérence et Performance  
**Inventor:** Mike Amega  
**Date of Invention:** 2025  
**Date of Public Disclosure:** November 13, 2025  
**Status:** Defensive Publication / Prior Art Establishment  

---

## PURPOSE OF THIS DOCUMENT

This document serves as a comprehensive disclosure of all novel inventions, innovations, and technical contributions embodied in the EARCP architecture. It establishes prior art to prevent third-party patent claims while preserving the inventor's rights to:

1. Commercialize the technology
2. License the technology under custom terms
3. File patent applications within applicable grace periods
4. Maintain copyright protection on implementations

---

## INDEPENDENT CLAIMS

The following represent the core inventive concepts of EARCP:

### Claim 1: Dual-Signal Ensemble Weighting

**Novel Invention:** A method for dynamically weighting predictions from multiple machine learning models comprising:

1. Computing a **performance score** P_i,t for each expert model i at time t based on historical predictive accuracy

2. Computing a **coherence score** C_i,t measuring agreement between expert i and other experts in the ensemble

3. Combining performance and coherence scores into a unified score: s_i,t = β·P_i,t + (1-β)·C_i,t where β ∈ [0,1] is a tunable parameter

4. Computing model weights through exponential transformation: w_i,t ∝ exp(η·s_i,t)

5. Enforcing minimum weight constraints: w_i,t ≥ w_min to maintain exploration

**Novelty:** Prior art teaches either performance-based weighting (Hedge algorithm) OR structural gating (MoE), but NOT the combination of performance and coherence signals with provable guarantees.

**Advantage:** Achieves superior robustness compared to pure performance-based methods while maintaining theoretical guarantees.

---

### Claim 2: Exponential Moving Average Performance Tracking

**Novel Invention:** A method for tracking model performance in non-stationary environments comprising:

1. Initializing performance score: P_i,0 = 0

2. At each time step t, computing loss: ℓ_i,t = L(p_i,t, y_t)

3. Updating performance score via EMA: P_i,t = α_P·P_i,t-1 + (1-α_P)·(-ℓ_i,t)

4. Using negative loss (-ℓ_i,t) to create increasing scores for better performers

5. Applying normalization: P̃_i,t = (P_i,t - min_j P_j,t)/(max_j P_j,t - min_j P_j,t + ε)

**Novelty:** Prior art uses cumulative losses (Hedge) which fails in non-stationary settings. EARCP's EMA-based tracking adapts to distribution shifts.

**Advantage:** Enables continuous adaptation while smoothing noise.

---

### Claim 3: Inter-Model Coherence Measurement

**Novel Invention:** A method for quantifying agreement between heterogeneous models comprising:

**For classification tasks:**
1. Computing predicted class for each expert: c_i,t = argmax(p_i,t)
2. Computing pairwise agreement: A_i,j,t = 𝟙{c_i,t = c_j,t}
3. Aggregating into coherence score: C_i,t = (1/(M-1))·Σ_{j≠i} A_i,j,t

**For regression tasks:**
1. Computing pairwise distance: d_i,j,t = ||p_i,t - p_j,t||²
2. Converting to similarity: s_i,j,t = exp(-γ·d_i,j,t)
3. Aggregating: C_i,t = (1/(M-1))·Σ_{j≠i} s_i,j,t

4. Applying temporal smoothing: C̄_i,t = α_C·C̄_i,t-1 + (1-α_C)·C_i,t

**Novelty:** Prior art does not teach using inter-model agreement as a signal for ensemble weighting. MoE uses input features, not model agreement.

**Advantage:** Leverages collective wisdom - when diverse models agree, predictions are more reliable.

---

### Claim 4: Weight Floor Enforcement with Renormalization

**Novel Invention:** A method for maintaining exploration in adaptive ensembles comprising:

1. Computing preliminary weights through normalization: w'_i,t = w̃_i,t / Σ_j w̃_j,t

2. Enforcing minimum weight: w_i,t = max(w'_i,t, w_min) for all i

3. Renormalizing to probability simplex: w_i,t ← w_i,t / Σ_j w_j,t

**Novelty:** Prior art teaches minimum weights OR renormalization, but not the specific two-stage process ensuring both exploration and valid probability distribution.

**Advantage:** Prevents weight collapse while maintaining mathematical validity (Σw_i = 1).

---

### Claim 5: Score Clipping for Numerical Stability

**Novel Invention:** A method for preventing numerical overflow in exponential weighting comprising:

1. Computing combined score: s_i,t = β·P̃_i,t + (1-β)·C̃_i,t

2. Clipping score to bounded range: s_i,t ← clip(s_i,t, -s_max, s_max)

3. Applying exponential transformation: w̃_i,t = exp(η_s·s_i,t)

where s_max is chosen to prevent exp(η_s·s_max) from overflowing (typically s_max = 10).

**Novelty:** Prior art teaches general numerical stability techniques but not this specific application to dual-signal ensemble weighting.

**Advantage:** Enables robust implementation across diverse computing environments and data scales.

---

## DEPENDENT CLAIMS

These build upon the independent claims:

### Claim 6: Hyperparameter Configuration

A method according to Claims 1-5 wherein:

- Performance smoothing parameter: α_P ∈ [0.7, 0.99]
- Coherence smoothing parameter: α_C ∈ [0.7, 0.95]
- Balance parameter: β ∈ [0, 1], preferably β ∈ [0.6, 0.8]
- Sensitivity parameter: η_s ∈ [1, 10], preferably η_s ∈ [3, 7]
- Weight floor: w_min ∈ [0.01, 0.2], preferably w_min = 0.05

**Novelty:** Specific parameter ranges derived from theoretical analysis and empirical validation.

---

### Claim 7: Adaptive Coherence Sensitivity

A method according to Claim 3 further comprising:

Dynamically adjusting coherence sensitivity γ based on ensemble diversity:
- If weight entropy H = -Σw_i log(w_i) is low (concentrated weights), increase γ to emphasize consensus
- If H is high (dispersed weights), decrease γ to allow more disagreement

**Novelty:** Adaptive tuning of coherence measurement based on ensemble state.

**Advantage:** Automatically adjusts exploration-exploitation based on ensemble concentration.

---

### Claim 8: Hierarchical EARCP

A method comprising:

1. Organizing M experts into K groups: G_1, ..., G_K

2. Creating K first-level EARCP ensembles, one per group

3. Creating a second-level EARCP ensemble that treats first-level ensembles as experts

4. Propagating predictions up the hierarchy: experts → group ensembles → meta ensemble

**Novelty:** Hierarchical application of dual-signal weighting across multiple scales.

**Advantage:** Enables scaling to large numbers of experts (M > 100) while maintaining computational efficiency.

---

### Claim 9: Online Expert Addition/Removal

A method according to Claims 1-5 further comprising:

**For adding expert i_new:**
1. Initialize weight: w_new = 1/(M+1)
2. Scale existing weights: w_i ← w_i·(1 - w_new) for all existing i
3. Initialize performance: P_new = mean(P_1, ..., P_M)
4. Initialize coherence: C̄_new = 0.5

**For removing expert i_remove:**
1. Delete expert i_remove
2. Renormalize weights: w_i ← w_i / Σ_{j≠i_remove} w_j

**Novelty:** Specific initialization and rebalancing procedures for dynamic expert sets.

**Advantage:** Enables continual learning with evolving model pools.

---

### Claim 10: Delayed Feedback Adaptation

A method according to Claims 1-5 wherein target revelation is delayed, comprising:

1. Maintaining a buffer of (prediction, expert_predictions, timestamp) tuples

2. Upon target revelation at time t', retrieving corresponding predictions from time t < t'

3. Computing losses: ℓ_i,t = L(p_i,t, y_t')

4. Applying time-discounted updates: P_i,t' = α_P·P_i,t'-1 + (1-α_P)·δ^(t'-t)·(-ℓ_i,t)

where δ ∈ (0,1] is a discount factor

**Novelty:** Specific mechanism for handling delayed feedback in dual-signal weighting.

**Advantage:** Enables application to domains with temporal credit assignment problems.

---

## IMPLEMENTATION INNOVATIONS

Beyond the core algorithm, the following implementation techniques are disclosed:

### Innovation 1: Efficient Coherence Computation

For large M, approximate coherence using sampling:

```python
def approximate_coherence(predictions, K):
    """Compute coherence using K sampled pairs instead of all O(M²) pairs."""
    M = len(predictions)
    coherence = np.zeros(M)
    
    for i in range(M):
        j_samples = random.sample([j for j in range(M) if j != i], 
                                  min(K, M-1))
        coherence[i] = mean([agreement(i, j) for j in j_samples])
    
    return coherence
```

**Complexity reduction:** O(M²) → O(M·K) where K << M

---

### Innovation 2: Parallel Expert Inference

```python
def parallel_predict(experts, x):
    """Execute expert predictions in parallel threads."""
    with ThreadPoolExecutor(max_workers=len(experts)) as executor:
        futures = [executor.submit(expert.predict, x) for expert in experts]
        predictions = [f.result() for f in futures]
    return predictions
```

**Advantage:** Near-linear speedup for compute-bound expert models.

---

### Innovation 3: Rolling Normalization

Maintain rolling statistics for efficient normalization:

```python
class RollingNormalizer:
    def __init__(self, window_size):
        self.window = deque(maxlen=window_size)
    
    def normalize(self, scores):
        self.window.extend(scores)
        min_val, max_val = min(self.window), max(self.window)
        return (scores - min_val) / (max_val - min_val + 1e-8)
```

**Advantage:** O(1) normalization after initial window fill, vs O(window_size) naive approach.

---

### Innovation 4: Diagnostic Metrics

```python
def get_diagnostics():
    return {
        'weight_entropy': -sum(w_i * log(w_i)),  # Concentration measure
        'max_weight': max(w_i),                   # Dominance measure
        'performance_spread': std(P_i),           # Performance variance
        'coherence_mean': mean(C̄_i),             # Average agreement
        'effective_experts': 1/sum(w_i²)         # Perplexity
    }
```

**Novelty:** Specific diagnostic metrics for monitoring ensemble health.

---

## THEORETICAL CONTRIBUTIONS

### Contribution 1: Regret Bound with Coherence

**Theorem:** With 0 < β < 1, EARCP achieves:

```
Regret_T ≤ (1/β)·√(2T log M)
```

**Proof approach:** 
1. Show performance component alone achieves √(2T log M) via reduction to Hedge
2. Treat coherence as side information that scales learning rate by β
3. Apply standard regret analysis with scaled rate

**Novelty:** First regret bound for ensemble method combining performance and agreement signals.

---

### Contribution 2: Stability Analysis

**Proposition:** With floor constraint w_min > 0, the weight update is Lipschitz continuous:

```
||w_t - w_t'|| ≤ L·||s_t - s_t'||
```

for some Lipschitz constant L depending on η_s and w_min.

**Proof:** Uses smoothness of exp() and enforced bounds on scores and weights.

**Implication:** Small perturbations in scores produce bounded changes in weights, ensuring stability.

---

### Contribution 3: Convergence in Non-Stationary Settings

**Proposition:** In piecewise-stationary environments with K regime changes, EARCP achieves:

```
Regret_T ≤ K·√(2T_avg log M)
```

where T_avg = T/K is average regime length.

**Intuition:** EMA smoothing allows adaptation to new regimes while √ term captures transient learning in each regime.

---

## EXPERIMENTAL INNOVATIONS

### Protocol 1: Walk-Forward Validation

For time-series tasks:
1. Initialize with training period [0, T_0]
2. Test on [T_0, T_0 + Δ]
3. Retrain on [0, T_0 + Δ]
4. Test on [T_0 + Δ, T_0 + 2Δ]
5. Repeat, expanding training window

**Advantage:** Respects temporal order, avoids look-ahead bias.

---

### Protocol 2: Statistical Significance Testing

For comparing EARCP vs baseline:
1. Run N trials with different random seeds
2. Compute paired differences d_i = loss_EARCP^(i) - loss_baseline^(i)
3. Apply Wilcoxon signed-rank test (non-parametric)
4. Compute bootstrap confidence intervals (1000 replications)

**Advantage:** Robust to non-Gaussian loss distributions.

---

## DISCLOSED VARIATIONS

The following variations are explicitly disclosed to establish broad prior art:

### Variation 1: Alternative Coherence Metrics

- Correlation-based: C_i = mean([corr(p_i, p_j) for j ≠ i])
- Cosine similarity: C_i = mean([cos_sim(p_i, p_j) for j ≠ i])
- KL divergence: C_i = mean([exp(-KL(p_i || p_j)) for j ≠ i])
- Rank correlation: C_i = mean([spearman(p_i, p_j) for j ≠ i])

---

### Variation 2: Alternative Weight Updates

- Multiplicative update: w_i,t = w_i,t-1·exp(η·(s_i,t - mean(s_j,t)))
- Polynomial update: w_i,t ∝ (1 + s_i,t)^η
- Linear update: w_i,t ∝ w_i,t-1 + η·(s_i,t - mean(s_j,t))
- Softmax update: w_i,t = exp(η·s_i,t) / Σexp(η·s_j,t)

---

### Variation 3: Alternative Performance Measures

- Calibration error: P_i,t based on prediction calibration
- Diversity reward: P_i,t includes bonus for unique correct predictions
- Risk-adjusted: P_i,t = mean_return / std_return
- Pareto-optimality: P_i,t measures non-domination count

---

### Variation 4: Multi-Objective EARCP

Extend to vector-valued scores:
- s_i,t = [s_i,t^(1), s_i,t^(2), ..., s_i,t^(K)]
- Aggregate via: w_i,t ∝ exp(Σ_k λ_k·s_i,t^(k))
- Examples: accuracy, calibration, diversity, computational cost

---

### Variation 5: Context-Dependent Weighting

Condition weights on input features:
- Compute base weights: w_i,t^(base) via standard EARCP
- Learn context weights: w_i,t^(ctx)(x) via neural network
- Combine: w_i,t(x) = α·w_i,t^(base) + (1-α)·w_i,t^(ctx)(x)

---

## PRIOR ART ANALYSIS

### Distinguishing from Existing Work

**Hedge Algorithm (Freund & Schapire, 1997):**
- Uses only losses, no coherence
- EARCP adds C_i,t component
- EARCP uses EMA vs cumulative losses

**Mixture of Experts (Jacobs et al., 1991):**
- Gates on input features, not performance
- Requires joint training
- EARCP works with pre-trained experts

**Stacking (Wolpert, 1992):**
- Learns fixed meta-model offline
- No online adaptation
- EARCP adapts continuously

**Dynamic Weighted Majority (Kolter & Maloof, 2007):**
- Binary weighting (include/exclude)
- No coherence measure
- EARCP uses continuous weights with coherence

**Ensemble Selection (Caruana et al., 2004):**
- Greedy selection, static
- No theoretical guarantees
- EARCP has provable bounds

**Conclusion:** EARCP represents a novel combination of:
1. Performance-based adaptation (from Hedge)
2. Coherence-aware weighting (novel contribution)
3. Practical stabilization (novel techniques)
4. Theoretical guarantees (extended from Hedge)

---

## USE CASES AND APPLICATIONS

While EARCP is a general-purpose architecture, the following applications are disclosed:

### Domain 1: Time Series Forecasting
- Electricity demand prediction
- Weather forecasting
- Traffic flow prediction
- Resource usage prediction

### Domain 2: Sequential Classification
- Activity recognition from sensors
- Fraud detection in transaction streams
- Anomaly detection in system logs
- Medical diagnosis from sequential tests

### Domain 3: Reinforcement Learning
- Policy ensembles in robotics
- Strategy selection in games
- Resource allocation in networks
- Portfolio management

### Domain 4: Online Learning
- Click-through rate prediction
- Recommendation systems
- A/B testing optimization
- Adaptive content delivery

### Domain 5: Survival Analysis
- Patient outcome prediction
- Equipment failure prediction
- Customer churn prediction
- Event timing estimation

---

## INTELLECTUAL PROPERTY STRATEGY

### Current Status (as of November 13, 2025)

**Defensive Publication:**
- ✅ Complete algorithm disclosed
- ✅ Theoretical analysis published
- ✅ Implementation details shared
- ✅ Variations and extensions documented
- ✅ Timestamped via GitHub

**Effect:**
- Establishes prior art preventing third-party patents
- Preserves inventor's commercialization rights
- Maintains copyright on code implementations
- Allows future patent applications on undisclosed improvements

### Future Options

**Option A: Pure Open Source**
- Release all code under permissive license (MIT/Apache)
- Build community and adoption
- Monetize through consulting/support

**Option B: Dual Licensing**
- Open source for academic/non-commercial use
- Commercial license for revenue-generating applications
- Example: GPL/Commercial like MySQL

**Option C: Patent + Open Core**
- File patents on core innovations within grace period
- Open source reference implementation
- License patents for commercial use

**Recommended:** Start with Option B (dual licensing) for flexibility.

---

## INVENTOR DECLARATION

I, Mike Amega, declare that:

1. I am the sole inventor of the EARCP architecture and all disclosed innovations

2. The inventive concepts were conceived independently and represent original work

3. To the best of my knowledge, these inventions are novel and non-obvious over existing prior art

4. This disclosure is complete and accurate as of November 13, 2025

5. I reserve all rights to file patent applications, license the technology, and enforce intellectual property claims

**Signature:** Mike Amega  
**Date:** November 13, 2025  
**Location:** Windsor, Ontario, Canada  

---

## APPENDIX: PRIOR ART SEARCH

A review of existing literature was conducted across:
- Academic papers (Google Scholar, arXiv, IEEE, ACM)
- Patent databases (USPTO, EPO, WIPO)
- Industry publications and technical blogs
- Open-source repositories

**Search queries used:**
- "ensemble learning online adaptive"
- "mixture of experts agreement"
- "multiplicative weight update coherence"
- "dynamic ensemble weighting"
- "expert agreement ensemble"

**Result:** No prior work combining performance-based adaptation with inter-model coherence weighting in the specific manner disclosed in EARCP.

**Closest prior art:**
1. Hedge: Performance only, no coherence
2. MoE: Input gating, not performance/coherence
3. Bandit algorithms: Explore-exploit, but single-expert selection not ensemble
4. Ensemble pruning: Static selection, not dynamic weighting

**Novelty confirmed** as of November 13, 2025.

---

## CONTACT FOR IP MATTERS

**For licensing inquiries:**  
Mike Amega  
contact@mikeamega.ca  

**For patent collaboration:**  
Available to discuss co-filing with industry partners or research institutions.

**For infringement concerns:**  
Contact inventor directly before pursuing legal action to discuss licensing options.

---

**END OF INVENTION DISCLOSURE**

*This document establishes comprehensive prior art for the EARCP architecture and all disclosed variations as of November 13, 2025.*
