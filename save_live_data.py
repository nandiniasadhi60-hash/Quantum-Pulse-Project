
from live_stock import get_stock_data
from database import create_table, insert_data

create_table()

df = get_stock_data("RELIANCE.NS")

if df.is_empty():
    print("No stock data available.")
else:
    for row in df.iter_rows(named=True):
        insert_data(
            str(row["Date"]),
            row["Open"],
            row["High"],
            row["Low"],
            row["Close"],
            row["Volume"]
        )

    print("Live stock data saved successfully!")
