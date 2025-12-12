# trading-core-types

Python types for trading systems with Pydantic validation and JSON serialization.

## Installation

```bash
pip install trading-core-types
```

## Features

- Pydantic models for trading types
- Wire format (JSON) with camelCase fields
- Runtime format with snake_case fields and `datetime` objects
- Type-safe conversion between wire and runtime formats

## Usage

```python
from trading_core import Asset, AssetWire

# Deserialize from JSON/API (wire format)
asset_wire = AssetWire.model_validate({
    "symbol": "AAPL",
    "currency": "USD",
    "validFrom": 1609459200000  # Unix timestamp in ms
})

# Convert to runtime format
asset = Asset.from_wire(asset_wire)
print(asset.valid_from)  # datetime object

# Convert back to wire format
wire_data = asset.to_wire()
json_str = wire_data.model_dump_json(by_alias=True)
```

## Available Types

**Market Data:** `Asset`, `MarketSnapshot`, `MarketQuote`, `MarketBar`
**Orders:** `Order`, `OrderState`, `Fill`
**Positions:** `Position`, `LongPosition`, `ShortPosition`

Each type has a corresponding `*Wire` class for JSON serialization.

## Example

See [examples/main.py](examples/main.py) for complete usage examples.
