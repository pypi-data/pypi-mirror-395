import torch
from .estimators import estimate_hurst

class HurstRegularizationLoss(torch.nn.Module):
    """
    Penalizes deviations from a target Hurst exponent.
    L = lambda * (H_est(y_pred) - H_target)^2
    
    Usage:
    loss = mse_loss(y_pred, y_true) + 0.1 * hurst_reg(y_pred)
    """
    def __init__(self, target_H: float = 0.5):
        super().__init__()
        self.target_H = target_H

    def forward(self, x):
        # Estimate H of the batch
        # x shape: (Batch, Time)
        h_est = estimate_hurst(x) # Returns (Batch,)
        
        # Mean Squared Error from target
        return torch.mean((h_est - self.target_H) ** 2)