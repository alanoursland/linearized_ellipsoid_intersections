Okay, here's the revised `ex8_nd_sphere_inout_grad.md` experiment report, incorporating your feedback, focusing on the learning rate discussion, and presented without preformatted blocks for easier copying.

# Reconstructing Vectors from Centroid Distances: Equivalence of Intuitive and Gradient-Based Approaches

## Introduction

This experiment investigates the problem of reconstructing an unknown vector in a high-dimensional space, given only its Euclidean distances to a set of known centroid vectors. This is analogous to an "inverse k-means" problem – recovering a data point from information about its distances to cluster centers. We explore two seemingly different approaches: an "intuitive" algorithm based on geometric reasoning and a standard gradient descent optimization. The key finding is the mathematical equivalence of these two approaches when properly formulated, demonstrating that the intuitive algorithm *is* gradient descent in disguise. This report details the algorithms, their derivation, the crucial role of learning rate scaling, experimental verification, and a discussion of the findings.

## The "Intuitive" Algorithm (Original Algorithm)

The original algorithm iteratively refines an estimate of the unknown vector (`x_est`) by considering its distances to known centroids (`c_i`). For each centroid:

1.  Calculate the estimated distance:  `d_est_i = ||x_est - c_i||`
2.  Calculate the difference between the true distance (`y[i]`) and the estimated distance: `delta_i = y[i] - d_est_i`
3.  Calculate a normalized direction vector from the centroid to the estimate: `direction_i = (x_est - c_i) / ||x_est - c_i||`
4.  Update the estimate: `x_est = x_est + step_fraction * delta_i * direction_i`

The core idea is simple: if the estimate is too far from a centroid, move it closer; if it's too close, move it away. The `step_fraction` controls the update magnitude. This process repeats iteratively, processing each centroid. Originally, this algorithm processed each centroid independently in an inner loop.

## Gradient Descent Formulation

We can also formulate the problem as minimizing a loss function. A natural choice is the sum of squared differences between estimated and true distances:

```
L(x_est) = 0.5 * sum_i ( ||x_est - c_i|| - y[i] )^2
```

To minimize this loss, we use gradient descent. The gradient of L(x_est) with respect to x_est is:

```
∂L / ∂x_est = sum_i ( ||x_est - c_i|| - y[i] ) * (x_est - c_i) / ||x_est - c_i||
```

This is derived using the chain rule and the derivative of the Euclidean norm. The gradient descent update rule is:

```
x_est = x_est - learning_rate * ∇L(x_est)
```

## Mathematical Equivalence

The "intuitive" algorithm and gradient descent are mathematically equivalent. Rewriting the original algorithm's update rule:

```
x_est = x_est + step_fraction * (y[i] - ||x_est - c_i||) * (x_est - c_i) / ||x_est - c_i||
x_est = x_est - step_fraction * (||x_est - c_i|| - y[i]) * (x_est - c_i) / ||x_est - c_i||
```

This is *identical* in form to the gradient descent update. The `step_fraction` acts as the `learning_rate`. When we vectorize the code to process all centroids simultaneously, the summation in the gradient is performed explicitly, making the equivalence complete.

## Learning Rate and Batch Size

A critical observation is the difference in how the learning rate (or step fraction) must be handled in the original iterative algorithm versus the vectorized, full-batch gradient descent.

*   **Original Algorithm (Implicitly Stochastic):** The original algorithm processed one centroid at a time.  A `step_fraction` of 1.0 (or a smaller value like 0.1) worked well because the updates were effectively being "averaged" over many iterations and different centroids.  This is analogous to *stochastic* gradient descent (SGD), where updates are made based on small subsets of the data.  SGD often allows for larger learning rates due to the inherent noise in the updates.

*   **Vectorized Gradient Descent (Full Batch):** The vectorized implementation calculates the gradient contribution from *all* centroids *simultaneously*.  This is *full-batch* gradient descent.  Using a learning rate of 1.0 would lead to massive overshooting and divergence.

*   **The `1/k` Heuristic:**  To achieve similar behavior to the original algorithm, the learning rate in the full-batch gradient descent needs to be scaled down.  A heuristic of `learning_rate = 1.0 / k` (where `k` is the number of centroids) was found to be effective. This effectively averages the gradient contributions from all centroids, making the update magnitude comparable to the *average* update magnitude in the original iterative algorithm. This can be viewed as transforming the full-batch gradient descent into an approximation of stochastic gradient descent.

* **Contrast with Linear Scaling Rule:** It's important to distinguish this `1/k` scaling from the *Linear Scaling Rule* often used in deep learning. The Linear Scaling Rule suggests *increasing* the learning rate proportionally to the batch size.  That rule is primarily concerned with maintaining a constant *variance* in the gradient updates as the batch size changes.  Our `1/k` scaling, in this specific context, is about matching the *magnitude* of the update in the full-batch case to the *average* magnitude of the updates in the implicitly stochastic original algorithm. We are effectively converting a full batch update into an averaged, single centroid update.

## Experimental Setup

Experiments were performed using PyTorch, with GPU acceleration if available. Parameters included:

*   **Dimensionality (D):** 784
*   **Number of Centroids (k):**  Tested with k=128 (underdetermined), k=784 (square), and k=1568 (overdetermined, k=2\*D).
*   **Iterations:** 10,000 and 100,000.
*   **Learning Rate (GD):** 1.0/k
*   **Step Fraction (Original):** 0.1
*   **Initialization:** Both algorithms started from the *same* random `x_est`.

Centroids and the true `x_true` were randomly generated. Distances `y` were calculated from `x_true` and the centroids.

## Results

*   **Underdetermined Case (k < D):** Both algorithms converged to a similar, relatively high error, unable to recover `x_true`.
*   **Overdetermined Case (k > D):** Both algorithms converged to a *very* low error, approaching machine precision with enough iterations, demonstrating successful reconstruction.
*   **Equivalence:** Convergence plots (error vs. iteration) were virtually identical for both algorithms, confirming their equivalence.
*   **Vectorization:** Vectorized implementations were significantly faster, especially on the GPU.
* **Learning Rate:** Using `1/k` as the gradient descent learning rate allowed it to match the convergence of the original method.

## Discussion

The core finding is the mathematical equivalence of the geometrically intuitive algorithm and gradient descent on the squared distance error loss. This validates the initial intuition and demonstrates a deep connection between geometric reasoning and optimization. The experiment also underscores the importance of having an overdetermined system (k > D) for accurate reconstruction from distances.

The discussion of the learning rate highlights a crucial difference between stochastic and full-batch gradient descent. The original algorithm, by processing one centroid at a time, implicitly performed a form of stochastic gradient descent, allowing for a larger "step fraction." The vectorized implementation, using full-batch gradient descent, required a much smaller learning rate, and the `1/k` scaling proved effective in bridging this gap.

## Conclusion

This experiment demonstrates that a simple, geometrically motivated algorithm for reconstructing a vector from its distances to centroids is, in fact, performing gradient descent. This equivalence highlights the power of intuitive reasoning in algorithm design. The experiment also reinforces the importance of understanding the relationship between learning rates, batch sizes, and the nature of the optimization algorithm (stochastic vs. full-batch). The problem becomes well-posed and solvable when we have enough constraints (k > D). Future work could explore the algorithm's robustness to noise and its application to real-world datasets.
