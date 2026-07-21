"""
One-time migration: adds the new pixel-hit tracking columns to the
existing `emails` table in email_tracker.db, without touching existing rows.

Run this once locally / on Render (via a shell) with:
    python migrate_add_pixel_columns.py
"""

import sqlite3

DB_PATH = "email_tracker.db"

NEW_COLUMNS = [
    ("pixel_hit_count", "INTEGER DEFAULT 0"),
    ("last_pixel_user_agent", "TEXT"),
    ("first_pixel_hit_at", "DATETIME"),
]


def main():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute("PRAGMA table_info(emails)")
    existing_columns = {row[1] for row in cur.fetchall()}

    for col_name, col_def in NEW_COLUMNS:
        if col_name in existing_columns:
            print(f"Skipping '{col_name}' -- already exists.")
            continue
        sql = f"ALTER TABLE emails ADD COLUMN {col_name} {col_def}"
        print(f"Running: {sql}")
        cur.execute(sql)

    con.commit()
    con.close()
    print("Migration complete.")


if __name__ == "__main__":
    main()