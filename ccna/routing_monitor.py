# ==========================================
# CISCO ROUTING TABLE MONITOR
# ==========================================

routes = [

    {
        "network": "192.168.1.0/24",
        "next_hop": "Directly Connected",
        "interface": "GigabitEthernet0/0"
    },

    {
        "network": "192.168.2.0/24",
        "next_hop": "192.168.1.2",
        "interface": "GigabitEthernet0/1"
    },

    {
        "network": "10.0.0.0/8",
        "next_hop": "192.168.1.254",
        "interface": "GigabitEthernet0/0"
    }

]


def show_routes():

    print("\n========== CISCO ROUTING TABLE ==========\n")

    print("{:<22} {:<25} {:<25}".format(
        "NETWORK",
        "NEXT HOP",
        "INTERFACE"
    ))

    print("-" * 75)

    for route in routes:

        print("{:<22} {:<25} {:<25}".format(
            route["network"],
            route["next_hop"],
            route["interface"]
        ))


if __name__ == "__main__":

    show_routes()