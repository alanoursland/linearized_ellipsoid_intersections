# Failure of Gaussian Product as Ellipsoid Intersection

## Motivation
This document outlines the key insight emerging from our ellipsoidal constraint fusion experiments: the use of Gaussian products as linear approximations to ellipsoid intersections becomes increasingly inaccurate as the number of constraints grows. This failure is not due to noise, finite sampling, or randomness, but is fundamental to the nature of the approximation itself.

The original hypothesis was that the **product of Gaussian distributions** could serve as a useful **linearized approximation to the intersection of ellipsoids**. This idea is attractive because Gaussian products are analytically tractable, and ellipsoid intersections are not.

The Gaussian product is attractive because it is mathematically convenient and analytically tractable, especially in high-dimensional inference problems. However, it does not correctly model the geometry of constraint surfaces like ellipsoids or hyperspheres.

## What Was Tried
To explore this, we compared two approaches:

1. **Geometric Intersection of Spheres** (as a simplification of ellipsoids):
   - Intersect spheres iteratively to refine a region containing the true point.
   - The radius of the intersection sphere serves as a direct expected error bound.

2. **Gaussian Products with Isotropic Covariance (modeled from sphere radii):**
   - Each sphere was treated as a Gaussian with covariance Σ = r ⋅ I.
   - Fused using the product rule for Gaussians.
   - The resulting mean and covariance estimate a belief over the true point.

## Observations

Across experiments using \( N = 2 \) through \( N = 10 \) randomly generated anisotropic Gaussians in 2D, and additional high-dimensional spherical experiments:

- The **actual reconstruction error increases** steadily with \( N \).
- The **expected error**, estimated from the square root of the mean eigenvalue of the fused covariance, **decreases** with \( N \).
- The **gap between actual and expected error widens** monotonically.
- Even with isotropic (spherical) constraints, the Gaussian product stagnates far from the true solution, while geometric intersection converges.

This demonstrates a consistent and systematic pattern of **overconfidence** in the Gaussian product approximation.

### Intersection Method
- Converged slowly but reliably.
- Expected error (intersection radius) matched observed error (true Euclidean distance).
- Given enough constraints, it refined the estimate down to near zero error.

### Product Method
- Converged quickly in terms of **variance/confidence**.
- Observed error stagnated far above zero.
- Final estimate was consistently off, despite tiny predicted uncertainty.
- Adding more constraints failed to correct the trajectory once confidence grew.

## Core Insight
The Gaussian product yields a single ellipsoid: a linear, unimodal, symmetric approximation. The true intersection of \( N \) ellipsoidal shells, however, is a **nonlinear, irregular region** that becomes more complex with each additional constraint.

> The Gaussian product does not converge to the true ellipsoid intersection. It converges to a simplified linearized approximation whose confidence increases while accuracy degrades.

As more shells are added, the product distribution becomes more "certain" in the sense of smaller covariance, but the estimated center drifts away from the true intersection, leading to increasing reconstruction error.

## Why It Fails

### 1. Gaussian Product Models Agreement, Not Constraint
The product gives a **mode** of overlapping probability densities, not the **boundary** of intersecting constraint surfaces. It doesn't preserve the feasible region.

### 2. Ellipsoid Intersections Are Non-Elliptical
Even in 2D, the intersection of ellipses isn't another ellipse. The Gaussian approximation cannot capture the true shape or size of the intersecting region.

### 3. Overconfidence
As more Gaussians are fused, the variance shrinks. But because the inputs represent constraints (not distributions), the shrinking variance is unjustified. The system becomes **overconfident and wrong**.

### 4. High-Dimensional Flatness
In high dimensions, most constraints are nearly flat at the surface. Gaussian fusion interprets them as noisy and soft, rather than hard geometric boundaries. This results in negligible updates despite informative observations.

## Conclusion
The use of Gaussian products to approximate ellipsoid intersections is inherently limited:

- It can work well with a small number of constraints.
- It fails to capture the geometry of true intersections as complexity increases.
- It produces increasingly overconfident and inaccurate estimates.

True intersection techniques are slower but reliable. If Gaussian fusion is to be used, it must be modified to account for shell-like constraints, e.g., via projection, covariance inflation, or hybrid inference techniques.

This insight rules out the Gaussian product as a scalable solution for ellipsoid intersection in its basic form. Future work must incorporate nonlinear corrections, iterative refinement, or alternative representations that respect the true structure of the intersection geometry.
