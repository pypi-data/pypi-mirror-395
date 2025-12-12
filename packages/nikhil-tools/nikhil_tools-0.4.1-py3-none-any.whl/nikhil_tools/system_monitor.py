"""System performance monitor module for OnWords."""

from __future__ import annotations

import platform
import subprocess
from dataclasses import dataclass
from typing import Optional

import psutil

# Brand colors for terminal output
RED = "\033[31m"
WHITE = "\033[37m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
DIM = "\033[2m"
RESET = "\033[0m"


@dataclass
class CPUInfo:
    """CPU information."""

    usage_percent: float
    core_count: int
    frequency_mhz: Optional[float]
    per_core_usage: list[float]


@dataclass
class MemoryInfo:
    """Memory/RAM information."""

    total_gb: float
    used_gb: float
    available_gb: float
    percent_used: float


@dataclass
class GPUInfo:
    """GPU information (macOS specific)."""

    name: str
    vendor: str
    vram_mb: Optional[int]


@dataclass
class TemperatureInfo:
    """Temperature readings."""

    cpu_temp_c: Optional[float]
    gpu_temp_c: Optional[float]
    battery_temp_c: Optional[float]


@dataclass
class BatteryInfo:
    """Battery information."""

    percent: float
    is_charging: bool
    is_plugged: bool
    time_left_mins: Optional[int]
    power_consumption_watts: Optional[float]


@dataclass
class DiskInfo:
    """Disk usage information."""

    total_gb: float
    used_gb: float
    free_gb: float
    percent_used: float


@dataclass
class NetworkSpeedInfo:
    """Network speed information."""

    bytes_sent: int
    bytes_recv: int
    upload_speed_mbps: float  # Current upload speed
    download_speed_mbps: float  # Current download speed
    packets_sent: int
    packets_recv: int


# Store previous network stats for speed calculation
_prev_net_io = None
_prev_net_time = None


@dataclass
class SystemStats:
    """Complete system statistics."""

    cpu: CPUInfo
    memory: MemoryInfo
    disk: DiskInfo
    battery: Optional[BatteryInfo]
    gpu: Optional[GPUInfo]
    temperature: Optional[TemperatureInfo]
    network: Optional[NetworkSpeedInfo]
    system_name: str
    uptime_hours: float


def get_cpu_info() -> CPUInfo:
    """Get CPU usage and information."""
    cpu_percent = psutil.cpu_percent(interval=0.5)
    per_core = psutil.cpu_percent(interval=0.1, percpu=True)
    freq = psutil.cpu_freq()

    return CPUInfo(
        usage_percent=cpu_percent,
        core_count=psutil.cpu_count(logical=True),
        frequency_mhz=freq.current if freq else None,
        per_core_usage=per_core,
    )


def get_memory_info() -> MemoryInfo:
    """Get RAM usage information."""
    mem = psutil.virtual_memory()

    return MemoryInfo(
        total_gb=mem.total / (1024**3),
        used_gb=mem.used / (1024**3),
        available_gb=mem.available / (1024**3),
        percent_used=mem.percent,
    )


def get_disk_info() -> DiskInfo:
    """Get disk usage information. Works on all platforms."""
    # Use appropriate path for each OS
    if platform.system() == "Windows":
        disk = psutil.disk_usage("C:\\")
    else:
        disk = psutil.disk_usage("/")

    return DiskInfo(
        total_gb=disk.total / (1024**3),
        used_gb=disk.used / (1024**3),
        free_gb=disk.free / (1024**3),
        percent_used=disk.percent,
    )


def get_battery_info() -> Optional[BatteryInfo]:
    """Get battery information."""
    battery = psutil.sensors_battery()
    if battery is None:
        return None

    time_left = None
    if battery.secsleft > 0:
        time_left = battery.secsleft // 60

    # Try to get power consumption on macOS
    power_watts = None
    if platform.system() == "Darwin":
        try:
            result = subprocess.run(
                ["pmset", "-g", "batt"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            # Parse power consumption if available
            for line in result.stdout.split("\n"):
                if "watt" in line.lower():
                    import re
                    match = re.search(r"([\d.]+)\s*[wW]", line)
                    if match:
                        power_watts = float(match.group(1))
        except Exception:
            pass

    return BatteryInfo(
        percent=battery.percent,
        is_charging=battery.power_plugged and battery.percent < 100,
        is_plugged=battery.power_plugged or False,
        time_left_mins=time_left,
        power_consumption_watts=power_watts,
    )


def get_gpu_info_macos() -> Optional[GPUInfo]:
    """Get GPU information on macOS."""
    try:
        result = subprocess.run(
            ["system_profiler", "SPDisplaysDataType", "-json"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        import json
        data = json.loads(result.stdout)

        displays = data.get("SPDisplaysDataType", [])
        if displays:
            gpu = displays[0]
            name = gpu.get("sppci_model", "Unknown GPU")
            vendor = gpu.get("spdisplays_vendor", "Unknown")
            vram = gpu.get("spdisplays_vram", "")

            # Parse VRAM
            vram_mb = None
            if vram:
                import re
                match = re.search(r"(\d+)", str(vram))
                if match:
                    vram_mb = int(match.group(1))

            return GPUInfo(name=name, vendor=vendor, vram_mb=vram_mb)
    except Exception:
        pass
    return None


def get_gpu_info_windows() -> Optional[GPUInfo]:
    """Get GPU information on Windows using WMIC."""
    try:
        result = subprocess.run(
            ["wmic", "path", "win32_VideoController", "get", "name,adapterram,driverversion"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        
        if result.returncode == 0:
            lines = [l.strip() for l in result.stdout.split("\n") if l.strip()]
            if len(lines) > 1:
                # Skip header line
                for line in lines[1:]:
                    parts = line.split()
                    if parts:
                        name = " ".join(parts[:-2]) if len(parts) > 2 else parts[0]
                        return GPUInfo(name=name, vendor="Unknown", vram_mb=None)
    except Exception:
        pass
    return None


def get_gpu_info_linux() -> Optional[GPUInfo]:
    """Get GPU information on Linux using lspci."""
    try:
        result = subprocess.run(
            ["lspci"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        
        if result.returncode == 0:
            for line in result.stdout.split("\n"):
                if "VGA" in line or "3D" in line or "Display" in line:
                    # Extract GPU name
                    parts = line.split(": ", 1)
                    if len(parts) > 1:
                        gpu_info = parts[1]
                        vendor = "Unknown"
                        if "NVIDIA" in gpu_info.upper():
                            vendor = "NVIDIA"
                        elif "AMD" in gpu_info.upper() or "ATI" in gpu_info.upper():
                            vendor = "AMD"
                        elif "INTEL" in gpu_info.upper():
                            vendor = "Intel"
                        return GPUInfo(name=gpu_info, vendor=vendor, vram_mb=None)
    except Exception:
        pass
    return None


def get_gpu_info() -> Optional[GPUInfo]:
    """Get GPU information. Works on macOS, Windows, and Linux."""
    system = platform.system()
    
    if system == "Darwin":
        return get_gpu_info_macos()
    elif system == "Windows":
        return get_gpu_info_windows()
    elif system == "Linux":
        return get_gpu_info_linux()
    return None


def get_temperature_macos() -> Optional[TemperatureInfo]:
    """Get temperature readings on macOS using powermetrics or osx-cpu-temp."""
    cpu_temp = None

    # Try using psutil first (may not work on all systems)
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            for name, entries in temps.items():
                for entry in entries:
                    if "cpu" in entry.label.lower() or "core" in entry.label.lower():
                        cpu_temp = entry.current
                        break
    except Exception:
        pass

    # Fallback: try reading from IOKit on macOS
    if cpu_temp is None:
        try:
            # Try osx-cpu-temp if installed
            result = subprocess.run(
                ["osx-cpu-temp"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                import re
                match = re.search(r"([\d.]+)", result.stdout)
                if match:
                    cpu_temp = float(match.group(1))
        except Exception:
            pass

    if cpu_temp is not None:
        return TemperatureInfo(
            cpu_temp_c=cpu_temp,
            gpu_temp_c=None,
            battery_temp_c=None,
        )
    return None


def get_temperature_info() -> Optional[TemperatureInfo]:
    """Get temperature information."""
    if platform.system() == "Darwin":
        return get_temperature_macos()

    # Linux
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            cpu_temp = None
            for name, entries in temps.items():
                for entry in entries:
                    if cpu_temp is None:
                        cpu_temp = entry.current
            if cpu_temp:
                return TemperatureInfo(
                    cpu_temp_c=cpu_temp,
                    gpu_temp_c=None,
                    battery_temp_c=None,
                )
    except Exception:
        pass
    return None


def get_uptime_hours() -> float:
    """Get system uptime in hours."""
    import time
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time
    return uptime_seconds / 3600


def get_network_speed() -> Optional[NetworkSpeedInfo]:
    """Get network speed information."""
    import time
    global _prev_net_io, _prev_net_time

    try:
        current_io = psutil.net_io_counters()
        current_time = time.time()

        upload_speed = 0.0
        download_speed = 0.0

        if _prev_net_io is not None and _prev_net_time is not None:
            time_delta = current_time - _prev_net_time
            if time_delta > 0:
                bytes_sent_delta = current_io.bytes_sent - _prev_net_io.bytes_sent
                bytes_recv_delta = current_io.bytes_recv - _prev_net_io.bytes_recv

                # Convert to Mbps (megabits per second)
                upload_speed = (bytes_sent_delta * 8) / (time_delta * 1_000_000)
                download_speed = (bytes_recv_delta * 8) / (time_delta * 1_000_000)

        # Store current values for next calculation
        _prev_net_io = current_io
        _prev_net_time = current_time

        return NetworkSpeedInfo(
            bytes_sent=current_io.bytes_sent,
            bytes_recv=current_io.bytes_recv,
            upload_speed_mbps=upload_speed,
            download_speed_mbps=download_speed,
            packets_sent=current_io.packets_sent,
            packets_recv=current_io.packets_recv,
        )
    except Exception:
        return None


def format_bytes(bytes_val: int) -> str:
    """Format bytes to human readable string."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_val < 1024:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.1f} PB"


def get_system_stats() -> SystemStats:
    """Get complete system statistics."""
    return SystemStats(
        cpu=get_cpu_info(),
        memory=get_memory_info(),
        disk=get_disk_info(),
        battery=get_battery_info(),
        gpu=get_gpu_info(),
        temperature=get_temperature_info(),
        network=get_network_speed(),
        system_name=f"{platform.system()} {platform.release()}",
        uptime_hours=get_uptime_hours(),
    )


def format_bar(percent: float, width: int = 20) -> str:
    """Create a progress bar string."""
    filled = int(width * percent / 100)
    empty = width - filled

    if percent >= 90:
        color = RED
    elif percent >= 70:
        color = YELLOW
    else:
        color = GREEN

    return f"{color}{'█' * filled}{'░' * empty}{RESET}"


def print_brand() -> None:
    """Print the OnWords brand header."""
    print(f"{RED}on{WHITE}words{RESET} · System Monitor\n")


def print_stats(stats: SystemStats) -> None:
    """Pretty-print system statistics."""
    print(f"{DIM}System:{RESET} {stats.system_name}")
    print(f"{DIM}Uptime:{RESET} {stats.uptime_hours:.1f} hours\n")

    # CPU
    print(f"{WHITE}CPU{RESET}")
    bar = format_bar(stats.cpu.usage_percent)
    freq = f" @ {stats.cpu.frequency_mhz:.0f} MHz" if stats.cpu.frequency_mhz else ""
    print(f"  Usage: [{bar}] {stats.cpu.usage_percent:.1f}%{freq}")
    print(f"  Cores: {stats.cpu.core_count}")

    # Per-core usage (compact)
    if stats.cpu.per_core_usage:
        cores_str = " ".join(f"{u:.0f}%" for u in stats.cpu.per_core_usage[:8])
        if len(stats.cpu.per_core_usage) > 8:
            cores_str += " ..."
        print(f"  {DIM}Per-core: {cores_str}{RESET}")
    print()

    # Memory
    print(f"{WHITE}Memory{RESET}")
    bar = format_bar(stats.memory.percent_used)
    print(f"  Usage: [{bar}] {stats.memory.percent_used:.1f}%")
    print(f"  {DIM}Used: {stats.memory.used_gb:.1f} GB / {stats.memory.total_gb:.1f} GB{RESET}")
    print(f"  {DIM}Available: {stats.memory.available_gb:.1f} GB{RESET}")
    print()

    # Disk
    print(f"{WHITE}Disk{RESET}")
    bar = format_bar(stats.disk.percent_used)
    print(f"  Usage: [{bar}] {stats.disk.percent_used:.1f}%")
    print(f"  {DIM}Used: {stats.disk.used_gb:.0f} GB / {stats.disk.total_gb:.0f} GB{RESET}")
    print(f"  {DIM}Free: {stats.disk.free_gb:.0f} GB{RESET}")
    print()

    # GPU
    if stats.gpu:
        print(f"{WHITE}GPU{RESET}")
        print(f"  {stats.gpu.name}")
        if stats.gpu.vram_mb:
            print(f"  {DIM}VRAM: {stats.gpu.vram_mb} MB{RESET}")
        print()

    # Temperature
    if stats.temperature:
        print(f"{WHITE}Temperature{RESET}")
        if stats.temperature.cpu_temp_c:
            temp = stats.temperature.cpu_temp_c
            color = RED if temp > 80 else (YELLOW if temp > 60 else GREEN)
            print(f"  CPU: {color}{temp:.1f}°C{RESET}")
        print()

    # Battery
    if stats.battery:
        print(f"{WHITE}Battery{RESET}")
        bar = format_bar(stats.battery.percent)
        status = "⚡ Charging" if stats.battery.is_charging else ("🔌 Plugged" if stats.battery.is_plugged else "🔋 On Battery")
        print(f"  Level: [{bar}] {stats.battery.percent:.0f}% {status}")
        if stats.battery.time_left_mins and not stats.battery.is_plugged:
            hours = stats.battery.time_left_mins // 60
            mins = stats.battery.time_left_mins % 60
            print(f"  {DIM}Time remaining: {hours}h {mins}m{RESET}")
        if stats.battery.power_consumption_watts:
            print(f"  {DIM}Power: {stats.battery.power_consumption_watts:.1f}W{RESET}")
        print()

    # Network
    if stats.network:
        print(f"{WHITE}Network{RESET}")
        dl_color = GREEN if stats.network.download_speed_mbps < 10 else (CYAN if stats.network.download_speed_mbps < 100 else YELLOW)
        ul_color = GREEN if stats.network.upload_speed_mbps < 10 else (CYAN if stats.network.upload_speed_mbps < 100 else YELLOW)
        print(f"  ↓ Download: {dl_color}{stats.network.download_speed_mbps:.2f} Mbps{RESET}")
        print(f"  ↑ Upload:   {ul_color}{stats.network.upload_speed_mbps:.2f} Mbps{RESET}")
        print(f"  {DIM}Total received: {format_bytes(stats.network.bytes_recv)}{RESET}")
        print(f"  {DIM}Total sent: {format_bytes(stats.network.bytes_sent)}{RESET}")
        print()


def main() -> None:
    """CLI entry point for system monitoring."""
    print_brand()

    try:
        stats = get_system_stats()
        print_stats(stats)
    except Exception as e:
        print(f"{RED}Error:{RESET} {e}")


if __name__ == "__main__":
    main()

