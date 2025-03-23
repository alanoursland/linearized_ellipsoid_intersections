# Comparison of Observed Error to Mean Eigenvalue Estimate

## Objective
To evaluate how well the mean eigenvalue of the product Gaussian covariance matrix predicts the actual reconstruction error across multiple trials.

## Setup
- In each of 100 trials:
  - A random point \( x \in \mathbb{R}^2 \) is sampled.
  - Three anisotropic Gaussian distributions are defined with random means and full-rank covariances.
  - Mahalanobis distances \( y_i \) are computed from \( x \) to each Gaussian.
  - Each Gaussian is scaled so that \( x \) lies on the unit Mahalanobis shell (\( y_i = 1 \)).
  - The scaled Gaussians are fused via Gaussian product.
  - The reconstruction \( \hat{x} \) and product covariance \( \Sigma \) are computed.

- For each trial:
  - The Euclidean reconstruction error \( \|x - \hat{x}\| \) is recorded.
  - The square root of the mean eigenvalue of \( \Sigma \) is used as an estimate of expected reconstruction error.

## Results Summary
- **Average Euclidean error** over 100 runs: **1.5479**
- **Average sqrt(mean eigenvalue)**: **1.3930**

## Interpretation
- The expected error, derived from the mean eigenvalue of the fused covariance, tracks closely with the true reconstruction error.
- The estimate is slightly optimistic (lower than the true error) but provides a strong approximation on average.
- This confirms that the **mean eigenvalue of the intersection covariance is a useful proxy** for the uncertainty in recovering \( x \).

## Conclusion
The average square root of the mean eigenvalue of the Gaussian product covariance provides a reliable expected error estimate in this setup. It supports the idea that the linearized Gaussian product approximation not only gives a good reconstruction \( \hat{x} \), but also produces meaningful uncertainty information that correlates with real geometric reconstruction error.

This reinforces the use of eigenvalue-based diagnostics as part of a broader theory for ellipsoidal shell intersection and inversion.

## Results
```
Average Euclidean error over 100 runs: 1.547927
Average sqrt(mean eigenvalue) (expected error): 1.392964
```