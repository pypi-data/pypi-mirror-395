"""
Tetnus NumPy-compatible API.
Provides a NumPy-like interface for Tetnus tensors.
"""

from parquetframe import _rustic

from .. import Tensor

try:
    _rust_tetnus = _rustic.tetnus
except AttributeError:
    _rust_tetnus = None


# Creation functions
def array(object):
    """Create a tensor from a list or existing data."""
    return Tensor(object)


def zeros(shape):
    """Return a new tensor of given shape and type, filled with zeros."""
    if _rust_tetnus is not None:
        return Tensor(_rust_tetnus.zeros(shape))
    return Tensor(
        [0.0] * (shape[0] if isinstance(shape, list | tuple) and shape else 1)
    )


def ones(shape):
    """Return a new tensor of given shape and type, filled with ones."""
    if _rust_tetnus is not None:
        return Tensor(_rust_tetnus.ones(shape))
    return Tensor(
        [1.0] * (shape[0] if isinstance(shape, list | tuple) and shape else 1)
    )


def arange(start, stop=None, step=1.0):
    """Return evenly spaced values within a given interval."""
    if stop is None:
        stop = start
        start = 0.0
    if _rust_tetnus is not None:
        return Tensor(_rust_tetnus.arange(float(start), float(stop), float(step)))
    return Tensor([0.0])  # Mock


def linspace(start, stop, num=50):
    """Return evenly spaced numbers over a specified interval."""
    if _rust_tetnus is not None:
        return Tensor(_rust_tetnus.linspace(float(start), float(stop), int(num)))
    return Tensor([0.0])  # Mock


def eye(n, m=None):
    """Return a 2-D tensor with ones on the diagonal and zeros elsewhere."""
    if _rust_tetnus is not None:
        return Tensor(_rust_tetnus.eye(int(n), int(m) if m is not None else None))
    return Tensor([0.0])  # Mock


def rand(*shape):
    """Random values in a given shape."""
    if len(shape) == 1 and isinstance(shape[0], list | tuple):
        shape = shape[0]
    if _rust_tetnus is not None:
        return Tensor(_rust_tetnus.rand(list(shape)))
    return Tensor([0.0])  # Mock


def randn(*shape):
    """Return a sample (or samples) from the \"standard normal\" distribution."""
    if len(shape) == 1 and isinstance(shape[0], list | tuple):
        shape = shape[0]
    if _rust_tetnus is not None:
        return Tensor(_rust_tetnus.randn(list(shape)))
    return Tensor([0.0])  # Mock


def full(shape, value):
    """Return a new tensor of given shape and type, filled with fill_value."""
    if not isinstance(shape, list | tuple):
        shape = [shape]
    if _rust_tetnus is not None:
        return Tensor(_rust_tetnus.full(list(shape), float(value)))
    return Tensor([float(value)])  # Mock


# Operations
def matmul(x1, x2):
    """Matrix product of two tensors."""
    if not isinstance(x1, Tensor):
        x1 = array(x1)
    if not isinstance(x2, Tensor):
        x2 = array(x2)
    return x1 @ x2


def add(x1, x2):
    """Add arguments element-wise."""
    if not isinstance(x1, Tensor):
        x1 = array(x1)
    if not isinstance(x2, Tensor):
        x2 = array(x2)
    return x1 + x2


def multiply(x1, x2):
    """Multiply arguments element-wise."""
    if not isinstance(x1, Tensor):
        x1 = array(x1)
    if not isinstance(x2, Tensor):
        x2 = array(x2)
    return x1 * x2


def reshape(a, newshape):
    """Gives a new shape to a tensor without changing its data."""
    if not isinstance(a, Tensor):
        a = array(a)
    return a.reshape(newshape)


def transpose(a):
    """Reverse or permute the axes of a tensor; returns the modified tensor."""
    if not isinstance(a, Tensor):
        a = array(a)
    return a.T()


def sum(a):
    """Sum of array elements."""
    if not isinstance(a, Tensor):
        a = array(a)
    return a.sum()


def sin(x):
    """Trigonometric sine, element-wise."""
    if not isinstance(x, Tensor):
        x = array(x)
    return x.sin()


def cos(x):
    """Cosine element-wise."""
    if not isinstance(x, Tensor):
        x = array(x)
    return x.cos()


def tan(x):
    """Compute tangent element-wise."""
    if not isinstance(x, Tensor):
        x = array(x)
    return x.tan()


def exp(x):
    """Calculate the exponential of all elements in the input tensor."""
    if not isinstance(x, Tensor):
        x = array(x)
    return x.exp()


def log(x):
    """Natural logarithm, element-wise."""
    if not isinstance(x, Tensor):
        x = array(x)
    return x.log()


def sqrt(x):
    """Return the non-negative square-root of an array, element-wise."""
    if not isinstance(x, Tensor):
        x = array(x)
    return x.sqrt()
