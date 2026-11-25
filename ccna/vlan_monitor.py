# ==========================================
# CISCO VLAN MONITOR
# ==========================================

vlans = [

    {
        "vlan_id": 1,
        "vlan_name": "DEFAULT",
        "status": "Active",
        "ports": "Gi0/1"
    },

    {
        "vlan_id": 10,
        "vlan_name": "ADMIN",
        "status": "Active",
        "ports": "Gi0/2"
    },

    {
        "vlan_id": 20,
        "vlan_name": "NETWORK",
        "status": "Active",
        "ports": "Gi0/3"
    },

    {
        "vlan_id": 30,
        "vlan_name": "SERVER",
        "status": "Active",
        "ports": "Gi0/4"
    }

]


def show_vlans():

    print("\n========== CISCO VLAN MONITOR ==========\n")

    print("{:<12} {:<15} {:<12} {:<15}".format(
        "VLAN ID", "VLAN NAME", "STATUS", "PORT"
    ))

    print("-" * 60)

    for vlan in vlans:

        print("{:<12} {:<15} {:<12} {:<15}".format(
            vlan["vlan_id"],
            vlan["vlan_name"],
            vlan["status"],
            vlan["ports"]
        ))


if __name__ == "__main__":

    show_vlans()