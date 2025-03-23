import torch

# Set seed for reproducibility
torch.manual_seed(42)
torch.set_printoptions(precision=6, sci_mode=False)

# Function to generate a random anisotropic Gaussian
def generate_gaussian(mean_shift):
    mu = torch.randn(2) + mean_shift
    A = torch.randn(2, 2)
    Sigma = A @ A.T + 0.5 * torch.eye(2)
    return mu, Sigma

# Run for N from 3 to 10
for N in range(2, 11):
    total_error = 0.0
    total_expected_error = 0.0
    num_trials = 1000

    for _ in range(num_trials):
        # Sample true point x
        x = torch.randn(2)

        # Generate N Gaussians
        gaussians = [generate_gaussian(i * 2.0) for i in range(N)]

        # Compute Mahalanobis distances
        ys = []
        for mu, Sigma in gaussians:
            delta = x - mu
            inv_Sigma = torch.inverse(Sigma)
            y = delta @ inv_Sigma @ delta
            ys.append(y)

        # Scale covariances and compute Gaussian product
        scaled_inverses = []
        weighted_means = []
        for (mu, Sigma), y in zip(gaussians, ys):
            scaled_Sigma = y * Sigma
            inv_scaled_Sigma = torch.inverse(scaled_Sigma)
            scaled_inverses.append(inv_scaled_Sigma)
            weighted_means.append(inv_scaled_Sigma @ mu)

        sum_inv = sum(scaled_inverses)
        Sigma_product = torch.inverse(sum_inv)
        mu_product = Sigma_product @ sum(weighted_means)

        # Compute errors
        error = torch.norm(x - mu_product).item()
        sqrt_mean_eigenvalue = torch.linalg.eigvalsh(Sigma_product).mean().sqrt().item()

        total_error += error
        total_expected_error += sqrt_mean_eigenvalue

    avg_error = total_error / num_trials
    avg_expected_error = total_expected_error / num_trials

    print(f"N = {N}")
    print(f"  Avg Euclidean error ||x - x̂||: {avg_error:.6f}")
    print(f"  Avg expected error (sqrt(mean eigenvalue)): {avg_expected_error:.6f}\n")
