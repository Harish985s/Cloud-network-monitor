# ==========================================
# CCNA DEVICE INVENTORY
# ==========================================

devices = [

    {
        "hostname": "Router-1",
        "device_type": "Router",
        "vendor": "Cisco",
        "ip_address": "192.168.1.1",
        "status": "Configured"
    },

    {
        "hostname": "Switch-1",
        "device_type": "Switch",
        "vendor": "Cisco",
        "ip_address": "192.168.1.2",
        "status": "Configured"
    },

]


# ==========================================
# DISPLAY DEVICE INVENTORY
# ==========================================

def show_devices():

    print("\n========== CCNA DEVICE INVENTORY ==========\n")

    for device in devices:

        print("Hostname:", device["hostname"])
        print("Device Type:", device["device_type"])
        print("Vendor:", device["vendor"])
        print("IP Address:", device["ip_address"])
        print("Status:", device["status"])

        print("------------------------------------------")


# ==========================================
# MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    show_devices()