# Experiment 6: Gaussian Product vs Spherical Intersection in High Dimensions

## Objective
To compare two different approaches for estimating a hidden point \( x \in \mathbb{R}^{784} \) using constraints from randomly generated spheres:

- **Spherical Intersection:** Iteratively intersecting geometric spheres.
- **Gaussian Product:** Interpreting each sphere as an isotropic Gaussian with covariance \( \Sigma = r \cdot I \), and computing the product distribution.

## Setup
- **Dimensions (D):** 784
- **Trials:** Single long trajectory (no averaging)
- **Spheres:** 128

### Procedure
Each sphere is defined by a center \( \mu_i \) and a radius \( r_i = \|x - \mu_i\| \), where \( x \) is a fixed random target point.

#### For Spherical Intersection:
Each new sphere is geometrically intersected with the current estimate, producing a new center and reduced radius.

#### For Gaussian Product:
Each new constraint is treated as a Gaussian:
- \( \mu_i \) is the mean.
- \( \Sigma_i = r_i \cdot I \) is the covariance.

The Kalman-style update computes the product Gaussian:
\[
\Sigma_p = \left(\Sigma_1^{-1} + \dots + \Sigma_n^{-1}\right)^{-1}, \quad \mu_p = \Sigma_p \left(\sum_i \Sigma_i^{-1} \mu_i\right)
\]

## Results Summary (Gaussian Product)
- **Initial error:** ~140 (matching initial radius)
- **Error drops quickly at first** (after 1–3 constraints), then slows significantly.
- **Expected error** (from the mean eigenvalue of \( \Sigma_p \)) drops to ~0.99 and stays there.
- **Observed error** remains **high** — converging very slowly toward \( x \), reaching ~47 after 128 constraints.
- Even after **1280 constraints**, the observed error is still \( \sim 29.1 \), while expected error remains ~0.993.

## Interpretation
### 1. **Overconfidence from Gaussian Product**
The Kalman-style fusion becomes increasingly overconfident. Once variances shrink, new Gaussians have negligible influence on the mean, even when the mean is far from correct.

### 2. **Why Spherical Intersection Performed Better Earlier**
Geometric intersection continued to reduce the error because it operates on actual containment logic — not belief propagation. Each intersection clips space based on geometry, not just likelihood.

### 3. **Soft vs Hard Constraints**
The Gaussian product is a soft fusion method. It is useful when distributions are well-aligned. But when modeling hard constraints ("point lies on shell"), soft fusion can mislead — suggesting a much tighter bound than actually exists.

### 4. **High-Dimensional Flattening**
In 784D space, almost all spheres are nearly flat at the point of contact. That flattens their contribution to the update, and makes the fusion insensitive to further changes.

## Conclusion
Treating spheres as Gaussians and applying product fusion leads to a **severely overconfident** and slow-converging estimate. While it trends in the right direction, it is clearly inferior to geometric intersection in this context.

To use Gaussian products effectively here, one must correct for the overconfidence — perhaps by inflating covariances or adjusting the fusion weights based on curvature or distance.

This experiment underscores the need to align your inference method with the nature of the constraint: **hard containment needs geometry; soft fusion needs careful calibration.**

