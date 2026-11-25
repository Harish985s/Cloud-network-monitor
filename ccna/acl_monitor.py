# CCNA Access Control List Monitoring

acl_output = [
    "10 permit ip 192.168.1.0 0.0.0.255 any",
    "20 deny ip 192.168.2.0 0.0.0.255 any",
    "30 permit tcp any any eq 80",
    "40 permit tcp any any eq 443",
    "50 deny ip any any"
]

print("========== ACL MONITORING ==========")

for rule in acl_output:

    parts = rule.split()

    rule_number = parts[0]
    action = parts[1].upper()

    if action == "PERMIT":
        status = "ALLOWED"
    elif action == "DENY":
        status = "BLOCKED"
    else:
        status = "UNKNOWN"

    print(f"Rule {rule_number}: {status}")
    print(f"Configuration: {rule}")
    print("--------------------------------")