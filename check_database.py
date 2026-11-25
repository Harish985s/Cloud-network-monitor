import sqlite3

db = sqlite3.connect("database/network_data.db")
cursor = db.cursor()

cursor.execute("PRAGMA table_info(network_logs)")

for column in cursor.fetchall():
    print(column)

db.close()