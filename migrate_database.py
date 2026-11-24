
import sqlite3
from database import DATABASE_FILE

conn = sqlite3.connect(DATABASE_FILE)

try:
    conn.execute("BEGIN")

    conn.execute("""
        DELETE FROM stocks
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM stocks
            GROUP BY date
        )
    """)

    conn.execute("""
        CREATE TABLE stocks_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL UNIQUE,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER
        )
    """)

    conn.execute("""
        INSERT INTO stocks_new
        (id, date, open, high, low, close, volume)
        SELECT id, date, open, high, low, close, volume
        FROM stocks
    """)

    conn.execute("DROP TABLE stocks")
    conn.execute("ALTER TABLE stocks_new RENAME TO stocks")

    conn.commit()
    print("Database migration completed successfully!")

except Exception as error:
    conn.rollback()
    print("Migration failed:", error)

finally:
    conn.close()
