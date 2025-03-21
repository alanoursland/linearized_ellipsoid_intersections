# Gaussian Products

## Mathematical Formulation

Consider two Gaussian probability density functions (PDFs) defined as:

\[
\mathcal{N}(x; \mu_1, \Sigma_1) \quad\text{and}\quad \mathcal{N}(x; \mu_2, \Sigma_2)
\]

The product of these two Gaussians (unnormalized) is also Gaussian:

\[
\mathcal{N}(x; \mu_1, \Sigma_1)\mathcal{N}(x; \mu_2, \Sigma_2) \propto \mathcal{N}(x; \mu, \Sigma)
\]

The resulting Gaussian parameters (mean \(\mu\) and covariance \(\Sigma\)) are:

### Precision Addition

Precision (inverse covariance) matrices sum linearly:

\[
\Sigma^{-1} = \Sigma_1^{-1} + \Sigma_2^{-1}
\]

### Mean Calculation

The mean is a precision-weighted average of the input means:

\[
\mu = \Sigma(\Sigma_1^{-1}\mu_1 + \Sigma_2^{-1}\mu_2)
\]

## Connection to Kalman Filters

Gaussian products appear naturally in the context of Kalman filtering, specifically during the measurement update (correction step). The prior state distribution (predicted state) is updated using measurement distribution (likelihood), and their product produces the posterior state distribution. Precisely:

- Prior distribution: \(\mathcal{N}(x; \mu_p, \Sigma_p)\)
- Measurement distribution (likelihood): \(\mathcal{N}(x; \mu_m, \Sigma_m)\)
- Posterior distribution:
\[
\Sigma^{-1} = \Sigma_p^{-1} + \Sigma_m^{-1}, \quad \mu = \Sigma(\Sigma_p^{-1}\mu_p + \Sigma_m^{-1}\mu_m)
\]

## Properties and Guarantees

### 1. Lower Variance (Higher Precision)

Because precision matrices sum, the covariance matrix of the product Gaussian always has equal or lower variance (higher precision) than each of the original distributions individually. Intuitively, combining information from two Gaussian sources always leads to increased certainty (lower variance) in the resulting distribution.

### 2. Sphericity Guarantees

Sphericity refers to how closely a Gaussian covariance is proportional to the identity matrix (equal eigenvalues). The product of Gaussians has notable properties regarding sphericity:

- **Never decreasing sphericity**: Multiplying Gaussians cannot make the resulting Gaussian less spherical. Formally, the ratio of largest-to-smallest eigenvalues (the condition number) will never increase, except in trivial aligned cases (identical anisotropy).
- **Usually increasing sphericity**: When Gaussian distributions are anisotropic in different directions (misaligned), their product tends to produce a distribution with eigenvalues that are more equal, hence increasing sphericity.

### Formal Eigenvalue Argument

Consider the eigenvalues \(\lambda_{i}\) of each precision matrix. The resulting covariance eigenvalues after product are inversely related to the sum of precisions:

\[
\lambda_i(\Sigma^{-1}) = \lambda_i(\Sigma_1^{-1} + \Sigma_2^{-1})
\]

This operation tends to equalize eigenvalues if the original distributions had complementary directions of anisotropy.

## Practical Implications

Gaussian products:

- Provide a computationally efficient means of merging uncertainty from multiple sources (as in sensor fusion).
- Are widely used in probabilistic inference, Kalman filtering, Gaussian process regression, and Bayesian machine learning.
- Act as a geometric "soft intersection" of ellipsoidal contours, offering a practical linearization or approximation of complex constraint sets.

## References

- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer-Verlag.
- Kalman, R. E. (1960). "A new approach to linear filtering and prediction problems." *Journal of Basic Engineering*, 82(1), 35–45.
- Murphy, K. P. (2012). *Machine Learning: A Probabilistic Perspective*. MIT Press.
- Bar-Shalom, Y., Li, X. R., & Kirubarajan, T. (2001). *Estimation with Applications to Tracking and Navigation: Theory Algorithms and Software*. Wiley-Interscience.
