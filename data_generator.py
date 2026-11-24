import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# ==========================================
# QUANTUMPULSE - FINANCIAL DATA GENERATOR
# ==========================================

DATA_FOLDER = "data"
OUTPUT_FILE = os.path.join(DATA_FOLDER, "financial_data.csv")


def generate_financial_data(number_of_records=10000):

    # Create data folder if it does not exist
    os.makedirs(DATA_FOLDER, exist_ok=True)

    # Set random seed for reproducible data
    np.random.seed(42)

    # Stock symbols and sample prices
    symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "NVDA"]

    base_prices = {
        "AAPL": 225.0,
        "GOOGL": 180.0,
        "MSFT": 420.0,
        "AMZN": 210.0,
        "NVDA": 140.0
    }

    # Generate transaction timestamps
    start_time = datetime.now().replace(
        hour=9,
        minute=15,
        second=0,
        microsecond=0
    )

    time_offsets = np.random.randint(
        0, 23400000, number_of_records
    )

    timestamps = [
        start_time + timedelta(milliseconds=int(ms))
        for ms in time_offsets
    ]

    # Generate transaction details
    selected_symbols = np.random.choice(
        symbols, number_of_records
    )

    quantities = np.random.randint(
        1, 1001, number_of_records
    )

    sides = np.random.choice(
        ["BUY", "SELL"], number_of_records
    )

    price_changes = np.random.normal(
        0, 0.15, number_of_records
    )

    prices = [
        round(max(base_prices[symbol] + change, 0.01), 2)
        for symbol, change in zip(
            selected_symbols, price_changes
        )
    ]

    # Create DataFrame
    df = pd.DataFrame({
        "trade_id": range(1, number_of_records + 1),
        "timestamp": timestamps,
        "symbol": selected_symbols,
        "price": prices,
        "quantity": quantities,
        "side": sides
    })

    # Sort transactions by timestamp
    df = df.sort_values(
        "timestamp"
    ).reset_index(drop=True)

    # Calculate total transaction value
    df["trade_value"] = (
        df["price"] * df["quantity"]
    ).round(2)

    # Save CSV file
    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\n===================================")
    print("       QUANTUMPULSE ENGINE")
    print("===================================")

    print("Financial data generated successfully!")
    print("Total records:", len(df))
    print("Saved file:", OUTPUT_FILE)

    print("\nSample Financial Transactions:")
    print(df.head())

    return df


# Run the program
if __name__ == "__main__":
    generate_financial_data()
