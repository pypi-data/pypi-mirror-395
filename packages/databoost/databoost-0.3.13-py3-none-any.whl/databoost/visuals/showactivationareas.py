import torch
import matplotlib.pyplot as plt
import numpy as np

def show_activation_areas(model, class_inputs, percentile=None, only_hidden=False, show_connections=True, weighted=True):
    """
    Visualize the *average activations* of a neural network over a given input set (e.g. a class),
    using a red–white–green color scale and optionally weighted connections.

    Each neuron represents the *mean activation* across all samples in `class_inputs`.
    Node color encodes the average activation value:
        - Red   → activation < 0
        - White → activation ≈ 0
        - Green → activation > 0
        - Saturation ∝ |activation|
        - If `percentile` is set, only neurons above threshold are colored; others are white.

    Connections (if enabled):
        - Gray → generic structural connection
        - If `weighted=True`: color and width reflect the *average weight* magnitude:
            • Green → positive weight
            • Red   → negative weight
            • Linewidth ∝ |weight|

    Parameters
    ----------
    model : torch.nn.Module
        Neural network to visualize. Its `forward` method must return either a tensor
        or a sequence of tensors representing activations of each layer.

    class_inputs : torch.Tensor
        Batch of input samples (N, input_dim), typically belonging to the same class.
        The function computes the mean activation over this batch.

    percentile : float, optional
        Activation percentile threshold (0–100). Only neurons above this value are
        colored by activation. Others appear white. If None, all neurons are colored.

    only_hidden : bool, default=False
        If True, display only hidden layers (omit input and output layers).

    show_connections : bool, default=True
        Whether to draw neuron connections between adjacent layers.

    weighted : bool, default=True
        If True, connection color and width reflect layer weights (requires Linear layers).

    Notes
    -----
    - The background is light gray (`#f0f0f0`) for readability.
    - Works best with fully connected networks.
    - Connection visualization is illustrative, not topologically precise.

    Example
    -------
    >>> subset = X_train[y_train == 2]
    >>> show_activation_areas(model, subset, percentile=90, weighted=True)
    """

    # Setup figure
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor("#f0f0f0")
    ax.set_facecolor("#e0e0e0")

    model.eval()
    with torch.inference_mode():
        acts = model(class_inputs)
        if not isinstance(acts, (tuple, list)):
            acts = (acts,)

    # Average activations per layer
    avg_input = class_inputs.detach().cpu().numpy().mean(axis=0)
    avg_acts = [avg_input] + [
        a.detach().cpu().numpy().mean(axis=0) if a.ndim == 2 else a.detach().cpu().numpy()
        for a in acts
    ]

    # Optionally remove input/output layers
    if only_hidden:
        avg_acts = avg_acts[1:-1] if len(avg_acts) > 2 else avg_acts[1:]

    n_layers = len(avg_acts)
    n_hidden = n_layers - (0 if only_hidden else 2)
    layer_names = [f"hidden{i+1}" for i in range(n_hidden)]
    if not only_hidden:
        layer_names = ["input"] + layer_names + ["output"]

    layer_neurons = [len(a) for a in avg_acts]
    neuroni_lista = []

    # Extract weight matrices if possible
    weights = []
    for module in model.modules():
        if isinstance(module, torch.nn.Linear):
            weights.append(module.weight.detach().cpu().numpy())

    # Draw neurons
    for i, layer_vals in enumerate(avg_acts):
        n_neurons = len(layer_vals)
        coords_y = np.linspace(-n_neurons / 2, n_neurons / 2, n_neurons)
        max_abs = np.max(np.abs(layer_vals)) + 1e-8

        ax.text(i, n_neurons / 2 + 1, layer_names[i], fontsize=12, ha="center", va="bottom")

        if percentile is not None:
            thresh = np.percentile(layer_vals, percentile)

        for idx, y in enumerate(coords_y):
            val = layer_vals[idx]
            norm = np.clip(val / max_abs, -1, 1)

            if percentile is not None and val < thresh:
                color = (1, 1, 1)
            elif norm > 0:
                color = (1 - norm, 1, 1 - norm)
            elif norm < 0:
                color = (1, 1 + norm, 1 + norm)
            else:
                color = (1, 1, 1)

            ax.scatter(i, y, color=color, s=500, zorder=3, edgecolors="k", linewidths=0.5)
            neuroni_lista.append((i, y))

    # Draw weighted connections
    if show_connections:
        for i in range(len(layer_neurons) - 1):
            current = [p for p in neuroni_lista if p[0] == i]
            nxt = [p for p in neuroni_lista if p[0] == i + 1]

            if weighted and i < len(weights):
                W = weights[i]
                W = np.mean(W, axis=0) if W.shape[0] != len(nxt) or W.shape[1] != len(current) else W
                max_w = np.max(np.abs(W)) + 1e-8
            else:
                W = None

            for j, (x1, y1) in enumerate(current):
                for k, (x2, y2) in enumerate(nxt):
                    if weighted and W is not None:
                        w_val = W[k % W.shape[0]] if W.ndim == 1 else W[k % W.shape[0], j % W.shape[1]]
                        norm_w = np.clip(w_val / max_w, -1, 1)
                        lw = 0.3 + 1.5 * abs(norm_w)
                        if norm_w > 0:
                            color = (1 - norm_w, 1, 1 - norm_w)
                        elif norm_w < 0:
                            color = (1, 1 + norm_w, 1 + norm_w)
                        else:
                            color = "lightgray"
                    else:
                        color = "gray"
                        lw = 0.4

                    ax.plot([x1, x2], [y1, y2], color=color, lw=lw, zorder=1, alpha=0.9)

    ax.axis("off")
    plt.tight_layout()
    plt.show()
