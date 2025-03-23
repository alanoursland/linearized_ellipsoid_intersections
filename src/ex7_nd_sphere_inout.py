import torch

# torch.manual_seed(42)
torch.set_printoptions(precision=6, sci_mode=False)

# Parameters
num_iters = 10000
D = 784

# True point we're trying to estimate
x_true = torch.randn(D)

# Initial estimate (start far away)
x_est = 10 * torch.randn(D)

print(f"Initial error: {torch.norm(x_true - x_est):.8f}")

# Hyperparameters
step_fraction = 1.00  # Move a fraction of the difference in distances

for i in range(1, num_iters + 1):
    # Generate a random centroid
    mu = 5 * torch.randn(D)

    # True distance from centroid to true point
    d_true = torch.norm(x_true - mu)

    # Current distance from centroid to estimate
    d_est = torch.norm(x_est - mu)

    # Direction from centroid to current estimate
    direction = (x_est - mu)
    direction = direction / (torch.norm(direction) + 1e-8)  # Normalize safely

    # Difference between actual and estimate distances
    delta = d_true - d_est

    # Move in the direction based on inside/outside status
    x_est = x_est + step_fraction * delta * direction

    if i % 100 == 0 or i == 1:
        err = torch.norm(x_true - x_est)
        print(f"{i}: Estimate Error: {err:.8f}")

