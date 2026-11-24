
import polars as pl


def calculate_ema(prices, period):
    """Calculate Exponential Moving Average."""

    if not prices:
        return []

    multiplier = 2 / (period + 1)

    ema_values = []
    ema = prices[0]

    for price in prices:
        ema = (price * multiplier) + (
            ema * (1 - multiplier)
        )
        ema_values.append(ema)

    return ema_values


def calculate_rsi(prices, period=14):
    """Calculate Relative Strength Index."""

    rsi_values = [None] * len(prices)

    if len(prices) <= period:
        return rsi_values

    gains = []
    losses = []

    for i in range(1, len(prices)):
        change = prices[i] - prices[i - 1]

        gains.append(max(change, 0))
        losses.append(max(-change, 0))

    for i in range(period, len(prices)):
        start = i - period

        avg_gain = sum(gains[start:i]) / period
        avg_loss = sum(losses[start:i]) / period

        if avg_loss == 0 and avg_gain == 0:
            rsi = 50
        elif avg_loss == 0:
            rsi = 100
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

        rsi_values[i] = rsi

    return rsi_values


def add_technical_indicators(df):
    """Add SMA, EMA, MACD and RSI to stock data."""

    if df.is_empty():
        return df

    if "Close" not in df.columns:
        raise ValueError("Stock data must contain a Close column.")

    prices = df["Close"].to_list()

    if any(price is None for price in prices):
        raise ValueError("Closing prices contain missing values.")

    prices = [float(price) for price in prices]

    # SMA - 20 days
    sma_20 = []

    for i in range(len(prices)):
        if i < 19:
            sma_20.append(None)
        else:
            average = sum(prices[i - 19:i + 1]) / 20
            sma_20.append(average)

    # EMA - 12 and 26 days
    ema_12 = calculate_ema(prices, 12)
    ema_26 = calculate_ema(prices, 26)

    # MACD
    macd = [
        short - long
        for short, long in zip(ema_12, ema_26)
    ]

    # MACD Signal - 9 days
    macd_signal = calculate_ema(macd, 9)

    # RSI - 14 days
    rsi_14 = calculate_rsi(prices, 14)

    # Add indicator columns
    result = df.with_columns([
        pl.Series("SMA_20", sma_20),
        pl.Series("EMA_12", ema_12),
        pl.Series("EMA_26", ema_26),
        pl.Series("MACD", macd),
        pl.Series("MACD_Signal", macd_signal),
        pl.Series("RSI_14", rsi_14)
    ])

    return result
