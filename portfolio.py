
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_FILE = DATA_DIR / "quantumpulse.db"


def create_portfolio_table():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS portfolio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                purchase_price REAL NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)


def add_stock(symbol, quantity, purchase_price):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            INSERT INTO portfolio
            (symbol, quantity, purchase_price)
            VALUES (?, ?, ?)
        """, (symbol, quantity, purchase_price))


def get_portfolio():
    with sqlite3.connect(DB_FILE) as conn:
        return conn.execute("""
            SELECT id, symbol, quantity, purchase_price, created_at
  FROM portfolio
            ORDER BY id DESC
        """).fetchall()

def delete_stock(stock_id):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "DELETE FROM portfolio WHERE id = ?",
            (stock_id,)
        )


if __name__ == "__main__":
    create_portfolio_table()
    print("Portfolio table created successfully!")
