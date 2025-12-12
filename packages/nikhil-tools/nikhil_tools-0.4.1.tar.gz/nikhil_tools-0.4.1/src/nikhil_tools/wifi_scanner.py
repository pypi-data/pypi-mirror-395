"""WiFi scanner module for OnWords (macOS, Windows, Linux)."""

from __future__ import annotations

import subprocess
import re
import plistlib
from dataclasses import dataclass

# Brand colors for terminal output
RED = "\033[31m"
WHITE = "\033[37m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
DIM = "\033[2m"
RESET = "\033[0m"


@dataclass
class WiFiNetwork:
    """WiFi network information."""

    ssid: str
    bssid: str
    rssi: int
    channel: int
    security: str

    def __str__(self) -> str:
        return f"{self.ssid} ({self.bssid}) — RSSI: {self.rssi} dBm, Ch: {self.channel}"

    @property
    def signal_quality(self) -> str:
        """Return human-readable signal quality."""
        if self.rssi >= -50:
            return "Excellent"
        elif self.rssi >= -60:
            return "Good"
        elif self.rssi >= -70:
            return "Fair"
        else:
            return "Weak"

    @property
    def signal_color(self) -> str:
        """Return ANSI color based on signal strength."""
        if self.rssi >= -50:
            return GREEN
        elif self.rssi >= -60:
            return CYAN
        elif self.rssi >= -70:
            return YELLOW
        else:
            return RED


def scan_wifi_macos_corewlan() -> list[WiFiNetwork]:
    """
    Scan WiFi networks on macOS using CoreWLAN via PyObjC.

    Returns:
        List of WiFiNetwork objects sorted by RSSI (strongest first).
    """
    try:
        import objc
        from CoreWLAN import CWInterface, CWNetwork

        interface = CWInterface.interface()
        if interface is None:
            raise RuntimeError("No WiFi interface found")

        networks_set, error = interface.scanForNetworksWithName_error_(None, None)
        if error:
            raise RuntimeError(f"Scan failed: {error}")

        networks: list[WiFiNetwork] = []
        for net in networks_set:
            ssid = net.ssid() or "(Hidden)"
            bssid = net.bssid() or "Unknown"
            rssi = net.rssiValue()
            channel = net.wlanChannel().channelNumber() if net.wlanChannel() else 0

            # Get security type
            security_parts = []
            if net.supportsSecurity_(1):  # WEP
                security_parts.append("WEP")
            if net.supportsSecurity_(2):  # WPA Personal
                security_parts.append("WPA")
            if net.supportsSecurity_(4):  # WPA2 Personal
                security_parts.append("WPA2")
            if net.supportsSecurity_(8):  # WPA Enterprise
                security_parts.append("WPA-Enterprise")
            if net.supportsSecurity_(16):  # WPA2 Enterprise
                security_parts.append("WPA2-Enterprise")
            if net.supportsSecurity_(32):  # WPA3 Personal
                security_parts.append("WPA3")
            security = ", ".join(security_parts) if security_parts else "Open"

            networks.append(
                WiFiNetwork(
                    ssid=ssid,
                    bssid=bssid,
                    rssi=rssi,
                    channel=channel,
                    security=security,
                )
            )

        networks.sort(key=lambda n: n.rssi, reverse=True)
        return networks

    except ImportError:
        raise RuntimeError("CoreWLAN not available. Install pyobjc-framework-CoreWLAN.")


def scan_wifi_macos_system_profiler() -> list[WiFiNetwork]:
    """
    Scan WiFi networks on macOS using system_profiler (fallback).

    Returns:
        List of WiFiNetwork objects sorted by RSSI (strongest first).
    """
    try:
        result = subprocess.run(
            ["system_profiler", "SPAirPortDataType", "-xml"],
            capture_output=True,
            timeout=15,
        )

        if result.returncode != 0:
            raise RuntimeError("system_profiler failed")

        plist = plistlib.loads(result.stdout)
        networks: list[WiFiNetwork] = []

        # Navigate the plist structure to find networks
        for item in plist:
            if "_items" in item:
                for airport_item in item["_items"]:
                    if "spairport_airport_other_local_wireless_networks" in airport_item:
                        for net in airport_item["spairport_airport_other_local_wireless_networks"]:
                            ssid = net.get("_name", "(Hidden)")
                            bssid = net.get("spairport_network_bssid", "Unknown")
                            rssi = net.get("spairport_signal_noise", -100)
                            channel_str = net.get("spairport_network_channel", "0")
                            # Channel can be like "6" or "6 (2.4 GHz)"
                            channel = int(re.match(r"\d+", str(channel_str)).group()) if channel_str else 0
                            security = net.get("spairport_security_mode", "Open")

                            networks.append(
                                WiFiNetwork(
                                    ssid=ssid,
                                    bssid=bssid,
                                    rssi=rssi if isinstance(rssi, int) else -100,
                                    channel=channel,
                                    security=security,
                                )
                            )

        networks.sort(key=lambda n: n.rssi, reverse=True)
        return networks

    except Exception as e:
        raise RuntimeError(f"system_profiler scan failed: {e}")


def scan_wifi_macos() -> list[WiFiNetwork]:
    """
    Scan WiFi networks on macOS using best available method.

    Returns:
        List of WiFiNetwork objects sorted by RSSI (strongest first).
    """
    # Try CoreWLAN first (most reliable)
    try:
        return scan_wifi_macos_corewlan()
    except Exception:
        pass

    # Fallback to system_profiler
    return scan_wifi_macos_system_profiler()


def scan_wifi_windows() -> list[WiFiNetwork]:
    """
    Scan WiFi networks on Windows using netsh.
    
    Returns:
        List of WiFiNetwork objects sorted by RSSI (strongest first).
    """
    try:
        result = subprocess.run(
            ["netsh", "wlan", "show", "networks", "mode=Bssid"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        
        if result.returncode != 0:
            raise RuntimeError("netsh wlan command failed")
        
        networks: list[WiFiNetwork] = []
        current_ssid = None
        current_bssid = None
        current_signal = 0
        current_channel = 0
        current_security = "Open"
        
        for line in result.stdout.split("\n"):
            line = line.strip()
            
            if line.startswith("SSID") and "BSSID" not in line:
                # Save previous network if exists
                if current_ssid and current_bssid:
                    # Convert signal percentage to approximate dBm
                    rssi = int((current_signal / 2) - 100)
                    networks.append(WiFiNetwork(
                        ssid=current_ssid,
                        bssid=current_bssid,
                        rssi=rssi,
                        channel=current_channel,
                        security=current_security,
                    ))
                current_ssid = line.split(":", 1)[1].strip() if ":" in line else None
                current_bssid = None
                
            elif "BSSID" in line and ":" in line:
                parts = line.split(":", 1)
                if len(parts) > 1:
                    current_bssid = parts[1].strip()
                    
            elif "Signal" in line:
                match = re.search(r"(\d+)%", line)
                if match:
                    current_signal = int(match.group(1))
                    
            elif "Channel" in line:
                match = re.search(r":\s*(\d+)", line)
                if match:
                    current_channel = int(match.group(1))
                    
            elif "Authentication" in line:
                current_security = line.split(":", 1)[1].strip() if ":" in line else "Open"
        
        # Don't forget the last network
        if current_ssid and current_bssid:
            rssi = int((current_signal / 2) - 100)
            networks.append(WiFiNetwork(
                ssid=current_ssid,
                bssid=current_bssid,
                rssi=rssi,
                channel=current_channel,
                security=current_security,
            ))
        
        networks.sort(key=lambda n: n.rssi, reverse=True)
        return networks
        
    except Exception as e:
        raise RuntimeError(f"Windows WiFi scan failed: {e}")


def scan_wifi_linux() -> list[WiFiNetwork]:
    """
    Scan WiFi networks on Linux using nmcli or iwlist.
    
    Returns:
        List of WiFiNetwork objects sorted by RSSI (strongest first).
    """
    networks: list[WiFiNetwork] = []
    
    # Try nmcli first (NetworkManager)
    try:
        result = subprocess.run(
            ["nmcli", "-t", "-f", "SSID,BSSID,SIGNAL,CHAN,SECURITY", "dev", "wifi", "list"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        
        if result.returncode == 0:
            for line in result.stdout.strip().split("\n"):
                if not line:
                    continue
                parts = line.split(":")
                if len(parts) >= 5:
                    ssid = parts[0] or "(Hidden)"
                    bssid = parts[1]
                    signal_pct = int(parts[2]) if parts[2] else 0
                    channel = int(parts[3]) if parts[3] else 0
                    security = parts[4] or "Open"
                    
                    # Convert signal percentage to approximate dBm
                    rssi = int((signal_pct / 2) - 100)
                    
                    networks.append(WiFiNetwork(
                        ssid=ssid,
                        bssid=bssid,
                        rssi=rssi,
                        channel=channel,
                        security=security,
                    ))
            
            networks.sort(key=lambda n: n.rssi, reverse=True)
            return networks
            
    except FileNotFoundError:
        pass
    except Exception:
        pass
    
    # Fallback to iwlist (requires sudo)
    try:
        result = subprocess.run(
            ["iwlist", "scan"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        
        if result.returncode == 0:
            current_bssid = None
            current_ssid = None
            current_signal = -100
            current_channel = 0
            current_security = "Open"
            
            for line in result.stdout.split("\n"):
                line = line.strip()
                
                if "Cell" in line and "Address:" in line:
                    # Save previous
                    if current_bssid and current_ssid:
                        networks.append(WiFiNetwork(
                            ssid=current_ssid,
                            bssid=current_bssid,
                            rssi=current_signal,
                            channel=current_channel,
                            security=current_security,
                        ))
                    current_bssid = line.split("Address:")[1].strip()
                    current_ssid = None
                    current_signal = -100
                    
                elif "ESSID:" in line:
                    match = re.search(r'ESSID:"([^"]*)"', line)
                    if match:
                        current_ssid = match.group(1) or "(Hidden)"
                        
                elif "Signal level=" in line:
                    match = re.search(r"Signal level[=:](-?\d+)", line)
                    if match:
                        current_signal = int(match.group(1))
                        
                elif "Channel:" in line:
                    match = re.search(r"Channel:(\d+)", line)
                    if match:
                        current_channel = int(match.group(1))
                        
                elif "Encryption key:on" in line:
                    current_security = "Encrypted"
            
            # Last network
            if current_bssid and current_ssid:
                networks.append(WiFiNetwork(
                    ssid=current_ssid,
                    bssid=current_bssid,
                    rssi=current_signal,
                    channel=current_channel,
                    security=current_security,
                ))
            
            networks.sort(key=lambda n: n.rssi, reverse=True)
            return networks
            
    except Exception:
        pass
    
    raise RuntimeError("Linux WiFi scan failed. Try: sudo nmcli dev wifi list")


def scan_wifi() -> list[WiFiNetwork]:
    """
    Scan for nearby WiFi networks.

    Supports macOS, Windows, and Linux.

    Returns:
        List of WiFiNetwork objects sorted by signal strength.
    """
    import platform

    system = platform.system()
    
    if system == "Darwin":
        return scan_wifi_macos()
    elif system == "Windows":
        return scan_wifi_windows()
    elif system == "Linux":
        return scan_wifi_linux()
    else:
        raise RuntimeError(f"WiFi scanning not supported on {system}")


def print_brand() -> None:
    """Print the OnWords brand header."""
    print(f"{RED}on{WHITE}words{RESET} · WiFi Scanner\n")


def print_networks(networks: list[WiFiNetwork]) -> None:
    """Pretty-print discovered networks."""
    if not networks:
        print(f"{DIM}No networks found.{RESET}")
        return

    print(f"Found {CYAN}{len(networks)}{RESET} network(s):\n")

    for i, net in enumerate(networks, 1):
        color = net.signal_color
        quality = net.signal_quality

        print(f"  {DIM}{i:>2}.{RESET} {WHITE}{net.ssid}{RESET}")
        print(f"      {DIM}BSSID:{RESET}    {net.bssid}")
        print(f"      {DIM}RSSI:{RESET}     {color}{net.rssi} dBm{RESET} ({quality})")
        print(f"      {DIM}Channel:{RESET}  {net.channel}")
        print(f"      {DIM}Security:{RESET} {net.security}\n")


def main() -> None:
    """CLI entry point for WiFi scanning."""
    print_brand()
    print(f"{DIM}Scanning for nearby WiFi networks...{RESET}\n")

    try:
        networks = scan_wifi()
        print_networks(networks)
    except Exception as e:
        print(f"{RED}Error:{RESET} {e}")


if __name__ == "__main__":
    main()

