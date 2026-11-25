import socket

udp_ports = {
    53: "DNS",
    67: "DHCP Server",
    69: "TFTP",
    123: "NTP",
    161: "SNMP"
}

target = input("Enter target IP address: ")

print("\n========== UDP PORT MONITOR ==========")

for port, service in udp_ports.items():

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2)

    try:
        sock.sendto(b"\x00", (target, port))
        data, address = sock.recvfrom(1024)

        print(f"{service} (Port {port}): RESPONSE RECEIVED")

    except socket.timeout:
        print(f"{service} (Port {port}): NO RESPONSE")

    except OSError as error:
        print(f"{service} (Port {port}): ERROR - {error}")

    finally:
        sock.close()