# Gaussian Product as a Linearized Ellipsoid Intersection

## Introduction

Intersecting multiple ellipsoids, each defined by quadratic Mahalanobis distance constraints, is inherently nonlinear, complex, and computationally challenging. A direct algebraic solution generally does not exist due to the intersection set's complicated geometry. To overcome this, we propose using Gaussian products to create a linearized approximation of the intersection.

## Nonlinear Nature of Ellipsoid Intersection

Each ellipsoid is described by the quadratic form:

\[
(x - \mu_i)^\top \Sigma_i^{-1}(x - \mu_i) = y_i,
\]

The intersection set, formed by simultaneously satisfying multiple such equations, is generally:
- **Nonlinear**: Defined by multiple simultaneous quadratic equations.
- **Non-convex**: Intersection shapes can be complex, disconnected, or irregular.
- **Intractable analytically**: Closed-form solutions rarely exist beyond trivial symmetric cases.

## Linearizing the Intersection

We propose approximating this complex intersection with a single ellipsoid that "best" represents the joint constraint set. This approximating ellipsoid is formed by the product of appropriately scaled Gaussian distributions.

### Gaussian Product Method

Each ellipsoid can be represented probabilistically as an unnormalized Gaussian:

\[
f_i(x) \propto \exp\left[-\frac{1}{2y_i}(x - \mu_i)^\top \Sigma_i^{-1}(x - \mu_i)\right].
\]

Taking the product across all ellipsoids yields:

\[
f(x) = \prod_i f_i(x) \propto \exp\left[-\frac{1}{2}\sum_i \frac{1}{y_i}(x - \mu_i)^\top \Sigma_i^{-1}(x - \mu_i)\right].
\]

This product simplifies to a single Gaussian with parameters:

- Precision matrix (inverse covariance):

\[
\Sigma^{-1} = \sum_i \frac{1}{y_i}\Sigma_i^{-1}
\]

- Mean (center):

\[
\mu = \Sigma\sum_i \frac{1}{y_i}\Sigma_i^{-1}\mu_i
\]

This defines an explicit linear (single quadratic form) approximation to the nonlinear ellipsoid intersection.

## Scaling Covariances for Normalization

A crucial step is scaling each covariance matrix \(\Sigma_i\) to ensure the observed Mahalanobis distance \(y_i\) corresponds exactly to unit variance:

\[
\tilde{\Sigma}_i = y_i \Sigma_i,
\quad\text{so that}\quad
(x - \mu_i)^\top \tilde{\Sigma}_i^{-1}(x - \mu_i) = 1.
\]

The Gaussian product of these scaled ellipsoids then becomes:

\[
\Sigma^{-1} = \sum_i (y_i\Sigma_i)^{-1}, \quad
\mu = \Sigma\sum_i (y_i\Sigma_i)^{-1}\mu_i.
\]

## Upper Bound Property

Importantly, this Gaussian product approximation acts as an upper bound (outer approximation) to the true intersection set. Specifically, for any point \(x^*\) that exactly satisfies all original ellipsoid constraints:

\[
(x^* - \mu)^\top \Sigma^{-1}(x^* - \mu) \leq 1.
\]

Thus, the resulting ellipsoid defined by the Gaussian product generally "contains" the true intersection set, providing a safe and conservative approximation.

## Error Analysis and Bounds

The Gaussian product approach provides a practical, efficient approximation, but inherently introduces approximation error since the exact intersection set is nonlinear and not ellipsoidal.

Potential strategies for quantifying this error include:

- Comparing volumes of intersection sets numerically.
- Computing distances between Gaussian product means and centroids of true intersections.
- Eigenvalue-based analysis to measure directional approximation error.

Numerical simulations and empirical analyses are recommended to characterize these errors precisely.

## Conclusion and Future Directions

The Gaussian product method provides a principled, analytically tractable linear approximation to the complex, nonlinear problem of ellipsoid intersection. It leverages probabilistic reasoning, geometric intuition, and covariance scaling to deliver practical solutions.

Future work involves rigorous numerical experimentation, bounding approximation errors, and exploring scenarios and conditions that minimize approximation gaps.

This method has significant potential for applications in probabilistic inference, sensor fusion, invertible neural networks, and uncertainty-aware modeling.

---

**References:**

- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer.
- Murphy, K. P. (2012). *Machine Learning: A Probabilistic Perspective*. MIT Press.
- Bar-Shalom, Y., Li, X. R., & Kirubarajan, T. (2001). *Estimation with Applications to Tracking and Navigation*. Wiley-Interscience.

