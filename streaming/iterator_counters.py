# These iterators are the same as the generators in simple_counters.py
# Usually generators are the simplest and most convenient way to define iterators
# however sometimes you need more control, in these cases iterators can be useful.
import time
import asyncio
import numpy as np


class Counter:
    def __init__(self, stop: int, updates_per_second: int) -> None:
        """Generates a sequence of numbers up to stop at a rate of updates_per_second."""
        self._stop = stop
        self._updates_per_second = updates_per_second
        self._i = 0

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self._i >= self._stop:
            raise StopIteration
        time.sleep(1.0 / self._updates_per_second)
        i = self._i
        self._i += 1
        return i


class ArrayCounter:
    def __init__(self, stop: int, updates_per_second: int) -> None:
        """Generates a sequence of numpy arrays filled with numbers up to stop at a rate of updates_per_second."""
        self._stop = stop
        self._updates_per_second = updates_per_second
        self._i = 0

    def __iter__(self):
        return self

    def __next__(self) -> np.ndarray:
        if self._i >= self._stop:
            raise StopIteration
        time.sleep(1.0 / self._updates_per_second)
        a = np.full((2, 2), self._i)
        self._i += 1
        return a


class AsyncCounter:
    def __init__(self, stop: int, updates_per_second: int) -> None:
        """Asynchronously generates a sequence of numbers up to stop at a rate of updates_per_second."""
        self._stop = stop
        self._updates_per_second = updates_per_second
        self._i = 0

    def __aiter__(self):
        return self

    async def __anext__(self) -> int:
        if self._i >= self._stop:
            raise StopAsyncIteration
        await asyncio.sleep(1.0 / self._updates_per_second)
        i = self._i
        self._i += 1
        return i


class AsyncArrayCounter:
    def __init__(self, stop: int, updates_per_second: int) -> None:
        """Asynchronously generates a sequence of numpy arrays up to stop at a rate of updates_per_second."""
        self._stop = stop
        self._updates_per_second = updates_per_second
        self._i = 0

    def __aiter__(self):
        return self

    async def __anext__(self) -> np.ndarray:
        if self._i >= self._stop:
            raise StopAsyncIteration
        await asyncio.sleep(1.0 / self._updates_per_second)
        a = np.full((2, 2), self._i)
        self._i += 1
        return a


def array_sum(a: np.ndarray) -> float:
    """Sum the elements in the array."""
    return float(np.sum(a))


if __name__ == "__main__":

    # Test the regular iterators
    stop = 10
    updates_per_second = 2

    for i in Counter(stop, updates_per_second):
        print(i)

    for i in ArrayCounter(stop, updates_per_second):
        print(i)
        print(array_sum(i))

    # This helper function is needed to test the async iterators
    async def async_test(stop, updates_per_second):
        async for i in AsyncCounter(stop, updates_per_second):
            print(i)

        async for i in AsyncArrayCounter(stop, updates_per_second):
            print(i)
            print(array_sum(i))

    # Test the async iterators
    asyncio.run(async_test(stop, updates_per_second))
