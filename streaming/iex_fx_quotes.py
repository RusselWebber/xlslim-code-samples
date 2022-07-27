# IEX offers financial data via their API
# The pyEX package wraps the API
import datetime
import asyncio
from typing import Any, List, Dict

# This can be installed using pip
# See https://github.com/timkpaine/pyEX
import pyEX

TEST_TOKEN = "Tpk_0021da5cdccd46deba3845de6206d238"


async def iex_fx_quote(symbol: str) -> Dict:
    """Get test FX quotes from IEX."""
    c = pyEX.Client(TEST_TOKEN, version="sandbox")
    async for data in c.streaming.fxSSEAsync(symbol):
        for d in data:
            yield d


def display_fx_quote(quote: Dict) -> List[Any]:
    """Reformat the quote dictionary."""
    return [
        quote["symbol"],
        # The timestamps from the test server are nonsense
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        quote["rate"],
    ]


async def main():
    async for x in iex_fx_quote("EURUSD"):
        print(display_fx_quote(x))


if __name__ == "__main__":
    asyncio.run(main())
