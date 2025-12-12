import numpy as np
from uq_calculator.get_nll import get_nll
from uq_calculator.get_ece import get_ece
from uq_calculator.plot_confidence_band import plot_confidence_band



def evaluate_all(
        y_true: np.ndarray,
        mu: np.ndarray,
        sigma: np.ndarray,
        alpha: float = 0.05,
        max_points: int | None = 2000,
        title: str = "Uncertainty Evaluation"
):
    """
    Compute NLL, ECE, and generate a confidence band plot.

    Parameters
    y_true : np.ndarray
        Ground truth values (N,)
    mu : np.ndarray
        Predicted mean values (N,)
    sigma : np.ndarray
        Predicted standard deviation values (N,)
    alpha : float, default=0.05
        Significance level for the confidence interval (0.05 -> 95% CI).
    max_points : int or None
        Max number of points to plot (subsample if dataset is large).
    title : str
        Title for the visualization.

    Returns
    metrics : dict
        Contains {"NLL": float, "ECE": float}
    fig, ax : matplotlib Figure and Axes
        The generated confidence band plot
    """

    nll = get_nll(y_true, mu, sigma)
    ece = get_ece(y_true, mu, sigma)

    metrics = {
        "NLL": float(nll),
        "ECE": float(ece),
    }

    fig, ax = plot_confidence_band(
        y_true=y_true,
        mu=mu,
        sigma=sigma,
        alpha=alpha,
        title=title,
        max_points=max_points,
    )

    return metrics, (fig, ax)
