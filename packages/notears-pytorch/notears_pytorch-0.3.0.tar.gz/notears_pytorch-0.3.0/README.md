


A PyTorch implementation of the NOTEARS algorithm (Non-parametric Optimization for Structure Learning) for causal discovery.

This package provides a continuous optimization approach to learning DAGs (Directed Acyclic Graphs) from data, harnessing the power of GPUs to accelerate the learning process.

Note: The original NOTEARS Linear implementation is CPU only.

📦 Installation

You can install this package directly from PyPi:

```

pip install notears-pytorch


```

🚀 Usage

Below is a basic example of how to use the linear NOTEARS algorithm.

```
from notears_pytorch import notears_linear


# 2. Run optimization
# Returns a binary adjacency matrix where B[i, j] = 1 implies i -> j
adj_matrix = notears_linear(X, lambda1=0.1, w_threshold=0.3)

print("Estimated Adjacency Matrix:")
print(adj_matrix)


```

📚 API Description 

### `notears_linear`

```python
notears_linear(X, lambda1=0.1, rho_init=1.0, alpha_init=0.0, 
               outer_iter=50, inner_iter=100, init_lr=1e-2, 
               h_tol=1e-8, w_threshold=0.3, use_gpu=False)
```

**Arguments:**
- `X` (`np.ndarray`): Input data matrix of shape (n_samples, n_features).
- `lambda1` (`float`): L1 regularization strength for sparsity.
- `rho_init` (`float`): Initial penalty parameter for the augmented Lagrangian.
- `alpha_init` (`float`): Initial value for the Lagrange multiplier.
- `outer_iter` (`int`): Number of outer optimization iterations.
- `inner_iter` (`int`): Number of inner Adam optimizer iterations per sub-problem.
- `init_lr` (`float`): Initial learning rate for Adam optimizer.
- `h_tol` (`float`): Tolerance for the acyclicity constraint.
- `w_threshold` (`float`): Threshold for pruning weak edges in the adjacency matrix.
- `use_gpu` (`bool`): If `True`, computation is performed on GPU (if available).

**Returns:**
- `np.ndarray`: Estimated binary adjacency matrix of shape (n_features, n_features), where entry `[i, j] = 1` indicates a directed edge from node `i` to node `j`.

**Description:**
This function runs the linear NOTEARS algorithm to estimate the structure of a directed acyclic graph (DAG) from observational data. It uses continuous optimization and supports GPU acceleration for faster computation.


📄 Citation

If you use this implementation in your research, please cite this GitHub repository and the original paper:

Zheng, X., Aragam, B., Ravikumar, P. K., & Xing, E. P. (2018). DAGs with NO TEARS: Continuous Optimization for Structure Learning. Advances in Neural Information Processing Systems.
