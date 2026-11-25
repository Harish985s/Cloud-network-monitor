import subprocess
import platform

target = input("Enter IP address or domain: ")

print("\n========== PING TEST ==========")

system = platform.system().lower()

if system == "windows":
    ping_command = ["ping", "-n", "4", target]
else:
    ping_command = ["ping", "-c", "4", target]

subprocess.run(ping_command)

print("\n========== TRACEROUTE TEST ==========")

if system == "windows":
    trace_command = ["tracert", target]
else:
    trace_command = ["traceroute", target]

try:
    subprocess.run(trace_command)
except FileNotFoundError:
    print("Traceroute command is not installed.")