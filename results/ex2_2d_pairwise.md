# Experiment 2: 2D Pairwise Gaussian Fusion

## Objective
To evaluate whether performing pairwise intersections of Gaussian shells (A·B, B·C, A·C), followed by a second fusion of the resulting intermediate shells, leads to improved or tighter reconstruction of the true point \( x \) compared to a direct 3-way Gaussian product (A·B·C).

## Setup
- A random point \( x \in \mathbb{R}^2 \) is sampled.
- Three anisotropic Gaussians (A, B, C) are defined with random means and full-rank positive definite covariances.
- Mahalanobis distances \( y_i = (x - \mu_i)^\top \Sigma_i^{-1}(x - \mu_i) \) are computed for each Gaussian.
- Each Gaussian is scaled so that \( x \) lies on its unit Mahalanobis shell (i.e., scaled covariance \( \tilde{\Sigma}_i = y_i \Sigma_i \)).

## Methods
### Direct Fusion (Baseline)
- Compute the Gaussian product A·B·C using scaled covariances.
- This gives the estimate \( \hat{x} \) and covariance \( \Sigma \).

### Pairwise Fusion
- Compute three pairwise Gaussian products: A·B, B·C, A·C.
- Treat these three pairwise product Gaussians as new "shells."
- Fuse these three intermediate Gaussians using the standard product rule.
- Evaluate the resulting \( \hat{x} \) and fused covariance.

## Results Summary
In a representative run:
- The reconstructed \( \hat{x} \) was nearly identical between the direct and pairwise methods.
- However, the covariance from the pairwise method was significantly smaller.
- The mean eigenvalue (expected error) was **underreported**.

Example (pairwise method):
- Observed error: 0.1462
- \( \sqrt{\text{mean eigenvalue}} \): 0.1085
- Indicates **overconfidence** in uncertainty estimate due to double-counting Gaussians.

## Conclusion
The pairwise fusion strategy does **not** lead to a tighter or more accurate bound. Instead:
- It introduces **information redundancy** by using each Gaussian more than once.
- This results in **underestimated uncertainty**, despite the reconstruction point being nearly identical.

The direct product of all Gaussians remains the cleanest and most principled approximation for intersection.

## Future Work
- Explore iterative refinement using the reconstructed \( \hat{x} \) to resample Mahalanobis shells.
- Investigate tighter fusion with more than 3 independent constraints.
- Evaluate sphericity and error contraction over multiple iterations.

## Output

```
Sampled true x: [0.33669036626815796, 0.12880940735340118]

Computing Mahalanobis distances:
  Gaussian 1:
    mu = [0.23446236550807953, 0.23033303022384644]
    Sigma = tensor([[ 1.795525, -2.360616],
        [-2.360616,  5.783194]])
    y (Mahalanobis^2) = 0.0062
  Gaussian 2:
    mu = [2.4616572856903076, 2.267350912094116]
    Sigma = tensor([[ 1.441182, -0.773752],
        [-0.773752,  4.588165]])
    y (Mahalanobis^2) = 5.7105
  Gaussian 3:
    mu = [3.011040210723877, 4.957971572875977]
    Sigma = tensor([[ 2.915840, -1.625943],
        [-1.625943,  1.649943]])
    y (Mahalanobis^2) = 56.1986

Pairwise Gaussian Products:
  Pair 1-2:
    mu_pair = [0.2363051176071167, 0.23017215728759766]
    Sigma_pair = tensor([[ 0.011157, -0.014662],
        [-0.014662,  0.035934]])
  Pair 2-3:
    mu_pair = [2.495351791381836, 3.3376290798187256]
    Sigma_pair = tensor([[ 7.835908, -4.266020],
        [-4.266020, 17.495508]])
  Pair 1-3:
    mu_pair = [0.23338139057159424, 0.23425859212875366]
    Sigma_pair = tensor([[ 0.011172, -0.014685],
        [-0.014685,  0.035973]])

Fusing Pairwise Shells:
  Pairwise Shell 1:
    mu = [0.2363051176071167, 0.23017215728759766]
    Sigma = tensor([[ 0.011157, -0.014662],
        [-0.014662,  0.035934]])
    Inverse Sigma = tensor([[193.263321,  78.855301],
        [ 78.855301,  60.003506]])
  Pairwise Shell 2:
    mu = [2.495351791381836, 3.3376290798187256]
    Sigma = tensor([[ 7.835908, -4.266020],
        [-4.266020, 17.495508]])
    Inverse Sigma = tensor([[0.147152, 0.035881],
        [0.035881, 0.065907]])
  Pairwise Shell 3:
    mu = [0.23338139057159424, 0.23425859212875366]
    Sigma = tensor([[ 0.011172, -0.014685],
        [-0.014685,  0.035973]])
    Inverse Sigma = tensor([[193.143204,  78.846092],
        [ 78.846092,  59.985466]])

--- Final Reconstruction from Pairwise Fusion ---
Reconstructed x̂ (mean): [0.23522695899009705, 0.23409146070480347]
True x: [0.33669036626815796, 0.12880940735340118]
Euclidean error ||x - x̂||: 0.146216

--- Covariance Diagnostics ---
Final covariance matrix:
tensor([[ 0.005577, -0.007328],
        [-0.007328,  0.017957]])
Eigenvalues: [0.0021749050356447697, 0.021359160542488098]
√(max eigenvalue) (Max error): 0.146148
√(mean eigenvalue) (Expected error): 0.108476
Sphericity (geometric / arithmetic mean): 0.579222
```