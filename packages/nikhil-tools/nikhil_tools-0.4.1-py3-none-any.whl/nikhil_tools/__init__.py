"""
nikhil-tools - Python toolkit for network scanning and system monitoring.

Modules:
    - ble_scanner: Bluetooth Low Energy device discovery
    - wifi_scanner: WiFi network scanning (macOS)
    - ip_scanner: Local network IP scanning
    - system_monitor: CPU, memory, disk, battery monitoring
"""

__version__ = "0.4.1"
__author__ = "Nikhil Deepak"

# Core data classes
from nikhil_tools.ble_scanner import BLEDeviceInfo, scan_devices, scan_devices_sync
from nikhil_tools.wifi_scanner import WiFiNetwork, scan_wifi
from nikhil_tools.ip_scanner import NetworkDevice, scan_network, get_local_ip
from nikhil_tools.system_monitor import (
    SystemStats,
    CPUInfo,
    MemoryInfo,
    DiskInfo,
    BatteryInfo,
    GPUInfo,
    NetworkSpeedInfo,
    get_system_stats,
    get_cpu_info,
    get_memory_info,
    get_disk_info,
    get_battery_info,
    get_gpu_info,
    get_network_speed,
)

__all__ = [
    # Version
    "__version__",
    # BLE
    "BLEDeviceInfo",
    "scan_devices",
    "scan_devices_sync",
    # WiFi
    "WiFiNetwork",
    "scan_wifi",
    # IP
    "NetworkDevice",
    "scan_network",
    "get_local_ip",
    # System Monitor
    "SystemStats",
    "CPUInfo",
    "MemoryInfo",
    "DiskInfo",
    "BatteryInfo",
    "GPUInfo",
    "NetworkSpeedInfo",
    "get_system_stats",
    "get_cpu_info",
    "get_memory_info",
    "get_disk_info",
    "get_battery_info",
    "get_gpu_info",
    "get_network_speed",
]
