from parquetframe import _rustic

try:
    _rust_tetnus = _rustic.tetnus
except AttributeError:
    _rust_tetnus = None


class SGD:
    """Stochastic Gradient Descent optimizer."""

    def __init__(self, params, lr=0.1, momentum=0.0):
        """
        Args:
            params: List of Tensors to optimize
            lr: Learning rate
            momentum: Momentum factor (default: 0)
        """
        # params must be list of Tensors
        # Extract inner tensors
        inner_params = [p._tensor for p in params]
        self._inner = _rust_tetnus.optim.SGD(inner_params, float(lr), float(momentum))

    def step(self):
        """Perform a single optimization step."""
        self._inner.step()

    def zero_grad(self):
        """Clear gradients of all parameters."""
        self._inner.zero_grad()


class Adam:
    """Adam optimizer."""

    def __init__(self, params, lr=0.001):
        """
        Args:
            params: List of Tensors to optimize
            lr: Learning rate
        """
        inner_params = [p._tensor for p in params]
        self._inner = _rust_tetnus.optim.Adam(inner_params, float(lr))

    def step(self):
        """Perform a single optimization step."""
        self._inner.step()

    def zero_grad(self):
        """Clear gradients of all parameters."""
        self._inner.zero_grad()
