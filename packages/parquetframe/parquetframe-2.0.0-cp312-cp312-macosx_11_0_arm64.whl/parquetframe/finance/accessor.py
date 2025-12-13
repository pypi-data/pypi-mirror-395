"""
Financial Accessor for ParquetFrame.

Provides .fin accessor for financial and technical analysis operations.
"""

import numpy as np
import pandas as pd


class FinanceAccessor:
    """
    Financial and technical analysis accessor.

    Accessed via df.fin for financial DataFrames.

    Example:
        >>> import pandas as pd
        >>> prices = pd.DataFrame({
        ...     'date': pd.date_range('2024-01-01', periods=100),
        ...     'close': np.random.randn(100).cumsum() + 100
        ... }).set_index('date')
        >>>
        >>> # Calculate indicators
        >>> sma = prices.fin.sma(window=20)
        >>> rsi = prices.fin.rsi(period=14)
    """

    def __init__(self, pandas_obj):
        """Initialize accessor with DataFrame."""
        self._obj = pandas_obj

    def sma(self, column: str | None = None, window: int = 20) -> pd.Series:
        """
        Simple Moving Average.

        Args:
            column: Column to calculate on (default: first numeric column)
            window: Window size

        Returns:
            Series with SMA values
        """
        if column is None:
            column = self._obj.select_dtypes(include=[np.number]).columns[0]
        return self._obj[column].rolling(window=window).mean()

    def ema(self, column: str | None = None, span: int = 20) -> pd.Series:
        """
        Exponential Moving Average.

        Args:
            column: Column to calculate on
            span: Span for EMA

        Returns:
            Series with EMA values
        """
        if column is None:
            column = self._obj.select_dtypes(include=[np.number]).columns[0]
        return self._obj[column].ewm(span=span, adjust=False).mean()

    def rsi(self, column: str | None = None, period: int = 14) -> pd.Series:
        """
        Relative Strength Index.

        Args:
            column: Column to calculate on (usually 'close')
            period: RSI period (default 14)

        Returns:
            Series with RSI values (0-100)
        """
        if column is None:
            column = self._obj.select_dtypes(include=[np.number]).columns[0]

        delta = self._obj[column].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def macd(
        self,
        column: str | None = None,
        fast: int = 12,
        slow: int = 26,
        signal: int = 9,
    ) -> pd.DataFrame:
        """
        Moving Average Convergence Divergence.

        Args:
            column: Column to calculate on
            fast: Fast EMA period
            slow: Slow EMA period
            signal: Signal line period

        Returns:
            DataFrame with 'macd', 'signal', and 'histogram' columns
        """
        if column is None:
            column = self._obj.select_dtypes(include=[np.number]).columns[0]

        ema_fast = self._obj[column].ewm(span=fast, adjust=False).mean()
        ema_slow = self._obj[column].ewm(span=slow, adjust=False).mean()

        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line

        return pd.DataFrame(
            {"macd": macd_line, "signal": signal_line, "histogram": histogram}
        )

    def bollinger_bands(
        self, column: str | None = None, window: int = 20, num_std: float = 2.0
    ) -> pd.DataFrame:
        """
        Bollinger Bands.

        Args:
            column: Column to calculate on
            window: Moving average window
            num_std: Number of standard deviations

        Returns:
            DataFrame with 'upper', 'middle', 'lower' bands
        """
        if column is None:
            column = self._obj.select_dtypes(include=[np.number]).columns[0]

        middle = self._obj[column].rolling(window=window).mean()
        std = self._obj[column].rolling(window=window).std()

        upper = middle + (std * num_std)
        lower = middle - (std * num_std)

        return pd.DataFrame({"upper": upper, "middle": middle, "lower": lower})

    def atr(
        self,
        high: str = "high",
        low: str = "low",
        close: str = "close",
        period: int = 14,
    ) -> pd.Series:
        """
        Average True Range.

        Args:
            high: High price column
            low: Low price column
            close: Close price column
            period: ATR period

        Returns:
            Series with ATR values
        """
        high_low = self._obj[high] - self._obj[low]
        high_close = np.abs(self._obj[high] - self._obj[close].shift())
        low_close = np.abs(self._obj[low] - self._obj[close].shift())

        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = true_range.rolling(window=period).mean()

        return atr

    def returns(self, column: str | None = None, periods: int = 1) -> pd.Series:
        """
        Calculate returns.

        Args:
            column: Column to calculate on
            periods: Number of periods

        Returns:
            Series with percentage returns
        """
        if column is None:
            column = self._obj.select_dtypes(include=[np.number]).columns[0]
        return self._obj[column].pct_change(periods=periods)

    def cumulative_returns(self, column: str | None = None) -> pd.Series:
        """
        Calculate cumulative returns.

        Args:
            column: Column to calculate on

        Returns:
            Series with cumulative returns
        """
        if column is None:
            column = self._obj.select_dtypes(include=[np.number]).columns[0]
        return (1 + self.returns(column)).cumprod() - 1

    def volatility(
        self, column: str | None = None, window: int = 20, annualize: bool = True
    ) -> pd.Series:
        """
        Calculate rolling volatility.

        Args:
            column: Column to calculate on
            window: Rolling window
            annualize: Annualize volatility (multiply by sqrt(252))

        Returns:
            Series with volatility values
        """
        if column is None:
            column = self._obj.select_dtypes(include=[np.number]).columns[0]

        returns = self.returns(column)
        vol = returns.rolling(window=window).std()

        if annualize:
            vol = vol * np.sqrt(252)  # Trading days per year

        return vol


# Register accessor with pandas
@pd.api.extensions.register_dataframe_accessor("fin")
class FinAccessor(FinanceAccessor):
    """Pandas DataFrame accessor for financial operations."""

    pass


__all__ = ["FinanceAccessor", "FinAccessor"]
