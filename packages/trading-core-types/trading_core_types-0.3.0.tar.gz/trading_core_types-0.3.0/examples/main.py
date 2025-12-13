"""Example usage of trading-core-serdes."""

from datetime import datetime, timezone

from trading_core import (
    Asset,
    AssetWire,
    MarketQuote,
    MarketQuoteWire,
    Order,
    OrderType,
    OrderWire,
)


def main():
    # Example 1: Asset wire deserialization
    asset_wire_data = {
        "symbol": "AAPL",
        "currency": "USD",
        "exchange": "NASDAQ",
        "name": "Apple Inc.",
        "lotSize": 100,
        "tickSize": 0.01,
        "validFrom": 1609459200000,
    }

    asset_wire = AssetWire.model_validate(asset_wire_data)
    asset = Asset.from_wire(asset_wire)
    print(f"Asset: {asset.symbol} - {asset.name}")
    print(f"Valid from: {asset.valid_from}")

    # Convert back to wire format
    back_to_wire = asset.to_wire()
    print(f"Back to wire: {back_to_wire.model_dump(by_alias=True, exclude_none=True)}")
    print()

    # Example 2: Market quote
    quote_wire = MarketQuoteWire(
        symbol="AAPL",
        price=150.25,
        volume=1000000,
        totalVolume=5000000,
        timestamp=int(datetime.now(timezone.utc).timestamp() * 1000),
        bid=150.20,
        ask=150.30,
    )

    quote = MarketQuote.from_wire(quote_wire)
    print(f"Quote: {quote.symbol} @ ${quote.price}")
    print(f"Timestamp: {quote.timestamp}")
    print()

    # Example 3: Order
    order_wire = OrderWire(
        id="order-123",
        symbol="AAPL",
        side="BUY",
        effect="OPEN_LONG",
        type=OrderType.LIMIT,
        quantity=100,
        price=150.00,
        created=int(datetime.now(timezone.utc).timestamp() * 1000),
    )

    order = Order.from_wire(order_wire)
    print(f"Order: {order.side} {order.quantity} {order.symbol} @ ${order.price}")
    print(f"Created: {order.created}")

    # Serialize to JSON
    print(f"Order as JSON: {order_wire.model_dump_json(by_alias=True)}")


if __name__ == "__main__":
    main()
