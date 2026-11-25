# ==========================================
# CISCO INTERFACE MONITOR
# ==========================================

def monitor_interfaces():

    print("\n========== CISCO INTERFACE MONITOR ==========\n")

    router_output = """
Interface              IP-Address      OK? Method Status Protocol
GigabitEthernet0/0      192.168.1.1     YES manual up     up
GigabitEthernet0/1      192.168.2.1     YES manual down   down
FastEthernet0/0         unassigned      YES unset  down   down
"""

    lines = router_output.strip().split("\n")

    print("{:<25} {:<18} {:<12} {:<12}".format(
        "Interface", "IP Address", "Status", "Protocol"
    ))

    print("-" * 70)

    for line in lines[1:]:

        parts = line.split()

        if len(parts) >= 6:

            interface = parts[0]
            ip_address = parts[1]
            status = parts[4]
            protocol = parts[5]

            print("{:<25} {:<18} {:<12} {:<12}".format(
                interface,
                ip_address,
                status,
                protocol
            ))


if __name__ == "__main__":

    monitor_interfaces()