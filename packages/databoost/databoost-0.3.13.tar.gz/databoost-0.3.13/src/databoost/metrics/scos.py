import numpy as np

def ScoS(y_true, y_pred, method="linear", factor=None, input_type="numerical", classes_dict=None):
    """
    Scolz's Distance Score (ScoS)
    -----------------------------
    Computes the mean ordinal distance between predictions and true labels,
    penalizing errors according to the chosen scaling method.

    Supports both numerical and raw (categorical) labels. When using raw labels,
    the provided mapping must assign *integer values* to ensure consistent distance logic.

    Parameters
    ----------
    y_true : array-like
        True labels (numeric or raw).
    y_pred : array-like
        Predicted labels (numeric or raw).
    method : str, default="linear"
        Scaling method for error distance:
        - "linear"    → |diff|
        - "quadratic" → |diff|²
        - "sqrt"      → √|diff|
        - "log"       → log(1 + |diff|)
        - "custom"    → |diff|**factor
    factor : float, optional
        Exponent for "custom" method.
    input_type : str, default="numerical"
        Input type:
        - "numerical" : labels are numeric
        - "raw"       : labels mapped via `classes_dict`
    classes_dict : dict, optional
        Mapping from raw labels to integer values.
        Required if input_type="raw".

    Returns
    -------
    float
        Mean penalized distance (lower = better).

    Raises
    ------
    ValueError
        If input types mismatch, mapping is missing, or mapping values are not integers.

    Example
    -------
    >>> y_true = ["no", "yes", "absolutely"]
    >>> y_pred = ["yes", "yes", "no"]
    >>> mapping = {"no": 0, "yes": 1, "absolutely": 2}
    >>> ScoS(y_true, y_pred, method="quadratic", input_type="raw", classes_dict=mapping)
    1.0
    """

    # --- Validate input type ---
    if input_type not in ("numerical", "raw"):
        raise ValueError("input_type must be 'numerical' or 'raw'.")

    if input_type == "raw":
        if classes_dict is None:
            raise ValueError("For input_type='raw', you must provide a 'classes_dict'.")

        # Ensure all values are integers
        if not all(isinstance(v, int) for v in classes_dict.values()):
            raise ValueError("All values in classes_dict must be integers.")

        try:
            y_true = np.array([classes_dict[v] for v in y_true], dtype=float)
            y_pred = np.array([classes_dict[v] for v in y_pred], dtype=float)
        except KeyError as e:
            raise ValueError(f"Label '{e.args[0]}' not found in classes_dict.") from None
    else:
        y_true = np.asarray(y_true, dtype=float)
        y_pred = np.asarray(y_pred, dtype=float)

    if y_true.shape != y_pred.shape:
        raise ValueError("y_true and y_pred must have the same length.")

    # --- Compute absolute distances ---
    diff = np.abs(y_true - y_pred)

    # --- Apply scaling ---
    if method == "linear":
        weighted = diff
    elif method == "quadratic":
        weighted = diff ** 2
    elif method == "sqrt":
        weighted = np.sqrt(diff)
    elif method == "log":
        weighted = np.log1p(diff)
    elif method == "custom":
        if factor is None:
            raise ValueError("You must provide 'factor' when using method='custom'.")
        weighted = diff ** factor
    else:
        raise ValueError(f"Unknown method '{method}'.")

    return float(np.mean(weighted))
