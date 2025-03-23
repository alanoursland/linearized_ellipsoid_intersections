import torch

# Set seed for reproducibility
torch.manual_seed(42)
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

n_spheres = 30
n_dims = 100
num_trials = 1000
print(f"Intersecting {n_spheres} spheres across {n_dims} dimensions with {num_trials} trials")

# Run for N from 2 to 10
for N in range(2, n_spheres+1):
    total_error = 0.0
    total_expected_error = 0.0

    for trial in range(num_trials):
        # Sample true point x
        x = torch.randn(n_dims)

        # Generate N sphere constraints: centers and radii
        centers = [torch.randn(n_dims) + i * 2.0 for i in range(N)]
        radii = [torch.norm(x - mu) for mu in centers]

        # Initialize intersection
        mu_intersect, r_intersect = centers[0], radii[0]

        # Iteratively intersect with remaining spheres
        for i in range(1, N):
            mu_next, r_next, isect = intersect_spheres(
                mu_intersect, r_intersect, centers[i], radii[i]
            )
            if isect > -1:
                mu_intersect, r_intersect = mu_next, r_next
            # else:
            #     print(f"{N} {trial} {i} No intersection")

        # Estimated x̂ is the final intersection center
        x_hat = mu_intersect
        error = torch.norm(x - x_hat).item()
        expected_error = r_intersect.item()

        total_error += error
        total_expected_error += expected_error

    avg_error = total_error / num_trials
    avg_expected_error = total_expected_error / num_trials

    print(f"N = {N}")
    print(f"  Avg Euclidean error ||x - x̂||: {avg_error:.6f}")
    print(f"  Avg expected error (intersection radius): {avg_expected_error:.6f}\n")
