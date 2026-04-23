import numpy as np

def kendall_tau_b(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Compute Kendall's Tau-b correlation coefficient between two rankings.
    
    Args:
        x: A 1D array of shape (n,) representing the first ranking.
        y: A 1D array of shape (n,) representing the second ranking.
    Returns:
        A scalar representing the Kendall's Tau-b correlation coefficient.
    """
    n = x.shape[0]
    assert y.shape[0] == n, "Inputs array must have the same length"
    dx = x[:, None] - x[None, :]
    dy = y[:, None] - y[None, :]
    concordant = np.sum((dx * dy) > 0).astype(int)
    discordant = np.sum((dx * dy) < 0).astype(int)
    ties_x = np.sum(dx == 0) - n  # Exclude diagonal
    ties_y = np.sum(dy == 0) - n  # Exclude
    denominator = np.sqrt((concordant + discordant + ties_x) * (concordant + discordant + ties_y))
    return (concordant - discordant) / denominator