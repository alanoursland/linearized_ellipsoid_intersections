# Mahalanobis Geometry and Multivariate Gaussians

## Multivariate Gaussian Distribution

A multivariate Gaussian (normal) distribution in \(\mathbb{R}^d\) is given by:

\[
\mathcal{N}(x; \mu, \Sigma) = \frac{1}{(2\pi)^{d/2}|\Sigma|^{1/2}} \exp\left(-\frac{1}{2}(x - \mu)^\top \Sigma^{-1}(x - \mu)\right),
\]

where:
- \(\mu \in \mathbb{R}^d\) is the mean vector (center).
- \(\Sigma \in \mathbb{R}^{d \times d}\) is the positive-definite covariance matrix (determining shape and orientation).
- \(|\Sigma|\) denotes the determinant of \(\Sigma\).

## Mahalanobis Distance (MD)

Mahalanobis distance measures how far a point \(x\) is from the mean \(\mu\) of a Gaussian distribution, considering the covariance \(\Sigma\). It generalizes Euclidean distance by accounting for covariance structure:

\[
D_M(x, \mu; \Sigma) = \sqrt{(x - \mu)^\top \Sigma^{-1}(x - \mu)}.
\]

The squared Mahalanobis distance is:

\[
D_M^2(x, \mu; \Sigma) = (x - \mu)^\top \Sigma^{-1}(x - \mu).
\]

This scalar value represents how many standard deviations (adjusted for correlations and anisotropy) \(x\) is away from the Gaussian mean.

## Geometric Interpretation: Ellipsoids

Mahalanobis distance defines **ellipsoidal shells** around the Gaussian mean. Points with the same Mahalanobis distance form ellipsoidal contours:

\[
(x - \mu)^\top \Sigma^{-1}(x - \mu) = c,
\]

where \(c\) determines the radius of the ellipsoid in Mahalanobis units.

- For \(c = 1\), the ellipsoid represents the "unit-variance ellipsoid," often called the "1-sigma contour."
- Increasing \(c\) expands these contours outward, forming concentric ellipsoids.

The principal axes of these ellipsoids are given by the eigenvectors of \(\Sigma\), with lengths proportional to the square roots of eigenvalues of \(\Sigma\).

## Whitening Transformation

Whitening is a linear transformation of a Gaussian-distributed random vector \(x\) to remove covariance:

- Goal: Transform \(x\) to a new vector \(z\), which has zero mean and identity covariance \(\mathbb{I}\).
- Definition:
  \[
  z = \Sigma^{-1/2}(x - \mu),
  \]
  where \(\Sigma^{-1/2}\) denotes the symmetric inverse square-root of the covariance matrix.

After whitening:
- \(\mathbb{E}[z] = 0\)
- \(\mathrm{Cov}(z) = \mathbb{I}\)

Whitening transforms ellipsoidal contours in \(x\)-space into spherical contours in \(z\)-space, simplifying geometry significantly.

## Unit Variance Ellipsoids and MD Ellipsoids

- **Unit Variance Ellipsoid**: defined by Mahalanobis distance \(D_M = 1\). Represents the boundary of points exactly 1 Mahalanobis unit from the mean:
  \[
  (x - \mu)^\top \Sigma^{-1}(x - \mu) = 1
  \]

- **MD Ellipsoids**: general ellipsoids defined by arbitrary Mahalanobis distance \(D_M = \sqrt{c}\):
  \[
  (x - \mu)^\top \Sigma^{-1}(x - \mu) = c
  \]

These ellipsoids explicitly encode shape, orientation, and scale defined by \(\Sigma\).

## Relationship to Chi-Square Distribution

For a \(d\)-dimensional Gaussian, squared Mahalanobis distance from a randomly sampled point follows a chi-square distribution with \(d\) degrees of freedom:

\[
D_M^2(x, \mu; \Sigma) \sim \chi^2(d)
\]

This relationship is useful in statistical hypothesis testing and anomaly detection.

## Practical Importance

- Mahalanobis distance is widely used for outlier detection, clustering, and pattern recognition.
- Whitening transformations are central to PCA, ICA, and signal processing.
- Ellipsoidal geometries derived from Mahalanobis distance underpin probabilistic inference, uncertainty quantification, and optimization in machine learning.

## References

- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer.
- Duda, R. O., Hart, P. E., & Stork, D. G. (2000). *Pattern Classification*. Wiley.
- De Maesschalck, R., Jouan-Rimbaud, D., & Massart, D. L. (2000). "The Mahalanobis distance." *Chemometrics and Intelligent Laboratory Systems*, 50(1), 1–18.
- Murphy, K. P. (2012). *Machine Learning: A Probabilistic Perspective*. MIT Press.

