import sqlite3
from travel_explorer.generate_db import create_sample_db, SAMPLE_DATA


def test_create_sample_db(tmp_path):
    db_file = tmp_path / "sample.db"
    create_sample_db(str(db_file))
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM bookings")
    row_count = cur.fetchone()[0]
    conn.close()
    assert row_count == len(SAMPLE_DATA)
