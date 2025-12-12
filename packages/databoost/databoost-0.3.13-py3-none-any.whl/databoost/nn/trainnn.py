import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import torch.optim as optim

def train_nn(
    model: nn.Module,
    loss_fn: nn.modules.loss._Loss,
    optimizer: torch.optim.Optimizer,
    metric: callable,
    maximize_metric: bool,
    train_input: torch.Tensor,
    train_output: torch.Tensor,
    test_input: torch.Tensor,
    test_output: torch.Tensor,
    problem: str,
    epochs: int,
    patience: int = None,
    early_stopping: bool = False,
    random_seed: int = None,
    train_losses: list = None,
    test_losses: list = None,
    metrics: list = None,
    epochs_counter: list = None,
    verbose: int = 1,
    plot: bool = True
):
    """
    Train a PyTorch neural network with optional early stopping and plotting.

    This function handles training for regression, binary classification, and
    multiclass classification tasks. It supports tracking of training and test
    losses, custom metric evaluation, early stopping based on metric stagnation,
    and optional plotting of the training history.

    Parameters
    ----------
    model : nn.Module
        The PyTorch neural network model to train.
    loss_fn : nn.modules.loss._Loss
        Loss function used for training (e.g., nn.MSELoss(), nn.CrossEntropyLoss()).
    optimizer : torch.optim.Optimizer
        Optimizer for updating model parameters (e.g., torch.optim.Adam).
    metric : callable
        Function accepting (y_true, y_pred) and returning a numeric score for evaluation.
    maximize_metric : bool
        If True, training aims to maximize the metric; if False, aims to minimize it.
    train_input : torch.Tensor
        Input features for training.
    train_output : torch.Tensor
        Target outputs for training.
    test_input : torch.Tensor
        Input features for validation/testing.
    test_output : torch.Tensor
        Target outputs for validation/testing.
    problem : str
        Task type: "regression", "classification_binary", or "classification_multiclass".
    epochs : int
        Number of epochs to train in this call.
    patience : int or float, optional
        Number of epochs (or fraction of training epochs) without improvement
        to wait before triggering early stopping.
    early_stopping : bool, default False
        Whether to enable early stopping based on metric stagnation.
    random_seed : int, optional
        Random seed for reproducibility.
    train_losses : list, optional
        List to append training loss values per epoch.
    test_losses : list, optional
        List to append test/validation loss values per epoch.
    metrics : list, optional
        List to append metric values per epoch.
    epochs_counter : list, optional
        Single-element list storing cumulative number of epochs across multiple calls.
    verbose : int, default 1
        Verbosity level: 0 = silent, 1 = minimal, 2 = detailed.
    plot : bool, default True
        If True, plots training and validation loss and metric curves at the end.

    Returns
    -------
    A summary with the best metric, best epoch, last test loss and last metric (also early stop if triggered)

    Notes
    -----
    - The function automatically handles output transformation for classification
      (binary thresholding or argmax for multiclass).
    - Keeps track of the best metric and the corresponding epoch.
    - Early stopping is based on the selected metric and the `maximize_metric` flag.
    - Can be called multiple times to continue training; `epochs_counter` maintains
      cumulative epoch count.
    - Provides informative summary and plots at the end of training.
    """

    # ----------------- PARAMETER CHECKS -----------------
    if problem not in ["regression", "classification_binary", "classification_multiclass"]:
        raise ValueError("Invalid problem type. Must be 'regression', 'classification_binary', or 'classification_multiclass'.")

    if maximize_metric is None:
        maximize_metric = True

    if patience is not None and int(patience) != float(patience): # is fraction
      patience = round(epochs*patience)

    # ----------------- INITIALIZATION -----------------
    if random_seed is not None:
        torch.manual_seed(random_seed)

    train_losses = train_losses if train_losses is not None else []
    test_losses = test_losses if test_losses is not None else []
    metrics = metrics if metrics is not None else []
    epochs_counter = epochs_counter if epochs_counter is not None else [0]
    metr_funct = max if maximize_metric else min
    triggered = False

    starting_done_epochs = epochs_counter[0]

    digits = 4 if verbose == 1 else 6 if verbose == 2 else 3
    verb_print = 10 if verbose == 1 else epochs if verbose == 2 else 0

  
    try:
        # Attempt to get output and check its type and dimension
        initial_output = model(train_input)
        if isinstance(initial_output, (list, tuple)) and initial_output[-1].ndim == 1:
            only_output = False
        else:
            only_output = True
    except Exception: # Fallback if initial check fails, assume single tensor output
        only_output = True

    best_metric = float('-inf') if maximize_metric else float('inf')
    best_epoch = 0
    epochs_since_improve = 0

    # ----------------- TRAINING LOOP -----------------
    for epoch in range(epochs):
        # --- Forward & backward pass ---
        model.train()
        y_pred = model(train_input) if only_output else model(train_input)[-1]

        if problem == "regression":
            loss = loss_fn(y_pred, train_output)
        elif problem == "classification_binary":
            loss = loss_fn(y_pred, train_output.float())
        elif problem == "classification_multiclass":
            target = torch.argmax(train_output, dim=1) if train_output.ndim > 1 else train_output
            loss = loss_fn(y_pred, target)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        train_losses.append(loss.item())

        # --- Validation ---
        model.eval()
        with torch.no_grad():
            y_test_pred = model(test_input) if only_output else model(test_input)[-1]

            if problem == "regression":
                test_loss = float(loss_fn(y_test_pred, test_output).detach().numpy())
                metr = metric(test_output.detach().numpy(), y_test_pred.detach().numpy())
            elif problem == "classification_binary":
                test_loss = float(loss_fn(y_test_pred, test_output.float()).detach().numpy())
                y_pred_labels = (y_test_pred > 0.5).int()
                metr = metric(test_output.detach().numpy(), y_pred_labels.detach().numpy())
            elif problem == "classification_multiclass":
                y_true_labels = torch.argmax(test_output, dim=1).detach().numpy() if test_output.ndim > 1 else test_output.detach().numpy()
                y_pred_labels = torch.argmax(y_test_pred, dim=1).detach().numpy()
                test_loss = float(loss_fn(y_test_pred, torch.from_numpy(y_true_labels)).detach().numpy())
                metr = metric(y_true_labels, y_pred_labels)

            test_losses.append(test_loss)
            metrics.append(metr)

        epochs_counter[0] += 1

        # --- Early stopping logic ---
        improved = (metr > best_metric) if maximize_metric else (metr < best_metric)
        if improved:
            best_metric = metr_funct(metrics)
            best_epoch = epochs_counter[0] # Update best epoch to current cumulative epoch
            epochs_since_improve = 0 # Reset counter if metric improved
        else:
            epochs_since_improve += 1

        if early_stopping and patience is not None and epochs_since_improve >= patience:
            triggered = True
            break

        # --- Verbose print ---
        if (epoch % max(1, epochs // verb_print) == 0 or epoch == epochs-1) and verbose != 0:
            print(f"Epoch {epoch+starting_done_epochs+1} - Test Loss: {round(test_loss, digits)} - "
                  f"Train Loss: {round(loss.item(), digits)} - Metric: {metr:.{digits}f}")

    # ----------------- PLOTTING -----------------
    if plot:
        plt.figure(figsize=(8,4))
        plt.plot(range(starting_done_epochs + 1, epochs_counter[0] + 1), train_losses, label="Train Loss", color="green")
        plt.plot(range(starting_done_epochs + 1, epochs_counter[0] + 1), test_losses, label="Test Loss", color="red")
        plt.title("Loss over epochs")
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.grid(True)
        plt.legend()
        plt.show()

        plt.figure(figsize=(8,4))
        plt.plot(range(starting_done_epochs + 1, epochs_counter[0] + 1), metrics, color="blue", label="Metric")
        plt.title("Metric over epochs")
        plt.xlabel("Epoch")
        plt.ylabel("Metric")
        plt.grid(True)
        plt.legend()
        plt.show()

    # ----------------- SUMMARY -----------------
    print(f"\n\n--------- SUMMARY {'(Early stopped)' if triggered else ''} ---------\n\nFinished training at epoch {epochs_counter[0]} starting from {starting_done_epochs} (trained for {epoch+1} epochs in this call)")
    if triggered:
      print(f"Early stopping triggered at epoch {epochs_counter[0]}")
    print(f"\nBest metric: {best_metric:.{digits}f} at epoch {best_epoch}")

    last_test_loss = test_losses[-1] if test_losses else None
    last_metric = metrics[-1] if metrics else None

    print(f"\nLast model's loss: {round(last_test_loss, digits)}")
    print(f"Last model's metric: {last_metric:.{digits}f}")

    if patience is not None and not triggered:
        # Correctly find the epoch where the best metric was achieved
        best_metric_index = -1
        if maximize_metric:
            best_metric_val = float('-inf')
            for i, m in enumerate(metrics):
                if m > best_metric_val:
                    best_metric_val = m
                    best_metric_index = i
        else:
            best_metric_val = float('inf')
            for i, m in enumerate(metrics):
                if m < best_metric_val:
                    best_metric_val = m
                    best_metric_index = i

        if best_metric_index != -1:
            last_improve_epoch = starting_done_epochs + best_metric_index + 1
            epochs_since_last_improve = epochs_counter[0] - last_improve_epoch

            if epochs_since_last_improve >= patience:
                print(f"\nMetric hasn't improved in the last {epochs_since_last_improve} epochs, consider finishing training")
            else:
                print(f"\nMetric has improved in the last {epochs_since_last_improve} epochs, consider continuing training")
        else:
            print("Could not determine epoch of last improvement.")
