import streamlit as st
import polars as pl
import plotly.graph_objects as go
from pathlib import Path

from processor import process_financial_data
from database import get_all_data
from live_stock import get_stock_data
from indicators import add_technical_indicators
from stock_alerts import (
    create_alert_table,
    add_alert,
    get_alerts,
    delete_alert,
    check_alerts
)
from portfolio import (
    create_portfolio_table,
    add_stock,
    get_portfolio,
    delete_stock
)
# ==========================================
# QUANTUMPULSE FINANCIAL ANALYTICS
# ==========================================

st.set_page_config(
    page_title="QuantumPulse Financial Analytics",
    page_icon="📈",
    layout="wide"
)

# Dashboard heading
st.title("📈 QuantumPulse")
st.subheader("High-Frequency Financial Data Density Engine")


st.markdown("""
Monitor stock prices, analyze financial data,
compare stocks and download market records.
""")

st.divider()

st.markdown("---")

# Load financial data
DATA_FILE = Path(__file__).parent / "data" / "financial_data.csv"

if not DATA_FILE.exists():
    st.error("Financial data file not found!")
    st.info("Please check data/financial_data.csv")
    st.stop()

try:
    df, statistics = process_financial_data(str(DATA_FILE))

    if df.is_empty():
        st.warning("No financial data available.")
        st.stop()

    st.success("Financial data loaded successfully!")

    # Identify numeric columns
    numeric_columns = [
        col for col, dtype in zip(df.columns, df.dtypes)
        if dtype.is_numeric()
    ]

    if not numeric_columns:
        st.warning("No numeric columns found in the CSV file.")
        st.stop()

    # Dashboard metrics
    st.header("📊 Financial Overview")

    preferred_column = next(
        (col for col in numeric_columns if col.lower() == "close"),
        numeric_columns[0]
    )

    metric_values = statistics.get(preferred_column, {})

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average Price",
        f"{metric_values.get('mean', 0):,.2f}"
    )

    col2.metric(
        "Maximum Price",
        f"{metric_values.get('max', 0):,.2f}"
    )

    col3.metric(
        "Minimum Price",
        f"{metric_values.get('min', 0):,.2f}"
    )

    st.markdown("---")

    # Stock data table
    st.header("📋 Financial Data")

    st.dataframe(
        df,
        use_container_width=True
    )

    # Interactive chart
    st.header("📈 Financial Analytics Chart")

    selected_column = st.selectbox(
        "Select financial column",
        numeric_columns,
        index=numeric_columns.index(preferred_column)
    )

    # Find a date or time column
    date_column = next(
        (
            col for col in df.columns
            if col.lower() in ["date", "datetime", "timestamp"]
        ),
        None
    )

    if date_column:
        x_values = df[date_column].to_list()
    else:
        x_values = list(range(len(df)))

    y_values = df[selected_column].to_list()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=y_values,
            mode="lines",
            name=selected_column
        )
    )

    fig.update_layout(
        title=f"{selected_column} Analysis",
        xaxis_title=date_column or "Record Number",
        yaxis_title=selected_column,
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Statistics
    st.header("📊 Statistical Analysis")

    st.json(statistics)

    st.markdown("---")

    st.caption(
        "QuantumPulse | Financial Analytics Dashboard"
    )

except Exception as e:
    st.error(f"Dashboard Error: {e}")


# Your existing app.py code above

# ==================================
# QUANTUMPULSE SQLITE DATABASE
# ==================================

st.subheader("📊 Saved Stock Database")

records = get_all_data()


if records:
    stock_data = []

    for record in records:
        stock_data.append({
            "ID": record[0],
            "Date": record[1],
            "Open": record[2],
            "High": record[3],
            "Low": record[4],
            "Close": record[5],
            "Volume": record[6]
        })

    st.dataframe(stock_data, width="stretch")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=[row["Date"] for row in stock_data],
        y=[row["Close"] for row in stock_data],
        mode="lines+markers",
        name="Closing Price"
    ))

    fig.update_layout(
        title="Saved Stock Price History",
        xaxis_title="Date",
        yaxis_title="Closing Price"
    )

    st.plotly_chart(fig, width="stretch")

else:
    st.info("No stock records found in the database.")

# STOCK SELECTION

st.sidebar.header("Stock Selection")

symbol = st.sidebar.selectbox(
    "Choose Stock",
    ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"]
)

if st.sidebar.button("Fetch Stock Data"):
    stock_data = get_stock_data(symbol)

    if not stock_data.is_empty():
        st.subheader(f"{symbol} Stock Data")
        st.dataframe(stock_data)
    else:
        st.warning("No stock data available.")
        # STOCK PRICE COMPARISON

st.subheader("📈 Stock Price Comparison")

col1, col2 = st.columns(2)

with col1:
    stock1 = st.selectbox(
        "Select First Stock",
        ["RELIANCE.NS", "TCS.NS", "INFY.NS"],
        key="stock1"
    )

with col2:
    stock2 = st.selectbox(
        "Select Second Stock",
        ["TCS.NS", "INFY.NS", "HDFCBANK.NS"],
        key="stock2"
    )

if st.button("Compare Stocks"):

    if stock1 == stock2:
        st.warning("Please select two different stocks.")

    else:
        data1 = get_stock_data(stock1)
        data2 = get_stock_data(stock2)

        if not data1.is_empty() and not data2.is_empty():

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=data1["Date"].to_list(),
                y=data1["Close"].to_list(),
                mode="lines",
                name=stock1
            ))

            fig.add_trace(go.Scatter(
                x=data2["Date"].to_list(),
                y=data2["Close"].to_list(),
                mode="lines",
                name=stock2
            ))

            fig.update_layout(
                title="Stock Price Comparison",
                xaxis_title="Date",
                yaxis_title="Closing Price",
                template="plotly_dark"
            )

            st.plotly_chart(fig, width="stretch")

        else:
            st.warning("Stock data is not available.")
            # DOWNLOAD STOCK DATA

st.subheader("📥 Download Stock Data")

download_symbol = st.selectbox(
    "Select Stock to Download",
    ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"],
    key="download_stock"
)

download_data = get_stock_data(download_symbol)

if not download_data.is_empty():

    csv_data = download_data.write_csv()

    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name=f"{download_symbol}_stock_data.csv",
        mime="text/csv"
    )

else:
    st.warning("No stock data available for download.")
    # ADVANCED FINANCIAL ANALYTICS

st.subheader("📊 Advanced Financial Analytics")

analytics_symbol = st.selectbox(
    "Select Stock for Analysis",
    ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"],
    key="analytics_stock"
)

if st.button("Analyze Stock"):
    analytics_data = get_stock_data(analytics_symbol)

    if not analytics_data.is_empty():

        closing_prices = analytics_data["Close"].to_list()
        volumes = analytics_data["Volume"].to_list()

        latest_price = closing_prices[-1]
        highest_price = max(closing_prices)
        lowest_price = min(closing_prices)
        average_volume = sum(volumes) / len(volumes)

        if len(closing_prices) >= 2 and closing_prices[-2] != 0:
            change = (
                (latest_price - closing_prices[-2])
                / closing_prices[-2]
            ) * 100
        else:
            change = 0

        col1, col2 = st.columns(2)

        col1.metric("Latest Closing Price", f"₹{latest_price:.2f}")
        col2.metric("Price Change", f"{change:.2f}%")

        col1.metric("Highest Price", f"₹{highest_price:.2f}")
        col2.metric("Lowest Price", f"₹{lowest_price:.2f}")

        st.metric("Average Trading Volume", f"{average_volume:,.0f}")

    else:
        st.warning("No stock data available.")

# TECHNICAL INDICATORS

st.subheader("📈 Technical Indicators Analysis")

indicator_symbol = st.selectbox(
    "Select Stock for Technical Analysis",
    ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"],
    key="indicator_stock"
)

if st.button("Calculate Technical Indicators"):

    indicator_data = get_stock_data(indicator_symbol)

    if not indicator_data.is_empty():

        result = add_technical_indicators(indicator_data)

        st.success("Technical indicators calculated successfully!")

        st.dataframe(result, width="stretch")

        # Stock price and moving averages
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=result["Date"].to_list(),
            y=result["Close"].to_list(),
            mode="lines",
            name="Closing Price"
        ))

        fig.add_trace(go.Scatter(
            x=result["Date"].to_list(),
            y=result["SMA_20"].to_list(),
            mode="lines",
            name="SMA 20"
        ))

        fig.add_trace(go.Scatter(
            x=result["Date"].to_list(),
            y=result["EMA_12"].to_list(),
            mode="lines",
            name="EMA 12"
        ))

        fig.add_trace(go.Scatter(
            x=result["Date"].to_list(),
            y=result["EMA_26"].to_list(),
            mode="lines",
            name="EMA 26"
        ))

        fig.update_layout(
            title=f"{indicator_symbol} Moving Average Analysis",
            xaxis_title="Date",
            yaxis_title="Stock Price",
            template="plotly_dark"
        )

        st.plotly_chart(fig, width="stretch")

        # RSI Chart
        rsi_fig = go.Figure()

        rsi_fig.add_trace(go.Scatter(
            x=result["Date"].to_list(),
            y=result["RSI_14"].to_list(),
            mode="lines",
            name="RSI 14"
        ))

        rsi_fig.add_hline(y=70, line_dash="dash")
        rsi_fig.add_hline(y=30, line_dash="dash")

        rsi_fig.update_layout(
            title="Relative Strength Index (RSI)",
            xaxis_title="Date",
            yaxis_title="RSI",
            yaxis_range=[0, 100],
            template="plotly_dark"
        )

        st.plotly_chart(rsi_fig, width="stretch")

        # MACD Chart
        macd_fig = go.Figure()

        macd_fig.add_trace(go.Scatter(
            x=result["Date"].to_list(),
            y=result["MACD"].to_list(),
            mode="lines",
            name="MACD"
        ))

        macd_fig.add_trace(go.Scatter(
            x=result["Date"].to_list(),
            y=result["MACD_Signal"].to_list(),
            mode="lines",
            name="Signal Line"
        ))

        macd_fig.update_layout(
            title="MACD Analysis",
            xaxis_title="Date",
            yaxis_title="MACD Value",
            template="plotly_dark"
        )

        st.plotly_chart(macd_fig, width="stretch")

    else:
        st.warning("No stock data available.")

# STOCK PRICE ALERTS

create_alert_table()

st.divider()
st.subheader("🔔 Stock Price Alerts")

alert_symbol = st.selectbox(
    "Select Stock",
    ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"],
    key="alert_symbol"
)

target_price = st.number_input(
    "Enter Target Price (₹)",
    min_value=0.01,
    value=1000.0,
    step=10.0
)

condition = st.selectbox(
    "Alert Condition",
    ["Above", "Below"],
    key="alert_condition"
)

if st.button("Create Price Alert"):
    add_alert(alert_symbol, target_price, condition)
    st.success("Price alert created successfully!")

st.subheader("📋 Your Saved Alerts")

alerts = get_alerts()

if alerts:
    st.dataframe(
        [
            {
                "ID": a[0],
                "Stock": a[1],
                "Target Price": a[2],
                "Condition": a[3],
                "Created At": a[4]
            }
            for a in alerts
        ],
        width="stretch"
    )

    delete_id = st.number_input(
        "Enter Alert ID to Delete",
        min_value=1,
        step=1
    )

    if st.button("Delete Alert"):
        delete_alert(int(delete_id))
        st.success("Alert deleted. Refresh the page to update the list.")

st.subheader("🔍 Check Current Stock Price")

if st.button("Check My Alerts"):
    current_data = get_stock_data(alert_symbol)

    if not current_data.is_empty():
        current_price = float(current_data["Close"][-1])

        st.metric("Latest Available Closing Price", f"₹{current_price:.2f}")

        messages = check_alerts(alert_symbol, current_price)

        if messages:
            for message in messages:
                st.warning(message)
        else:
            st.info("No price alert conditions have been reached.")
    else:
        st.warning("No stock data available.")


# PORTFOLIO MANAGEMENT

create_portfolio_table()

st.divider()
st.subheader("💼 Portfolio Management")

portfolio_symbol = st.selectbox(
    "Select Stock",
    ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"],
    key="portfolio_symbol"
)

quantity = st.number_input(
    "Enter Quantity",
    min_value=1,
    value=1,
    step=1
)

purchase_price = st.number_input(
    "Enter Purchase Price (₹)",
    min_value=0.01,
    value=1000.0,
    step=10.0
)

if st.button("Add Stock to Portfolio"):
    add_stock(
        portfolio_symbol,
        int(quantity),
        float(purchase_price)
    )
    st.success("Stock added to your portfolio!")

st.subheader("📋 My Investment Portfolio")

portfolio = get_portfolio()

if portfolio:
    portfolio_rows = []
    total_investment = 0
    total_current_value = 0

    for item in portfolio:
        stock_id, symbol, qty, buy_price, created_at = item

        stock_data = get_stock_data(symbol)

        if not stock_data.is_empty():
            current_price = float(stock_data["Close"][-1])
        else:
            current_price = buy_price

        investment = qty * buy_price
        current_value = qty * current_price
        profit_loss = current_value - investment

        total_investment += investment
        total_current_value += current_value

        portfolio_rows.append({
            "ID": stock_id,
            "Stock": symbol,
            "Quantity": qty,
            "Purchase Price": round(buy_price, 2),
            "Latest Available Price": round(current_price, 2),
            "Investment": round(investment, 2),
            "Current Value": round(current_value, 2),
            "Profit / Loss": round(profit_loss, 2)
        })

    st.dataframe(portfolio_rows, width="stretch")

    total_profit_loss = total_current_value - total_investment

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Investment",
        f"₹{total_investment:,.2f}"
    )

    col2.metric(
        "Current Value",
        f"₹{total_current_value:,.2f}"
    )

    col3.metric(
        "Profit / Loss",
        f"₹{total_profit_loss:,.2f}",
        delta=f"{total_profit_loss:,.2f}"
    )

    st.subheader("🗑️ Remove Stock")

    delete_id = st.number_input(
        "Enter Stock ID to Delete",
        min_value=1,
        step=1,
        key="portfolio_delete_id"
    )

    if st.button("Delete Portfolio Stock"):
        delete_stock(int(delete_id))
        st.success("Stock deleted successfully!")
        st.rerun()

else:
    st.info("Your portfolio is empty. Add your first stock above.")

