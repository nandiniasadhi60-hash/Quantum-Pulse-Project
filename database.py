
import sqlite3
from pathlib import Path

# Database location
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATABASE_FILE = DATA_DIR / "quantumpulse.db"


# Connect to SQLite database
def connect_database():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DATABASE_FILE)
    return conn


# Create financial data table
def create_table():
    conn = connect_database()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER
        )
    """)

    conn.commit()
    conn.close()


# Insert financial records
def insert_data(date, open_price, high, low, close, volume):
    conn = connect_database()
    conn.execute("""
        INSERT OR IGNORE INTO stocks
        (date, open, high, low, close, volume)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, open_price, high, low, close, volume))
    conn.commit()
    conn.close()


# Read financial records
def get_all_data():
    conn = connect_database()

    cursor = conn.execute(
        "SELECT * FROM stocks ORDER BY date"
    )

    records = cursor.fetchall()
    conn.close()

    return records


# Run database setup
if __name__ == "__main__":
    create_table()
    print("QuantumPulse database created successfully!")
