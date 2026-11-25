import sqlite3

db = sqlite3.connect("database/network_data.db")
cursor = db.cursor()

cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
)

tables = cursor.fetchall()

for table in tables:
    name = table[0]

    print("\nTABLE:", name)

    cursor.execute(f"PRAGMA table_info({name})")

    columns = cursor.fetchall()

    for column in columns:
        print(column)

db.close()