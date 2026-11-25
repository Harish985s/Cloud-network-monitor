import psutil
import platform
import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "network_data.db"

cpu = psutil.cpu_percent(interval=1)
memory = psutil.virtual_memory()
disk = psutil.disk_usage("C:\\")

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

print("====================================")
print("       SYSTEM RESOURCE MONITOR")
print("====================================")

print("Date and Time:", datetime.now())
print("Operating System:", platform.system())
print("Computer Name:", platform.node())

print("------------------------------------")
print("CPU Usage:", cpu, "%")
print("RAM Usage:", memory.percent, "%")
print("RAM Available:", round(memory.available / (1024 ** 3), 2), "GB")
print("Disk Usage:", disk.percent, "%")
print("Disk Free:", round(disk.free / (1024 ** 3), 2), "GB")

cursor.execute(
"INSERT INTO system_logs (cpu_usage, ram_usage, disk_usage) VALUES (?, ?, ?)",
(cpu, memory.percent, disk.percent)
)

connection.commit()
connection.close()

print("------------------------------------")
print("System results saved successfully in SQLite.")