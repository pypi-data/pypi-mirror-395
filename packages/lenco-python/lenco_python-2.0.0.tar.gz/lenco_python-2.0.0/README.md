# lenco-python

Python SDK for Lenco API - Payments, Transfers, Collections

## Installation

```bash
pip install lenco-python
# or
poetry add lenco-python
```

## Quick Start

```python
from lenco import Lenco

client = Lenco(
    api_key="your-api-key",
    environment="production"  # or "sandbox"
)

# Get accounts
accounts = client.accounts.list()

# Transfer to bank account
transfer = client.transfers.to_bank_account(
    account_id="your-account-uuid",
    account_number="0123456789",
    bank_id="bank-uuid",
    amount=10000,
    reference="payment-001",
    narration="Payment for services"
)

# Collect via mobile money
collection = client.collections.from_mobile_money(
    amount=5000,
    reference="order-123",
    phone="0971234567",
    operator="airtel",
    country="zm"
)
```

## Async Support

```python
import asyncio
from lenco import AsyncLenco

async def main():
    client = AsyncLenco(api_key="your-api-key")
    
    # Concurrent requests
    accounts, banks = await asyncio.gather(
        client.accounts.list(),
        client.banks.list(country="ng")
    )
    
    print(f"Found {len(accounts)} accounts")
    print(f"Found {len(banks)} banks")

asyncio.run(main())
```

## Features

- [x] Full type hints support
- [x] Sync and async clients
- [x] Accounts, Banks, Transfers, Collections, Settlements, Transactions APIs
- [x] Webhook signature verification
- [x] Automatic retries with exponential backoff
- [x] Pydantic models for request/response validation

## Documentation

Full API documentation available at [docs.lenco.co](https://docs.lenco.co)

## Author

Alexander Asomba ([@alexasomba](https://github.com/alexasomba)) · [𝕏 @alexasomba](https://x.com/alexasomba)

## License

MIT
