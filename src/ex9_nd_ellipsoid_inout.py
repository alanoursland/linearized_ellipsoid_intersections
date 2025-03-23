import torch

# Detect device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Running on device: {device}")

torch.set_printoptions(precision=6, sci_mode=False)

# Parameters
num_iters = 10000
D = 784

# True point we're trying to estimate (on device)
x_true = torch.randn(D, device=device)

# Initial estimate (start far away)
x_est = 10 * torch.randn(D, device=device)

print(f"Initial error: {torch.norm(x_true - x_est):.8f}")

# Step size for updates
step_fraction = 1.0

for i in range(1, num_iters + 1):
    # Generate a random ellipsoid
    mu = 5 * torch.randn(D, device=device)
    A = torch.randn(D, D, device=device)
    Sigma = A @ A.T + 0.5 * torch.eye(D, device=device)  # Ensure positive-definite
    Sigma_inv = torch.linalg.inv(Sigma)

    # Mahalanobis distance of true point
    diff_true = x_true - mu
    d_true = torch.sqrt(diff_true @ Sigma_inv @ diff_true)

    # Mahalanobis distance of current estimate
    diff_est = x_est - mu
    d_est = torch.sqrt(diff_est @ Sigma_inv @ diff_est)

    # Direction: normalized Mahalanobis gradient
    direction = Sigma_inv @ diff_est
    direction = direction / (torch.norm(direction) + 1e-8)

    # Update toward or away from ellipsoid surface
    delta = d_true - d_est
    x_est = x_est + step_fraction * delta * direction

    if i % 100 == 0 or i == 1:
        err = torch.norm(x_true - x_est)
        print(f"{i}: Estimate Error: {err:.8f}")
