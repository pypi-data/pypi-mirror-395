"""
Neural Network module for Tetnus.
"""

from parquetframe import _rustic

from .. import Tensor

try:
    _rust_tetnus = _rustic.tetnus
except AttributeError:
    _rust_tetnus = None


class Module:
    """Base class for all neural network modules."""

    def __call__(self, *args, **kwargs):
        return self.forward(*args, **kwargs)

    def forward(self, *args, **kwargs):
        raise NotImplementedError

    def parameters(self):
        """Return list of parameters."""
        return []


class Linear(Module):
    """Applies a linear transformation to the incoming data: y = xA^T + b"""

    def __init__(self, in_features: int, out_features: int, bias: bool = True):
        self._inner = _rust_tetnus.nn.Linear(in_features, out_features, bias)
        self.in_features = in_features
        self.out_features = out_features

    def forward(self, input: Tensor) -> Tensor:
        if not isinstance(input, Tensor):
            raise TypeError("input must be a Tensor")

        # Call Rust forward with inner PyTensor
        out_rust = self._inner.forward(input._tensor)
        return Tensor(out_rust)

    def parameters(self):
        # Return wrapped Tensors
        return [Tensor(p) for p in self._inner.parameters()]

    def __repr__(self):
        return (
            f"Linear(in_features={self.in_features}, out_features={self.out_features})"
        )


class ReLU(Module):
    """Rectified Linear Unit"""

    def __init__(self):
        self._inner = _rust_tetnus.nn.ReLU()

    def forward(self, input: Tensor) -> Tensor:
        if not isinstance(input, Tensor):
            raise TypeError("input must be a Tensor")
        out_rust = self._inner.forward(input._tensor)
        return Tensor(out_rust)

    def __repr__(self):
        return "ReLU()"


class Embedding(Module):
    """Lookup table for embeddings."""

    def __init__(self, num_embeddings: int, embedding_dim: int):
        self._inner = _rust_tetnus.nn.Embedding(num_embeddings, embedding_dim)
        self.num_embeddings = num_embeddings
        self.embedding_dim = embedding_dim

    def forward(self, input: Tensor) -> Tensor:
        if not isinstance(input, Tensor):
            raise TypeError("input must be a Tensor")
        out_rust = self._inner.forward(input._tensor)
        return Tensor(out_rust)

    def parameters(self):
        return [Tensor(p) for p in self._inner.parameters()]

    def __repr__(self):
        return f"Embedding(num_embeddings={self.num_embeddings}, embedding_dim={self.embedding_dim})"


class LayerNorm(Module):
    """Applies Layer Normalization over a mini-batch of inputs."""

    def __init__(self, normalized_shape: list[int], eps: float = 1e-5):
        self._inner = _rust_tetnus.nn.LayerNorm(normalized_shape, eps)
        self.normalized_shape = normalized_shape
        self.eps = eps

    def forward(self, input: Tensor) -> Tensor:
        if not isinstance(input, Tensor):
            raise TypeError("input must be a Tensor")
        out_rust = self._inner.forward(input._tensor)
        return Tensor(out_rust)

    def parameters(self):
        return [Tensor(p) for p in self._inner.parameters()]

    def __repr__(self):
        return f"LayerNorm(normalized_shape={self.normalized_shape}, eps={self.eps})"


class NumericalProcessor(Module):
    """Processor for numerical features (learnable normalization)."""

    def __init__(self):
        self._inner = _rust_tetnus.nn.NumericalProcessor()

    def forward(self, input: Tensor) -> Tensor:
        if not isinstance(input, Tensor):
            raise TypeError("input must be a Tensor")
        out_rust = self._inner.forward(input._tensor)
        return Tensor(out_rust)

    def parameters(self):
        return [Tensor(p) for p in self._inner.parameters()]

    def __repr__(self):
        return "NumericalProcessor()"


class CategoricalProcessor(Module):
    """Processor for categorical features (embedding lookup)."""

    def __init__(self, num_categories: int, embedding_dim: int):
        self._inner = _rust_tetnus.nn.CategoricalProcessor(
            num_categories, embedding_dim
        )
        self.num_categories = num_categories
        self.embedding_dim = embedding_dim

    def forward(self, input: Tensor) -> Tensor:
        if not isinstance(input, Tensor):
            raise TypeError("input must be a Tensor")
        out_rust = self._inner.forward(input._tensor)
        return Tensor(out_rust)

    def parameters(self):
        return [Tensor(p) for p in self._inner.parameters()]

    def __repr__(self):
        return f"CategoricalProcessor(num_categories={self.num_categories}, embedding_dim={self.embedding_dim})"


class Sequential(Module):
    """A sequential container."""

    def __init__(self, *args):
        self._inner = _rust_tetnus.nn.Sequential()
        self._modules = []
        for module in args:
            self.add(module)

    def add(self, module: Module):
        if not hasattr(module, "_inner"):
            raise TypeError("Sequential currently only supports Rust-backed modules")

        # Add to Rust sequential
        # Note: this copies/clones the module into Rust Sequential
        self._inner.add(module._inner)
        self._modules.append(module)

    def forward(self, input: Tensor) -> Tensor:
        if not isinstance(input, Tensor):
            raise TypeError("input must be a Tensor")
        out_rust = self._inner.forward(input._tensor)
        return Tensor(out_rust)

    def parameters(self):
        return [Tensor(p) for p in self._inner.parameters()]

    def __repr__(self):
        return "Sequential(\n  " + "\n  ".join(str(m) for m in self._modules) + "\n)"


class MSELoss(Module):
    """Mean Squared Error Loss."""

    def __init__(self):
        self._inner = _rust_tetnus.nn.MSELoss()

    def forward(self, input: Tensor, target: Tensor) -> Tensor:
        if not isinstance(input, Tensor) or not isinstance(target, Tensor):
            raise TypeError("input and target must be Tensors")
        out_rust = self._inner.forward(input._tensor, target._tensor)
        return Tensor(out_rust)

    def __repr__(self):
        return "MSELoss()"


class CrossEntropyLoss(Module):
    """Cross Entropy Loss."""

    def __init__(self):
        self._inner = _rust_tetnus.nn.CrossEntropyLoss()

    def forward(self, input: Tensor, target: Tensor) -> Tensor:
        if not isinstance(input, Tensor) or not isinstance(target, Tensor):
            raise TypeError("input and target must be Tensors")
        out_rust = self._inner.forward(input._tensor, target._tensor)
        return Tensor(out_rust)

    def __repr__(self):
        return "CrossEntropyLoss()"
