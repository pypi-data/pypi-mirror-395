import numpy as np
import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt


def plot_confidence_band(
        y_true: np.ndarray,
        mu: np.ndarray,
        sigma: np.ndarray,
        alpha: float = 0.05,
        title: str = "Confidence Band Plot",
        max_points: int | None = 2000,
        random: bool = False
):
    """
    Visualize prediction uncertainty with a confidence band.

    Parameters
    y_true, mu, sigma : np.ndarray
        Arrays of shape (N,)
    alpha : float
        Significance level (0.05 → 95% CI)
    max_points : int or None
        Maximum points to display (subsamples if dataset is large)
    random : bool
        If True → random subsample, else → evenly spaced.

    Returns
    fig, ax
    """

    try:
        from scipy.stats import norm
    except ImportError:
        raise ImportError("SciPy required — install with: pip install uq-calculator[plot]")

    # Compute confidence interval
    z = norm.ppf(1 - alpha / 2)
    lower = mu - z * sigma
    upper = mu + z * sigma

    # Optional downsampling for visual clarity
    N = len(mu)
    if max_points is not None and N > max_points:
        if random:
            idx = np.random.choice(N, max_points, replace=False)
        else:
            idx = np.linspace(0, N - 1, max_points).astype(int)

        y_true = y_true[idx]
        mu = mu[idx]
        lower = lower[idx]
        upper = upper[idx]

    x = np.arange(len(mu))

    # Plot
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, y_true, "k.", markersize=2, label="True")
    ax.plot(x, mu, "b-", linewidth=1, label="Predicted Mean")
    ax.fill_between(x, lower, upper, color="blue", alpha=0.2,
                    label=f"{int((1 - alpha) * 100)}% CI")

    ax.set_title(title)
    ax.set_xlabel("Sample Index")
    ax.set_ylabel("Value")
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()

    return fig, ax
