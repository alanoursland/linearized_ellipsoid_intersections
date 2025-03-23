# Experiment 7: High-Dimensional Sphere In-Out Estimation

## Overview

This experiment evaluates a high-dimensional estimation method based on inside-out updates from randomly generated hyperspheres. The approach uses only local distance comparisons between a candidate estimate and the true point, guided by synthetic spherical constraints.

## Objective

To test whether a point `x ∈ ℝ^D` can be estimated purely from iteratively comparing its distances to random sphere centroids, without storing prior constraints or computing true intersections.

---

## Method

1. A target point `x_true ∈ ℝ^D` is randomly sampled.
2. An initial guess `x_est` is generated far from `x_true`.
3. For `num_iters` iterations:
   - A random centroid `μ ∈ ℝ^D` is sampled.
   - The true distance `d_true = ||x_true - μ||` is computed.
   - The estimate distance `d_est = ||x_est - μ||` is computed.
   - If `d_est < d_true`, move the estimate **away** from the centroid.
   - If `d_est > d_true`, move the estimate **toward** the centroid.
   - The step size is a fraction (learning rate) of the distance difference.

This simple geometric rule is evaluated in two forms:
- **Soft nudging** (`lr = 0.99`)
- **Exact projection** (`lr = 1.0`)

---

## Configuration

| Parameter      | Value          |
|----------------|----------------|
| Dimensions `D` | 784            |
| Iterations     | 10,000         |
| Initial error  | ~280–290       |
| Norm           | Euclidean `L2` |

---

## Results

### Learning Rate: `0.99` (Soft Step)

- Converges smoothly from ~280 to **0.061**
- Error drops consistently across all iterations
- More conservative updates, highly stable

### Learning Rate: `1.0` (Projection Step)

- Slightly faster early convergence
- Converges from ~290 to **0.085**
- Matches surface more aggressively
- Slightly less stable in late-stage convergence

---

## Observations

- Both strategies converge to sub-0.1 error in 784 dimensions using *only local surface information*.
- The system exhibits **robust convergence without memory**, relying only on one random sphere at a time.
- The method validates the intuition that a point can be constrained within an intersection of stochastic geometric surfaces, using only directional feedback.
- The learning rate effectively controls whether the system behaves more like a **gradient follower** or a **surface projector**.

---

## Future Work

- Add adaptive learning rate decay for smoother late-stage convergence.
- Explore ensemble averaging from multiple initializations.
- Introduce noise in distance estimates to simulate real-world uncertainty.
- Generalize to ellipsoids using Mahalanobis-based surface projection and local metrics.
- Analyze convergence in terms of curvature, coverage, and constraint density.

---

## Conclusion

This experiment demonstrates a highly efficient and scalable method for estimating a point in high-dimensional space using a stream of local spherical constraints. The inside-out approach achieves subunit accuracy in thousands of dimensions with no stored state and only simple vector arithmetic. It offers a strong foundation for constraint-based estimation systems — and can be naturally extended to anisotropic (ellipsoidal) surfaces.
