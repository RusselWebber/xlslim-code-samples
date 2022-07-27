import time
import asyncio


def counter(stop: int, updates_per_second: int) -> int:
    """Generates a sequence of number up to stop at a rate of updates_per_second."""

    for i in range(stop):
        time.sleep(1.0 / updates_per_second)
        yield i


async def async_counter(stop: int, updates_per_second: int) -> int:
    """Asynchronously generates a sequence of number up to stop at a rate of updates_per_second."""

    for i in range(stop):
        await asyncio.sleep(1.0 / updates_per_second)
        yield i


if __name__ == "__main__":

    # Test the regular generator function
    stop = 100
    updates_per_second = 10
    for i in counter(stop, updates_per_second):
        print(i)

    # This helper function is needed to test the async generator function
    async def async_test(stop, updates_per_second):
        async for i in async_counter(stop, updates_per_second):
            print(i)

    # Test the async generator function
    asyncio.run(async_test(stop, updates_per_second))
