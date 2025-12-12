# py-futuur-client

A Python client library for developers and clients of [futuur.com](https://futuur.com) to interacting with the public Futuur API. This package provides easy-to-use classes to access market data, categories, user details, and trading endpoints (bets and orders).

## 🌟 Features

- **Secure Authentication**: Handles HMAC-SHA512 signing automatically using your private key.
- **Market Data**: Easily fetch lists of available markets, retrieve specific market details, and get real-time order book data.
- **User Information**: Retrieve personal account details and statistics using the `/me/` endpoint.
- **Category Navigation**: Access various category listings (featured, main, root) to organize markets.
- **Trading (Bets & Orders)**: Supports core trading actions including purchasing/selling positions and placing/cancelling Limit Orders.

## 🔑 Requirements

- Python 3.10+
- A Futuur Public API Key and Private Key (obtainable from your Account Settings in the "API" section).

## ⚙️ Installation

```bash
pip install py-futuur-client==1.0.2
```

## 🚀 Quick Start (How to Use)

### 1. Import and Instantiate the Client

The core **`Client`** class handles your API key authentication (HMAC signature) and manages connections to the different API groups.

```python
from py_futuur_client.client import Client

# IMPORTANT: Replace these placeholders with your actual keys
PUBLIC_KEY = 'YOUR_PUBLIC_KEY'
PRIVATE_KEY = 'YOUR_PRIVATE_KEY'

# Instantiate the client
client = Client(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY)
```

### 2. Interacting with Endpoint Groups

The client's architecture maps directly to the API documentation's groups, allowing you to access functionalities via simple dot notation (e.g., client.market for all market endpoints).

### 💰 Trading — Bets (.bet)

Interact wagers (.list, .purchase, .detail, .sell, .get_partial_amount_on_sell, .get_latest_purchase_actions, .get_current_rates, .simulate_purchase).

```python
# GET /api/v1/bets/
# Example: List your 10 most recent active bets (status=purchased)
active_bets = client.bet.list(params={'active': True, 'limit': 10})
print(f"You have {len(active_bets['results'])} active bets.")
```

### 🏷️ Categories (.category)

Interact with categories (.list, .get, .list_featured, .list_main, .list_root, .list_root_and_main_children).

```python
# GET /api/v1/categories/root/
# Fetch all top-level categories
root_categories = client.category.list_root()
print("Root Categories:")
for category in root_categories:
    print(f"  - {category['title']}")
```

### 📊 Market Data (.market)

Interact with market (.list, .detail, .get_order_book, .get_related_markets, .suggest_market)

```python
# GET /api/v1/markets/
# Example: Fetching the first 5 active markets
markets_list = client.market.list(params={
    'limit': 5,
    'resolved_only': False
})

print(f"Total active markets: {markets_list['pagination']['total']}")
for market in markets_list['results']:
    print(f"- ID {market['id']}: {market['title']}")
```

### 👤 User (.user)

Interact we user (.get_datails)

```python
# GET /api/v1/me/
my_details = client.user.get_details()
print(f"Logged in as: {my_details['username']}")
print(f"Play Money Wagers: {my_details['wagers_count_play_money']}")
```

### 📜 Trading — Limit Orders (.limit_order)

Interact with orders (.list, .create, .cancel).

```python
# POST /api/v1/orders/
# Place a BUY (bid) Limit Order
payload = {
    'outcome': 123,
    'currency': 'OOM',
    'shares': 0.2,
    'shares_requested': 0.2,
    'side': 'bid',
    'position': 'l'
}

try:
    new_order = client.limit_order.create(payload=payload)
    print(f"Limit Order created: ID {new_order['id']} at price {new_order['price']}")
except Exception as e:
    print(f"Failed to create order. Check payload fields: {e}")
```
