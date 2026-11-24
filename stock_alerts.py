
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_FILE = DATA_DIR / "quantumpulse.db"


def create_alert_table():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS stock_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                target_price REAL NOT NULL,
                condition TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)


def add_alert(symbol, target_price, condition):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            INSERT INTO stock_alerts
            (symbol, target_price, condition)
            VALUES (?, ?, ?)
        """, (symbol, target_price, condition))


def get_alerts():
    with sqlite3.connect(DB_FILE) as conn:
        return conn.execute("""
            SELECT id, symbol, target_price, condition, created_at
            FROM stock_alerts
            ORDER BY id DESC
        """).fetchall()


def delete_alert(alert_id):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "DELETE FROM stock_alerts WHERE id = ?",
            (alert_id,)
        )


def check_alerts(symbol, current_price):
    alerts = get_alerts()
    messages = []

    for alert in alerts:
        alert_id, alert_symbol, target, condition, created_at = alert

        if alert_symbol != symbol:
            continue

        if condition == "Above" and current_price >= target:
            messages.append(
                f"Alert #{alert_id}: {symbol} reached ₹{target:.2f}!"
            )

        elif condition == "Below" and current_price <= target:
            messages.append(
                f"Alert #{alert_id}: {symbol} fell to ₹{target:.2f}!"
            )

    return messages


if __name__ == "__main__":
    create_alert_table()
    print("Stock Alerts table created successfully!")
