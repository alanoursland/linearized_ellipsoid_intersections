# Ellipsoid Intersection

## Mathematical Formulation

An ellipsoid in \(\mathbb{R}^d\) is defined by a quadratic form:

\[
(x - \mu)^\top \Sigma^{-1}(x - \mu) = 1,
\]

where:
- \( \mu \in \mathbb{R}^d \) is the center of the ellipsoid.
- \( \Sigma \in \mathbb{R}^{d \times d} \) is a positive definite covariance matrix defining shape and orientation.

When considering the intersection of \(k\) ellipsoids, the mathematical problem becomes solving a system of \(k\) quadratic equations:

\[
\begin{aligned}
(x - \mu_1)^\top \Sigma_1^{-1}(x - \mu_1) &= 1 \\
(x - \mu_2)^\top \Sigma_2^{-1}(x - \mu_2) &= 1 \\
&\vdots \\
(x - \mu_k)^\top \Sigma_k^{-1}(x - \mu_k) &= 1
\end{aligned}
\]

## Geometric Complexity

Unlike the intersection of hyperspheres (special ellipsoids with isotropic covariance), the intersection of general ellipsoids is significantly more complex:

1. **Non-ellipsoidal Intersection**:  
   Ellipsoids are quadratic forms, and their intersection represents the common solutions of multiple quadratic equations. The intersection of two or more ellipsoids generally does not result in another ellipsoid unless they share identical eigenvectors (axes) and differ only by scaling or translation.

2. **Non-convexity and Shape Complexity**:  
   The intersection set is generally non-convex. For two ellipsoids, the intersection typically forms a "lens-like" shape (elliptical or hyperbolic cross-section), or even more complicated shapes when more than two ellipsoids intersect. With three or more ellipsoids, the resulting intersection can form disconnected regions or intricate surfaces, increasing complexity significantly.

3. **Analytical Intractability**:  
   The algebraic solution to multiple quadratic equations quickly becomes difficult. While intersections can sometimes be parameterized for two ellipsoids, general analytic solutions for more than two ellipsoids rarely exist.

## Example: Two Ellipsoid Intersection

Consider two ellipsoids:
\[
(x - \mu_1)^\top \Sigma_1^{-1}(x - \mu_1) = 1 \quad\text{and}\quad
(x - \mu_2)^\top \Sigma_2^{-1}(x - \mu_2) = 1.
\]

Subtracting one equation from the other yields another quadratic equation:

\[
(x - \mu_1)^\top \Sigma_1^{-1}(x - \mu_1) - (x - \mu_2)^\top \Sigma_2^{-1}(x - \mu_2) = 0,
\]

representing the implicit equation of the boundary curve or surface where both ellipsoids intersect. Even in two or three dimensions, explicit analytic solutions require special structure (alignment, proportionality, or symmetry) to simplify.

## Computational Challenges

- **Numerical instability**: Solving the intersection of general ellipsoids numerically is often ill-conditioned, especially when ellipsoids become nearly aligned or very anisotropic.
- **High-dimensional complexity**: In high dimensions (as common in machine learning and neural networks), ellipsoid intersections quickly become computationally prohibitive.

## References

- Boyd, Stephen, and Lieven Vandenberghe. *Convex Optimization*. Cambridge University Press, 2004.
- Gander, W., Golub, G. H., & Strebel, R. (1994). "Least-squares fitting of circles and ellipses." *BIT Numerical Mathematics*, 34(4), 558–578.
- Pope, D. A. (2008). "The geometry of ellipsoid intersections." *Proceedings of the Royal Society A: Mathematical, Physical and Engineering Sciences*, 464(2093), 303–322.

