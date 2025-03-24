import torch
from putils import Timer

def adam_update(x, grad, state, lr, beta1=0.9, beta2=0.999, eps=1e-8, t=1):
    exp_avg, exp_avg_sq = state

    exp_avg.mul_(beta1).add_(grad, alpha=1 - beta1)
    exp_avg_sq.mul_(beta2).addcmul_(grad, grad, value=1 - beta2)

    bias_correction1 = 1 - beta1 ** t
    bias_correction2 = 1 - beta2 ** t
    step_size = lr * (bias_correction2**0.5) / bias_correction1

    step = step_size * exp_avg / (exp_avg_sq.sqrt() + eps)
    x -= step

    return x

def train_manual_adam(x_est, x_true, criterion, num_iters, lr, device, label=""):
    D = x_est.shape[0]
    exp_avg = torch.zeros(D, device=device)
    exp_avg_sq = torch.zeros(D, device=device)
    state = (exp_avg, exp_avg_sq)

    timer = Timer()

    for t in range(1, num_iters + 1):
        loss, grad = criterion(x_est)
        x_est = adam_update(x_est, grad, state, lr, t=t)

        if t % 1000 == 0:
            err = torch.norm(x_true - x_est).item()
            print(f"{label} Iteration {t:6d}: Error = {err:.6f}, Loss = {loss.item():.6f}")

    print(f"{label} Time: {timer.tick():.2f}s")
    final_error = torch.norm(x_true - x_est).item()
    print(f"{label} Final Error: {final_error:.6f}")
    return x_est

class SphericalLoss:
    def __init__(self, mus, y):
        self.mus = mus
        self.y = y.view(-1, 1)

    def __call__(self, x):
        diffs = x - self.mus
        d = torch.norm(diffs, dim=1, keepdim=True) + 1e-8
        delta = d - self.y
        grad = torch.sum(delta * (diffs / d), dim=0)
        loss = 0.5 * torch.sum(delta**2)
        return loss, grad


class EllipticalLoss:
    def __init__(self, mus, inv_Sigmas, y):
        self.mus = mus
        self.inv_Sigmas = inv_Sigmas
        self.y = y.view(-1, 1)

    def __call__(self, x):
        diffs = x - self.mus
        d2 = torch.einsum('ki,kij,kj->k', diffs, self.inv_Sigmas, diffs).unsqueeze(1)
        d = torch.sqrt(d2 + 1e-8)
        delta = d - self.y
        grad_per = torch.einsum('kij,kj->ki', self.inv_Sigmas, diffs) / (d + 1e-8)
        grad = torch.sum(delta * grad_per, dim=0)
        loss = 0.5 * torch.sum(delta**2)
        return loss, grad

class PrincipalComponentLoss:
    def __init__(self, mus, V, Lambda, y, norm_type='l2'):
        """
        PCA-based Mahalanobis loss using top r principal components.

        Args:
            mus:     (k, D)        - Gaussian means
            V:       (k, r, D)     - Top principal components per Gaussian
            Lambda:  (k, r)        - Corresponding eigenvalues
            y:       (k,)          - Target distances
            norm_type: 'l2' or 'l1'
        """
        self.mus = mus               # (k, D)
        self.V = V                   # (k, r, D)
        self.Lambda = Lambda         # (k, r)
        self.y = y.view(-1, 1)       # (k, 1)
        self.norm_type = norm_type

        # Precompute W = V / sqrt(Lambda)
        self.W = self.V / (self.Lambda.sqrt().unsqueeze(-1) + 1e-8)  # (k, r, D)

    def __call__(self, x):
        """
        Args:
            x: (D,) - current estimate
        Returns:
            loss: scalar
            grad: (D,) gradient
        """
        k, r, D = self.W.shape

        diffs = x - self.mus  # (k, D)
        proj = torch.einsum('krd,kd->kr', self.W, diffs)  # (k, r)

        if self.norm_type == 'l2':
            norms = torch.norm(proj, dim=1, keepdim=True)  # (k, 1)
        elif self.norm_type == 'l1':
            norms = torch.sum(proj.abs(), dim=1, keepdim=True)  # (k, 1)
        else:
            raise ValueError("norm_type must be 'l1' or 'l2'")

        delta = norms - self.y  # (k, 1)
        loss = 0.5 * torch.sum(delta ** 2)

        if self.norm_type == 'l2':
            # Safe normalization of projection vectors
            norm_safe = norms + 1e-8
            weights = (proj / norm_safe)  # (k, r)
        else:
            weights = torch.sign(proj)  # (k, r)

        # Gradient contribution from each component
        grad_components = delta * weights  # (k, r)
        grad = torch.sum(grad_components.unsqueeze(-1) * self.W, dim=(0, 1))  # (D,)

        return loss, grad

# --- Setup ---
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

D = 784
k = 1024
num_iters = 10000
lr = 1.0 / k
n_pca = 32

print(f"D={D}, k={k}, num_iters={num_iters}, lr={lr}, n_pca={n_pca}, ")

torch.manual_seed(42)

x_true = torch.randn(D, device=device)
x_init = torch.randn(D, device=device)

# -- Generate ellipsoids --
print("Generating data")
with torch.no_grad():
    setup_timer = Timer()
    print("\tCreating random means")
    mus = torch.randn(k, D, device=device)
    print("\tCreating random covariances")
    As = torch.randn(k, D, D, device=device)
    Sigmas = torch.matmul(As, As.transpose(-1, -2)) + 0.5 * torch.eye(D, device=device)
    print("\tInverting covariances")
    inv_Sigmas = torch.linalg.inv(Sigmas)

    # Precompute PCA components
    print("\tPCA covariances")
    eigvals, eigvecs = torch.linalg.eigh(Sigmas)  # (k, D), (k, D, D)
    idx = torch.argsort(eigvals, dim=1, descending=True)[:, :n_pca]  # top n_pca
    batch_indices = torch.arange(k, device=device).unsqueeze(1)
    top_V = eigvecs[batch_indices, :, idx]  # (k, D, r)
    top_Lambda = torch.gather(eigvals, 1, idx)  # (k, n_pca)

print(f"\tDone ({setup_timer.tick():.2f}s)")

print("Evaluating initial state")
with torch.no_grad():
    diffs = x_true - mus
    y_ellip = torch.sqrt(torch.einsum('ki,kij,kj->k', diffs, inv_Sigmas, diffs))
    y_sphere = torch.norm(diffs, dim=1)
    proj = torch.einsum('krd,kd->kr', top_V, diffs)           # (k, r)
    scaled = proj / (top_Lambda.sqrt() + 1e-8)                # (k, r)
    y_pca_l2 = torch.norm(scaled, dim=1)                      # (k,)
    y_pca_l1 = torch.sum(scaled.abs(), dim=1)  # (k,)
print(f"\tDone ({setup_timer.tick():.2f}s)")

# --- PCA L2 Reconstruction ---
print("----- PCA L2 Manual Adam Reconstruction -----")
x_est = x_init.clone().detach()
criterion = PrincipalComponentLoss(mus, top_V, top_Lambda, y_pca_l2, norm_type='l2')
x_est = train_manual_adam(x_est, x_true, criterion, num_iters, lr, device, label="PCA-L2")

print()

# --- PCA L1 Reconstruction ---
print("----- PCA L1 Manual Adam Reconstruction -----")
x_est = x_init.clone().detach()
criterion = PrincipalComponentLoss(mus, top_V, top_Lambda, y_pca_l1, norm_type='l1')
x_est = train_manual_adam(x_est, x_true, criterion, num_iters, lr, device, label="PCA-L1")

print()

# --- Ellipsoidal Reconstruction ---
print("----- Ellipsoidal Manual Adam Reconstruction -----")
x_est = x_init.clone().detach()
criterion = EllipticalLoss(mus, inv_Sigmas, y_ellip)
x_est = train_manual_adam(x_est, x_true, criterion, num_iters, lr, device, label="Elliptical")

print()

# --- Spherical Reconstruction ---
print("----- Spherical Manual Adam Reconstruction -----")
x_est = x_init.clone().detach()
criterion = SphericalLoss(mus, y_sphere)
x_est = train_manual_adam(x_est, x_true, criterion, num_iters, lr, device, label="Spherical")
