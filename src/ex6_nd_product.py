import torch

# Set seed for reproducibility
# torch.manual_seed(42)
torch.set_printoptions(precision=6, sci_mode=False)

# Compute intersection of two Nd spheres
def intersect_spheres(mu1, r1, mu2, r2):
    """
    Calculates the intersection of two spheres in N dimensions.

    Args:
        mu1: Tensor, shape (N,), center of the first sphere.
        r1: Tensor, shape (), radius of the first sphere (scalar).
        mu2: Tensor, shape (N,), center of the second sphere.
        r2: Tensor, shape (), radius of the second sphere (scalar).

    Returns:
        A tuple: (mu_intersection, r_intersection, dim_intersection)
            mu_intersection: Tensor, shape (N,), the "mean" of the intersection.
                             If the spheres intersect in a lower-dimensional
                             hypersphere, this is the center of that hypersphere.
            r_intersection: Tensor, shape (), the "radius" of the intersection.
                             If the spheres intersect in a lower-dimensional
                             hypersphere, this is the radius of that hypersphere.
            dim_intersection: int, the dimensionality of the intersection.
                              -  0:  Intersection is two points (a 0-sphere).
                              -  1:  Intersection is a circle (a 1-sphere).
                              -  2:  Intersection is a 2-sphere (surface of a 3D ball).
                              -  ...
                              -  N-1: Intersection is an (N-1)-sphere.
                              - -1: No intersection, or spheres are identical.

            Returns (mu1, r1, -1) if the spheres do not intersect or are coincident.
    """
    d = torch.linalg.norm(mu1 - mu2)

    # Check for intersection (and handle edge cases)
    if d > r1 + r2 or d < torch.abs(r1 - r2) or (d == 0 and r1 == r2):
        return mu1, r1, -1  # No (N-1)-sphere intersection, or identical spheres

    # Direction vector from mu1 to mu2 (unit vector)
    u = (mu2 - mu1) / d

    # Distance from mu1 to the hyperplane of intersection
    a = (r1**2 - r2**2 + d**2) / (2 * d)
    # No need to clamp a here.  The intersection check above guarantees
    # that 0 <= a <= d.  Clamping can introduce errors.

    # Center of the intersection hypersphere
    mu_intersection = mu1 + a * u

    # Calculate h (radius of the intersection hypersphere)
    h_sq = r1**2 - a**2
    h_sq = torch.clamp(h_sq, min=0.0)  # Ensure non-negative due to numerical error.
    h = torch.sqrt(h_sq)
    r_intersection = h

    # Determine the dimensionality of the intersection
    dim_intersection = mu1.shape[0] - 1

    return mu_intersection, r_intersection, dim_intersection

# Function: geometric intersection of two Nd spheres
def multiply_spheres(mu1, r1, mu2, r2):
    """
    Treats spheres as Gaussians with covariance = r * I.
    Computes product of two Gaussians.

    Returns:
        mu_product: mean of resulting product Gaussian
        r_product: average variance (mean eigenvalue) as scalar
    """
    D = mu1.shape[0]
    I = torch.eye(D)

    Sigma1 = r1 * I
    Sigma2 = r2 * I

    inv_Sigma1 = torch.inverse(Sigma1)
    inv_Sigma2 = torch.inverse(Sigma2)

    sum_inv = inv_Sigma1 + inv_Sigma2
    Sigma_p = torch.inverse(sum_inv)

    mu_p = Sigma_p @ (inv_Sigma1 @ mu1 + inv_Sigma2 @ mu2)

    # Expected error proxy: sqrt(mean variance)
    mean_variance = torch.trace(Sigma_p) / D
    expected_error = torch.sqrt(mean_variance)

    return mu_p, expected_error


# Configuration
N = 1280
D = 784
print(f"Intersecting {N} spheres across {D} dimensions")

# Step 1: Sample true point
x = torch.randn(D)

# Step 2: Sample initial center and radius
mu_x = 5 * torch.randn(D)
r_x = torch.norm(x - mu_x)
print(f"0: Expected Error: {r_x:.8f}, Observed Error: {torch.norm(x - mu_x):.8f}")

# Step 3: Iteratively intersect with new spheres
for i in range(1, N):
    mu_i = 5 * torch.randn(D)
    r_i = torch.norm(x - mu_i)

    mu_x, r_x = multiply_spheres(mu_x, r_x, mu_i, r_i)

    print(f"{i}: Expected Error: {r_x:.8f}, Observed Error: {torch.norm(x - mu_x):.8f}")
