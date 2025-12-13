"""Type annotations for Blocky API responses."""

from typing import TypedDict, List, Optional


class TickerData(TypedDict, total=False):
    """24-hour ticker statistics."""
    open: str
    high: str
    low: str
    close: str
    base_volume: str
    quote_volume: str
    change: str
    change_percentage: str


class MarketInfo(TypedDict, total=False):
    """Market configuration."""
    market: str
    market_id: int
    base_instrument: str
    base_instrument_id: int
    base_instrument_name: str
    base_precision: int
    quote_instrument: str
    quote_instrument_id: int
    quote_instrument_name: str
    quote_precision: int
    tick_size: str
    minimum_base_volume: str
    minimum_quote_volume: str
    maker_fee: str
    taker_fee: str
    is_latest_tx_buy: bool
    ticker: TickerData


class WalletBalance(TypedDict, total=False):
    """Wallet balance information."""
    instrument: str
    name: str
    balance: str
    frozen: str


class OrderInfo(TypedDict, total=False):
    """Order information."""
    order_id: int
    market: str
    type: str
    side: str
    price: str
    quantity: str
    remaining: str
    fulfilled: str
    fulfilled_percentage: str
    status: str
    sub_wallet_id: int
    maker_fee: str
    taker_fee: str
    created_at: str
    finalized_at: str


class TradeInfo(TypedDict, total=False):
    """Trade/execution information."""
    id: int
    market: str
    side: str
    price: str
    quantity: str
    total: str
    fee: str
    role: str
    created_at: str


class TransferInfo(TypedDict, total=False):
    """Transfer information."""
    id: int
    source_user_id: int
    source_user_uuid: str
    source_sub_wallet_id: int
    destination_user_id: int
    destination_user_uuid: str
    destination_sub_wallet_id: int
    quantity: str
    instrument: str
    created_at: str
    memo: str
    role: str


class DepositInfo(TypedDict, total=False):
    """Deposit information."""
    tx_id: str
    instrument: str
    quantity: str
    address_id: str
    memo: str
    created_at: str


class WithdrawalInfo(TypedDict, total=False):
    """Withdrawal information."""
    tx_id: str
    instrument: str
    quantity: str
    address_id: str
    memo: str
    created_at: str


class OrderbookSide(TypedDict):
    """One side of the orderbook."""
    price: List[str]
    quantity: List[str]
    count: int
    base_volume: str
    quote_volume: str


class Orderbook(TypedDict):
    """Full orderbook data."""
    bids: OrderbookSide
    asks: OrderbookSide
    spread: str
    spread_percentage: str


# WebSocket message types

class WSOrderbookMessage(TypedDict):
    """WebSocket orderbook snapshot message."""
    channel: str
    spread: str
    spread_percentage: str
    asks: OrderbookSide
    bids: OrderbookSide


class WSTransactionMessage(TypedDict):
    """WebSocket transaction message."""
    channel: str
    price: str
    quantity: str
    is_buying_tx: bool
    created_at: int  # Unix timestamp in milliseconds
