# Experiment 11: Manual Gradient with Adam for High-Dimensional Reconstruction

## Overview

This experiment builds on previous work (Experiments 8 and 10) to explore high-dimensional reconstruction using full-batch gradient descent, but now with a **manually implemented Adam optimizer**. This allows us to preserve the speed and structure of direct vector updates (as in Experiment 8), while gaining the convergence benefits of Adam — all **without using autograd, torch.nn.Parameter, or torch.optim.Adam**.

We compare reconstruction performance between:
- **Spherical constraints** (Euclidean distances to centroids)
- **Ellipsoidal constraints** (Mahalanobis distances to Gaussians with full-rank covariance)

## Key Goals

- Reconstruct a point `x_true ∈ ℝ^D` from its distances to `k` known centroids
- Implement **manual Adam** optimizer with no PyTorch optimizer overhead
- Compare runtime and accuracy for **spherical** vs **ellipsoidal** distance constraints
- Benchmark against previous results

## Setup

- **Dimension (D):** 784
- **Number of centroids (k):** 1024
- **Iters:** 10,000
- **Learning rate:** `1.0 / k = 0.0009765625`
- **Optimizer:** Manual Adam (β₁=0.9, β₂=0.999, ε=1e-8)
- **Device:** CUDA GPU

### Reconstruction Objective

Let `y_i` be the known distance from `x_true` to centroid `μ_i`:

- **Spherical:** `y_i = ||x_true - μ_i||₂`
- **Ellipsoidal:** `y_i = sqrt((x_true - μ_i)^T Σ_i⁻¹ (x_true - μ_i))`

We recover `x_est` to minimize:

```
L(x) = 0.5 * Σ_i (d_i(x) - y_i)^2
```

Where `d_i(x)` is either Euclidean or Mahalanobis distance.

### Manual Adam Update

For each step:

```
g_t = ∇L(x)
m_t = β₁ * m_{t-1} + (1 - β₁) * g_t
v_t = β₂ * v_{t-1} + (1 - β₂) * g_t²

x_t = x_{t-1} - α * m_t / (sqrt(v_t) + ε)
```

Implemented entirely in-place using native PyTorch tensor ops.

---

## Results

### ⏱ Runtime and Accuracy

| Method      | Final Error | Total Time | Notes                      |
|-------------|-------------|------------|----------------------------|
| Ellipsoidal | **0.318**   | **63.03s** | Best accuracy, slowest     |
| Spherical   | 1.717       | 3.19s      | Fastest, moderate accuracy |

### 🌀 Ellipsoidal Reconstruction

```
Iteration   1000: Error = 31.755505, Loss = 194.555573
Iteration  10000: Error = 0.318262,  Loss = 0.001087
Final Error: 0.318262
Time: 63.03s
```

### ⚪ Spherical Reconstruction

```
Iteration   1000: Error = 32.973167, Loss = 236.017319
Iteration  10000: Error = 1.717282,  Loss = 0.030457
Final Error: 1.717282
Time: 3.19s
```

---

## Discussion

This experiment shows that **manually implementing Adam** enables fast, stable convergence without PyTorch's built-in autograd and optimizer overhead. This design is more performant than using `torch.optim.Adam` (as in Experiment 10), especially in high-dimensional settings.

The **spherical case** is significantly faster due to cheaper distance/gradient computations. The **ellipsoidal case**, while slower, achieves substantially higher accuracy — demonstrating the potential benefit of leveraging full covariance structure when modeling uncertainty or manifold curvature.

This tradeoff between accuracy and runtime is especially relevant in latent-space reconstruction, manifold learning, or any setting where Mahalanobis metrics are used.

---

## Takeaways

- ✅ Manual Adam is **fast, memory-efficient**, and **modular**
- ✅ Spherical models are **fast and reasonable** for approximate reconstruction
- ✅ Ellipsoidal models are **more precise** but computationally heavier
- ✅ This architecture is ideal for scalable, interpretable optimization

---

## Next Steps

- Plot convergence curves for loss/error over time
- Add Gaussian noise to `y_i` to test robustness
- Try low-rank or diagonal covariance matrices
- Extend to **partial distance** inputs (subset of `y`)
- Implement other optimizers manually (e.g., RMSprop, AdaGrad)

---
