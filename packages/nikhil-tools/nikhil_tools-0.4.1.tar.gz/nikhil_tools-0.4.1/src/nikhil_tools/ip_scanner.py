"""IP scanner module for OnWords - discovers devices on local network."""

from __future__ import annotations

import asyncio
import socket
import subprocess
import re
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

# Brand colors for terminal output
RED = "\033[31m"
WHITE = "\033[37m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
DIM = "\033[2m"
RESET = "\033[0m"


@dataclass
class NetworkDevice:
    """Network device information."""

    ip: str
    mac: Optional[str] = None
    hostname: Optional[str] = None
    vendor: Optional[str] = None
    latency_ms: Optional[float] = None

    def __str__(self) -> str:
        parts = [self.ip]
        if self.hostname:
            parts.append(f"({self.hostname})")
        if self.mac:
            parts.append(f"[{self.mac}]")
        return " ".join(parts)


def get_local_ip() -> str:
    """Get the local IP address of this machine."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "192.168.1.1"


def get_network_prefix(ip: str) -> str:
    """Get the network prefix (first 3 octets) from an IP."""
    parts = ip.split(".")
    return ".".join(parts[:3])


def ping_host(ip: str, timeout: float = 1.0) -> Optional[float]:
    """
    Ping a host and return latency in ms, or None if unreachable.
    Works on Windows, macOS, and Linux.
    """
    import platform
    
    try:
        system = platform.system().lower()
        
        if system == "windows":
            # Windows: -n count, -w timeout in milliseconds
            cmd = ["ping", "-n", "1", "-w", str(int(timeout * 1000)), ip]
        else:
            # macOS/Linux: -c count, -W timeout in seconds (macOS) or seconds (Linux)
            if system == "darwin":
                cmd = ["ping", "-c", "1", "-W", str(int(timeout * 1000)), ip]
            else:
                cmd = ["ping", "-c", "1", "-W", str(int(timeout)), ip]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout + 2,
        )
        
        if result.returncode == 0:
            # Extract latency - works for all platforms
            match = re.search(r"time[=<](\d+\.?\d*)", result.stdout)
            if match:
                return float(match.group(1))
            return 0.0
        return None
    except (subprocess.TimeoutExpired, Exception):
        return None


def get_arp_table() -> dict[str, str]:
    """
    Get the ARP table mapping IP to MAC addresses.
    Works on Windows, macOS, and Linux.
    """
    import platform
    
    arp_map: dict[str, str] = {}
    try:
        result = subprocess.run(
            ["arp", "-a"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        
        system = platform.system().lower()
        
        for line in result.stdout.split("\n"):
            if system == "windows":
                # Windows format: 192.168.1.1    aa-bb-cc-dd-ee-ff    dynamic
                match = re.search(r"(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F-]+)", line)
                if match:
                    ip, mac = match.groups()
                    mac = mac.replace("-", ":").upper()
                    arp_map[ip] = mac
            else:
                # macOS/Linux format: hostname (ip) at mac on interface
                match = re.search(r"\((\d+\.\d+\.\d+\.\d+)\)\s+at\s+([0-9a-fA-F:]+)", line)
                if match:
                    ip, mac = match.groups()
                    if mac != "(incomplete)":
                        arp_map[ip] = mac.upper()
    except Exception:
        pass
    return arp_map


def resolve_hostname(ip: str) -> Optional[str]:
    """Try to resolve hostname for an IP address."""
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except (socket.herror, socket.gaierror):
        return None


def get_mac_for_ip(ip: str) -> Optional[str]:
    """Get MAC address for a specific IP after ping."""
    import platform
    
    try:
        result = subprocess.run(
            ["arp", "-a", ip] if platform.system() != "Windows" else ["arp", "-a"],
            capture_output=True,
            text=True,
            timeout=2,
        )
        
        system = platform.system().lower()
        
        for line in result.stdout.split("\n"):
            if ip in line:
                if system == "windows":
                    match = re.search(r"([0-9a-fA-F-]{17})", line)
                    if match:
                        return match.group(1).replace("-", ":").upper()
                else:
                    match = re.search(r"at\s+([0-9a-fA-F:]{17})", line)
                    if match:
                        mac = match.group(1).upper()
                        if mac != "(INCOMPLETE)":
                            return mac
    except Exception:
        pass
    return None


# Common MAC vendor prefixes (OUI)
MAC_VENDORS = {
    "00:00:0C": "Cisco",
    "00:1A:2B": "Cisco",
    "00:50:56": "VMware",
    "00:0C:29": "VMware",
    "08:00:27": "VirtualBox",
    "00:1C:42": "Parallels",
    "00:03:FF": "Microsoft",
    "00:15:5D": "Microsoft Hyper-V",
    "00:1A:11": "Google",
    "3C:5A:B4": "Google",
    "F4:F5:D8": "Google",
    "AC:DE:48": "Apple",
    "00:1E:C2": "Apple",
    "00:03:93": "Apple",
    "A4:83:E7": "Apple",
    "F0:18:98": "Apple",
    "00:26:BB": "Apple",
    "D0:03:4B": "Apple",
    "BC:92:6B": "Apple",
    "78:31:C1": "Apple",
    "00:25:00": "Apple",
    "00:1F:F3": "Apple",
    "00:21:E9": "Apple",
    "B8:27:EB": "Raspberry Pi",
    "DC:A6:32": "Raspberry Pi",
    "E4:5F:01": "Raspberry Pi",
    "00:E0:4C": "Realtek",
    "52:54:00": "QEMU/KVM",
    "00:16:3E": "Xen",
    "02:42:AC": "Docker",
    "00:0D:3A": "Microsoft Azure",
    "00:17:88": "Philips Hue",
    "EC:FA:BC": "Espressif (ESP32)",
    "24:6F:28": "Espressif (ESP32)",
    "AC:67:B2": "Espressif (ESP32)",
    "30:AE:A4": "Espressif (ESP8266)",
    "CC:50:E3": "Espressif",
    "A0:20:A6": "Espressif",
    "00:1B:63": "Intel",
    "00:1E:67": "Intel",
    "00:22:FA": "Intel",
    "3C:97:0E": "Intel",
    "AC:22:05": "HP",
    "00:1E:0B": "HP",
    "00:30:C1": "HP",
    "94:57:A5": "Samsung",
    "00:1E:75": "Samsung",
    "00:26:5D": "Samsung",
    "E8:6F:38": "Xiaomi",
    "64:CC:2E": "Xiaomi",
    "38:A4:ED": "Xiaomi",
    "F8:A2:D6": "TP-Link",
    "00:1D:0F": "TP-Link",
    "50:C7:BF": "TP-Link",
    "00:24:01": "D-Link",
    "00:1E:58": "D-Link",
    "28:10:7B": "D-Link",
    "00:18:E7": "Netgear",
    "00:1F:33": "Netgear",
    "A0:63:91": "Netgear",
    "00:1D:7E": "Linksys",
    "00:22:6B": "Linksys",
    "98:FC:11": "Linksys",
    "44:D9:E7": "Ubiquiti",
    "00:27:22": "Ubiquiti",
    "FC:EC:DA": "Ubiquiti",
    "EC:75:0C": "Airtel (Router)",
    "C0:5D:89": "Airtel (Router)",
    "FC:E8:C0": "Airtel (Router)",
}


def get_vendor_from_mac(mac: str) -> Optional[str]:
    """Get vendor name from MAC address prefix."""
    if not mac:
        return None
    
    # Normalize MAC
    mac = mac.upper().replace("-", ":")
    
    # Check 3-byte prefix (OUI)
    prefix = mac[:8]
    if prefix in MAC_VENDORS:
        return MAC_VENDORS[prefix]
    
    # Check 2.5-byte prefix for some vendors
    prefix_short = mac[:7]
    for oui, vendor in MAC_VENDORS.items():
        if oui.startswith(prefix_short[:7]):
            return vendor
    
    return None


def scan_ip(ip: str, arp_table: dict[str, str]) -> Optional[NetworkDevice]:
    """Scan a single IP address."""
    latency = ping_host(ip, timeout=0.5)
    if latency is not None:
        # First try from pre-fetched ARP table
        mac = arp_table.get(ip)
        
        # If no MAC, try getting it directly after ping
        if not mac:
            mac = get_mac_for_ip(ip)
        
        hostname = resolve_hostname(ip)
        vendor = get_vendor_from_mac(mac)
        
        return NetworkDevice(
            ip=ip,
            mac=mac,
            hostname=hostname,
            vendor=vendor,
            latency_ms=latency,
        )
    return None


def scan_network(
    network_prefix: Optional[str] = None,
    start: int = 1,
    end: int = 254,
    max_workers: int = 50,
    progress_callback=None,
) -> list[NetworkDevice]:
    """
    Scan a network range for active devices.

    Args:
        network_prefix: First 3 octets (e.g., "192.168.1"). Auto-detected if None.
        start: Starting host number (default 1).
        end: Ending host number (default 254).
        max_workers: Number of parallel threads (default 50).
        progress_callback: Optional callback(current, total) for progress updates.

    Returns:
        List of NetworkDevice objects for reachable hosts.
    """
    if network_prefix is None:
        local_ip = get_local_ip()
        network_prefix = get_network_prefix(local_ip)

    # Pre-fetch ARP table
    arp_table = get_arp_table()

    # Generate IP list
    ips = [f"{network_prefix}.{i}" for i in range(start, end + 1)]
    total = len(ips)
    devices: list[NetworkDevice] = []
    scanned = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(scan_ip, ip, arp_table): ip for ip in ips}

        for future in futures:
            result = future.result()
            scanned += 1
            if progress_callback:
                progress_callback(scanned, total)
            if result:
                devices.append(result)

    # Sort by IP address
    devices.sort(key=lambda d: [int(x) for x in d.ip.split(".")])
    return devices


def scan_network_async(
    network_prefix: Optional[str] = None,
    start: int = 1,
    end: int = 254,
) -> list[NetworkDevice]:
    """Synchronous wrapper for network scanning."""
    return scan_network(network_prefix, start, end)


def print_brand() -> None:
    """Print the OnWords brand header."""
    print(f"{RED}on{WHITE}words{RESET} · IP Scanner\n")


def print_devices(devices: list[NetworkDevice], local_ip: str) -> None:
    """Pretty-print discovered devices."""
    if not devices:
        print(f"{DIM}No devices found.{RESET}")
        return

    print(f"Found {CYAN}{len(devices)}{RESET} device(s) on the network:\n")

    for i, device in enumerate(devices, 1):
        is_local = device.ip == local_ip
        marker = f" {GREEN}← this device{RESET}" if is_local else ""

        print(f"  {DIM}{i:>2}.{RESET} {WHITE}{device.ip}{RESET}{marker}")

        if device.hostname:
            print(f"      {DIM}Hostname:{RESET} {device.hostname}")
        if device.mac:
            vendor_str = f" ({CYAN}{device.vendor}{RESET})" if device.vendor else ""
            print(f"      {DIM}MAC:{RESET}      {device.mac}{vendor_str}")
        if device.latency_ms is not None:
            color = GREEN if device.latency_ms < 10 else (YELLOW if device.latency_ms < 50 else RED)
            print(f"      {DIM}Latency:{RESET}  {color}{device.latency_ms:.1f} ms{RESET}")
        print()


def main() -> None:
    """CLI entry point for IP scanning."""
    print_brand()

    local_ip = get_local_ip()
    network_prefix = get_network_prefix(local_ip)

    print(f"{DIM}Local IP:{RESET} {local_ip}")
    print(f"{DIM}Scanning:{RESET} {network_prefix}.1-254\n")

    scanned = [0]

    def progress(current: int, total: int) -> None:
        scanned[0] = current
        pct = int(current / total * 100)
        bar_len = 30
        filled = int(bar_len * current / total)
        bar = "█" * filled + "░" * (bar_len - filled)
        print(f"\r{DIM}Progress:{RESET} [{CYAN}{bar}{RESET}] {pct}%", end="", flush=True)

    try:
        devices = scan_network(network_prefix, progress_callback=progress)
        print("\r" + " " * 60 + "\r")  # Clear progress line
        print_devices(devices, local_ip)
    except Exception as e:
        print(f"\n{RED}Error:{RESET} {e}")


if __name__ == "__main__":
    main()

