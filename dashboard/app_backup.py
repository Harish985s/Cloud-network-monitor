import sqlite3
import os

from pathlib import Path
from flask import Flask, render_template_string


app = Flask(__name__)


# ==========================================
# DATABASE CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "network_data.db"


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_db_connection():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn


# ==========================================
# DASHBOARD DATA
# ==========================================

def get_dashboard_data():

    conn = get_db_connection()

    cursor = conn.cursor()

    # NETWORK STATISTICS

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM network_logs
    """)

    total_network_logs = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(DISTINCT ip_address) AS total
        FROM network_logs
    """)

    total_devices = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(DISTINCT ip_address) AS total
        FROM network_logs
        WHERE LOWER(status) IN ('online', 'up')
    """)

    online_devices = cursor.fetchone()["total"]

    offline_devices = max(
        total_devices - online_devices, 0
    )

    # LATEST NETWORK LOGS

    cursor.execute("""
        SELECT *
        FROM network_logs
        ORDER BY timestamp DESC
        LIMIT 10
    """)

    network_logs = [
        dict(row) for row in cursor.fetchall()
    ]

    # PORT STATISTICS

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM port_logs
    """)

    total_ports = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM port_logs
        WHERE LOWER(status) = 'open'
    """)

    open_ports = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM port_logs
        WHERE LOWER(status) = 'closed'
    """)

    closed_ports = cursor.fetchone()["total"]

    # LATEST PORT LOGS

    cursor.execute("""
        SELECT *
        FROM port_logs
        ORDER BY timestamp DESC
        LIMIT 10
    """)

    port_logs = [
        dict(row) for row in cursor.fetchall()
    ]

    # SYSTEM STATISTICS

    cursor.execute("""
        SELECT *
        FROM system_logs
        ORDER BY timestamp DESC
        LIMIT 1
    """)

    latest_system = cursor.fetchone()

    system_data = (
        dict(latest_system)
        if latest_system else None
    )

    # SYSTEM HISTORY

    cursor.execute("""
        SELECT cpu_usage, ram_usage,
               disk_usage, timestamp
        FROM (
            SELECT *
            FROM system_logs
            ORDER BY timestamp DESC
            LIMIT 20
        )
        ORDER BY timestamp ASC
    """)

    system_history = [
        dict(row) for row in cursor.fetchall()
    ]

    # NETWORK HISTORY

    cursor.execute("""
        SELECT ip_address, response_time_ms, timestamp
        FROM (
            SELECT *
            FROM network_logs
            ORDER BY timestamp DESC
            LIMIT 20
        )
        ORDER BY timestamp ASC
    """)

    network_history = [
        dict(row) for row in cursor.fetchall()
    ]

# ALERT STATISTICS

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM alerts
    """)

    total_alerts = cursor.fetchone()["total"]

    # LATEST ALERTS

    cursor.execute("""
        SELECT *
        FROM alerts
        ORDER BY timestamp DESC
        LIMIT 10
    """)

    alert_logs = [
        dict(row) for row in cursor.fetchall()
    ]


    conn.close()

    return {
        "total_devices": total_devices,
        "online_devices": online_devices,
        "offline_devices": offline_devices,
        "total_network_logs": total_network_logs,
        "total_ports": total_ports,
        "open_ports": open_ports,
        "closed_ports": closed_ports,
        "network_logs": network_logs,
        "port_logs": port_logs,
        "system_data": system_data,
        "system_history": system_history,
        "network_history": network_history,
        "total_alerts": total_alerts,
        "alert_logs": alert_logs,
    }


# ==========================================
# DASHBOARD HTML
# ==========================================

HTML = """
<!DOCTYPE html>

<html>

<head>

<title>Cloud Network Monitor</title>

<meta name="viewport"
content="width=device-width, initial-scale=1">

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<meta http-equiv="refresh" content="10">

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #101827;
    color: white;
}

header {
    background: #172438;
    padding: 22px;
    border-bottom: 1px solid #29384c;
}

header h1 {
    margin: 0;
    color: #38bdf8;
}

header p {
    color: #94a3b8;
}

.container {
    padding: 25px;
}

.cards {
    display: grid;
    grid-template-columns:
    repeat(auto-fit, minmax(180px, 1fr));
    gap: 18px;
    margin-bottom: 25px;
}

.card {
    background: #1e293b;
    padding: 22px;
    border-radius: 12px;
    border: 1px solid #334155;
}

.card h3 {
    color: #94a3b8;
    font-size: 14px;
}

.card h2 {
    font-size: 30px;
    color: #38bdf8;
}

.section {
    background: #1e293b;
    padding: 22px;
    border-radius: 12px;
    margin-bottom: 25px;
    overflow-x: auto;
}

.section h2 {
    color: #38bdf8;
}

table {
    width: 100%;
    border-collapse: collapse;
    min-width: 500px;
}

th, td {
    padding: 13px;
    text-align: left;
    border-bottom: 1px solid #334155;
}

th {
    color: #38bdf8;
}

.online, .open {
    color: #4ade80;
    font-weight: bold;
}

.offline, .closed {
    color: #f87171;
    font-weight: bold;
}

.chart-container {
    background: #1e293b;
    padding: 22px;
    border-radius: 12px;
    margin-bottom: 25px;
}

.chart-container h2 {
    color: #38bdf8;
}

.chart-box {
    position: relative;
    height: 300px;
}

.system-grid {
    display: grid;
    grid-template-columns:
    repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
}

footer {
    text-align: center;
    padding: 20px;
    color: #94a3b8;
}

</style>

</head>

<body>

<header>

<h1>☁ Cloud Network Monitor</h1>

<p>Network and Cloud Infrastructure Monitoring Dashboard</p>

</header>


<div class="container">


<!-- STATISTICS -->

<div class="cards">

<div class="card">

<h3>Total Devices</h3>

<h2>{{ data.total_devices }}</h2>

</div>


<div class="card">

<h3>Online Devices</h3>

<h2>{{ data.online_devices }}</h2>

</div>


<div class="card">

<h3>Offline Devices</h3>

<h2>{{ data.offline_devices }}</h2>

</div>


<div class="card">

<h3>Total Ports</h3>

<h2>{{ data.total_ports }}</h2>

</div>


<div class="card">

<h3>Open Ports</h3>

<h2>{{ data.open_ports }}</h2>

</div>


<div class="card">

<h3>Closed Ports</h3>

<h2>{{ data.closed_ports }}</h2>

</div>

</div>


<!-- NETWORK MONITORING -->

<div class="section">

<h2>Network Monitoring</h2>

<table>

<tr>

<th>IP Address</th>

<th>Status</th>

<th>Response Time</th>

<th>Timestamp</th>

</tr>

{% for row in data.network_logs %}

<tr>

<td>{{ row.ip_address }}</td>

<td class="{% if row.status|lower in ['online', 'up'] %}online{% else %}offline{% endif %}">

{{ row.status }}

</td>

<td>{{ row.response_time_ms }} ms</td>

<td>{{ row.timestamp }}</td>

</tr>

{% else %}

<tr>
<td colspan="4">No network records available</td>
</tr>

{% endfor %}

</table>

</div>


<!-- PORT MONITORING -->

<div class="section">

<h2>Port Monitoring</h2>

<table>

<tr>

<th>Host</th>

<th>Port</th>

<th>Status</th>

<th>Timestamp</th>

</tr>

{% for row in data.port_logs %}

<tr>

<td>{{ row.host }}</td>

<td>{{ row.port }}</td>

<td class="{% if row.status|lower == 'open' %}open{% else %}closed{% endif %}">

{{ row.status }}

</td>

<td>{{ row.timestamp }}</td>

</tr>

{% else %}

<tr>
<td colspan="4">No port records available</td>
</tr>

{% endfor %}

</table>

</div>

<!-- ALERT MONITORING -->

<div class="section">

<h2>🚨 Alert Monitoring</h2>

<div class="cards">

<div class="card">

<h3>Total Alerts</h3>

<h2>{{ data.total_alerts }}</h2>

</div>

</div>

<table>

<tr>

<th>Alert ID</th>
<th>Alert Type</th>
<th>Message</th>
<th>Severity</th>
<th>Timestamp</th>

</tr>

{% for alert in data.alert_logs %}

<tr>

<td>{{ alert.id }}</td>

<td>{{ alert.alert_type }}</td>

<td>{{ alert.message }}</td>

<td>
<strong>{{ alert.severity }}</strong>
</td>

<td>{{ alert.timestamp }}</td>

</tr>

{% else %}

<tr>

<td colspan="5">No alerts available</td>

</tr>

{% endfor %}

</table>

</div>



<!-- SYSTEM MONITORING -->

<div class="section">

<h2>System Monitoring</h2>

{% if data.system_data %}

<div class="system-grid">

<div class="card">

<h3>CPU Usage</h3>

<h2>{{ data.system_data.cpu_usage }}%</h2>

</div>


<div class="card">

<h3>RAM Usage</h3>

<h2>{{ data.system_data.ram_usage }}%</h2>

</div>


<div class="card">

<h3>Disk Usage</h3>

<h2>{{ data.system_data.disk_usage }}%</h2>

</div>

</div>

{% else %}

<p>No system records available.</p>

{% endif %}

</div>


<!-- SYSTEM CHART -->

<div class="chart-container">

<h2>System Performance History</h2>

<div class="chart-box">

<canvas id="systemChart"></canvas>

</div>

</div>


<!-- NETWORK CHART -->

<div class="chart-container">

<h2>Network Response Time</h2>

<div class="chart-box">

<canvas id="networkChart"></canvas>

</div>

</div>


</div>


<footer>

Cloud Network Monitor | Auto Refresh: 10 Seconds

</footer>


<script>

const systemHistory =
{{ data.system_history | tojson }};

const networkHistory =
{{ data.network_history | tojson }};


new Chart(
    document.getElementById('systemChart'),
    {
        type: 'line',

        data: {
            labels: systemHistory.map(
                item => item.timestamp
            ),

            datasets: [

                {
                    label: 'CPU Usage',
                    data: systemHistory.map(
                        item => item.cpu_usage
                    ),
                    borderWidth: 2
                },

                {
                    label: 'RAM Usage',
                    data: systemHistory.map(
                        item => item.ram_usage
                    ),
                    borderWidth: 2
                },

                {
                    label: 'Disk Usage',
                    data: systemHistory.map(
                        item => item.disk_usage
                    ),
                    borderWidth: 2
                }

            ]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    }
);


new Chart(
    document.getElementById('networkChart'),
    {
        type: 'line',

        data: {
            labels: networkHistory.map(
                item => item.timestamp
            ),

            datasets: [

                {
                    label: 'Response Time (ms)',

                    data: networkHistory.map(
                        item => item.response_time_ms
                    ),

                    borderWidth: 2
                }

            ]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    }
);

</script>

</body>

</html>
"""


# ==========================================
# DASHBOARD ROUTE
# ==========================================

@app.route("/")

def dashboard():

    try:

        data = get_dashboard_data()


        return render_template_string(
            HTML,
            data=data
        )

    except sqlite3.Error as error:

        return f"Database Error: {error}", 500


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )