# CCNA Network Topology Monitoring

devices = {
    "Router-1": "192.168.1.1",
    "Switch-1": "192.168.1.2",
    "PC-1": "192.168.1.10",
    "PC-2": "192.168.1.11",
    "Server-1": "192.168.1.100"
}

connections = [
    ("Router-1", "Switch-1"),
    ("Switch-1", "PC-1"),
    ("Switch-1", "PC-2"),
    ("Switch-1", "Server-1")
]

print("========== NETWORK TOPOLOGY ==========")

print("\nCONNECTED DEVICES:")

for device, ip in devices.items():
    print(f"{device} -> {ip}")

print("\nNETWORK CONNECTIONS:")

for source, destination in connections:
    print(f"{source} --------> {destination}")

print("\nTotal Devices:", len(devices))
print("Total Connections:", len(connections))