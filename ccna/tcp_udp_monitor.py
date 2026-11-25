import socket

# Common TCP ports
ports = {
    20: "FTP Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS"
}

target = input("Enter target IP address: ")

print("\n========== TCP PORT MONITOR ==========")

for port, service in ports.items():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

    result = sock.connect_ex((target, port))

    if result == 0:
        print(f"{service} (Port {port}): OPEN")
    else:
        print(f"{service} (Port {port}): CLOSED or FILTERED")

    sock.close()