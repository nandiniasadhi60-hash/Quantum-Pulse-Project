
import yfinance as yf
import polars as pl

def get_stock_data(symbol="RELIANCE.NS"):
    stock = yf.Ticker(symbol)

    data = stock.history(period="1mo", interval="1d")

    if data.empty:
        return pl.DataFrame()

    data = data.reset_index()

    return pl.DataFrame({
        "Date": data["Date"].astype(str).tolist(),
        "Open": data["Open"].tolist(),
        "High": data["High"].tolist(),
        "Low": data["Low"].tolist(),
        "Close": data["Close"].tolist(),
        "Volume": data["Volume"].tolist()
    })


if __name__ == "__main__":
    df = get_stock_data("RELIANCE.NS")
    print(df)
