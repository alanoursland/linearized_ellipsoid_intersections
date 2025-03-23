import torch

# Set seed and options
torch.manual_seed(42)
torch.set_printoptions(precision=6, sci_mode=False)

# Parameters
num_trials = 100
dim = 2

errors = []
mean_eigenvalue_sqrts = []

def generate_gaussian(mean_shift):
    mu = torch.randn(dim) + mean_shift
    A = torch.randn(dim, dim)
    Sigma = A @ A.T + 0.5 * torch.eye(dim)
    return mu, Sigma

for _ in range(num_trials):
    x = torch.randn(dim)
    gaussians = [generate_gaussian(i * 2.0) for i in range(3)]

    # Compute Mahalanobis distances
    ys = []
    for mu, Sigma in gaussians:
        delta = x - mu
        inv_Sigma = torch.inverse(Sigma)
        y = delta @ inv_Sigma @ delta
        ys.append(y)

    # Scale and compute Gaussian product
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

    # Track errors
    error = torch.norm(x - mu_product).item()
    mean_eigen_sqrt = torch.linalg.eigvalsh(Sigma_product).mean().sqrt().item()

    errors.append(error)
    mean_eigenvalue_sqrts.append(mean_eigen_sqrt)

# Final summary
avg_error = sum(errors) / num_trials
avg_expected = sum(mean_eigenvalue_sqrts) / num_trials

print(f"Average Euclidean error over {num_trials} runs: {avg_error:.6f}")
print(f"Average sqrt(mean eigenvalue) (expected error): {avg_expected:.6f}")
