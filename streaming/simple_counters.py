import time
import asyncio
import numpy as np


def counter(stop: int, updates_per_second: int) -> int:
    """Generates a sequence of numbers up to stop at a rate of updates_per_second."""

    for i in range(stop):
        time.sleep(1.0 / updates_per_second)
        yield i


def array_counter(stop: int, updates_per_second: int) -> np.ndarray:
    """Generates a sequence of numpy arrays filled with numbers up to stop at a rate of updates_per_second."""

    for i in range(stop):
        time.sleep(1.0 / updates_per_second)
        yield np.full((2, 2), i)


async def async_counter(stop: int, updates_per_second: int) -> int:
    """Asynchronously generates a sequence of numbers up to stop at a rate of updates_per_second."""

    for i in range(stop):
        await asyncio.sleep(1.0 / updates_per_second)
        yield i


async def async_array_counter(stop: int, updates_per_second: int) -> np.ndarray:
    """Asynchronously generates a sequence of numpy arrays up to stop at a rate of updates_per_second."""

    for i in range(stop):
        await asyncio.sleep(1.0 / updates_per_second)
        yield np.full((2, 2), i)


def array_sum(a: np.ndarray) -> float:
    """Sum the elements in the array."""
    return float(np.sum(a))


if __name__ == "__main__":

    # Test the regular generator functions
    stop = 10
    updates_per_second = 2

    for i in counter(stop, updates_per_second):
        print(i)

    for i in array_counter(stop, updates_per_second):
        print(i)

    # This helper function is needed to test the async generator functions
    async def async_test(stop, updates_per_second):
        async for i in async_counter(stop, updates_per_second):
            print(i)
            print(array_sum(i))

        async for i in async_array_counter(stop, updates_per_second):
            print(i)
            print(array_sum(i))

    # Test the async generator functions
    asyncio.run(async_test(stop, updates_per_second))
