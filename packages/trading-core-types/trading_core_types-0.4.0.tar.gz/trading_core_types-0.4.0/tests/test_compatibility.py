"""Cross-language compatibility tests using shared JSON fixtures."""

import json
from pathlib import Path

from trading_core import (
    Asset,
    AssetWire,
    Fill,
    FillWire,
    MarketBar,
    MarketBarWire,
    MarketQuote,
    MarketQuoteWire,
    Order,
    OrderState,
    OrderStateWire,
    OrderWire,
    Position,
    PositionWire,
)

FIXTURES_DIR = Path(__file__).parent.parent.parent / "fixtures"


def load_fixture(filename: str) -> dict:
    """Load a JSON fixture file."""
    with open(FIXTURES_DIR / filename) as f:
        return json.load(f)


def test_asset_wire_compatibility():
    """Test Asset wire format compatibility with TypeScript."""
    data = load_fixture("asset.json")
    wire = AssetWire.model_validate(data)

    assert wire.symbol == "AAPL"
    assert wire.currency == "USD"
    assert wire.exchange == "NASDAQ"
    assert wire.lotSize == 100
    assert wire.tickSize == 0.01
    assert wire.validFrom == 1609459200000

    asset = Asset.from_wire(wire)
    assert asset.symbol == "AAPL"
    assert asset.valid_from.timestamp() == 1609459200.0

    # Round-trip test
    back_to_wire = asset.to_wire()
    serialized = back_to_wire.model_dump(by_alias=True, exclude_none=True)
    assert serialized["symbol"] == data["symbol"]
    assert serialized["validFrom"] == data["validFrom"]


def test_market_quote_wire_compatibility():
    """Test MarketQuote wire format compatibility with TypeScript."""
    data = load_fixture("market_quote.json")
    wire = MarketQuoteWire.model_validate(data)

    assert wire.symbol == "AAPL"
    assert wire.price == 150.25
    assert wire.volume == 1000000
    assert wire.bid == 150.20
    assert wire.ask == 150.30

    quote = MarketQuote.from_wire(wire)
    assert quote.symbol == "AAPL"
    assert quote.price == 150.25

    # Round-trip test
    back_to_wire = quote.to_wire()
    serialized = back_to_wire.model_dump(by_alias=True)
    assert serialized["symbol"] == data["symbol"]
    assert serialized["totalVolume"] == data["totalVolume"]
    assert serialized["bidVol"] == data["bidVol"]


def test_market_bar_wire_compatibility():
    """Test MarketBar wire format compatibility with TypeScript."""
    data = load_fixture("market_bar.json")
    wire = MarketBarWire.model_validate(data)

    assert wire.symbol == "GOOGL"
    assert wire.open == 2800.00
    assert wire.high == 2850.00
    assert wire.low == 2795.00
    assert wire.close == 2835.50
    assert wire.interval.value == "5m"

    bar = MarketBar.from_wire(wire)
    assert bar.symbol == "GOOGL"
    assert bar.close == 2835.50

    # Round-trip test
    back_to_wire = bar.to_wire()
    serialized = back_to_wire.model_dump(by_alias=True)
    assert serialized["symbol"] == data["symbol"]
    assert serialized["interval"] == data["interval"]


def test_order_wire_compatibility():
    """Test Order wire format compatibility with TypeScript."""
    data = load_fixture("order.json")
    wire = OrderWire.model_validate(data)

    assert wire.id == "order-12345"
    assert wire.symbol == "TSLA"
    assert wire.side == "BUY"
    assert wire.effect == "OPEN_LONG"
    assert wire.quantity == 100
    assert wire.price == 250.50

    order = Order.from_wire(wire)
    assert order.id == "order-12345"
    assert order.side == "BUY"

    # Round-trip test
    back_to_wire = order.to_wire()
    serialized = back_to_wire.model_dump(by_alias=True, exclude_none=True)
    assert serialized["id"] == data["id"]
    assert serialized["side"] == data["side"]
    assert serialized["effect"] == data["effect"]


def test_order_state_wire_compatibility():
    """Test OrderState wire format compatibility with TypeScript."""
    data = load_fixture("order_state.json")
    wire = OrderStateWire.model_validate(data)

    assert wire.id == "order-12345"
    assert wire.filledQuantity == 50
    assert wire.remainingQuantity == 50
    assert wire.status.value == "PARTIAL"

    state = OrderState.from_wire(wire)
    assert state.filled_quantity == 50
    assert state.status.value == "PARTIAL"

    # Round-trip test
    back_to_wire = state.to_wire()
    serialized = back_to_wire.model_dump(by_alias=True, exclude_none=True)
    assert serialized["filledQuantity"] == data["filledQuantity"]
    assert serialized["remainingQuantity"] == data["remainingQuantity"]
    assert serialized["status"] == data["status"]


def test_fill_wire_compatibility():
    """Test Fill wire format compatibility with TypeScript."""
    data = load_fixture("fill.json")
    wire = FillWire.model_validate(data)

    assert wire.id == "fill-98765"
    assert wire.orderId == "order-12345"
    assert wire.quantity == 50
    assert wire.price == 250.50
    assert wire.commission == 2.50

    fill = Fill.from_wire(wire)
    assert fill.id == "fill-98765"
    assert fill.order_id == "order-12345"

    # Round-trip test
    back_to_wire = fill.to_wire()
    serialized = back_to_wire.model_dump(by_alias=True)
    assert serialized["orderId"] == data["orderId"]
    assert serialized["commission"] == data["commission"]


def test_position_wire_compatibility():
    """Test Position wire format compatibility with TypeScript."""
    data = load_fixture("position.json")
    wire = PositionWire.model_validate(data)

    assert wire.cash == 50000.00
    assert wire.long is not None
    assert "AAPL" in wire.long
    assert wire.long["AAPL"].quantity == 100
    assert len(wire.long["AAPL"].lots) == 2

    assert wire.short is not None
    assert "TSLA" in wire.short
    assert wire.short["TSLA"].quantity == 50

    position = Position.from_wire(wire)
    assert position.cash == 50000.00
    assert position.long is not None
    assert position.long["AAPL"].quantity == 100
    assert position.short is not None
    assert position.short["TSLA"].quantity == 50

    # Round-trip test
    back_to_wire = position.to_wire()
    serialized = back_to_wire.model_dump(by_alias=True, exclude_none=True)
    assert serialized["cash"] == data["cash"]
    assert serialized["totalCommission"] == data["totalCommission"]
    assert serialized["realisedPnL"] == data["realisedPnL"]
    assert "AAPL" in serialized["long"]
    assert "TSLA" in serialized["short"]


def test_python_to_ts_serialization():
    """Test that Python can serialize to TypeScript-compatible JSON."""
    # Create a complex position in Python
    from datetime import datetime, timezone

    from trading_core import (
        LongPosition,
        LongPositionLot,
        ShortPosition,
        ShortPositionLot,
    )

    long_pos = LongPosition(
        quantity=100,
        total_cost=15000.0,
        realised_pnl=100.0,
        lots=[
            LongPositionLot(quantity=100, price=150.0, totalCost=15000.0),
        ],
        modified=datetime(2021, 1, 1, tzinfo=timezone.utc),
    )

    short_pos = ShortPosition(
        quantity=50,
        total_proceeds=12500.0,
        realised_pnl=-50.0,
        lots=[
            ShortPositionLot(quantity=50, price=250.0, totalProceeds=12500.0),
        ],
        modified=datetime(2021, 1, 1, tzinfo=timezone.utc),
    )

    position = Position(
        cash=10000.0,
        long={"AAPL": long_pos},
        short={"TSLA": short_pos},
        total_commission=15.0,
        realised_pnl=50.0,
        modified=datetime(2021, 1, 1, tzinfo=timezone.utc),
    )

    # Serialize to wire format
    wire = position.to_wire()
    json_str = wire.model_dump_json(by_alias=True)
    data = json.loads(json_str)

    # Verify camelCase keys (TypeScript convention)
    assert "totalCommission" in data
    assert "realisedPnL" in data
    assert "totalCost" in data["long"]["AAPL"]
    assert "totalProceeds" in data["short"]["TSLA"]

    # Verify timestamps are in milliseconds
    assert isinstance(data["modified"], int)
    assert data["modified"] == 1609459200000

    # Verify TypeScript can parse it back
    parsed_wire = PositionWire.model_validate(data)
    parsed_position = Position.from_wire(parsed_wire)

    assert parsed_position.cash == position.cash
    assert parsed_position.total_commission == position.total_commission
