# Experiment 10: High-Dimensional Ellipsoid Intersection via Gradient Descent

## Objective

This experiment explores the use of full-batch gradient descent to reconstruct a high-dimensional point `x_true` from its distances to a set of ellipsoids, using **Mahalanobis distance** as the constraint function. The goal is to evaluate accuracy, convergence, and computational cost of this approach using standard deep learning tooling (`torch.nn.Module`, `torch.optim.Adam`, autograd).

We compare this to prior work in Experiment 8, which used a direct, hand-coded update rule without autograd for spherical constraints.

---

## Problem Formulation

Given:
- `x_true ∈ ℝ^D` is a hidden vector
- A set of `k` ellipsoids, each defined by:
  - Mean: `μ_i ∈ ℝ^D`
  - Covariance: `Σ_i ∈ ℝ^{D×D}`, positive definite
- The Mahalanobis distance from `x_true` to each ellipsoid is measured as:

\[
y_i = \sqrt{(x - \mu_i)^T \Sigma_i^{-1} (x - \mu_i)}
\]

We aim to reconstruct `x_true` by minimizing the loss:

\[
\mathcal{L}(x) = \frac{1}{2} \sum_{i=1}^k \left( \|x - \mu_i\|_{\Sigma_i^{-1}} - y_i \right)^2
\]

---

## Implementation Details

- Framework: PyTorch (autograd + `torch.optim`)
- Loss: Custom `MahalanobisLoss` class (vectorized, batched)
- Optimizer: Adam
- Parameter: `x_est` as a `torch.nn.Parameter`
- No batching or sampling — full-batch gradient descent
- Hardware: Single GPU (CUDA)
- Dataset:
  - `D = 784` (dimensionality)
  - `k = 1024` ellipsoids (overdetermined)

### Hyperparameters

| Parameter        | Value       |
|------------------|-------------|
| Learning Rate    | `1.0 / k`   |
| Iterations       | `10,000`    |
| Optimizer        | Adam        |

---

## Results

### Reconstruction Accuracy

| Metric           | Value       |
|------------------|-------------|
| Initial Error    | 39.95       |
| Final Error      | **0.23** ✅ |
| Final Loss       | 0.00078     |
| Runtime (10k iters) | **64.29s** ⏱️ |

The reconstruction error decreased dramatically, achieving sub-unit accuracy after 10,000 steps. The optimizer converged to a point lying extremely close to `x_true`, and the loss suggests all Mahalanobis constraints are being satisfied.

---

## Comparison to Previous Methods

We compared this gradient-based approach to two prior reconstruction strategies:

| Method           | Final Error | Runtime  | Autograd | Geometry      |
|------------------|-------------|----------|----------|---------------|
| Direct In/Out Loop (Exp 8) | 0.60        | **1.75s** ✅ | ❌        | Spherical     |
| Spherical + Adam           | 0.64        | 8.06s     | ✅        | Spherical     |
| **Ellipsoidal + Adam**     | **0.23** ✅ | 64.29s    | ✅        | **Ellipsoidal** ✅ |

Despite being slower, the ellipsoidal method was **more accurate** by a large margin, reducing error by ~3× and loss by nearly an order of magnitude compared to the spherical case.

---

## Observations

- Autograd introduces a significant **performance cost** compared to direct updates (35× slower than the inout loop).
- However, it enables a clean, modular training loop compatible with any PyTorch optimizer or model.
- The **expressiveness of ellipsoids** (directional, anisotropic constraints) enables superior reconstruction accuracy, particularly when `k > D`.

---

## Takeaways

- This experiment demonstrates that **gradient-based reconstruction using Mahalanobis constraints** is feasible, accurate, and stable with standard optimizers.
- Ellipsoids offer significantly improved constraint precision over spheres — but at **substantial computational cost**.
- The performance bottleneck suggests a hybrid future direction: implementing fast, hand-coded gradients or custom autograd functions.

---

## Future Work

- Profile and optimize autograd with `torch.compile()` or custom `torch.autograd.Function`
- Implement hybrid approach: manual gradients + PyTorch optimizer
- Explore mini-batching, sparse ellipsoids, and shared covariance structures
- Add noise to `y` and test robustness
- Compare recovery performance across `k < D`, `k = D`, `k > D`
