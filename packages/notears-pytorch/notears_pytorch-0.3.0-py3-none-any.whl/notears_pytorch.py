import torch
import torch.nn as nn
import numpy as np

class NotearsModel(nn.Module):
    def __init__(self, d, use_gpu=False):
        super(NotearsModel, self).__init__()
        self.d = d
        self.device = torch.device("cuda" if use_gpu and torch.cuda.is_available() else "cpu")
        
        # Initialize W ~ Uniform or Normal. 
        # TF default for get_variable is Glorot Uniform, we use small random here.
        self.W = nn.Parameter(torch.zeros(d, d).to(self.device))
        
        # Mask to zero out the diagonal
        self.mask = (torch.ones(d, d) - torch.eye(d)).to(self.device)
        self.to(self.device)

    def forward(self, x):
        return torch.matmul(x, self.W * self.mask)

    def get_w(self):
        # Return W with diagonal zeroed
        return (self.W * self.mask).detach().cpu().numpy()

def notears_linear(X, lambda1=0.1, rho_init=1.0, alpha_init=0.0, 
                   outer_iter=50, inner_iter=100, init_lr=1e-2, 
                   h_tol=1e-8, w_threshold=0.3, use_gpu=False):
    """
    API Wrapper for Notears Linear Optimization
    
    Args:
        X (np.ndarray): n x d data matrix
        lambda1 (float): L1 penalty coefficient
        rho_init (float): Initial penalty parameter
        alpha_init (float): Initial Lagrange multiplier
        outer_iter (int): Number of Augmented Lagrangian iterations
        inner_iter (int): Number of Adam iterations per sub-problem
        init_lr (float): Initial learning rate
        h_tol (float): Tolerance for acyclicity constraint
        w_threshold (float): Threshold for final edge pruning
        use_gpu (bool): Whether to use GPU if available

    Returns:
        np.ndarray: Estimated binary adjacency matrix (d x d)
    """
    
    n, d = X.shape
    model = NotearsModel(d, use_gpu=use_gpu)
    
    # Convert data to tensor
    X_torch = torch.from_numpy(X.astype(np.float32)).to(model.device)
    
    rho = rho_init
    alpha = alpha_init
    h_val = np.inf

    for _ in range(outer_iter):
        
        # Reset optimizer for every outer iteration (Solving sub-problem)
        optimizer = torch.optim.Adam(model.parameters(), lr=init_lr)
        
        h_new = np.inf
        
        for t in range(inner_iter):
            # Manual LR decay matching the TF code: step / sqrt(1 + t)
            lr = init_lr / np.sqrt(1.0 + t)
            for param_group in optimizer.param_groups:
                param_group['lr'] = lr
            
            optimizer.zero_grad()
            
            # --- Calculate Loss ---
            # 1. Enforce zero diagonal during computation
            W_masked = model.W * model.mask
            
            # 2. Least Squares Loss: 1/(2n) * ||X - XW||^2
            X_hat = torch.matmul(X_torch, W_masked)
            loss_xw = 0.5 / n * torch.sum((X_torch - X_hat) ** 2)
            
            # 3. Acyclicity Constraint: tr(e^(W*W)) - d = 0
            # Note: The TF code uses W**2 (element-wise square) inside exp
            h_val_torch = torch.trace(torch.matrix_exp(W_masked * W_masked)) - d
            
            # 4. Total Loss (Augmented Lagrangian)
            # loss = MSE + rho/2 * h^2 + alpha * h + lambda * |W|_1
            loss_obj = loss_xw + \
                       (rho / 2.0) * (h_val_torch * h_val_torch) + \
                       alpha * h_val_torch + \
                       lambda1 * torch.sum(torch.abs(W_masked))
            
            loss_obj.backward()
            optimizer.step()
            
            # Update current h for loop check
            if t == inner_iter - 1:
                h_new = h_val_torch.item()

        # Update Augmented Lagrangian parameters
        h_val = h_new
        if h_val <= h_tol:
            break
            
        # Update dual variables
        alpha += rho * h_val
        rho *= 1.25

    # Retrieve W and apply threshold
    W_est = model.get_w()
    B_est = (np.abs(W_est) > w_threshold).astype(int)
    
    return B_est

# --- Usage Demonstration ---
if __name__ == "__main__":
    # Generate synthetic data
    # X = n x d
    n, d = 100, 5
    np.random.seed(42)
    X_synthetic = np.random.randn(n, d)
    
    print("Running Notears PyTorch...")
    
    # API Usage requested by user
    B_est = notears_linear(X_synthetic, lambda1=0.05, w_threshold=0.3)
    
    print("Optimization Finished.")
    print("Estimated Binary Adjacency Matrix:")
    print(B_est)