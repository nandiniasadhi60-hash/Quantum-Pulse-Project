
import streamlit as st
import plotly.graph_objects as go
from live_stock import get_stock_data

st.set_page_config(
    page_title="QuantumPulse Live Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 QuantumPulse - Live Stock Dashboard")
st.write("Stock market data powered by Yahoo Finance")

# Select stock
symbol = st.selectbox(
    "Select Stock",
    [
        "RELIANCE.NS",
        "TCS.NS",
        "INFY.NS",
        "HDFCBANK.NS",
        "ICICIBANK.NS"
    ]
)

if st.button("Fetch Stock Data"):
    with st.spinner("Fetching stock data..."):
        try:
            df = get_stock_data(symbol)

            if df.is_empty():
                st.warning("No stock data found. Try again.")
            else:
                st.success(f"Data loaded for {symbol}")

                # Display latest closing price
                latest_close = df["Close"][-1]

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Latest Close",
                    f"₹{latest_close:.2f}"
                )

                col2.metric(
                    "Highest Price",
                    f"₹{df['High'].max():.2f}"
                )

                col3.metric(
                    "Lowest Price",
                    f"₹{df['Low'].min():.2f}"
                )

                # Stock price chart
                fig = go.Figure()

                fig.add_trace(go.Scatter(
                    x=df["Date"].to_list(),
                    y=df["Close"].to_list(),
                    mode="lines+markers",
                    name="Closing Price"
                ))

                fig.update_layout(
                    title=f"{symbol} Stock Price",
                    xaxis_title="Date",
                    yaxis_title="Price (INR)"
                )

                st.plotly_chart(fig, use_container_width=True)

                # Stock data table
                st.subheader("Stock Market Data")
                st.dataframe(df)

                # Download CSV
                st.download_button(
                    "Download Stock Data",
                    data=df.write_csv(),
                    file_name="live_stock_data.csv",
                    mime="text/csv"
                )

        except Exception as error:
            st.error(f"Error: {error}")
