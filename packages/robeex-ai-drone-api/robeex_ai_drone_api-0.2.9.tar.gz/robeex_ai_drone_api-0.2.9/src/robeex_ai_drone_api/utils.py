import platform
import subprocess

def get_wifi_status():
    system = platform.system()

    try:
        if system == "Linux":
            result = subprocess.run(['nmcli', '-t', '-f', 'ACTIVE,SSID', 'dev', 'wifi'],
                                     stdout=subprocess.PIPE, text=True)
            active_connections = [line.split(':')[1] for line in result.stdout.splitlines() if line.startswith('yes')]
            return active_connections if active_connections else "No active Wi-Fi connection"

        elif system == "Windows":
            result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'],
                                     stdout=subprocess.PIPE, text=True)
            for line in result.stdout.splitlines():
                if "SSID" in line and "BSSID" not in line:
                    return line.split(":")[1].strip()
            return "No active Wi-Fi connection"

        elif system == "Darwin":  # macOS
            result = subprocess.run(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I'],
                                     stdout=subprocess.PIPE, text=True)
            for line in result.stdout.splitlines():
                if " SSID" in line:
                    return line.split(":")[1].strip()
            return "No active Wi-Fi connection"

        else:
            return "Unsupported operating system"

    except Exception as e:
        return f"Error retrieving Wi-Fi status: {e}"
