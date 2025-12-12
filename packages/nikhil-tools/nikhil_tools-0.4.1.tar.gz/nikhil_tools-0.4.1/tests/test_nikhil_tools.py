"""Tests for nikhil_tools package."""

import pytest


def test_import():
    """Test package imports correctly."""
    import nikhil_tools
    assert nikhil_tools.__version__ == "0.1.0"


def test_system_monitor_cpu():
    """Test CPU info retrieval."""
    from nikhil_tools import get_cpu_info
    
    cpu = get_cpu_info()
    assert cpu.core_count > 0
    assert 0 <= cpu.usage_percent <= 100


def test_system_monitor_memory():
    """Test memory info retrieval."""
    from nikhil_tools import get_memory_info
    
    mem = get_memory_info()
    assert mem.total_gb > 0
    assert mem.used_gb > 0
    assert 0 <= mem.percent_used <= 100


def test_system_monitor_disk():
    """Test disk info retrieval."""
    from nikhil_tools import get_disk_info
    
    disk = get_disk_info()
    assert disk.total_gb > 0
    assert 0 <= disk.percent_used <= 100


def test_ip_scanner_local_ip():
    """Test getting local IP."""
    from nikhil_tools import get_local_ip
    
    ip = get_local_ip()
    assert ip is not None
    parts = ip.split(".")
    assert len(parts) == 4


def test_exports():
    """Test all expected exports exist."""
    from nikhil_tools import (
        BLEDeviceInfo,
        scan_devices,
        scan_devices_sync,
        WiFiNetwork,
        scan_wifi,
        NetworkDevice,
        scan_network,
        get_local_ip,
        SystemStats,
        get_system_stats,
    )
    # Just checking imports work
    assert True
