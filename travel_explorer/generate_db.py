import sqlite3
from pathlib import Path

SAMPLE_DATA = [
    ('USA', 'Alice', 'France', 1000, '2023-01-10'),
    ('USA', 'Bob', 'Japan', 1500, '2023-02-12'),
    ('France', 'Claire', 'USA', 1200, '2023-03-15'),
    ('Japan', 'Daisuke', 'Brazil', 1300, '2023-04-18'),
    ('Brazil', 'Elisa', 'USA', 1100, '2023-05-20'),
]

CREATE_TABLE_SQL = '''
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country TEXT,
    agent TEXT,
    destination TEXT,
    price REAL,
    date TEXT
)'''

INSERT_SQL = (
    'INSERT INTO bookings (country, agent, destination, price, date) '
    'VALUES (?, ?, ?, ?, ?)'
)

def create_sample_db(db_path: str = 'bookings.db') -> None:
    """Create a SQLite database with a simple bookings table and sample data."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(CREATE_TABLE_SQL)
    cur.executemany(INSERT_SQL, SAMPLE_DATA)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_sample_db()
    print("Database created with sample data.")
