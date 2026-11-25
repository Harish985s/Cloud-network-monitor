import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "network_data.db"

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS port_logs (
id INTEGER PRIMARY KEY AUTOINCREMENT,
host TEXT,
port INTEGER,
status TEXT,
timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS system_logs (
id INTEGER PRIMARY KEY AUTOINCREMENT,
cpu_usage REAL,
ram_usage REAL,
disk_usage REAL,
timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

connection.commit()
connection.close()

print("====================================")
print("DATABASE SETUP SUCCESSFUL")
print("====================================")
print("Port monitoring table created.")
print("System monitoring table created.")
print("Database:", DB_PATH)