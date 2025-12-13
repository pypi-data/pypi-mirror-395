"""Tests for trading_core types."""

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from trading_core import (
    Asset,
    AssetWire,
    Fill,
    FillWire,
    LongPosition,
    LongPositionLot,
    LongPositionWire,
    MarketBar,
    MarketBarInterval,
    MarketBarWire,
    MarketQuote,
    MarketQuoteWire,
    MarketSnapshot,
    MarketSnapshotWire,
    Order,
    OrderState,
    OrderStateWire,
    OrderStatus,
    OrderType,
    OrderWire,
    Position,
    PositionWire,
)


def test_asset_wire_to_runtime():
    """Test Asset wire to runtime conversion."""
    wire = AssetWire(
        symbol="AAPL",
        currency="USD",
        exchange="NASDAQ",
        name="Apple Inc.",
        lotSize=100,
        tickSize=0.01,
        validFrom=1609459200000,
    )

    asset = Asset.from_wire(wire)

    assert asset.symbol == "AAPL"
    assert asset.currency == "USD"
    assert asset.exchange == "NASDAQ"
    assert asset.name == "Apple Inc."
    assert asset.lot_size == 100
    assert asset.tick_size == 0.01
    assert isinstance(asset.valid_from, datetime)
    assert asset.valid_from == datetime(
        2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc)


def test_asset_runtime_to_wire():
    """Test Asset runtime to wire conversion."""
    asset = Asset(
        symbol="GOOGL",
        currency="USD",
        lot_size=1,
        tick_size=0.01,
        valid_from=datetime(2021, 1, 1, tzinfo=timezone.utc),
    )

    wire = asset.to_wire()

    assert wire.symbol == "GOOGL"
    assert wire.currency == "USD"
    assert wire.lotSize == 1
    assert wire.tickSize == 0.01
    assert wire.validFrom == 1609459200000


def test_market_snapshot_conversion():
    """Test MarketSnapshot conversion."""
    wire = MarketSnapshotWire(
        price={"AAPL": 150.0, "GOOGL": 2800.0}, timestamp=1609459200000
    )

    snapshot = MarketSnapshot.from_wire(wire)

    assert snapshot.price["AAPL"] == 150.0
    assert snapshot.price["GOOGL"] == 2800.0
    assert isinstance(snapshot.timestamp, datetime)

    back_to_wire = snapshot.to_wire()
    assert back_to_wire.price == wire.price
    assert back_to_wire.timestamp == wire.timestamp


def test_market_quote_validation():
    """Test MarketQuote validation."""
    wire = MarketQuoteWire(
        symbol="AAPL",
        price=150.25,
        volume=1000000,
        timestamp=1609459200000,
        bid=150.20,
        ask=150.30,
    )

    quote = MarketQuote.from_wire(wire)

    assert quote.symbol == "AAPL"
    assert quote.price == 150.25
    assert quote.volume == 1000000
    assert quote.bid == 150.20
    assert quote.ask == 150.30


def test_market_bar_with_interval():
    """Test MarketBar with interval enum."""
    wire = MarketBarWire(
        symbol="AAPL",
        open=150.0,
        high=151.0,
        low=149.5,
        close=150.5,
        volume=1000000,
        timestamp=1609459200000,
        interval=MarketBarInterval.M5,
    )

    bar = MarketBar.from_wire(wire)

    assert bar.symbol == "AAPL"
    assert bar.interval == MarketBarInterval.M5
    assert bar.interval.value == "5m"


def test_order_discriminated_union():
    """Test Order with discriminated union (side/effect)."""
    buy_order = OrderWire(
        id="order-1",
        symbol="AAPL",
        side="BUY",
        effect="OPEN_LONG",
        type=OrderType.LIMIT,
        quantity=100,
        price=150.0,
    )

    order = Order.from_wire(buy_order)
    assert order.side == "BUY"
    assert order.effect == "OPEN_LONG"

    sell_order = OrderWire(
        id="order-2",
        symbol="AAPL",
        side="SELL",
        effect="CLOSE_LONG",
        type=OrderType.MARKET,
        quantity=50,
    )

    order2 = Order.from_wire(sell_order)
    assert order2.side == "SELL"
    assert order2.effect == "CLOSE_LONG"


def test_order_state_with_status():
    """Test OrderState with status."""
    wire = OrderStateWire(
        id="order-1",
        symbol="AAPL",
        side="BUY",
        effect="OPEN_LONG",
        type=OrderType.LIMIT,
        quantity=100,
        price=150.0,
        filledQuantity=50,
        remainingQuantity=50,
        status=OrderStatus.PARTIAL,
        modified=1609459200000,
    )

    state = OrderState.from_wire(wire)

    assert state.filled_quantity == 50
    assert state.remaining_quantity == 50
    assert state.status == OrderStatus.PARTIAL


def test_fill_conversion():
    """Test Fill wire to runtime conversion."""
    wire = FillWire(
        id="fill-1",
        orderId="order-1",
        symbol="AAPL",
        side="BUY",
        effect="OPEN_LONG",
        quantity=100,
        price=150.0,
        commission=1.0,
        created=1609459200000,
    )

    fill = Fill.from_wire(wire)

    assert fill.id == "fill-1"
    assert fill.order_id == "order-1"
    assert fill.quantity == 100
    assert fill.price == 150.0
    assert fill.commission == 1.0
    assert isinstance(fill.created, datetime)


def test_long_position_with_lots():
    """Test LongPosition with lots."""
    lot1 = LongPositionLot(quantity=50, price=150.0, totalCost=7500.0)
    lot2 = LongPositionLot(quantity=50, price=151.0, totalCost=7550.0)

    wire = LongPositionWire(
        quantity=100,
        totalCost=15050.0,
        realisedPnL=0.0,
        lots=[lot1, lot2],
        modified=1609459200000,
    )

    position = LongPosition.from_wire(wire)

    assert position.quantity == 100
    assert position.total_cost == 15050.0
    assert len(position.lots) == 2
    assert position.lots[0].price == 150.0
    assert position.lots[1].price == 151.0


def test_position_with_long_and_short():
    """Test Position with long and short positions."""
    long_pos = LongPositionWire(
        quantity=100,
        totalCost=15000.0,
        realisedPnL=0.0,
        lots=[LongPositionLot(quantity=100, price=150.0, totalCost=15000.0)],
        modified=1609459200000,
    )

    wire = PositionWire(
        cash=10000.0,
        long={"AAPL": long_pos},
        short=None,
        totalCommission=10.0,
        realisedPnL=100.0,
        modified=1609459200000,
    )

    position = Position.from_wire(wire)

    assert position.cash == 10000.0
    assert position.long is not None
    assert "AAPL" in position.long
    assert position.long["AAPL"].quantity == 100
    assert position.short is None
    assert position.total_commission == 10.0


def test_validation_error_on_invalid_data():
    """Test that validation errors are raised for invalid data."""
    with pytest.raises(ValidationError):
        # Missing required field
        AssetWire(symbol="AAPL")

    with pytest.raises(ValidationError):
        # Invalid enum value
        OrderWire(
            id="order-1",
            symbol="AAPL",
            side="BUY",
            effect="INVALID_EFFECT",
            type=OrderType.LIMIT,
            quantity=100,
        )


def test_json_serialization():
    """Test JSON serialization with camelCase."""
    order = OrderWire(
        id="order-1",
        symbol="AAPL",
        side="BUY",
        effect="OPEN_LONG",
        type=OrderType.LIMIT,
        quantity=100,
        price=150.0,
        stopPrice=149.0,
    )

    json_str = order.model_dump_json(by_alias=True)

    assert "stopPrice" in json_str
    assert "stop_price" not in json_str
