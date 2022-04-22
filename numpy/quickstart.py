import numpy as np
from numpy.linalg import inv
from typing import List


def create_random_array(
    minimum: int = 0, maximum: int = 100, rows: int = 1, columns: int = 1
) -> np.ndarray:
    """Create a matrix of random integers between minimum and maximum with x rows and y columns."""
    return np.random.randint(minimum, maximum, size=(rows, columns))


def invert_array(x: np.ndarray) -> np.ndarray:
    """Compute the (multiplicative) inverse of a matrix."""
    return inv(x)


def echo_array(x: np.ndarray) -> np.ndarray:
    """Return the supplied array."""
    return x


def add_arrays(arrays: List[np.ndarray]) -> np.ndarray:
    """Add the supplied arrays."""
    s = None
    for a in arrays:
        if s is not None:
            s += a
        else:
            s = a
    return s


def multiply_arrays(arrays: List[np.ndarray]) -> np.ndarray:
    """Multiply the supplied arrays."""
    s = None
    for a in arrays:
        if s is not None:
            s *= a
        else:
            s = a
    return s


def add_two_arrays(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Add two arrays."""
    return a + b


if __name__ == "__main__":
    a = create_random_array(rows=10, columns=10)
    a_inv = invert_array(a)
    print(echo_array(a_inv))
