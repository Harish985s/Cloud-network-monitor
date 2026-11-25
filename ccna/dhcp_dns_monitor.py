import subprocess
import platform
import socket


def dhcp_monitor():
	print("\n========== DHCP MONITORING ==========")

	if platform.system() == "Windows":
		try:
			result = subprocess.check_output(
				"ipconfig /all",
				shell=True,
				text=True
			)

			for line in result.splitlines():
				if "DHCP Server" in line or "IPv4 Address" in line or "Default Gateway" in line or "Subnet Mask" in line:
					print(line.strip())

		except Exception as e:
			print("DHCP Error:", e)


def dns_monitor():
	print("\n========== DNS MONITORING ==========")

	if platform.system() == "Windows":
		try:
			result = subprocess.check_output(
				"ipconfig /all",
				shell=True,
				text=True
			)

			for line in result.splitlines():
				if "DNS Servers" in line:
					print(line.strip())

		except Exception as e:
			print("DNS Error:", e)


def dns_resolution_test():
	print("\n========== DNS RESOLUTION TEST ==========")

	try:
		ip_address = socket.gethostbyname("google.com")
		print("Domain: google.com")
		print("Resolved IP:", ip_address)
		print("DNS Status: SUCCESSFUL")

	except Exception as e:
		print("DNS Status: FAILED")
		print("Error:", e)


if __name__ == "__main__":
	dhcp_monitor()
	dns_monitor()
	dns_resolution_test()

	print("\nMONITORING COMPLETED")