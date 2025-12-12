import numpy as np

def get_nll(y_true: np.ndarray, mu: np.ndarray, sigma: np.ndarray, eps: float = 1e-9) -> float:
    """
    Compute the negative log likelihood under a Gaussian assumption.

    Parameters:

    y_true : np.ndarray
    True target values (N,)
    mu : np.ndarray
    Predicted means (N,)
    sigma : np.ndarray
    Predicted standard deviations (N,)
    eps_float : int
    Small constant added to sigma^2 for numerical stability.

    Returns
    float
        Mean negative log-likelihood across all samples.
        Lower values indicate better-calibrated predictive distributions.
    """
    y_true = np.asarray(y_true).flatten()
    mu = np.asarray(mu).flatten()
    sigma = np.asarray(sigma).flatten()

    var = np.maximum(sigma ** 2, eps)
    nll = (0.5 * np.log(2 * np.pi * var) + 0.5 * ((y_true - mu)**2) / var)
    return np.mean(nll)