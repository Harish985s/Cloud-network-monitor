import socket
import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "network_data.db"

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

host = "8.8.8.8"
port = 443

result = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result.settimeout(3)

status_code = result.connect_ex((host, port))
result.close()

status = "OPEN" if status_code == 0 else "CLOSED"

print("NETWORK PORT MONITOR")
print("--------------------")
print("Host:", host)
print("Port:", port)
print("Status:", status)
print("Time:", datetime.now())

cursor.execute(
"INSERT INTO port_logs (host, port, status) VALUES (?, ?, ?)",
(host, port, status)
)

connection.commit()
connection.close()

print("Result saved successfully in SQLite.")