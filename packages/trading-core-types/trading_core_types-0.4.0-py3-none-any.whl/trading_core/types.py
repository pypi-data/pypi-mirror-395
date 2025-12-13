"""Core trading types with Pydantic validation."""

from datetime import datetime, timezone
from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel


def ms_to_datetime(ms: int) -> datetime:
    """Convert epoch milliseconds to datetime."""
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc)


def datetime_to_ms(dt: datetime) -> int:
    """Convert datetime to epoch milliseconds."""
    return int(dt.timestamp() * 1000)


# ============================================================================
# Asset
# ============================================================================


class AssetWire(BaseModel):
    """Wire format for Asset."""

    symbol: str
    type: Optional[str] = None
    name: Optional[str] = None
    exchange: Optional[str] = None
    currency: str
    lotSize: Optional[float] = None
    tickSize: Optional[float] = None
    validFrom: Optional[int] = None
    validUntil: Optional[int] = None

    model_config = {"populate_by_name": True, "extra": "allow"}


class Asset(BaseModel):
    """Runtime Asset type."""

    symbol: str
    type: Optional[str] = None
    name: Optional[str] = None
    exchange: Optional[str] = None
    currency: str
    lot_size: Optional[float] = None
    tick_size: Optional[float] = None
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None

    @classmethod
    def from_wire(cls, wire: AssetWire) -> "Asset":
        """Create Asset from wire format."""
        return cls(
            symbol=wire.symbol,
            type=wire.type,
            name=wire.name,
            exchange=wire.exchange,
            currency=wire.currency,
            lot_size=wire.lotSize,
            tick_size=wire.tickSize,
            valid_from=ms_to_datetime(
                wire.validFrom) if wire.validFrom else None,
            valid_until=ms_to_datetime(
                wire.validUntil) if wire.validUntil else None,
        )

    def to_wire(self) -> AssetWire:
        """Convert to wire format."""
        return AssetWire(
            symbol=self.symbol,
            type=self.type,
            name=self.name,
            exchange=self.exchange,
            currency=self.currency,
            lotSize=self.lot_size,
            tickSize=self.tick_size,
            validFrom=datetime_to_ms(
                self.valid_from) if self.valid_from else None,
            validUntil=datetime_to_ms(
                self.valid_until) if self.valid_until else None,
        )


# ============================================================================
# MarketSnapshot
# ============================================================================


class MarketSnapshotWire(BaseModel):
    """Wire format for MarketSnapshot."""

    price: dict[str, float]
    timestamp: int

    model_config = {"populate_by_name": True, "extra": "allow"}


class MarketSnapshot(BaseModel):
    """Runtime MarketSnapshot type."""

    price: dict[str, float]
    timestamp: datetime

    @classmethod
    def from_wire(cls, wire: MarketSnapshotWire) -> "MarketSnapshot":
        """Create MarketSnapshot from wire format."""
        return cls(
            price=wire.price,
            timestamp=ms_to_datetime(wire.timestamp),
        )

    def to_wire(self) -> MarketSnapshotWire:
        """Convert to wire format."""
        return MarketSnapshotWire(
            price=self.price,
            timestamp=datetime_to_ms(self.timestamp),
        )


# ============================================================================
# MarketQuote
# ============================================================================


class MarketQuoteWire(BaseModel):
    """Wire format for MarketQuote."""

    symbol: str
    price: float
    volume: Optional[float] = None
    totalVolume: Optional[float] = None
    timestamp: int
    bid: Optional[float] = None
    bidVol: Optional[float] = None
    ask: Optional[float] = None
    askVol: Optional[float] = None
    preClose: Optional[float] = None

    model_config = {"populate_by_name": True, "extra": "allow"}


class MarketQuote(BaseModel):
    """Runtime MarketQuote type."""

    symbol: str
    price: float
    volume: Optional[float] = None
    total_volume: Optional[float] = None
    timestamp: datetime
    bid: Optional[float] = None
    bid_vol: Optional[float] = None
    ask: Optional[float] = None
    ask_vol: Optional[float] = None
    pre_close: Optional[float] = None

    @classmethod
    def from_wire(cls, wire: MarketQuoteWire) -> "MarketQuote":
        """Create MarketQuote from wire format."""
        return cls(
            symbol=wire.symbol,
            price=wire.price,
            volume=wire.volume,
            total_volume=wire.totalVolume,
            timestamp=ms_to_datetime(wire.timestamp),
            bid=wire.bid,
            bid_vol=wire.bidVol,
            ask=wire.ask,
            ask_vol=wire.askVol,
            pre_close=wire.preClose,
        )

    def to_wire(self) -> MarketQuoteWire:
        """Convert to wire format."""
        return MarketQuoteWire(
            symbol=self.symbol,
            price=self.price,
            volume=self.volume,
            totalVolume=self.total_volume,
            timestamp=datetime_to_ms(self.timestamp),
            bid=self.bid,
            bidVol=self.bid_vol,
            ask=self.ask,
            askVol=self.ask_vol,
            preClose=self.pre_close,
        )


# ============================================================================
# MarketBar
# ============================================================================


class MarketBarInterval(str, Enum):
    """Market bar interval."""

    M1 = "1m"
    M5 = "5m"
    M15 = "15m"
    M30 = "30m"
    H1 = "1h"
    H2 = "2h"
    H4 = "4h"
    D1 = "1d"
    W1 = "1w"
    MONTH1 = "1M"


class MarketBarWire(BaseModel):
    """Wire format for MarketBar."""

    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    timestamp: int
    interval: MarketBarInterval

    model_config = {"populate_by_name": True, "extra": "allow"}


class MarketBar(BaseModel):
    """Runtime MarketBar type."""

    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    timestamp: datetime
    interval: MarketBarInterval

    @classmethod
    def from_wire(cls, wire: MarketBarWire) -> "MarketBar":
        """Create MarketBar from wire format."""
        return cls(
            symbol=wire.symbol,
            open=wire.open,
            high=wire.high,
            low=wire.low,
            close=wire.close,
            volume=wire.volume,
            timestamp=ms_to_datetime(wire.timestamp),
            interval=wire.interval,
        )

    def to_wire(self) -> MarketBarWire:
        """Convert to wire format."""
        return MarketBarWire(
            symbol=self.symbol,
            open=self.open,
            high=self.high,
            low=self.low,
            close=self.close,
            volume=self.volume,
            timestamp=datetime_to_ms(self.timestamp),
            interval=self.interval,
        )


# ============================================================================
# Order Types
# ============================================================================


class OrderType(str, Enum):
    """Order type."""

    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"


class OrderStatus(str, Enum):
    """Order status."""

    PENDING = "PENDING"
    OPEN = "OPEN"
    PARTIAL = "PARTIAL"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECT = "REJECT"


class BuyOrderWire(BaseModel):
    """Wire format for Buy order action."""

    side: Literal["BUY"]
    effect: Literal["OPEN_LONG", "CLOSE_SHORT"]


class SellOrderWire(BaseModel):
    """Wire format for Sell order action."""

    side: Literal["SELL"]
    effect: Literal["CLOSE_LONG", "OPEN_SHORT"]


class OrderWire(BaseModel):
    """Wire format for Order."""

    id: str
    symbol: str
    side: Literal["BUY", "SELL"]
    effect: Literal["OPEN_LONG", "CLOSE_SHORT", "CLOSE_LONG", "OPEN_SHORT"]
    type: OrderType
    quantity: float
    price: Optional[float] = None
    stopPrice: Optional[float] = None
    created: Optional[int] = None

    model_config = {"populate_by_name": True, "extra": "allow"}


class Order(BaseModel):
    """Runtime Order type."""

    id: str
    symbol: str
    side: Literal["BUY", "SELL"]
    effect: Literal["OPEN_LONG", "CLOSE_SHORT", "CLOSE_LONG", "OPEN_SHORT"]
    type: OrderType
    quantity: float
    price: Optional[float] = None
    stop_price: Optional[float] = None
    created: Optional[datetime] = None

    @classmethod
    def from_wire(cls, wire: OrderWire) -> "Order":
        """Create Order from wire format."""
        return cls(
            id=wire.id,
            symbol=wire.symbol,
            side=wire.side,
            effect=wire.effect,
            type=wire.type,
            quantity=wire.quantity,
            price=wire.price,
            stop_price=wire.stopPrice,
            created=ms_to_datetime(wire.created) if wire.created else None,
        )

    def to_wire(self) -> OrderWire:
        """Convert to wire format."""
        return OrderWire(
            id=self.id,
            symbol=self.symbol,
            side=self.side,
            effect=self.effect,
            type=self.type,
            quantity=self.quantity,
            price=self.price,
            stopPrice=self.stop_price,
            created=datetime_to_ms(self.created) if self.created else None,
        )


# ============================================================================
# Partial Order Types
# ============================================================================


class PartialOrderWire(BaseModel):
    """Partial order wire format for amendments and updates."""

    id: str  # ID typically required for amendments
    symbol: Optional[str] = None
    side: Optional[Literal["BUY", "SELL"]] = None
    effect: Optional[Literal["OPEN_LONG", "CLOSE_SHORT",
                             "CLOSE_LONG", "OPEN_SHORT"]] = None
    type: Optional[OrderType] = None
    quantity: Optional[float] = None
    price: Optional[float] = None
    stopPrice: Optional[float] = None
    created: Optional[int] = None

    model_config = {"populate_by_name": True, "extra": "allow"}


class PartialOrder(BaseModel):
    """Runtime PartialOrder type."""

    id: str
    symbol: Optional[str] = None
    side: Optional[Literal["BUY", "SELL"]] = None
    effect: Optional[Literal["OPEN_LONG", "CLOSE_SHORT",
                             "CLOSE_LONG", "OPEN_SHORT"]] = None
    type: Optional[OrderType] = None
    quantity: Optional[float] = None
    price: Optional[float] = None
    stop_price: Optional[float] = None
    created: Optional[datetime] = None

    @classmethod
    def from_wire(cls, wire: PartialOrderWire) -> "PartialOrder":
        """Create PartialOrder from wire format."""
        return cls(
            id=wire.id,
            symbol=wire.symbol,
            side=wire.side,
            effect=wire.effect,
            type=wire.type,
            quantity=wire.quantity,
            price=wire.price,
            stop_price=wire.stopPrice,
            created=ms_to_datetime(wire.created) if wire.created else None,
        )

    def to_wire(self) -> PartialOrderWire:
        """Convert to wire format."""
        return PartialOrderWire(
            id=self.id,
            symbol=self.symbol,
            side=self.side,
            effect=self.effect,
            type=self.type,
            quantity=self.quantity,
            price=self.price,
            stopPrice=self.stop_price,
            created=datetime_to_ms(self.created) if self.created else None,
        )


# ============================================================================
# OrderState
# ============================================================================


class OrderStateWire(BaseModel):
    """Wire format for OrderState."""

    id: str
    symbol: str
    side: Literal["BUY", "SELL"]
    effect: Literal["OPEN_LONG", "CLOSE_SHORT", "CLOSE_LONG", "OPEN_SHORT"]
    type: OrderType
    quantity: float
    price: Optional[float] = None
    stopPrice: Optional[float] = None
    created: Optional[int] = None
    filledQuantity: float
    remainingQuantity: float
    status: OrderStatus
    modified: int

    model_config = {"populate_by_name": True, "extra": "allow"}


class OrderState(BaseModel):
    """Runtime OrderState type."""

    id: str
    symbol: str
    side: Literal["BUY", "SELL"]
    effect: Literal["OPEN_LONG", "CLOSE_SHORT", "CLOSE_LONG", "OPEN_SHORT"]
    type: OrderType
    quantity: float
    price: Optional[float] = None
    stop_price: Optional[float] = None
    created: Optional[datetime] = None
    filled_quantity: float
    remaining_quantity: float
    status: OrderStatus
    modified: datetime

    @classmethod
    def from_wire(cls, wire: OrderStateWire) -> "OrderState":
        """Create OrderState from wire format."""
        return cls(
            id=wire.id,
            symbol=wire.symbol,
            side=wire.side,
            effect=wire.effect,
            type=wire.type,
            quantity=wire.quantity,
            price=wire.price,
            stop_price=wire.stopPrice,
            created=ms_to_datetime(wire.created) if wire.created else None,
            filled_quantity=wire.filledQuantity,
            remaining_quantity=wire.remainingQuantity,
            status=wire.status,
            modified=ms_to_datetime(wire.modified),
        )

    def to_wire(self) -> OrderStateWire:
        """Convert to wire format."""
        return OrderStateWire(
            id=self.id,
            symbol=self.symbol,
            side=self.side,
            effect=self.effect,
            type=self.type,
            quantity=self.quantity,
            price=self.price,
            stopPrice=self.stop_price,
            created=datetime_to_ms(self.created) if self.created else None,
            filledQuantity=self.filled_quantity,
            remainingQuantity=self.remaining_quantity,
            status=self.status,
            modified=datetime_to_ms(self.modified),
        )


# ============================================================================
# Fill
# ============================================================================


class FillWire(BaseModel):
    """Wire format for Fill."""

    id: str
    orderId: str
    symbol: str
    side: Literal["BUY", "SELL"]
    effect: Literal["OPEN_LONG", "CLOSE_SHORT", "CLOSE_LONG", "OPEN_SHORT"]
    quantity: float
    price: float
    commission: float
    created: int

    model_config = {"populate_by_name": True, "extra": "allow"}


class Fill(BaseModel):
    """Runtime Fill type."""

    id: str
    order_id: str
    symbol: str
    side: Literal["BUY", "SELL"]
    effect: Literal["OPEN_LONG", "CLOSE_SHORT", "CLOSE_LONG", "OPEN_SHORT"]
    quantity: float
    price: float
    commission: float
    created: datetime

    @classmethod
    def from_wire(cls, wire: FillWire) -> "Fill":
        """Create Fill from wire format."""
        return cls(
            id=wire.id,
            order_id=wire.orderId,
            symbol=wire.symbol,
            side=wire.side,
            effect=wire.effect,
            quantity=wire.quantity,
            price=wire.price,
            commission=wire.commission,
            created=ms_to_datetime(wire.created),
        )

    def to_wire(self) -> FillWire:
        """Convert to wire format."""
        return FillWire(
            id=self.id,
            orderId=self.order_id,
            symbol=self.symbol,
            side=self.side,
            effect=self.effect,
            quantity=self.quantity,
            price=self.price,
            commission=self.commission,
            created=datetime_to_ms(self.created),
        )


# ============================================================================
# Position Types
# ============================================================================


class LongPositionLot(BaseModel):
    """Long position lot."""

    quantity: float
    price: float
    totalCost: float

    model_config = {"populate_by_name": True, "extra": "allow"}


class LongPositionWire(BaseModel):
    """Wire format for LongPosition."""

    quantity: float
    totalCost: float
    realisedPnL: float
    lots: list[LongPositionLot]
    modified: int

    model_config = {"populate_by_name": True, "extra": "allow"}


class LongPosition(BaseModel):
    """Runtime LongPosition type."""

    quantity: float
    total_cost: float
    realised_pnl: float
    lots: list[LongPositionLot]
    modified: datetime

    @classmethod
    def from_wire(cls, wire: LongPositionWire) -> "LongPosition":
        """Create LongPosition from wire format."""
        return cls(
            quantity=wire.quantity,
            total_cost=wire.totalCost,
            realised_pnl=wire.realisedPnL,
            lots=wire.lots,
            modified=ms_to_datetime(wire.modified),
        )

    def to_wire(self) -> LongPositionWire:
        """Convert to wire format."""
        return LongPositionWire(
            quantity=self.quantity,
            totalCost=self.total_cost,
            realisedPnL=self.realised_pnl,
            lots=self.lots,
            modified=datetime_to_ms(self.modified),
        )


class ShortPositionLot(BaseModel):
    """Short position lot."""

    quantity: float
    price: float
    totalProceeds: float

    model_config = {"populate_by_name": True, "extra": "allow"}


class ShortPositionWire(BaseModel):
    """Wire format for ShortPosition."""

    quantity: float
    totalProceeds: float
    realisedPnL: float
    lots: list[ShortPositionLot]
    modified: int

    model_config = {"populate_by_name": True, "extra": "allow"}


class ShortPosition(BaseModel):
    """Runtime ShortPosition type."""

    quantity: float
    total_proceeds: float
    realised_pnl: float
    lots: list[ShortPositionLot]
    modified: datetime

    @classmethod
    def from_wire(cls, wire: ShortPositionWire) -> "ShortPosition":
        """Create ShortPosition from wire format."""
        return cls(
            quantity=wire.quantity,
            total_proceeds=wire.totalProceeds,
            realised_pnl=wire.realisedPnL,
            lots=wire.lots,
            modified=ms_to_datetime(wire.modified),
        )

    def to_wire(self) -> ShortPositionWire:
        """Convert to wire format."""
        return ShortPositionWire(
            quantity=self.quantity,
            totalProceeds=self.total_proceeds,
            realisedPnL=self.realised_pnl,
            lots=self.lots,
            modified=datetime_to_ms(self.modified),
        )


class PositionWire(BaseModel):
    """Wire format for Position."""

    cash: float
    long: Optional[dict[str, LongPositionWire]] = None
    short: Optional[dict[str, ShortPositionWire]] = None
    totalCommission: float
    realisedPnL: float
    modified: int

    model_config = {"populate_by_name": True, "extra": "allow"}


class Position(BaseModel):
    """Runtime Position type."""

    cash: float
    long: Optional[dict[str, LongPosition]] = None
    short: Optional[dict[str, ShortPosition]] = None
    total_commission: float
    realised_pnl: float
    modified: datetime

    @classmethod
    def from_wire(cls, wire: PositionWire) -> "Position":
        """Create Position from wire format."""
        return cls(
            cash=wire.cash,
            long={k: LongPosition.from_wire(v) for k, v in wire.long.items()}
            if wire.long
            else None,
            short={k: ShortPosition.from_wire(v)
                   for k, v in wire.short.items()}
            if wire.short
            else None,
            total_commission=wire.totalCommission,
            realised_pnl=wire.realisedPnL,
            modified=ms_to_datetime(wire.modified),
        )

    def to_wire(self) -> PositionWire:
        """Convert to wire format."""
        return PositionWire(
            cash=self.cash,
            long={k: v.to_wire()
                  for k, v in self.long.items()} if self.long else None,
            short={k: v.to_wire() for k, v in self.short.items()}
            if self.short
            else None,
            totalCommission=self.total_commission,
            realisedPnL=self.realised_pnl,
            modified=datetime_to_ms(self.modified),
        )


class CloseStrategy(str, Enum):
    """Close strategy."""

    FIFO = "FIFO"
    LIFO = "LIFO"
