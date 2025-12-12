import torch
import matplotlib.pyplot as plt
import numpy as np

def show_forward_pass(model, x_input, percentile=None, show_connections=True, weighted=True):
    """
    Visualize the forward activations of a neural network with a red–white–green scale,
    optionally including weighted connections based on layer weights.

    Each neuron is represented as a circle; its color encodes the activation value:
        - Red   → activation < 0
        - White → activation ≈ 0
        - Green → activation > 0
        - Saturation proportional to |activation|
        - If `percentile` is set, only neurons >= that percentile are colored; others are white.

    Connections (if enabled):
        - Gray → show structural connection
        - If `weighted=True`: color and thickness represent the mean weight:
            • Green → positive weight
            • Red   → negative weight
            • Linewidth proportional to |weight|

    Parameters
    ----------
    model : torch.nn.Module
        Neural network to visualize. Must return either a tensor or a sequence
        of tensors corresponding to layer activations.

    x_input : torch.Tensor or np.ndarray
        Input vector or batch of inputs. If a single sample, it is unsqueezed
        before being passed through the model.

    percentile : float, optional
        Percentile threshold (0–100). Only activations above this value are shown
        in color; others appear white.

    show_connections : bool, default=True
        Whether to draw lines connecting neurons between adjacent layers.

    weighted : bool, default=True
        If True, connection color and width reflect the average weight of each
        layer (only works for `torch.nn.Linear` layers).

    Notes
    -----
    - Background: light gray figure with slightly darker axes.
    - The visualization is schematic: neurons are evenly spaced, weights are averaged
      if dimensions mismatch.
    - Works best with fully connected feed-forward networks.

    Example
    -------
    >>> x = torch.randn(4)
    >>> show_forward_pass(model, x, percentile=80, weighted=True)
    """

    # Setup figure and gray backgrounds
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor("#f0f0f0")
    ax.set_facecolor("#e0e0e0")

    model.eval()
    with torch.inference_mode():
        acts = model(x_input.unsqueeze(0)) if x_input.ndim == 1 else model(x_input)

    if not isinstance(acts, (tuple, list)):
        acts = (acts,)

    # Gather activations (include input layer)
    input_vals = x_input.detach().cpu().numpy() if isinstance(x_input, torch.Tensor) else np.array(x_input)
    activations = [input_vals] + [
        a.detach().cpu().numpy()[0] if a.ndim == 2 else a.detach().cpu().numpy()
        for a in acts
    ]

    layer_names = ["input"] + [f"hidden{i+1}" for i in range(len(activations) - 2)] + ["output"]
    layer_neurons = [len(a) for a in activations]
    neuroni_lista = []

    # Extract weights if available
    weights = []
    for module in model.modules():
        if isinstance(module, torch.nn.Linear):
            weights.append(module.weight.detach().cpu().numpy())
    # weights[i] ≈ connection matrix from layer i → i+1

    # Plot neurons layer by layer
    for i, layer_vals in enumerate(activations):
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
                color = (1 - norm, 1, 1 - norm)  # green
            elif norm < 0:
                color = (1, 1 + norm, 1 + norm)  # red
            else:
                color = (1, 1, 1)

            ax.scatter(i, y, color=color, s=500, zorder=3, edgecolors="k", linewidths=0.5)
            neuroni_lista.append((i, y))

    # Plot connections
    if show_connections:
        for i in range(len(layer_neurons) - 1):
            current = [p for p in neuroni_lista if p[0] == i]
            nxt = [p for p in neuroni_lista if p[0] == i + 1]

            # Get weight matrix if available
            if weighted and i < len(weights):
                W = weights[i]
                W = np.mean(W, axis=0) if W.shape[0] != len(nxt) or W.shape[1] != len(current) else W
                max_w = np.max(np.abs(W)) + 1e-8
            else:
                W = None

            for j, (x1, y1) in enumerate(current):
                for k, (x2, y2) in enumerate(nxt):
                    if weighted and W is not None:
                        # handle dimensional mismatch
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
