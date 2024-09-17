from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA, RSI
from surmount.logging import log
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "AAPL"  # Trading AAPL

    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        return "1day"  # Daily interval for EMA and RSI calculation

    def run(self, data):
        # Extracts the ohlcv data for AAPL
        ohlcv_data = data["ohlcv"]

        # Calculate EMA and RSI for AAPL with specified lengths
        ema_length = 20  # Length of the EMA window
        rsi_length = 14  # Length of the RSI window

        ema_data = EMA(self.ticker, ohlcv_data, ema_length)
        rsi_data = RSI(self.ticker, ohlcv_data, rsi_length)

        # Check the last two points to determine EMA trend direction
        last_ema = ema_data[-1] if len(ema_data) > 0 else 0
        prev_ema = ema_data[-2] if len(ema_data) > 1 else 0

        # Get the latest RSI value
        last_rsi = rsi_data[-1] if len(rsi_data) > 0 else 0

        # Log current indicators
        log(f"EMA: {last_ema}, Prev EMA: {prev_ema}, RSI: {last_rsi}")

        # Trading logic
        if last_ema > prev_ema and last_rsi < 30:
            # EMA trending up and RSI indicates oversold, consider buying
            allocation = {"AAPL": 1}  # Full allocation to AAPL
        elif last_ema < prev_ema and last_rsi > 70:
            # EMA trending down and RSI indicates overbought, consider selling
            allocation = {"AAPL": 0}  # No allocation to AAPL
        else:
            # Hold current position if no clear buy/sell signal
            allocation = {}  # Keep current allocation

        return TargetAllocation(allocation)