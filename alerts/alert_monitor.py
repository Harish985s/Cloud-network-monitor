import sqlite3
from pathlib import Path
from datetime import datetime


# ==========================================
# DATABASE CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "network_data.db"


# ==========================================
# ALERT THRESHOLDS
# ==========================================

CPU_THRESHOLD = 80
RAM_THRESHOLD = 90
DISK_THRESHOLD = 90


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_connection():

    conn = sqlite3.connect(DB_PATH)

    return conn


# ==========================================
# CREATE ALERT TABLE
# ==========================================

def create_alert_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alert_type TEXT,
            message TEXT,
            severity TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()

    conn.close()


# ==========================================
# SAVE ALERT
# ==========================================

def save_alert(alert_type, message, severity):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO alerts (
            alert_type,
            message,
            severity,
            timestamp
        )
        VALUES (?, ?, ?, ?)
    """, (
        alert_type,
        message,
        severity,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()

    conn.close()


# ==========================================
# SYSTEM ALERT MONITORING
# ==========================================

def check_system_alerts():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT cpu_usage, ram_usage, disk_usage
        FROM system_logs
        ORDER BY timestamp DESC
        LIMIT 1
    """)

    system = cursor.fetchone()

    conn.close()

    if system is None:
        print("No system monitoring data available.")
        return

    cpu, ram, disk = system

    if cpu >= CPU_THRESHOLD:

        save_alert(
            "CPU",
            f"High CPU usage: {cpu}%",
            "WARNING"
        )

    if ram >= RAM_THRESHOLD:

        save_alert(
            "RAM",
            f"High RAM usage: {ram}%",
            "CRITICAL"
        )

    if disk >= DISK_THRESHOLD:

        save_alert(
            "DISK",
            f"High Disk usage: {disk}%",
            "CRITICAL"
        )


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    create_alert_table()

    check_system_alerts()

    print("Alert monitoring completed.")