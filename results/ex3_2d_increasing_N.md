# Experiment 3: Increasing Number of Gaussians in 2D Reconstruction

## Objective
To investigate the relationship between the number of ellipsoidal constraints (Gaussian shells) and the accuracy of the reconstruction estimate \( \hat{x} \), as well as how well the fused covariance captures the actual reconstruction error.

## Setup
- A true point \( x \in \mathbb{R}^2 \) is randomly sampled.
- For each trial, \( N \in [3, 10] \) Gaussian shells are generated with random means and anisotropic covariances.
- Each Gaussian is scaled so that \( x \) lies on the unit Mahalanobis shell.
- The Gaussian product of the scaled constraints is used to reconstruct \( \hat{x} \) and compute the fused covariance.
- For each \( N \), 1000 trials are conducted to compute the average observed error and the average expected error (from the mean eigenvalue of the product covariance).

## Results
```
N = 3
  Avg Euclidean error ||x - x̂||: 1.722072
  Avg expected error (sqrt(mean eigenvalue)): 1.456048

N = 4
  Avg Euclidean error ||x - x̂||: 1.841031
  Avg expected error (sqrt(mean eigenvalue)): 1.416511

N = 5
  Avg Euclidean error ||x - x̂||: 1.906884
  Avg expected error (sqrt(mean eigenvalue)): 1.345490

N = 6
  Avg Euclidean error ||x - x̂||: 1.997917
  Avg expected error (sqrt(mean eigenvalue)): 1.337721

N = 7
  Avg Euclidean error ||x - x̂||: 2.118360
  Avg expected error (sqrt(mean eigenvalue)): 1.345012

N = 8
  Avg Euclidean error ||x - x̂||: 2.209989
  Avg expected error (sqrt(mean eigenvalue)): 1.331536

N = 9
  Avg Euclidean error ||x - x̂||: 2.196645
  Avg expected error (sqrt(mean eigenvalue)): 1.312979

N = 10
  Avg Euclidean error ||x - x̂||: 2.259772
  Avg expected error (sqrt(mean eigenvalue)): 1.296441
```

## Analysis
Contrary to expectations, increasing the number of Gaussian constraints \( N \) did not lead to improved accuracy. Instead:

- **Observed reconstruction error increases** with \( N \).
- **Expected error (from covariance eigenvalues) decreases** with \( N \).
- The **gap between observed and expected error widens** as \( N \) grows.

## Interpretation
The root cause of this discrepancy lies in the nature of the Gaussian product approximation:

> The Gaussian product is a linear approximation to the true (non-linear) intersection of ellipsoidal shells.

As the number of constraints increases:
- The true intersection region becomes smaller and more non-linear.
- The Gaussian product, constrained to be a single ellipsoid, becomes **more confident** (smaller covariance).
- However, this confidence is **misplaced**: the product does not converge to the true intersection.

Thus, the estimated error based on the product covariance becomes **overconfident**—it reports a tighter bound than is justified by the actual error in reconstructing \( x \).

## Conclusion
This experiment demonstrates a key limitation of using Gaussian products to approximate ellipsoidal intersection:

- As more constraints are added, the approximation becomes increasingly overconfident.
- The fused covariance underestimates the true uncertainty, especially in regions of nonlinear constraint geometry.

The Gaussian product becomes more certain but not more correct.

Future work should explore alternatives:
- Iterative refinement or geometric fusion of constraints
- Normalization of constraint geometry
- Nonlinear approximators for true intersection shape


## Results
```
N = 2
  Avg Euclidean error ||x - x̂||: 1.613686
  Avg expected error (sqrt(mean eigenvalue)): 1.578627

N = 3
  Avg Euclidean error ||x - x̂||: 1.709568
  Avg expected error (sqrt(mean eigenvalue)): 1.460536

N = 4
  Avg Euclidean error ||x - x̂||: 1.783997
  Avg expected error (sqrt(mean eigenvalue)): 1.386752

N = 5
  Avg Euclidean error ||x - x̂||: 1.858274
  Avg expected error (sqrt(mean eigenvalue)): 1.340768

N = 6
  Avg Euclidean error ||x - x̂||: 2.005261
  Avg expected error (sqrt(mean eigenvalue)): 1.340319

N = 7
  Avg Euclidean error ||x - x̂||: 2.077118
  Avg expected error (sqrt(mean eigenvalue)): 1.336583

N = 8
  Avg Euclidean error ||x - x̂||: 2.199324
  Avg expected error (sqrt(mean eigenvalue)): 1.327197

N = 9
  Avg Euclidean error ||x - x̂||: 2.191336
  Avg expected error (sqrt(mean eigenvalue)): 1.306696

N = 10
  Avg Euclidean error ||x - x̂||: 2.281215
  Avg expected error (sqrt(mean eigenvalue)): 1.321023
  ```