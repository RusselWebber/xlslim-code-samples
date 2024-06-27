import numpy as np
from numpy.linalg import inv
from typing import List, Optional


def create_random_array(
    minimum: Optional[int] = 0,
    maximum: Optional[int] = 100,
    rows: Optional[int] = 1,
    columns: Optional[int] = 1,
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

def create_random_row_vector(
    minimum: Optional[int] = 0,
    maximum: Optional[int] = 100,
    columns: Optional[int] = 1,
) -> np.ndarray:
    """Create a vector of random integers between minimum and maximum with x rows and y columns."""
    return np.random.randint(minimum, maximum, size=(1, columns))

def create_random_column_vector(
    minimum: Optional[int] = 0,
    maximum: Optional[int] = 100,
    rows: Optional[int] = 1,
) -> np.ndarray:
    """Create a vector of random integers between minimum and maximum with x rows and y columns."""
    return np.random.randint(minimum, maximum, size=(rows, 1))

def create_random_vector(
    minimum: Optional[int] = 0,
    maximum: Optional[int] = 100,
    n: Optional[int] = 1,
) -> np.ndarray:
    """Create a vector of random integers between minimum and maximum with x rows and y columns."""
    return np.random.randint(minimum, maximum, n)


if __name__ == "__main__":
    a = create_random_array(rows=10, columns=10)
    a_inv = invert_array(a)
    print(echo_array(a_inv))
    b =  create_random_row_vector(columns=3)
    print(b)
    c =  create_random_column_vector(rows=3)
    print(c)
    d = create_random_vector(n=5)
    print(d)