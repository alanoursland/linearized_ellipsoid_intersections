import torch
from putils import Timer

def reconstruct_from_distances_gradient(x_init, y, centroids, num_iters=1000, learning_rate=1e-3, device='cpu'):
    """
    Reconstructs a vector x from its distances to centroids using gradient descent (vectorized).
    """
    k, D = centroids.shape
    x_est = x_init.clone().detach().to(device)
    centroids = centroids.to(device)
    y = y.to(device)  # y should also be on the device

    for iter in range(num_iters):
        # Vectorized gradient calculation
        diffs = x_est - centroids  # (k, D) - (D) broadcasts to (k, D)
        d_est = torch.norm(diffs, dim=1, keepdim=True)  # (k, 1) distances
        # Avoid division by zero.  Adding to d_est *before* the division is better.
        d_est_safe = d_est + 1e-8
        gradient = torch.sum((d_est_safe - y.view(-1, 1)) * diffs / d_est_safe, dim=0)

        # Gradient DESCENT update
        x_est = x_est - learning_rate * gradient

        if (iter + 1) % 1000 == 0:
            error = torch.norm(x_true - x_est)
            loss = 0.5 * torch.sum((d_est - y.view(-1, 1)) ** 2)  # Calculate Loss
            print(f"GD Iteration {iter+1}: Error = {error.item():.6f}, Loss = {loss.item():.6f}")

    return x_est

def reconstruct_from_distances(x_init, y, centroids, num_iters=100, step_fraction=1.0, device='cpu'):
    """
    Original distance-based reconstruction, vectorized.
    """
    k, D = centroids.shape
    x_est = x_init.clone().detach().to(device)
    centroids = centroids.to(device)
    y = y.to(device)  # Ensure y is on the correct device

    for _ in range(num_iters):
        # Vectorized calculations
        diffs = x_est - centroids  # (k, D) - (D,) broadcasts to (k, D)
        d_est = torch.norm(diffs, dim=1, keepdim=True)  # (k, 1)
        d_true = y.view(-1,1) #Reshape y for broadcasting
        direction = diffs / (d_est + 1e-8)  # (k, D)
        delta = d_true - d_est  # (k, 1)
        x_est = x_est + step_fraction * torch.sum(delta * direction, dim=0)

        if (_ + 1) % 1000 == 0:
            error = torch.norm(x_true - x_est)
            print(f"Original (Vectorized) Iteration {(_ + 1)}: Error = {error.item()}")

    return x_est

# --- Device Selection (CPU or GPU) ---
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# Experiment Setup (D=784, k=128)
D = 784
k = 1024 
num_iters = 10000  # Increased iterations
lr = 1.0 / k

# Generate random centroids and true x
centroids = torch.randn(k, D, device=device)
x_true = torch.randn(D, device=device)
x_init = torch.randn(D, device=device)

# Calculate distances (y)
y = torch.tensor([torch.norm(x_true - centroids[i]) for i in range(k)])

# --- Gradient Descent Reconstruction ---
print("----- Gradient Descent Reconstruction -----")
timer = Timer()
x_est_gd = reconstruct_from_distances_gradient(x_init, y, centroids, num_iters=num_iters, learning_rate=lr, device=device)
gd_error = torch.norm(x_true - x_est_gd)
print(f"{timer.tick():.2f}s")

# # --- Original Algorithm Reconstruction ---
# print("\n----- Original Algorithm Reconstruction -----")
# x_est_orig = reconstruct_from_distances(x_init, y, centroids, num_iters=num_iters, step_fraction=lr, device=device)
# orig_error = torch.norm(x_true - x_est_orig)

print(f"Initial Error: {torch.norm(x_true - x_init)}")
print(f"Final GD Error: {gd_error.item()}")
# print(f"Final Original Error: {orig_error.item()}")

# Linear Scaling Rule (Goyal et al., 2017) - when you increase the batch size by a factor of n, you should also increase the learning rate by a factor of n. It keeps the variance of the updates roughly constant.
# We are doing the opposite.

# The key here is that the variance of the gradient estimate scales inversely with the batch size, but the magnitude of the full gradient scales linearly with the batch size.


