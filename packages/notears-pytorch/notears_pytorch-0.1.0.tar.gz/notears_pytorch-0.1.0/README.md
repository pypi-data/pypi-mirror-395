Notears PyTorch

A PyTorch implementation of the NOTEARS algorithm (Non-parametric Optimization for Structure Learning) for causal discovery. This package provides a continuous optimization approach to learning DAGs (Directed Acyclic Graphs) from data.

Installation

You can install this package directly from the source:

pip install .


Usage

import numpy as np
from notears_pytorch import notears_linear

# 1. Generate or load data (n_samples x n_features)
n, d = 100, 5
X = np.random.randn(n, d)

# 2. Run optimization
# Returns a binary adjacency matrix where B[i, j] = 1 implies i -> j
adj_matrix = notears_linear(X, lambda1=0.1, w_threshold=0.3)

print("Estimated Adjacency Matrix:")
print(adj_matrix)


API

notears_linear(X, lambda1=0.1, ...)

Solves the optimization problem to find the DAG structure.

X: np.ndarray of shape (n, d). The data matrix.

lambda1: float. L1 penalty parameter (sparsity).

rho_init: float. Initial value for the penalty parameter.

w_threshold: float. Edges with weight absolute value below this are pruned.

use_gpu: bool. If True and CUDA is available, computations run on GPU.

Citation

If you use this method, please cite the original paper:
Zheng, X., Aragam, B., Ravikumar, P. K., & Xing, E. P. (2018). DAGs with NO TEARS: Continuous Optimization for Structure Learning. Advances in Neural Information Processing Systems.