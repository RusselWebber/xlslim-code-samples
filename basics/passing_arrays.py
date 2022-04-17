import statistics
from random import randrange
from typing import List


def basic_stats(data: List[float]) -> List[float]:
    """Returns a list of [mean, median, mode] of the supplied list."""
    return [mean(data), median(data), mode(data)]


def mean(data: List[float]) -> float:
    """Calculate the arithmetic mean of the numbers in the list."""
    return statistics.mean(data)


def median(data: List[float]) -> float:
    """Calculate the median of the numbers in the list."""
    return statistics.median(data)


def mode(data: List[float]) -> float:
    """Calculate the mode of the numbers in the list."""
    return statistics.mode(data)


if __name__ == "__main__":
    print(basic_stats([randrange(10) for _ in range(100)]))
