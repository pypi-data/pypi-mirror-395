"""BLE (Bluetooth Low Energy) scanner module for OnWords."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Callable

from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

# Brand colors for terminal output
RED = "\033[31m"
WHITE = "\033[37m"
CYAN = "\033[36m"
DIM = "\033[2m"
RESET = "\033[0m"


@dataclass
class BLEDeviceInfo:
    """Simplified BLE device information."""

    address: str
    name: str | None
    rssi: int | None

    def __str__(self) -> str:
        name_display = self.name or "Unknown"
        rssi_display = f"{self.rssi} dBm" if self.rssi is not None else "N/A"
        return f"{name_display} ({self.address}) — RSSI: {rssi_display}"


async def scan_devices(timeout: float = 5.0) -> list[BLEDeviceInfo]:
    """
    Scan for nearby BLE devices.

    Args:
        timeout: How long to scan in seconds (default 5s).

    Returns:
        List of discovered BLE devices sorted by signal strength.
    """
    devices: list[BLEDeviceInfo] = []

    def detection_callback(device: BLEDevice, adv_data: AdvertisementData) -> None:
        # Avoid duplicates by address
        if not any(d.address == device.address for d in devices):
            devices.append(
                BLEDeviceInfo(
                    address=device.address,
                    name=device.name or adv_data.local_name,
                    rssi=adv_data.rssi,
                )
            )

    scanner = BleakScanner(detection_callback=detection_callback)
    await scanner.start()
    await asyncio.sleep(timeout)
    await scanner.stop()

    # Sort by RSSI (strongest first), treating None as very weak
    devices.sort(key=lambda d: d.rssi if d.rssi is not None else -999, reverse=True)
    return devices


def scan_devices_sync(timeout: float = 5.0) -> list[BLEDeviceInfo]:
    """Synchronous wrapper for scan_devices."""
    return asyncio.run(scan_devices(timeout))


def print_brand() -> None:
    """Print the OnWords brand header."""
    print(f"{RED}on{WHITE}words{RESET} · BLE Scanner\n")


def print_devices(devices: list[BLEDeviceInfo]) -> None:
    """Pretty-print discovered devices."""
    if not devices:
        print(f"{DIM}No devices found.{RESET}")
        return

    print(f"Found {CYAN}{len(devices)}{RESET} device(s):\n")
    for i, device in enumerate(devices, 1):
        name = device.name or "Unknown"
        rssi = f"{device.rssi} dBm" if device.rssi else "N/A"
        print(f"  {DIM}{i:>2}.{RESET} {WHITE}{name}{RESET}")
        print(f"      {DIM}Address:{RESET} {device.address}")
        print(f"      {DIM}RSSI:{RESET}    {CYAN}{rssi}{RESET}\n")


def main() -> None:
    """CLI entry point for BLE scanning."""
    print_brand()
    print(f"{DIM}Scanning for nearby BLE devices (5s)...{RESET}\n")

    try:
        devices = scan_devices_sync(timeout=5.0)
        print_devices(devices)
    except Exception as e:
        print(f"{RED}Error:{RESET} {e}")
        print(f"{DIM}Make sure Bluetooth is enabled and permissions are granted.{RESET}")


if __name__ == "__main__":
    main()

