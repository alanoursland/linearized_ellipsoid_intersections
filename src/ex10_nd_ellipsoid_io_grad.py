import torch
from torch import nn
from torch.optim import SGD
from putils import Timer

# For spherical intersection
class SphericalIntersectionLoss(nn.Module):
    def __init__(self, centroids, y):
        """
        Spherical (Euclidean) distance loss from x to a set of centroids.

        Args:
            centroids (Tensor): shape (k, D)
            y (Tensor): shape (k,) or (k, 1), the true distances from x_true to each centroid
        """
        super().__init__()
        self.centroids = centroids  # (k, D)
        self.y = y.view(-1, 1)      # (k, 1)

    def forward(self, x):
        # x: shape (D,) or (1, D)
        x = x.view(-1)  # Ensure shape (D,)
        diffs = self.centroids - x  # (k, D)
        d_est = torch.norm(diffs, dim=1, keepdim=True)  # (k, 1)
        loss = 0.5 * torch.sum((d_est - self.y) ** 2)
        return loss

# --- Custom Mahalanobis Loss ---
# For elliptical intersection
class EllipticalIntersectionLoss(nn.Module):
    def __init__(self, mus, inv_Sigmas, y):
        super().__init__()
        self.mus = mus  # (k, D)
        self.inv_Sigmas = inv_Sigmas  # (k, D, D)
        self.y = y.view(-1, 1)  # (k, 1)

    def forward(self, x):
        # x: shape (D,)
        diffs = x - self.mus  # (k, D)
        d_squared = torch.einsum('ki,kij,kj->k', diffs, self.inv_Sigmas, diffs).unsqueeze(1)
        d = torch.sqrt(d_squared + 1e-8)
        loss = 0.5 * torch.sum((d - self.y) ** 2)
        # loss = 0.5 * torch.sum((d_squared - y**2)**2 / (4 * (d_squared + 1e-8)))
        return loss

def train(model, x_true, criterion, optimizer, num_iters, lr, device):
    timer = Timer()
    with torch.no_grad():
        initial_error = torch.norm(x_true - model).item()
    # --- Setup Learnable Parameter and Training Components ---

    # --- Training Loop ---
    errors = []
    losses = []

    for iter in range(1, num_iters + 1):
        optimizer.zero_grad()
        loss = criterion(model)
        loss.backward()
        optimizer.step()

        if iter % 1000 == 0:
            with torch.no_grad():
                err = torch.norm(x_true - model)
                errors.append(err.item())
                losses.append(loss.item())
                print(f"Iteration {iter:6d}: Error = {err.item():.6f}, Loss = {loss.item():.6f}")

    # --- Final Result ---
    with torch.no_grad():
        final_error = torch.norm(x_true - model).item()

    print(f"Elapsed Time: {timer.tick():.2f}s")
    print(f"\nInitial Error: {initial_error:.6f}")
    print(f"  Final Error: {final_error:.6f}")

# --- Device Selection ---
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# --- Experiment Setup ---
D = 784
k = 1024
num_iters = 10000
lr = 1.0 / k

# torch.manual_seed(42)  # Optional reproducibility

# --- Generate Ground Truth and Ellipsoids ---
x_true = torch.randn(D, device=device)
x_init = torch.randn(D, device=device)

print("Generating ellipsoids...")
mus = torch.randn(k, D, device=device)
As = torch.randn(k, D, D, device=device)
Sigmas = torch.matmul(As, As.transpose(-1, -2)) + 0.5 * torch.eye(D, device=device)
inv_Sigmas = torch.linalg.inv(Sigmas)
mus.requires_grad_(False)
inv_Sigmas.requires_grad_(False)

# Compute target Mahalanobis distances
with torch.no_grad():
    diffs_true = x_true - mus
    y = torch.sqrt(torch.einsum('ki,kij,kj->k', diffs_true, inv_Sigmas, diffs_true))
    y.requires_grad_(False)

model = torch.nn.Parameter(x_init.clone().detach()).to(device)
criterion = EllipticalIntersectionLoss(mus, inv_Sigmas, y)
# optimizer = SGD([model], lr=lr)
optimizer = torch.optim.Adam([model], lr=lr)
print("----- Ellipsoidal Gradient Descent Reconstruction -----")
print(f"D={D}, k={k}, num_iters={num_iters}, lr={lr}, opt={type(optimizer)}")
train(model, x_true, criterion, optimizer, num_iters, lr, device)

print()

# Compute target L2 distances
with torch.no_grad():
    diffs_true = x_true - mus
    y = torch.norm(diffs_true, dim=1)
    y.requires_grad_(False)

model = torch.nn.Parameter(x_init.clone().detach()).to(device)
criterion = SphericalIntersectionLoss(mus, y)
# optimizer = SGD([model], lr=lr)
optimizer = torch.optim.Adam([model], lr=lr)
print("----- Spherical Gradient Descent Reconstruction -----")
print(f"D={D}, k={k}, num_iters={num_iters}, lr={lr}, opt={type(optimizer)}")
train(model, x_true, criterion, optimizer, num_iters, lr, device)