"""Internet speed test module for OnWords."""

from __future__ import annotations

import socket
import time
import urllib.request
from dataclasses import dataclass
from typing import Optional, Callable
from concurrent.futures import ThreadPoolExecutor
import ssl

# Brand colors for terminal output
RED = "\033[31m"
WHITE = "\033[37m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"


@dataclass
class SpeedTestResult:
    """Speed test results."""
    
    download_mbps: float
    upload_mbps: float
    ping_ms: float
    server: str
    timestamp: str


# Test servers (using common CDN endpoints for download tests)
TEST_SERVERS = [
    ("https://speed.cloudflare.com/__down?bytes=10000000", "Cloudflare"),
    ("https://proof.ovh.net/files/1Mb.dat", "OVH"),
]

UPLOAD_TEST_URL = "https://speed.cloudflare.com/__up"


def measure_ping(host: str = "8.8.8.8", port: int = 53, timeout: float = 3.0) -> Optional[float]:
    """
    Measure ping latency to a host.
    
    Returns:
        Latency in milliseconds, or None if failed.
    """
    try:
        start = time.perf_counter()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.close()
        end = time.perf_counter()
        return (end - start) * 1000
    except Exception:
        return None


def measure_download(
    url: str,
    duration: float = 10.0,
    progress_callback: Optional[Callable[[float, float], None]] = None
) -> float:
    """
    Measure download speed.
    
    Args:
        url: URL to download from
        duration: Max test duration in seconds
        progress_callback: Optional callback(downloaded_mb, speed_mbps)
    
    Returns:
        Download speed in Mbps
    """
    total_bytes = 0
    start_time = time.perf_counter()
    
    try:
        # Create SSL context that doesn't verify (for speed test purposes)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 nikhil-tools speed test'
        })
        
        with urllib.request.urlopen(req, timeout=duration + 5, context=ctx) as response:
            chunk_size = 1024 * 64  # 64KB chunks
            
            while True:
                elapsed = time.perf_counter() - start_time
                if elapsed >= duration:
                    break
                    
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                    
                total_bytes += len(chunk)
                
                if progress_callback and elapsed > 0:
                    speed_mbps = (total_bytes * 8) / (elapsed * 1_000_000)
                    downloaded_mb = total_bytes / (1024 * 1024)
                    progress_callback(downloaded_mb, speed_mbps)
                    
    except Exception as e:
        pass
    
    elapsed = time.perf_counter() - start_time
    if elapsed > 0:
        return (total_bytes * 8) / (elapsed * 1_000_000)
    return 0.0


def measure_upload(
    duration: float = 10.0,
    progress_callback: Optional[Callable[[float, float], None]] = None
) -> float:
    """
    Measure upload speed.
    
    Args:
        duration: Max test duration in seconds
        progress_callback: Optional callback(uploaded_mb, speed_mbps)
    
    Returns:
        Upload speed in Mbps
    """
    total_bytes = 0
    start_time = time.perf_counter()
    chunk_size = 1024 * 256  # 256KB chunks
    
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        # Generate random-ish data
        data_chunk = b'x' * chunk_size
        
        while True:
            elapsed = time.perf_counter() - start_time
            if elapsed >= duration:
                break
            
            try:
                req = urllib.request.Request(
                    UPLOAD_TEST_URL,
                    data=data_chunk,
                    headers={
                        'User-Agent': 'Mozilla/5.0 nikhil-tools speed test',
                        'Content-Type': 'application/octet-stream',
                    },
                    method='POST'
                )
                
                with urllib.request.urlopen(req, timeout=5, context=ctx) as response:
                    response.read()
                    total_bytes += chunk_size
                    
            except Exception:
                # Try with smaller chunk on failure
                total_bytes += chunk_size // 4
            
            if progress_callback and elapsed > 0:
                speed_mbps = (total_bytes * 8) / (elapsed * 1_000_000)
                uploaded_mb = total_bytes / (1024 * 1024)
                progress_callback(uploaded_mb, speed_mbps)
                
    except Exception:
        pass
    
    elapsed = time.perf_counter() - start_time
    if elapsed > 0:
        return (total_bytes * 8) / (elapsed * 1_000_000)
    return 0.0


def run_speed_test(
    download_duration: float = 10.0,
    upload_duration: float = 10.0,
    progress_callback: Optional[Callable[[str, float, float], None]] = None
) -> SpeedTestResult:
    """
    Run a complete speed test.
    
    Args:
        download_duration: Download test duration in seconds
        upload_duration: Upload test duration in seconds
        progress_callback: Optional callback(phase, progress_pct, speed_mbps)
    
    Returns:
        SpeedTestResult with all measurements
    """
    from datetime import datetime
    
    # Measure ping
    ping = measure_ping() or 0.0
    
    # Find best server and measure download
    best_speed = 0.0
    best_server = "Unknown"
    
    for url, server_name in TEST_SERVERS:
        def dl_progress(mb: float, speed: float):
            if progress_callback:
                progress_callback("download", min(99, (mb / 10) * 100), speed)
        
        speed = measure_download(url, download_duration, dl_progress)
        if speed > best_speed:
            best_speed = speed
            best_server = server_name
    
    download_speed = best_speed
    
    # Measure upload
    def ul_progress(mb: float, speed: float):
        if progress_callback:
            progress_callback("upload", min(99, (mb / 5) * 100), speed)
    
    upload_speed = measure_upload(upload_duration, ul_progress)
    
    return SpeedTestResult(
        download_mbps=download_speed,
        upload_mbps=upload_speed,
        ping_ms=ping,
        server=best_server,
        timestamp=datetime.now().isoformat(),
    )


def print_brand() -> None:
    """Print the OnWords brand header."""
    print(f"{RED}on{WHITE}words{RESET} · Speed Test\n")


def print_progress_bar(label: str, percent: float, speed: float, width: int = 30):
    """Print a progress bar."""
    filled = int(width * percent / 100)
    bar = "█" * filled + "░" * (width - filled)
    print(f"\r  {label}: [{CYAN}{bar}{RESET}] {speed:.1f} Mbps", end="", flush=True)


def main() -> None:
    """CLI entry point for speed test."""
    print_brand()
    
    print(f"{DIM}Testing internet speed...{RESET}\n")
    
    # Ping test
    print(f"  {DIM}Measuring ping...{RESET}", end="", flush=True)
    ping = measure_ping()
    if ping:
        color = GREEN if ping < 50 else (YELLOW if ping < 100 else RED)
        print(f"\r  Ping: {color}{ping:.1f} ms{RESET}          ")
    else:
        print(f"\r  Ping: {RED}Failed{RESET}          ")
    
    print()
    
    # Download test
    print(f"  {DIM}Testing download speed...{RESET}")
    
    def dl_callback(mb: float, speed: float):
        filled = min(30, int(30 * mb / 10))
        bar = "█" * filled + "░" * (30 - filled)
        print(f"\r  Download: [{CYAN}{bar}{RESET}] {speed:.1f} Mbps", end="", flush=True)
    
    download_speed = 0.0
    for url, server in TEST_SERVERS:
        speed = measure_download(url, duration=8.0, progress_callback=dl_callback)
        if speed > download_speed:
            download_speed = speed
            best_server = server
    
    color = GREEN if download_speed > 50 else (YELLOW if download_speed > 10 else RED)
    print(f"\r  Download: [{GREEN}{'█' * 30}{RESET}] {color}{download_speed:.1f} Mbps{RESET}   ")
    
    print()
    
    # Upload test
    print(f"  {DIM}Testing upload speed...{RESET}")
    
    def ul_callback(mb: float, speed: float):
        filled = min(30, int(30 * mb / 5))
        bar = "█" * filled + "░" * (30 - filled)
        print(f"\r  Upload:   [{CYAN}{bar}{RESET}] {speed:.1f} Mbps", end="", flush=True)
    
    upload_speed = measure_upload(duration=8.0, progress_callback=ul_callback)
    
    color = GREEN if upload_speed > 20 else (YELLOW if upload_speed > 5 else RED)
    print(f"\r  Upload:   [{GREEN}{'█' * 30}{RESET}] {color}{upload_speed:.1f} Mbps{RESET}   ")
    
    # Summary
    print(f"\n{BOLD}Results:{RESET}\n")
    print(f"  ↓ Download: {GREEN}{download_speed:.1f} Mbps{RESET}")
    print(f"  ↑ Upload:   {GREEN}{upload_speed:.1f} Mbps{RESET}")
    print(f"  ⏱ Ping:     {GREEN}{ping:.1f} ms{RESET}" if ping else f"  ⏱ Ping:     {RED}N/A{RESET}")
    print(f"  🌐 Server:   {best_server}")
    print()


if __name__ == "__main__":
    main()



