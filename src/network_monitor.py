import os
import platform
import time
import sqlite3


def save_log(ip, status):
    conn = sqlite3.connect("database/network_data.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO network_logs (ip_address, status) VALUES (?, ?)",
        (ip, status)
    )

    conn.commit()
    conn.close()


def check_device(ip):

    param = "-n" if platform.system().lower() == "windows" else "-c"

    command = f"ping {param} 1 {ip}"

    response = os.system(command)

    if response == 0:
        status = "ONLINE"
        print(f"{ip} is ONLINE")
    else:
        status = "OFFLINE"
        print(f"{ip} is OFFLINE")

    save_log(ip, status)


devices = [
    "8.8.8.8",
    "1.1.1.1",
    "127.0.0.1"
]

print("===== NETWORK MONITOR =====")

for ip in devices:
    check_device(ip)
    time.sleep(1)
print("===== MONITORING COMPLETED =====")