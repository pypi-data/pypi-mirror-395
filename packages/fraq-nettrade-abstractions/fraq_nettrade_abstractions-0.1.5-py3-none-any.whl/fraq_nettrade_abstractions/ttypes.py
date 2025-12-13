"""
Type definitions for FraQ NetTrade Python strategies.
"""

from typing import TypedDict, List


class Bar(TypedDict):
    """
    Single OHLC bar data.
    
    Attributes:
        open: Opening price
        high: Highest price
        low: Lowest price
        close: Closing price
        volume: Trading volume
        time: ISO format timestamp
    """
    open: float
    high: float
    low: float
    close: float
    volume: float
    time: str


class Symbol(TypedDict):
    """
    Symbol market data.
    
    Attributes:
        name: Symbol name (e.g., "EURUSD")
        bid: Current bid price
        ask: Current ask price
        spread: Bid-ask spread
        close: Current bar close price
        bars: Historical bar data
    """
    name: str
    bid: float
    ask: float
    spread: float
    close: float
    bars: List[Bar]


class Account(TypedDict):
    """
    Trading account state.
    
    Attributes:
        balance: Account balance
        equity: Current equity
        margin_used: Margin currently used
        margin_available: Available margin
    """
    balance: float
    equity: float
    margin_used: float
    margin_available: float


class TradeSignal(TypedDict):
    """
    Trade signal returned from strategy.
    
    Attributes:
        action: Trade action - 'buy', 'sell', or 'close'
        volume: Position size/volume
    """
    action: str
    volume: float