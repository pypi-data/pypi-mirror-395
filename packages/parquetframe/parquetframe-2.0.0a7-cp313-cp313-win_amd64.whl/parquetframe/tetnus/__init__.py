"""
Tetnus: DataFrame-Native ML Framework

A high-performance machine learning framework built on Arrow-native tensors
with automatic differentiation.
"""

# Core tensor operations
# Core tensor operations
import numpy as np

from parquetframe import _rustic

# Access the Rust submodule
try:
    _rust_tetnus = _rustic.tetnus
    _RustTensor = _rust_tetnus.Tensor
except AttributeError:
    # Fallback for when extension is not compiled/available (e.g. during linting)
    _rust_tetnus = None
    _RustTensor = None


# Tensor class wrapper
class Tensor:
    """
    High-level Tensor wrapper providing NumPy-like interface. Examples:
        >>> import parquetframe.tetnus as pt
        >>> a = pt.Tensor.zeros([2, 3])
        >>> b = pt.Tensor.ones([3, 2])
        >>> c = a @ b  # Matrix multiplication
        >>> c.sum().backward()  # Compute gradients
    """

    def __init__(self, data, shape=None):
        """
        Create tensor from data. Args:
            data: List or nested list of numbers
            shape: Optional shape (inferred if not provided)
        """
        if isinstance(data, list):
            if shape is None:
                # Infer shape from nested list
                shape = self._infer_shape(data)
            if _rust_tetnus is not None:
                self._tensor = _rust_tetnus.from_list(data, shape)
            else:
                # Mock tensor for when Rust extension is missing
                self._tensor = None
                self._data = data
                self._shape = shape or self._infer_shape(data)
        else:
            # Assume it's already a Rust tensor
            self._tensor = data

    @staticmethod
    def _infer_shape(data):
        """Infer shape from nested list."""
        shape = []
        current = data
        while isinstance(current, list):
            shape.append(len(current))
            if current:
                current = current[0]
            else:
                break
        return shape

    @staticmethod
    def zeros(shape):
        """Create tensor filled with zeros."""
        if _rust_tetnus is not None:
            return Tensor(_rust_tetnus.zeros(shape))
        return Tensor([0.0] * (shape[0] if shape else 1))  # Mock implementation

    @staticmethod
    def ones(shape):
        """Create tensor filled with ones."""
        if _rust_tetnus is not None:
            return Tensor(_rust_tetnus.ones(shape))
        return Tensor([1.0] * (shape[0] if shape else 1))  # Mock implementation

    @staticmethod
    def randn(*shape):
        """Create tensor with random values from standard normal distribution."""
        if len(shape) == 1 and isinstance(shape[0], list | tuple):
            shape = shape[0]
        return Tensor(_rust_tetnus.randn(list(shape)))

    @staticmethod
    def linspace(start, stop, num=50):
        """Create tensor with linearly spaced values."""
        return Tensor(_rust_tetnus.linspace(float(start), float(stop), int(num)))

    @property
    def shape(self):
        """Tensor shape."""
        if self._tensor is not None:
            return tuple(self._tensor.shape)
        return tuple(self._shape) if hasattr(self, "_shape") else ()

    @property
    def ndim(self):
        """Number of dimensions."""
        if self._tensor is not None:
            return self._tensor.ndim
        return len(self.shape)

    @property
    def size(self):
        """Total number of elements."""
        if self._tensor is not None:
            return self._tensor.numel
        # Calculate size from shape
        s = 1
        for d in self.shape:
            s *= d
        return s

    @property
    def grad(self):
        """Gradient tensor (if computed)."""
        if self._tensor is not None:
            grad_tensor = self._tensor.grad
            if grad_tensor is None:
                return None
            return Tensor(grad_tensor)
        return None

    @property
    def requires_grad(self):
        """Whether this tensor requires gradient."""
        if self._tensor is not None:
            return self._tensor.requires_grad
        return False

    def requires_grad_(self):
        """Enable gradient tracking (in-place)."""
        if self._tensor is not None:
            self._tensor = self._tensor.requires_grad_()
        return self

    def data(self):
        """Get tensor data as Python list."""
        if self._tensor is not None:
            return self._tensor.data()
        return self._data if hasattr(self, "_data") else []

    def backward(self):
        """Compute gradients via backpropagation."""
        if self._tensor is not None:
            _rust_tetnus.backward(self._tensor)
        # No-op for mock

    def to_numpy(self):
        """Convert to NumPy array."""
        if self._tensor is not None:
            return self._tensor.to_numpy()
        return np.array(self._data)

    # Operations
    def __matmul__(self, other):
        """Matrix multiplication: a @ b"""
        if self._tensor is not None:
            result = _rust_tetnus.matmul(self._tensor, other._tensor)
            return Tensor(result)
        # Mock implementation
        return Tensor.zeros([self.shape[0], other.shape[1]])

    def __add__(self, other):
        """Element-wise addition: a + b"""
        if self._tensor is not None:
            result = _rust_tetnus.add(self._tensor, other._tensor)
            return Tensor(result)
        return Tensor.zeros(self.shape)

    def __sub__(self, other):
        """Element-wise subtraction: a - b"""
        if self._tensor is not None:
            result = _rust_tetnus.sub(self._tensor, other._tensor)
            return Tensor(result)
        return Tensor.zeros(self.shape)

    def __mul__(self, other):
        """Element-wise multiplication: a * b"""
        if self._tensor is not None:
            result = _rust_tetnus.mul(self._tensor, other._tensor)
            return Tensor(result)
        return Tensor.zeros(self.shape)

    def __truediv__(self, other):
        """Element-wise division: a / b"""
        if self._tensor is not None:
            result = _rust_tetnus.div(self._tensor, other._tensor)
            return Tensor(result)
        return Tensor.zeros(self.shape)

    def add(self, other):
        return self + other

    def sub(self, other):
        return self - other

    def mul(self, other):
        return self * other

    def div(self, other):
        return self / other

    def reshape(self, *shape):
        """Reshape tensor."""
        if len(shape) == 1 and isinstance(shape[0], list | tuple):
            shape = shape[0]
        if self._tensor is not None:
            result = _rust_tetnus.reshape(self._tensor, list(shape))
            return Tensor(result)
        return Tensor.zeros(list(shape))

    def T(self):
        """Transpose (2D tensors only)."""
        if self._tensor is not None:
            result = _rust_tetnus.transpose(self._tensor)
            return Tensor(result)
        if len(self.shape) == 2:
            return Tensor.zeros([self.shape[1], self.shape[0]])
        return Tensor.zeros(self.shape)

    def transpose(self, *args):
        """Transpose tensor. Currently alias for T() for 2D."""
        return self.T()

    def sum(self):
        """Sum all elements."""
        if self._tensor is not None:
            result = _rust_tetnus.sum(self._tensor)
            return Tensor(result)
        return Tensor.zeros([1])

    def mean(self):
        """Mean of all elements."""
        if self._tensor is not None:
            result = _rust_tetnus.mean(self._tensor)
            return Tensor(result)
        return Tensor.zeros([1])

    def sin(self):
        """Element-wise sine."""
        if self._tensor is not None:
            result = _rust_tetnus.sin(self._tensor)
            return Tensor(result)
        return Tensor.zeros(self.shape)

    def cos(self):
        """Element-wise cosine."""
        if self._tensor is not None:
            result = _rust_tetnus.cos(self._tensor)
            return Tensor(result)
        return Tensor.zeros(self.shape)

    def tan(self):
        """Element-wise tangent."""
        if self._tensor is not None:
            result = _rust_tetnus.tan(self._tensor)
            return Tensor(result)
        return Tensor.zeros(self.shape)

    def exp(self):
        """Element-wise exponential."""
        if self._tensor is not None:
            result = _rust_tetnus.exp(self._tensor)
            return Tensor(result)
        return Tensor.zeros(self.shape)

    def log(self):
        """Element-wise natural logarithm."""
        if self._tensor is not None:
            result = _rust_tetnus.log(self._tensor)
            return Tensor(result)
        return Tensor.zeros(self.shape)

    def sqrt(self):
        """Element-wise square root."""
        if self._tensor is not None:
            result = _rust_tetnus.sqrt(self._tensor)
            return Tensor(result)
        return Tensor.zeros(self.shape)

    def __repr__(self):
        return f"Tensor(shape={self.shape}, requires_grad={self.requires_grad})"


# Alias for NumPy-like API
if _rust_tetnus is not None:
    zeros = Tensor.zeros
    ones = Tensor.ones
else:
    zeros = Tensor.zeros
    ones = Tensor.ones


# New NumPy-compatible creation functions
def arange(start, stop, step=1.0):
    """Create tensor with evenly spaced values."""
    if _rust_tetnus is not None:
        return Tensor(_rust_tetnus.arange(float(start), float(stop), float(step)))
    return Tensor.zeros([1])  # Mock fallback


def linspace(start, stop, num=50):
    """Create tensor with linearly spaced values."""
    if _rust_tetnus is not None:
        return Tensor(_rust_tetnus.linspace(float(start), float(stop), int(num)))
    return Tensor.zeros([1])  # Mock fallback


def eye(n, m=None):
    """Create identity matrix."""
    if _rust_tetnus is not None:
        return Tensor(_rust_tetnus.eye(int(n), int(m) if m is not None else None))
    return Tensor.zeros([n, n])  # Mock fallback


def rand(*shape):
    """Create tensor filled with random values [0, 1)."""
    if len(shape) == 1 and isinstance(shape[0], list | tuple):
        shape = shape[0]
    if _rust_tetnus is not None:
        return Tensor(_rust_tetnus.rand(list(shape)))
    return Tensor.zeros(list(shape))  # Mock fallback


def randn(*shape):
    """Create tensor with random values from standard normal distribution."""
    if len(shape) == 1 and isinstance(shape[0], list | tuple):
        shape = shape[0]
    if _rust_tetnus is not None:
        return Tensor(_rust_tetnus.randn(list(shape)))
    return Tensor.zeros(list(shape))  # Mock fallback


def full(shape, value):
    """Create tensor filled with a constant value."""
    if not isinstance(shape, list | tuple):
        shape = [shape]
    if _rust_tetnus is not None:
        return Tensor(_rust_tetnus.full(list(shape), float(value)))
    return Tensor.zeros(list(shape))  # Mock fallback


# Neural network layers
from . import nn, optim  # noqa: E402

# High-level API
from .api import Model, dataframe_to_tensor  # noqa: E402

__all__ = [
    "Tensor",
    "zeros",
    "ones",
    "arange",
    "linspace",
    "eye",
    "rand",
    "randn",
    "full",
    "numpy",
    "nn",
    "optim",
    "Model",
    "dataframe_to_tensor",
]

# Expose submodules
# Expose submodules
# Expose graph module from Rust
# Expose submodules
# Expose graph module from Rust
import sys  # noqa: E402

from . import numpy  # noqa: E402

try:
    graph = _rust_tetnus.graph
    sys.modules["parquetframe.tetnus.graph"] = graph
except AttributeError:
    # Fallback or warning if graph module is not available
    pass

# Expose llm module from Rust
try:
    llm = _rust_tetnus.llm
    sys.modules["parquetframe.tetnus.llm"] = llm
except AttributeError:
    # Fallback or warning if llm module is not available
    pass

# Expose edge module from Rust
try:
    edge = _rust_tetnus.edge
    sys.modules["parquetframe.tetnus.edge"] = edge
except AttributeError:
    # Fallback or warning if edge module is not available
    pass

__all__.append("graph")
__all__.append("llm")
__all__.append("edge")

if Tensor is None:
    pass
