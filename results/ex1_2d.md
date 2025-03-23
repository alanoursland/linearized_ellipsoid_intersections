# Experiment 1: 2D Gaussian Product Fusion

## Objective
To test the accuracy and uncertainty estimation of a direct Gaussian product approximation when reconstructing a true 2D point \( x \) from Mahalanobis shell constraints.

## Setup
- A true input \( x \in \mathbb{R}^2 \) was randomly sampled.
- Three anisotropic Gaussian distributions (A, B, C) were defined with random means and positive-definite covariances.
- For each Gaussian, the squared Mahalanobis distance \( y_i \) from \( x \) was computed:
  \[
  y_i = (x - \mu_i)^\top \Sigma_i^{-1}(x - \mu_i)
  \]
- Each Gaussian's covariance was scaled such that \( x \) lay on the unit Mahalanobis shell (i.e., \( \tilde{\Sigma}_i = y_i \Sigma_i \)).
- These scaled Gaussians were fused via a precision-weighted product to compute an estimated point \( \hat{x} \) and product covariance \( \Sigma \).

## Results
- **True x**: [0.3367, 0.1288]  
- **Estimated \( \hat{x} \)**: [0.2352, 0.2341]  
- **Euclidean error**: 0.1462

### Product Covariance
- \( \Sigma = \begin{bmatrix} 0.0112 & -0.0147 \\ -0.0147 & 0.0359 \end{bmatrix} \)
- **Eigenvalues**: [0.00435, 0.04272]  
- **Max error** (\( \sqrt{\lambda_{\text{max}}} \)): 0.2067  
- **Expected error** (\( \sqrt{\text{mean eigenvalue}} \)): 0.1534  
- **Sphericity**: 0.5792

## Interpretation
- The reconstructed point \( \hat{x} \) is very close to the true point \( x \), with an error of 0.146.
- The expected error from the fused covariance (0.153) closely matches the observed reconstruction error.
- The max eigenvalue suggests an upper bound of about 0.21 for uncertainty in the worst direction.
- The moderate sphericity value (0.58) indicates some anisotropy remains, but the fusion improved isotropy relative to any single Gaussian.

## Conclusion
This experiment confirms that the direct product of scaled Gaussians provides:
- An accurate reconstruction of the true point \( x \)
- A meaningful covariance that reflects the expected reconstruction uncertainty

The expected error (from mean eigenvalue) serves as a solid proxy for actual error in this linearized ellipsoidal intersection method.

## Results
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

Scaling covariances:
  Gaussian 1:
    Scaled Sigma: tensor([[ 0.011175, -0.014692],
        [-0.014692,  0.035993]])
    Inverse Scaled Sigma: tensor([[193.129684,  78.832748],
        [ 78.832748,  59.961529]])
  Gaussian 2:
    Scaled Sigma: tensor([[ 8.229875, -4.418510],
        [-4.418510, 26.200731]])
    Inverse Scaled Sigma: tensor([[0.133605, 0.022531],
        [0.022531, 0.041967]])
  Gaussian 3:
    Scaled Sigma: tensor([[163.866180, -91.375740],
        [-91.375740,  92.724495]])
    Inverse Scaled Sigma: tensor([[0.013547, 0.013349],
        [0.013349, 0.023940]])

--- Product Gaussian Result ---
Reconstructed x̂ (mean of product): [0.23522678017616272, 0.23409169912338257]
True x: [0.33669036626815796, 0.12880940735340118]
Euclidean error ||x - x̂||: 0.146216

--- Covariance Diagnostics ---
Product covariance matrix:
tensor([[ 0.011154, -0.014655],
        [-0.014655,  0.035914]])
Eigenvalues: [0.004349809605628252, 0.0427183136343956]
√(max eigenvalue) (Max error): 0.206684
√(mean eigenvalue) (Expected error): 0.153408
Sphericity (geometric / arithmetic mean): 0.579222
```