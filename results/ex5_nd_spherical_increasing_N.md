# Experiment 5: High-Dimensional Spherical Intersection with Increasing N

## Objective
To evaluate how increasing the number of high-dimensional spheres intersected affects the estimation of a hidden point \( x \) in \( \mathbb{R}^{100} \). Specifically, we examine whether increasing the number of constraints reduces the estimation error or tightens the intersection.

## Setup
- **Dimensions (D):** 100
- **Number of Spheres:** \( N = 2 \) to \( 30 \)
- **Trials per N:** 1000

### Procedure
For each trial:
1. A random target point \( x \in \mathbb{R}^{100} \) is sampled.
2. \( N \) random sphere centers \( \mu_i \sim \mathcal{N}(i \cdot 2, I) \) are generated.
3. Radii \( r_i = \|x - \mu_i\| \) are computed to ensure each sphere contains \( x \).
4. The spheres are intersected sequentially using geometric sphere intersection logic.
5. After all intersections, the final estimate \( \hat{x} \) is the center of the final intersection.
6. Two metrics are recorded:
   - **Observed error:** \( \|x - \hat{x}\| \)
   - **Expected error:** Radius of the intersection sphere

The final values reported are the averages over all trials for each \( N \).

## Results Summary
- The observed and expected errors start around **13.4** for \( N = 2 \)
- They decrease slightly up to around \( N = 5 \), then plateau
- Across \( N = 5 \) to \( N = 30 \), error remains approximately **13.3** with only minor fluctuations
- The expected error tracks the observed error nearly perfectly

## Interpretation
This experiment highlights a key property of high-dimensional inference using spherical intersections:

### 1. **Early Gains, Then Saturation**
The first few intersections slightly reduce error by adding constraints. However, after a small number of spheres, the benefit plateaus.

### 2. **Flatness of Constraints in High Dimensions**
Most spheres have large radii (\( \sim \sqrt{D} \)), and their surfaces near \( x \) are nearly flat. As a result, their intersection with existing estimates doesn't significantly constrain \( x \). Each new sphere essentially grazes the outer region of the current estimate, shaving off minimal volume.

### 3. **Random Features Are Not Informative**
Randomly generated spheres are unlikely to pass close to \( x \), so they don't contribute high-curvature (tight) constraints. This explains the lack of error reduction with higher \( N \).

---

## Conclusion
In high-dimensional space, increasing the number of intersected spheres does not significantly improve estimation accuracy unless some spheres are centered near the target point. Most random constraints are too flat and weakly informative. The system rapidly converges to a floor of estimation error set by the geometry of the initial constraints.

This reinforces the importance of curvature and constraint proximity when designing intersection-based inference systems in high dimensions.

## Results
```
Intersecting 30 spheres across 100 dimensions with 1000 trials
N = 2
  Avg Euclidean error ||x - x̂||: 13.408480
  Avg expected error (intersection radius): 13.408480

N = 3
  Avg Euclidean error ||x - x̂||: 13.385707
  Avg expected error (intersection radius): 13.385707

N = 4
  Avg Euclidean error ||x - x̂||: 13.358535
  Avg expected error (intersection radius): 13.358535

N = 5
  Avg Euclidean error ||x - x̂||: 13.317287
  Avg expected error (intersection radius): 13.317287

N = 6
  Avg Euclidean error ||x - x̂||: 13.356903
  Avg expected error (intersection radius): 13.356904

N = 7
  Avg Euclidean error ||x - x̂||: 13.326709
  Avg expected error (intersection radius): 13.326709

N = 8
  Avg Euclidean error ||x - x̂||: 13.320238
  Avg expected error (intersection radius): 13.320239

N = 9
  Avg Euclidean error ||x - x̂||: 13.344339
  Avg expected error (intersection radius): 13.344340

N = 10
  Avg Euclidean error ||x - x̂||: 13.279608
  Avg expected error (intersection radius): 13.279609

N = 11
  Avg Euclidean error ||x - x̂||: 13.351929
  Avg expected error (intersection radius): 13.351930

N = 12
  Avg Euclidean error ||x - x̂||: 13.262198
  Avg expected error (intersection radius): 13.262199

N = 13
  Avg Euclidean error ||x - x̂||: 13.373767
  Avg expected error (intersection radius): 13.373768

N = 14
  Avg Euclidean error ||x - x̂||: 13.353693
  Avg expected error (intersection radius): 13.353694

N = 15
  Avg Euclidean error ||x - x̂||: 13.370083
  Avg expected error (intersection radius): 13.370084

N = 16
  Avg Euclidean error ||x - x̂||: 13.348650
  Avg expected error (intersection radius): 13.348651

N = 17
  Avg Euclidean error ||x - x̂||: 13.315549
  Avg expected error (intersection radius): 13.315550

N = 18
  Avg Euclidean error ||x - x̂||: 13.335577
  Avg expected error (intersection radius): 13.335578

N = 19
  Avg Euclidean error ||x - x̂||: 13.321033
  Avg expected error (intersection radius): 13.321034

N = 20
  Avg Euclidean error ||x - x̂||: 13.299737
  Avg expected error (intersection radius): 13.299738

N = 21
  Avg Euclidean error ||x - x̂||: 13.270592
  Avg expected error (intersection radius): 13.270594

N = 22
  Avg Euclidean error ||x - x̂||: 13.311100
  Avg expected error (intersection radius): 13.311101

N = 23
  Avg Euclidean error ||x - x̂||: 13.319957
  Avg expected error (intersection radius): 13.319959

N = 24
  Avg Euclidean error ||x - x̂||: 13.320691
  Avg expected error (intersection radius): 13.320692

N = 25
  Avg Euclidean error ||x - x̂||: 13.301144
  Avg expected error (intersection radius): 13.301146

N = 26
  Avg Euclidean error ||x - x̂||: 13.303695
  Avg expected error (intersection radius): 13.303696

N = 27
  Avg Euclidean error ||x - x̂||: 13.247342
  Avg expected error (intersection radius): 13.247344

N = 28
  Avg Euclidean error ||x - x̂||: 13.265546
  Avg expected error (intersection radius): 13.265548

N = 29
  Avg Euclidean error ||x - x̂||: 13.343448
  Avg expected error (intersection radius): 13.343450

N = 30
  Avg Euclidean error ||x - x̂||: 13.337976
  Avg expected error (intersection radius): 13.337978
```