import os
import numpy as np

def get_mcd(model_or_path, x_data=None, n_samples=100, framework=None, safe_load=True):
    """
    Perform Monte Carlo Dropout (MCD) sampling with PyTorch or TensorFlow/Keras models.
    Detects model format and framework.

    Parameters:
    model_or_path : model object or str
        Either a loaded model object, or path to a model file/folder.
    x_data : array, tuple, or list
        Input data for prediction.
    n_samples : int
        Number of stochastic forward passes.
    framework : {'torch', 'tf', None}
        Framework information.
    safe_load : bool
        Try to safely open the model even if it’s from another Keras version.
    """

    model = model_or_path
    detected_fmt = None

    # Detect and load model from path
    if isinstance(model_or_path, str):
        path = model_or_path
        ext = os.path.splitext(path)[1].lower()
        is_dir = os.path.isdir(path)

        # Try to infer framework
        if framework is None:
            if ext in [".keras", ".h5"] or is_dir:
                framework = "tf"
            elif ext in [".pt", ".pth"]:
                framework = "torch"
            else:
                raise ValueError(f" Unknown model format: {path}")

        #  TensorFlow / Keras models
        if framework == "tf":
            import tensorflow as tf
            import keras

            if ext == ".keras":
                print(f" Detected Keras 3 format (.keras)")
                model = tf.keras.models.load_model(path, compile=False)
                detected_fmt = ".keras"

            elif ext == ".h5":
                print(f" Detected legacy Keras H5 model (.h5)")
                try:
                    model = tf.keras.models.load_model(path, compile=False)
                    detected_fmt = ".h5"
                except Exception as e:
                    if safe_load:
                        print(f" H5 load failed: {e}\nUsing TFSMLayer fallback...")
                        model = keras.layers.TFSMLayer(path, call_endpoint="serving_default")
                        detected_fmt = "TFSMLayer"
                    else:
                        raise

            elif is_dir:
                print(f" Detected TensorFlow SavedModel directory")
                model = keras.layers.TFSMLayer(path, call_endpoint="serving_default")
                detected_fmt = "SavedModel"

            else:
                raise ValueError(f" Unsupported TensorFlow model format: {path}")

        # PyTorch models
        elif framework == "torch":
            import torch
            print(f"Detected PyTorch model ({ext})")
            model = torch.load(path, map_location="cpu")
            detected_fmt = ext

    # Detect framework from loaded object
    if framework is None:
        # Try PyTorch
        try:
            import torch
            if isinstance(model, torch.nn.Module):
                framework = "torch"
        except ImportError:
            pass

        # Try TensorFlow / Keras
        if framework is None:
            try:
                import tensorflow as tf
                if isinstance(model, (tf.Module, tf.keras.Model)):
                    framework = "tf"
            except ImportError:
                pass

        # Still nothing?
        if framework is None:
            raise ValueError("Could not infer framework. Pass framework='torch' or 'tf'.")

    print(f" Loaded model using framework='{framework}' ({detected_fmt or 'object provided'})")

    # Run MC sampling
    preds = []

    if framework == "torch":
        import torch

        # Ensure x_data is a torch.Tensor
        if not torch.is_tensor(x_data):
            x_tensor = torch.as_tensor(x_data, dtype=torch.float32)
        else:
            x_tensor = x_data

        #  Move x_data + model to same device (if possible)
        try:
            device = next(model.parameters()).device
            model.to(device)
            x_tensor = x_tensor.to(device)
        except (StopIteration, AttributeError):
            device = torch.device("cpu")

        # Enable dropout for MC
        if hasattr(model, "train"):
            model.train()

        # Run MC sampling
        for _ in range(n_samples):
            with torch.no_grad():
                out = model(x_tensor)

            # Convert to numpy
            if hasattr(out, "detach"):
                out = out.detach().cpu().numpy()
            else:
                out = np.array(out)

            preds.append(out)


    elif framework == "tf":
        import tensorflow as tf
        for i in range(n_samples):
            out = model(x_data, training=True) # enable dropout
            out = out.numpy() if hasattr(out, "numpy") else np.array(out)
            preds.append(out)

    preds = np.stack(preds)
    mean_pred = np.mean(preds, axis=0)
    var_pred = np.var(preds, axis=0)
    #check preds
    #look into aleatoric

    print(f" Completed {n_samples} MC passes.")
    print(f" Output shapes → mean: {mean_pred.shape}, var: {var_pred.shape}")
    return mean_pred, var_pred, preds

