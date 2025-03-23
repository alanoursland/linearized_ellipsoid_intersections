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

# Step 4: Define a function to compute Gaussian product
def gaussian_product(mu1, Sigma1, mu2, Sigma2):
    inv1 = torch.inverse(Sigma1)
    inv2 = torch.inverse(Sigma2)
    Sigma_prod_inv = inv1 + inv2
    Sigma_prod = torch.inverse(Sigma_prod_inv)
    mu_prod = Sigma_prod @ (inv1 @ mu1 + inv2 @ mu2)
    return mu_prod, Sigma_prod

# Step 5: Build pairwise products
pair_indices = [(0,1), (1,2), (0,2)]
pairwise_shells = []

log.append("\nPairwise Gaussian Products:")
for i, (a, b) in enumerate(pair_indices):
    mu_a, Sigma_a = gaussians[a]
    mu_b, Sigma_b = gaussians[b]
    y_a = ys[a]
    y_b = ys[b]

    # Scale original covariances
    Sigma_a_scaled = y_a * Sigma_a
    Sigma_b_scaled = y_b * Sigma_b

    mu_pair, Sigma_pair = gaussian_product(mu_a, Sigma_a_scaled, mu_b, Sigma_b_scaled)
    pairwise_shells.append((mu_pair, Sigma_pair))
    log.append(f"  Pair {a+1}-{b+1}:")
    log.append(f"    mu_pair = {mu_pair.tolist()}")
    log.append(f"    Sigma_pair = {Sigma_pair}")

# Step 6: Final fusion of the three pairwise shells
scaled_inverses = []
weighted_means = []

log.append("\nFusing Pairwise Shells:")
for i, (mu, Sigma) in enumerate(pairwise_shells):
    inv_Sigma = torch.inverse(Sigma)
    scaled_inverses.append(inv_Sigma)
    weighted_means.append(inv_Sigma @ mu)
    log.append(f"  Pairwise Shell {i+1}:")
    log.append(f"    mu = {mu.tolist()}")
    log.append(f"    Sigma = {Sigma}")
    log.append(f"    Inverse Sigma = {inv_Sigma}")

# Compute final estimate
sum_inv = sum(scaled_inverses)
Sigma_final = torch.inverse(sum_inv)
mu_final = Sigma_final @ sum(weighted_means)

# Step 7: Report reconstruction
error = torch.norm(x - mu_final)
log.append("\n--- Final Reconstruction from Pairwise Fusion ---")
log.append(f"Reconstructed x̂ (mean): {mu_final.tolist()}")
log.append(f"True x: {x.tolist()}")
log.append(f"Euclidean error ||x - x̂||: {error.item():.6f}")

# Step 8: Analyze final covariance
eigvals = torch.linalg.eigvalsh(Sigma_final)
sqrt_max = eigvals.max().sqrt().item()
sqrt_mean = eigvals.mean().sqrt().item()
sphericity = (eigvals.prod().sqrt() / eigvals.mean()).item()

log.append("\n--- Covariance Diagnostics ---")
log.append(f"Final covariance matrix:\n{Sigma_final}")
log.append(f"Eigenvalues: {eigvals.tolist()}")
log.append(f"√(max eigenvalue) (Max error): {sqrt_max:.6f}")
log.append(f"√(mean eigenvalue) (Expected error): {sqrt_mean:.6f}")
log.append(f"Sphericity (geometric / arithmetic mean): {sphericity:.6f}")

# Output the log
print("\n".join(log))

