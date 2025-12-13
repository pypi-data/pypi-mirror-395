# Yafin

Unofficial [Yahoo!Ⓡ finance](https://finance.yahoo.com) Python API client.

- Not affiliated with Yahoo, Inc.
- Open source library that uses publicly available APIs.
- Intended for research, educational purposes and personal use only.
- Synchronous and asynchronous.
- Not returning pandas dataframes (because why?).
- Uses caching and utilizes singleton pattern in symbol class to save resources.
- Minimal and build on [curl-cffi](https://github.com/lexiforest/curl_cffi)
- Approx. 2x faster, than other Yahoo finance clients. Run the tests yourself - `make test-perf` (All tests running synchronously, returning pandas DataFrame and http responses are mocked.)

![test-perf](docs/test-perf.png)

**Installation**: `pip install yafin` for more details, see the [Documentation](https://lukinkratas.github.io/yafin/)

**Documentation and Examples**: [https://lukinkratas.github.io/yafin/](https://lukinkratas.github.io/yafin/)

## Quick Examples

### Symbol

```python
from yafin import Symbol

with Symbol('META') as meta:
    meta_1y_chart = meta.get_chart(interval='1d', period_range='1y')
```

### AsyncSymbol


```python
import asyncio
from yafin import AsyncSymbol

async def main() -> None:

    async with AsyncSymbol('META') as meta:
        meta_1y_chart = await meta.get_chart(interval='1d', period_range='1y')

if __name__ == '__main__':
    asyncio.run(main())
```

### Symbols

```python
from yafin import Symbols

with Symbols('META,AAPL') as meta_aapl:
    meta_aapl_1y_chart = meta_aapl.get_chart(interval='1d', period_range='1y')
```

For more details, see the [Examples](https://lukinkratas.github.io/yafin/examples/symbol/) section in documentation.
