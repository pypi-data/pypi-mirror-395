# py_futuur_client

A Python package for developers and clients of [futuur.com](https://futuur.com) to communicate easily with the Futuur public API.

## Features

- Authenticated requests using your API keys
- Fetch available markets
- Retrieve specific market details
- Get order book for a market
- Fetch market outcomes

## Installation

```bash
pip install py_futuur_client
```

Or if using your local copy:

```bash
pip install -e .
```

## Usage Example

```python
from py_futuur_client.client import Client

# Replace with your real credentials
client = Client(public_key='your_public_key', private_key='your_private_key')

# Fetch latest markets
markets = client.market.list()
print(markets)

# Fetch details for a specific market
market = client.market.get(market_id=12345)
print(market)
```

## Documentation

- The main entrypoint is the `Client` class.
- Each method corresponds to a Futuur public API endpoint.
- All methods return the API response parsed as Python dictionaries.

For more details, see the source code and method docstrings.
