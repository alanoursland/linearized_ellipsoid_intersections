# Problem Statement

This project addresses the challenge of reconstructing a high-dimensional input vector \( x \) from the outputs of a neural network composed of Gaussian-like units. Each neuron computes a squared Mahalanobis distance:

\[
y_i = (x - \mu_i)^\top \Sigma_i^{-1}(x - \mu_i)
\]

Each output \( y_i \) geometrically defines an ellipsoidal shell (or contour) in input space. Thus, recovering the original input \( x \) involves solving for the intersection of multiple ellipsoidal constraints:

\[
\{ x \mid (x - \mu_i)^\top \Sigma_i^{-1}(x - \mu_i) = y_i \quad \forall i \}
\]

In the simpler spherical case, where each covariance \( \Sigma_i \) is proportional to the identity matrix, the intersection reduces to a set of hyperspheres. In such cases, previous work has shown that it is feasible to reconstruct \( x \) efficiently and robustly using geometric methods. Specifically, the intersection of spheres can be managed by tracking only their centroids and radii, followed by a reinflation step to handle collapsed dimensions, making reconstruction straightforward.

However, when generalizing from spherical to ellipsoidal Gaussians (full covariance matrices), the geometry becomes significantly more complicated:
- Ellipsoid intersections are generally not ellipsoids.
- The intersection may be non-convex or difficult to characterize analytically.
- Direct inversion or geometric reconstruction becomes computationally demanding or unstable.

This project introduces a novel geometric and probabilistic approximation:

> **The product of scaled Gaussians provides the best quadratic approximation (linearization) of the ellipsoid intersection problem.**

By scaling each Gaussian to normalize observed Mahalanobis distances, and then taking their product, we propose obtaining a closed-form, analytically tractable approximation of the intersection. This approach:
- Is analogous to a least-squares linearization for nonlinear constraints.
- Provides a closed-form solution, avoiding explicit nonlinear optimization.
- Preserves interpretability through geometric intuition.

The ultimate goal of this project is to rigorously develop, validate, and explore this approximation method, clarify its theoretical properties and limitations, and demonstrate its practical value in invertible neural networks, uncertainty quantification, and other high-dimensional reconstruction problems.

