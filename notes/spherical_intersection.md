# Spherical Intersection

## Problem Setup

We consider the problem of finding a common point lying exactly on the surfaces of multiple intersecting hyperspheres in \(\mathbb{R}^d\). A hypersphere is defined as:

\[
\|x - \mu\|^2 = r^2,
\]

where:
- \(\mu \in \mathbb{R}^d\) is the center of the sphere.
- \(r \geq 0\) is its radius.

The intersection problem thus involves solving the system:

\[
\|x - \mu_i\|^2 = r_i^2 \quad \forall i \in \{1, \dots, k\}
\]

## Geometry of Intersection

### Dimension Reduction
Intersecting two spheres in \(\mathbb{R}^d\) results in a sphere (or a spherical shell) of dimension \(d-1\). Specifically, the intersection of two spheres defines a hyperplane along the vector connecting their two centers \(\mu_1\) and \(\mu_2\). This vector can be described as:

\[
v = \mu_2 - \mu_1.
\]

Thus, intersection between two spheres inherently collapses one spatial dimension along the vector \(v\). Each intersection reduces dimensionality by exactly one.

### Increasing Complexity with Multiple Intersections
Intersecting multiple spheres sequentially creates intersections of intersections, each time further flattening dimensions along new collapse vectors. These vectors represent directions between origins of intersected spheres, complicating the geometry and making algebraic solutions progressively challenging.

## Mathematical Formulation of Intersection

Consider two spheres defined by:

\[
\|x - \mu_1\|^2 = r_1^2, \quad \|x - \mu_2\|^2 = r_2^2
\]

Subtracting equations, we obtain:

\[
\|x - \mu_1\|^2 - \|x - \mu_2\|^2 = r_1^2 - r_2^2
\]

Expanding and simplifying, we find a hyperplane equation defining the intersection:

\[
2(\mu_2 - \mu_1)^\top x = r_1^2 - r_2^2 + \|\mu_2\|^2 - \|\mu_1\|^2
\]

Intersecting this hyperplane with either sphere yields a hypersphere in \(d-1\) dimensions.

## Intersection Origin and Error

The intersection hypersphere has an origin \(\hat{\mu}\), calculated as the projection of one sphere center onto the intersection hyperplane. Its radius \(\hat{r}\) defines uncertainty or error:

- The origin \(\hat{\mu}\) is the expected value (EV) of the intersection solution.
- The intersection radius \(\hat{r}\) quantifies the remaining uncertainty. Smaller \(\hat{r}\) implies higher certainty.

When the radius of intersection approaches zero, the intersection origin becomes an exact solution. Notably, if two spheres are tangent (touching at exactly one point), their intersection is a hypersphere with radius exactly zero, and the intersection origin precisely matches the true solution point.

## Radius Monotonicity

An important property is that intersection radii are strictly smaller than the parent spheres' radii:

\[
\hat{r} \leq \min(r_1, r_2)
\]

Equality occurs only in special limiting cases (e.g., fully overlapping spheres). This monotonic radius reduction is crucial for iterative solutions.

## Dimension Reinflation Strategy

Due to repeated dimension collapses, intersections quickly become numerically challenging. To manage complexity:

- **Discard collapsed dimensions**: Remove dimensions corresponding to collapse vectors after intersections.
- **Reinflate intersections**: After each intersection, treat the intersection sphere in its reduced-dimensionality form as a full-dimensional sphere again (by ignoring dimensions collapsed).
- **Iterative refinement**: Continue intersecting spheres iteratively, each time with fewer dimensions. As long as the intersection radius continues to shrink, dimensional reinflation remains stable.

This strategy iteratively narrows the solution space, converging until the radius of intersection is sufficiently small.

## Spherical Gaussians Interpretation

This intersection approach can be viewed probabilistically through spherical Gaussian distributions:
- Centers \(\mu_i\) are Gaussian means.
- Radii \(r_i\) represent standard deviations or "uncertainty radii."
- Intersection becomes a fusion of information (akin to precision addition in Gaussian product), progressively reducing uncertainty.

## Summary

The spherical intersection method:
- Sequentially intersects hyperspheres, reducing dimensionality at each step.
- Uses intersection radius as an uncertainty measure, converging as radii shrink.
- Simplifies geometric complexity by dimension reinflation.

This forms a clear geometric and probabilistic foundation for generalizing to ellipsoidal (full Gaussian covariance) intersections.