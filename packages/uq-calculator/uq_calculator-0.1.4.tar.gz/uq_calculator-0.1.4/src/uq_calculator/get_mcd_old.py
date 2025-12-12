'''import numpy as np

def get_mcd(model, x_data, n_samples=100, framework="torch"):
    """
    Perform Monte Carlo (MC) sampling with dropout enabled during training.

    Parameters
    model : torch.nn.Module or tf.keras.Model or callable
        The model to sample from.
    x_data : array
        Input data for prediction.
    n_samples : int
        Number of MC forward passes.
    framework : str
        Either 'torch' or 'tf'
    Returns
    mean_pred : np.ndarray
        Mean prediction across MC samples.
    var_pred : np.ndarray
        Variance across MC samples.
    all_preds : np.ndarray
        All sampled predictions.
    """
    preds = []

    if framework == "torch":
        try:
            import torch
        except ImportError:
            raise ImportError("PyTorch is not installed. Please install torch to use framework='torch'.")

        # Switch to training mode
        if hasattr(model, "train"):
            model.train()

        with torch.no_grad():
            for _ in range(n_samples):
                out = model(x_data)
                # handle both Tensor and NumPy output
                if hasattr(out, "detach"):
                    out = out.detach().cpu().numpy()
                preds.append(np.array(out))

    elif framework == "tf":
        try:
            import tensorflow as tf
        except ImportError:
            raise ImportError("TensorFlow is not installed. Please install tensorflow to use framework='tf'.")

        for _ in range(n_samples):
            out = model(x_data, training=True)
            # handle Tensor and NumPy output
            if hasattr(out, "numpy"):
                out = out.numpy()
            preds.append(np.array(out))

    else:
        raise ValueError("framework must be either 'torch' or 'tf'.")

    preds = np.stack(preds)
    mean_pred = np.mean(preds, axis=0)
    var_pred = np.var(preds, axis=0)

    return mean_pred, var_pred, preds'''