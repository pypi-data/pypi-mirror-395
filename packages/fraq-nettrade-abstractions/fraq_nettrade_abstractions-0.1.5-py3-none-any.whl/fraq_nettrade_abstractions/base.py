"""
Base classes for FraQ NetTrade Python strategies.
"""

from typing import Dict, Any, Optional


class Strategy:
    """
    Base class for FraQ trading strategies.
    
    Inherit from this class and override lifecycle methods to implement your strategy.
    
    Example:
        from fraq_nettrade_abstractions import Strategy
        
        class MyStrategy(Strategy):
            def on_start(self, context):
                self.sma_fast = context['indicators'].sma(period=10)
                self.sma_slow = context['indicators'].sma(period=20)
            
            def on_bar(self, symbol, index):
                if self.sma_fast[index] > self.sma_slow[index]:
                    return {'action': 'buy', 'volume': 1.0}
                return None
    """
    
    def on_start(self, context: Dict[str, Any]) -> None:
        """
        Called once when backtest starts.
        
        Use this method to:
        - Initialize indicators
        - Set up strategy state
        - Access account and symbol information
        
        Args:
            context: Dictionary containing:
                - 'account': Account information (balance, equity, etc.)
                - 'symbols': List of symbols being traded
                - 'indicators': Indicator factory for built-in indicators
        
        Example:
            def on_start(self, context):
                self.account = context['account']
                self.symbols = context['symbols']
                self.sma = context['indicators'].sma(period=20)
        """
        pass
    
    def on_bar(self, symbol: Dict[str, Any], index: int) -> Optional[Dict[str, Any]]:
        """
        Called on each new bar (REQUIRED - implement this method).
        
        This is where your main trading logic goes.
        
        Args:
            symbol: Symbol data dictionary with:
                - 'name': str (e.g., "EURUSD")
                - 'bid': float (current bid price)
                - 'ask': float (current ask price)
                - 'spread': float (bid-ask spread)
                - 'close': float (current bar close price)
                - 'bars': List[Dict] (historical bars)
            index: Current bar index (0-based)
        
        Returns:
            None: No trade action
            Dict: Trade signal with keys:
                - 'action': str - 'buy', 'sell', or 'close'
                - 'volume': float - Position size
        
        Example:
            def on_bar(self, symbol, index):
                close_price = symbol['close']
                
                if close_price > self.sma[index]:
                    return {'action': 'buy', 'volume': 1.0}
                elif close_price < self.sma[index]:
                    return {'action': 'sell', 'volume': 1.0}
                
                return None
        """
        pass
    
    def on_tick(self, symbol: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Called on each tick (optional, high frequency).
        
        Use for tick-level strategies. Most strategies only need on_bar.
        
        Args:
            symbol: Current tick data with same structure as on_bar
        
        Returns:
            Same as on_bar - trade signal or None
        
        Example:
            def on_tick(self, symbol):
                if symbol['bid'] > self.threshold:
                    return {'action': 'buy', 'volume': 0.1}
                return None
        """
        pass
    
    def on_stop(self) -> None:
        """
        Called when backtest ends (optional).
        
        Use for cleanup or final logging.
        
        Example:
            def on_stop(self):
                print(f"Strategy finished. Final balance: {self.account['balance']}")
        """
        pass