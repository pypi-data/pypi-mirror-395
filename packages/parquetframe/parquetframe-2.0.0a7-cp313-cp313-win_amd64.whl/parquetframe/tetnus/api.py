"""
High-level API for Tetnus ML framework.

Provides simple interfaces for model training and inference.
"""

import numpy as np


class Model:
    """
    High-level model wrapper for easy training.

    Example:
        >>> from parquetframe.tetnus import Model, nn
        >>> model = Model([
        ...     nn.Linear(784, 128),
        ...     nn.ReLU(),
        ...     nn.Linear(128, 10)
        ... ])
        >>> model.fit(X_train, y_train, epochs=10)
        >>> predictions = model.predict(X_test)
    """

    def __init__(self, layers: list):
        """
        Initialize model with layers.

        Args:
            layers: List of neural network layers
        """
        from parquetframe.tetnus.nn import Sequential

        self.model = Sequential(*layers)
        self._optimizer = None

    def fit(
        self,
        X,
        y,
        epochs: int = 10,
        lr: float = 0.01,
        batch_size: int | None = None,
        verbose: bool = True,
    ):
        """
        Train the model.

        Args:
            X: Input data (numpy array or Tensor)
            y: Target data (numpy array or Tensor)
            epochs: Number of training epochs
            lr: Learning rate
            batch_size: Batch size (None = full batch)
            verbose: Print training progress
        """
        from parquetframe.tetnus import Tensor
        from parquetframe.tetnus.nn import MSELoss
        from parquetframe.tetnus.optim import Adam

        # Convert to tensors if needed
        if isinstance(X, np.ndarray):
            X = Tensor(X.astype(np.float32))
        if isinstance(y, np.ndarray):
            y = Tensor(y.astype(np.float32))

        # Initialize optimizer
        if self._optimizer is None:
            self._optimizer = Adam(self.model.parameters(), lr=lr)

        loss_fn = MSELoss()

        for epoch in range(epochs):
            # Forward pass
            pred = self.model(X)
            loss = loss_fn(pred, y)

            # Backward pass
            loss.backward()
            self._optimizer.step()
            self._optimizer.zero_grad()

            if verbose and (epoch + 1) % max(1, epochs // 10) == 0:
                print(f"Epoch {epoch + 1}/{epochs}, Loss: {float(loss):.4f}")

    def predict(self, X):
        """
        Make predictions.

        Args:
            X: Input data

        Returns:
            Predictions as numpy array
        """
        from parquetframe.tetnus import Tensor

        if isinstance(X, np.ndarray):
            X = Tensor(X.astype(np.float32))

        pred = self.model(X)

        # Convert back to numpy
        if hasattr(pred, "numpy"):
            return pred.numpy()
        return np.array(pred)


def dataframe_to_tensor(df, columns=None):
    """
    Convert pandas DataFrame to Tensor.

    Args:
        df: pandas DataFrame
        columns: Optional list of columns to use

    Returns:
        Tensor

    Example:
        >>> import pandas as pd
        >>> from parquetframe.tetnus import dataframe_to_tensor
        >>> df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
        >>> tensor = dataframe_to_tensor(df)
    """
    from parquetframe.tetnus import Tensor

    if columns:
        data = df[columns].values
    else:
        data = df.values

    return Tensor(data.astype(np.float32))


__all__ = ["Model", "dataframe_to_tensor"]
