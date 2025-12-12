# nikhil-tools

Python toolkit with network scanning and system monitoring utilities.

## Installation

```bash
pip install nikhil-tools
```

## Features

- **BLE Scanner** - Discover Bluetooth Low Energy devices (all platforms)
- **WiFi Scanner** - Scan nearby WiFi networks (macOS, Windows, Linux)
- **IP Scanner** - Discover devices on local network (all platforms)
- **System Monitor** - CPU, memory, disk, battery, GPU stats (all platforms)

## Usage

### As a Library

```python
import nikhil_tools

# BLE Scanning
devices = nikhil_tools.scan_devices_sync(timeout=5.0)
for device in devices:
    print(f"{device.name} - {device.address}")

# WiFi Scanning
networks = nikhil_tools.scan_wifi()
for net in networks:
    print(f"{net.ssid} - {net.rssi} dBm")

# IP Scanning
devices = nikhil_tools.scan_network()
for device in devices:
    print(f"{device.ip} - {device.hostname}")

# System Stats
stats = nikhil_tools.get_system_stats()
print(f"CPU: {stats.cpu.usage_percent}%")
print(f"RAM: {stats.memory.percent_used}%")
print(f"Disk: {stats.disk.percent_used}%")
```

### CLI Commands

```bash
# Scan BLE devices
nikhil-ble

# Scan WiFi networks
nikhil-wifi

# Scan IP addresses on network
nikhil-ip

# Show system stats
nikhil-sysmon
```

## API Reference

### BLE Scanner
- `scan_devices(timeout)` - Async BLE scan
- `scan_devices_sync(timeout)` - Sync BLE scan
- `BLEDeviceInfo` - Device data class

### WiFi Scanner
- `scan_wifi()` - Scan WiFi networks
- `WiFiNetwork` - Network data class

### IP Scanner
- `scan_network(network_prefix, start, end)` - Scan IP range
- `get_local_ip()` - Get local IP address
- `NetworkDevice` - Device data class

### System Monitor
- `get_system_stats()` - Get all system stats
- `get_cpu_info()` - CPU usage
- `get_memory_info()` - RAM usage
- `get_disk_info()` - Disk usage
- `get_battery_info()` - Battery status
- `get_gpu_info()` - GPU info
- `get_network_speed()` - Network throughput

## Requirements

- Python 3.9+
- **macOS**, **Windows**, or **Linux**

### Platform Notes

| Feature | macOS | Windows | Linux |
|---------|-------|---------|-------|
| BLE Scanner | ✅ | ✅ | ✅ |
| WiFi Scanner | ✅ | ✅ | ✅ (requires nmcli or iwlist) |
| IP Scanner | ✅ | ✅ | ✅ |
| System Monitor | ✅ | ✅ | ✅ |

## License

MIT
