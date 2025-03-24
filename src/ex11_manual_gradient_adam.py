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


# --- Setup ---
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

D = 784
k = 1024
num_iters = 10000
lr = 1.0 / k

# torch.manual_seed(42)

x_true = torch.randn(D, device=device)
x_init = torch.randn(D, device=device)

# -- Generate ellipsoids --
mus = torch.randn(k, D, device=device)
As = torch.randn(k, D, D, device=device)
Sigmas = torch.matmul(As, As.transpose(-1, -2)) + 0.5 * torch.eye(D, device=device)
inv_Sigmas = torch.linalg.inv(Sigmas)

with torch.no_grad():
    diffs = x_true - mus
    y_ellip = torch.sqrt(torch.einsum('ki,kij,kj->k', diffs, inv_Sigmas, diffs))
    y_sphere = torch.norm(diffs, dim=1)

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
