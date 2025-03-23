import torch
import math

# Set seed
torch.manual_seed(42)
torch.set_printoptions(precision=6, sci_mode=False)

log = []

# Step 1: Sample true input
x = torch.randn(2)
log.append(f"Sampled true x: {x.tolist()}")

# Step 2: Define 3 anisotropic Gaussians
def generate_gaussian(mean_shift):
    mu = torch.randn(2) + mean_shift
    A = torch.randn(2, 2)
    Sigma = A @ A.T + 0.5 * torch.eye(2)
    return mu, Sigma

gaussians = [generate_gaussian(i * 2.0) for i in range(3)]

# Step 3: Compute Mahalanobis distances
ys = []
log.append("\nComputing Mahalanobis distances:")
for i, (mu, Sigma) in enumerate(gaussians):
    delta = x - mu
    inv_Sigma = torch.inverse(Sigma)
    y = delta @ inv_Sigma @ delta
    ys.append(y)
    log.append(f"  Gaussian {i+1}:")
    log.append(f"    mu = {mu.tolist()}")
    log.append(f"    Sigma = {Sigma}")
    log.append(f"    y (Mahalanobis^2) = {y.item():.4f}")

# Step 4: Scale the covariances
scaled_inverses = []
weighted_means = []
log.append("\nScaling covariances:")
for i, ((mu, Sigma), y) in enumerate(zip(gaussians, ys)):
    log.append(f"  Gaussian {i+1}:")
    scaled_Sigma = y * Sigma
    inv_scaled_Sigma = torch.inverse(scaled_Sigma)
    scaled_inverses.append(inv_scaled_Sigma)
    weighted_means.append(inv_scaled_Sigma @ mu)
    log.append(f"    Scaled Sigma: {scaled_Sigma}")
    log.append(f"    Inverse Scaled Sigma: {inv_scaled_Sigma}")

# Step 5: Compute Gaussian product
sum_inv = sum(scaled_inverses)
Sigma_product = torch.inverse(sum_inv)
mu_product = Sigma_product @ sum(weighted_means)

# Step 6: Report reconstruction
error = torch.norm(x - mu_product)
log.append("\n--- Product Gaussian Result ---")
log.append(f"Reconstructed x̂ (mean of product): {mu_product.tolist()}")
log.append(f"True x: {x.tolist()}")
log.append(f"Euclidean error ||x - x̂||: {error.item():.6f}")

# Step 7: Analyze product covariance
eigvals = torch.linalg.eigvalsh(Sigma_product)
sqrt_max = eigvals.max().sqrt().item()
sqrt_mean = eigvals.mean().sqrt().item()
sphericity = (eigvals.prod().sqrt() / eigvals.mean()).item()

log.append("\n--- Covariance Diagnostics ---")
log.append(f"Product covariance matrix:\n{Sigma_product}")
log.append(f"Eigenvalues: {eigvals.tolist()}")
log.append(f"√(max eigenvalue) (Max error): {sqrt_max:.6f}")
log.append(f"√(mean eigenvalue) (Expected error): {sqrt_mean:.6f}")
log.append(f"Sphericity (geometric / arithmetic mean): {sphericity:.6f}")

# Output the log
print("\n".join(log))
