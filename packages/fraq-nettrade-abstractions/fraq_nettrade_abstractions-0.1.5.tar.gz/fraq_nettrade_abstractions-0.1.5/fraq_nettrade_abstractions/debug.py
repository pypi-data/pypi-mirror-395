"""
Debugging utilities for FraQ NetTrade Python strategies.
"""

import sys
from datetime import datetime

class Logger:
    """
    Simple logger for strategy debugging.
    
    Writes to stderr which is captured by FraQ application.
    """
    
    def log(self, message: str, level: str = 'INFO') -> None:
        """
        Log a message.
        
        Args:
            message: Message to log
            level: Log level - 'INFO', 'WARNING', 'ERROR'
        
        Example:
            from fraq_nettrade_abstractions import logger
            
            logger.log("Buy signal generated", level='INFO')
            logger.log("Risk limit exceeded", level='WARNING')
        """
        timestamp = datetime.now().isoformat()
        log_line = f"[{timestamp}] [{level}] {message}"
        print(log_line, file=sys.stderr, flush=True)
    
    def info(self, message: str) -> None:
        """Log info message."""
        self.log(message, 'INFO')
    
    def warning(self, message: str) -> None:
        """Log warning message."""
        self.log(message, 'WARNING')
    
    def error(self, message: str) -> None:
        """Log error message."""
        self.log(message, 'ERROR')


# Global logger instance
logger = Logger()


def enable_debugger(port: int = 5678) -> None:
    """
    Enable remote debugging for VS Code.
    
    Call this in your strategy's on_start method to enable debugging.
    Requires debugpy package: pip install debugpy
    
    Args:
        port: TCP port for debugger (default: 5678)
    
    Example:
        from fraq_nettrade_abstractions import enable_debugger, Strategy
        
        class MyStrategy(Strategy):
            def on_start(self, context):
                enable_debugger()  # Wait for VS Code to attach
                # Set breakpoints and debug normally
    
    Usage:
        1. Add enable_debugger() to your strategy
        2. Start FraQ with --debug flag
        3. In VS Code, attach to port 5678
        4. Press Enter in FraQ console
        5. Debug with breakpoints
    """
    try:
        import debugpy
        debugpy.listen(('0.0.0.0', port), in_process_debug_adapter=True)
        print(f"[DEBUG] Waiting for debugger on 0.0.0.0:{port}...", file=sys.stderr, flush=True)
        debugpy.wait_for_client()
        print("[DEBUG] Debugger attached!", file=sys.stderr, flush=True)
    except ImportError:
        print("[ERROR] debugpy not installed. Run: pip install debugpy", file=sys.stderr, flush=True)
    except Exception as e:
        print(f"[ERROR] Failed to start debugger: {e}", file=sys.stderr, flush=True)