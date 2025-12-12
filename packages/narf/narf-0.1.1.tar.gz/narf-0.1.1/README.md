# Narf

**Narf** is a simple Python library for downloading historical cryptocurrency market data from Binance. Get klines (candlestick data), trades, and aggregated trades for spot and futures markets with just a few lines of code.

## Installation

```bash
pip install narf
```

## Quick Start

```python
from datetime import datetime
from narf.data import binance

# Load 1-minute klines for BTC/USDT futures (USD-M) from January 2023 to November 2025
df = binance.futures.um.klines.load("BTCUSDT", datetime(2023, 1, 1), datetime(2025, 11, 1))

# Load spot market aggregated trades for ETH/USDT with custom interval
df = binance.spot.aggTrades.load("ETHUSDT", datetime(2024, 1, 1), datetime(2024, 12, 31), interval="1h")

# Load data up to now (end date is optional)
df = binance.futures.um.klines.load("BTCUSDT", datetime(2024, 1, 1))
```

## Features

- **Simple API**: Intuitive interface for accessing Binance historical data
- **Date Range Support**: Load data for any date range with automatic month-by-month fetching
- **Automatic Caching**: Downloaded data is cached locally to avoid re-downloading
- **Pandas Integration**: Returns pandas DataFrames ready for analysis
- **Multiple Markets**: Support for spot, futures USD-M (UM), and futures Coin-M (CM)
- **Multiple Data Types**: Klines (candlestick), trades, and aggregated trades

## Available Markets

### Spot Market
```python
binance.spot.klines.load(symbol, start, end=None, interval="1m")
binance.spot.trades.load(symbol, start, end=None, interval="1m")
binance.spot.aggTrades.load(symbol, start, end=None, interval="1m")
```

### Futures Market - USD-M (UM)
```python
binance.futures.um.klines.load(symbol, start, end=None, interval="1m")
binance.futures.um.trades.load(symbol, start, end=None, interval="1m")
```

### Futures Market - Coin-M (CM)
```python
binance.futures.cm.klines.load(symbol, start, end=None, interval="1m")
binance.futures.cm.trades.load(symbol, start, end=None, interval="1m")
```

## Parameters

- **symbol**: Trading pair symbol (e.g., `"BTCUSDT"`, `"ETHUSDT"`)
- **start**: Start date as a `datetime` object (e.g., `datetime(2023, 1, 1)`)
- **end**: End date as a `datetime` object (optional, defaults to current date)
- **interval**: Time interval for klines (default: `"1m"`). Examples: `"1m"`, `"5m"`, `"1h"`, `"1d"`

## Supported Intervals

Common intervals include: `1m`, `3m`, `5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `6h`, `8h`, `12h`, `1d`, `3d`, `1w`, `1M`

## Data Format

All functions return pandas DataFrames with time-indexed data:

- **Klines**: Indexed by `open_time` with OHLCV (Open, High, Low, Close, Volume) columns
- **Trades**: Indexed by `timestamp` with trade details
- **Aggregated Trades**: Indexed by `timestamp` with aggregated trade information

## Examples

### Load multiple years of Bitcoin futures data

```python
from datetime import datetime
from narf.data import binance

# Load data from January 2023 to November 2025
df = binance.futures.um.klines.load("BTCUSDT", datetime(2023, 1, 1), datetime(2025, 11, 1))

print(df.head())
print(f"Total records: {len(df)}")
```

### Compare spot and futures prices

```python
from datetime import datetime
from narf.data import binance

start = datetime(2024, 1, 1)
end = datetime(2024, 12, 31)

spot = binance.spot.klines.load("BTCUSDT", start, end, interval="1d")
futures = binance.futures.um.klines.load("BTCUSDT", start, end, interval="1d")

# Compare closing prices
print(spot['close'].head())
print(futures['close'].head())
```

### Load recent data up to now

```python
from datetime import datetime
from narf.data import binance

# Load all data from January 2024 to now
df = binance.futures.um.klines.load("BTCUSDT", datetime(2024, 1, 1))
print(df.tail())
```

### Load aggregated trades for analysis

```python
from datetime import datetime
from narf.data import binance

# Load aggregated trades for a specific period
agg_trades = binance.spot.aggTrades.load(
    "ETHUSDT", 
    datetime(2024, 1, 1), 
    datetime(2024, 1, 31),
    interval="1h"
)
print(agg_trades.head())
```

## Caching

Narf automatically caches downloaded data in a local `cache/` directory. This means:
- First download: Data is fetched from Binance and saved
- Subsequent requests: Data is loaded from cache (much faster)

To clear the cache, simply delete the `cache/` directory.

## Requirements

- Python 3.12+
- pandas
- requests

## License

See the repository for license information.

## Links

- [GitHub Repository](https://github.com/numan-narf/narf-market-data)
- [Report Issues](https://github.com/numan-narf/narf-market-data/issues)
