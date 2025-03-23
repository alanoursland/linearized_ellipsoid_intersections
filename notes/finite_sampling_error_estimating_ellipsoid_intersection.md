# Finite Sampling Error in Estimating Ellipsoid Intersections

## Introduction

Estimating a hidden point \( x \in \mathbb{R}^d \) by intersecting a finite set of ellipsoidal constraints (scaled Gaussians) introduces systematic biases. Specifically, with a limited number of constraints, the covariance matrix resulting from their product often underestimates the true reconstruction uncertainty. This phenomenon parallels finite sampling biases in statistics, such as underestimating entropy with sparse data.

## Ellipsoid Intersection as Inverse Estimation

Each Gaussian constraint is represented as an ellipsoidal shell defined by:

\[
(x - \mu_i)^T \Sigma_i^{-1}(x - \mu_i) = y_i
\]

Scaling each Gaussian such that the point \( x \) lies exactly on its unit Mahalanobis shell creates constraints with the property:

\[
(x - \mu_i)^T (y_i\Sigma_i)^{-1}(x - \mu_i) = 1
\]

The intersection of these shells is approximated by a Gaussian product, where the covariance of the resulting Gaussian approximates the posterior uncertainty of \( x \).

## Finite Sampling Error Intuition

With a limited number (\(N\)) of Gaussian shells, certain directions in space remain under-constrained. Consequently, the covariance from their product does not adequately reflect the uncertainty along these directions. This underestimation is analogous to the finite-sample biases observed in entropy estimation and Fisher information accumulation.

## Quantifying Underestimation

Empirically, we observe:

\[
\mathbb{E}[||x - \hat{x}||] > \sqrt{\text{mean eigenvalue}}
\]

This discrepancy arises because each Gaussian constraint only partially informs the reconstruction. Areas between or beyond the constraints remain insufficiently covered, introducing hidden uncertainties that aren't reflected in the estimated covariance.

This underestimation is exacerbated by:
- Fewer Gaussians
- Poor spatial or directional coverage
- High anisotropy in the covariance matrices

## Theoretical Framing

Ideally, the covariance of the intersection estimate scales inversely with accumulated precision:

\[
\Sigma_{\text{posterior}} \propto \left(\sum_{i=1}^N \Sigma_i^{-1}\right)^{-1}
\]

However, this relationship assumes sufficient coverage and full rank constraints. With small \(N\), the computed covariance typically underestimates the true uncertainty. This resembles the Miller-Madow correction used in finite-sample entropy estimation, where a correction term is introduced to address bias.

## Possible Corrections

- **Empirical Correction**: Estimate the expected bias through simulation and adjust accordingly:

\[
\epsilon = \mathbb{E}[||x - \hat{x}||] - \sqrt{\bar{\lambda}}
\]

- **Scaling Factor**: Introduce a multiplicative factor to inflate covariance estimates based on the number and geometry of constraints.

- **Bootstrap or Monte Carlo Approaches**: Empirically estimate the uncertainty by resampling constraints and recomputing intersections multiple times.

## Experimental Validation

To validate finite sampling effects:
- Fix a known point \( x \).
- Vary the number of Gaussian constraints \( N \).
- Measure and compare actual reconstruction errors to predicted errors (via covariance eigenvalues).
- Observe how the discrepancy between observed and predicted errors decreases as \( N \) increases.

This experiment should demonstrate convergence, showing that increased constraint coverage reduces the error gap.

## Implications for Practice

When employing Gaussian product intersections for inverse estimation, practitioners should:
- Recognize covariance as a lower bound on uncertainty.
- Consider reporting an adjusted uncertainty estimate or clearly state the finite-sampling limitation.
- Aim to incorporate more independent constraints to minimize finite sampling errors.

## Conclusion

Finite sampling inherently leads to systematic underestimation of uncertainty in ellipsoid intersection problems. Understanding this limitation, quantifying its impact, and applying suitable corrections significantly improve the reliability and interpretability of reconstruction methods relying on Gaussian shell intersections.