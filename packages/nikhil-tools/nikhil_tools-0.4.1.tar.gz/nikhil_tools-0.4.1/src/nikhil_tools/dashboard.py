"""Live system dashboard module for OnWords."""

from __future__ import annotations

import os
import sys
import time
import platform
from datetime import datetime

# Brand colors for terminal output
RED = "\033[31m"
WHITE = "\033[37m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Cursor control
CLEAR_SCREEN = "\033[2J"
CURSOR_HOME = "\033[H"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"


def get_terminal_size() -> tuple[int, int]:
    """Get terminal width and height."""
    try:
        size = os.get_terminal_size()
        return size.columns, size.lines
    except Exception:
        return 80, 24


def format_bar(percent: float, width: int = 20, filled_char: str = "█", empty_char: str = "░") -> str:
    """Create a progress bar string."""
    filled = int(width * percent / 100)
    empty = width - filled
    
    if percent >= 90:
        color = RED
    elif percent >= 70:
        color = YELLOW
    else:
        color = GREEN
    
    return f"{color}{filled_char * filled}{DIM}{empty_char * empty}{RESET}"


def format_bytes(bytes_val: float) -> str:
    """Format bytes to human readable string."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_val < 1024:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.1f} PB"


def format_speed(mbps: float) -> str:
    """Format speed with color."""
    if mbps < 1:
        return f"{DIM}{mbps:.2f} Mbps{RESET}"
    elif mbps < 10:
        return f"{YELLOW}{mbps:.1f} Mbps{RESET}"
    elif mbps < 100:
        return f"{GREEN}{mbps:.1f} Mbps{RESET}"
    else:
        return f"{CYAN}{mbps:.1f} Mbps{RESET}"


def draw_box(title: str, content: list[str], width: int) -> list[str]:
    """Draw a box with title and content."""
    lines = []
    inner_width = width - 4
    
    # Top border
    lines.append(f"┌─ {WHITE}{title}{RESET} " + "─" * (inner_width - len(title) - 1) + "┐")
    
    # Content
    for line in content:
        # Strip ANSI for length calculation
        import re
        visible_len = len(re.sub(r'\033\[[0-9;]*m', '', line))
        padding = inner_width - visible_len
        lines.append(f"│ {line}{' ' * max(0, padding)} │")
    
    # Bottom border
    lines.append("└" + "─" * (width - 2) + "┘")
    
    return lines


def render_dashboard(stats, net_speed: tuple[float, float], width: int = 80) -> str:
    """Render the complete dashboard."""
    lines = []
    
    # Header
    now = datetime.now().strftime("%H:%M:%S")
    header = f"{RED}on{WHITE}words{RESET} · Live Dashboard"
    lines.append("")
    lines.append(f"  {header}  {DIM}│{RESET}  {now}  {DIM}│{RESET}  Press {CYAN}Ctrl+C{RESET} to exit")
    lines.append("")
    
    # System info
    sys_info = f"{platform.system()} {platform.release()} │ Uptime: {stats.uptime_hours:.1f}h"
    lines.append(f"  {DIM}{sys_info}{RESET}")
    lines.append("")
    
    col_width = (width - 6) // 2
    bar_width = col_width - 20
    
    # CPU Box
    cpu_content = [
        f"Usage:  [{format_bar(stats.cpu.usage_percent, bar_width)}] {stats.cpu.usage_percent:5.1f}%",
        f"Cores:  {stats.cpu.core_count}",
    ]
    if stats.cpu.frequency_mhz:
        cpu_content.append(f"Freq:   {stats.cpu.frequency_mhz:.0f} MHz")
    
    # Per-core mini bars
    if stats.cpu.per_core_usage:
        core_bars = ""
        for i, usage in enumerate(stats.cpu.per_core_usage[:8]):
            if usage >= 80:
                core_bars += f"{RED}▇{RESET}"
            elif usage >= 50:
                core_bars += f"{YELLOW}▆{RESET}"
            elif usage >= 20:
                core_bars += f"{GREEN}▄{RESET}"
            else:
                core_bars += f"{DIM}▂{RESET}"
        if len(stats.cpu.per_core_usage) > 8:
            core_bars += f" {DIM}+{len(stats.cpu.per_core_usage) - 8}{RESET}"
        cpu_content.append(f"Cores:  {core_bars}")
    
    cpu_box = draw_box("CPU", cpu_content, col_width)
    
    # Memory Box
    mem_content = [
        f"Usage:  [{format_bar(stats.memory.percent_used, bar_width)}] {stats.memory.percent_used:5.1f}%",
        f"Used:   {stats.memory.used_gb:.1f} GB / {stats.memory.total_gb:.1f} GB",
        f"Free:   {stats.memory.available_gb:.1f} GB",
    ]
    mem_box = draw_box("Memory", mem_content, col_width)
    
    # Combine CPU and Memory side by side
    for i in range(max(len(cpu_box), len(mem_box))):
        left = cpu_box[i] if i < len(cpu_box) else " " * col_width
        right = mem_box[i] if i < len(mem_box) else " " * col_width
        lines.append(f"  {left}  {right}")
    
    lines.append("")
    
    # Disk Box
    disk_content = [
        f"Usage:  [{format_bar(stats.disk.percent_used, bar_width)}] {stats.disk.percent_used:5.1f}%",
        f"Used:   {stats.disk.used_gb:.0f} GB / {stats.disk.total_gb:.0f} GB",
        f"Free:   {stats.disk.free_gb:.0f} GB",
    ]
    disk_box = draw_box("Disk", disk_content, col_width)
    
    # Network Box
    dl_speed, ul_speed = net_speed
    net_content = [
        f"↓ Down: {format_speed(dl_speed)}",
        f"↑ Up:   {format_speed(ul_speed)}",
        f"Total:  ↓{format_bytes(stats.network.bytes_recv if stats.network else 0)} ↑{format_bytes(stats.network.bytes_sent if stats.network else 0)}",
    ]
    net_box = draw_box("Network", net_content, col_width)
    
    # Combine Disk and Network
    for i in range(max(len(disk_box), len(net_box))):
        left = disk_box[i] if i < len(disk_box) else " " * col_width
        right = net_box[i] if i < len(net_box) else " " * col_width
        lines.append(f"  {left}  {right}")
    
    lines.append("")
    
    # Battery and GPU (if available)
    extra_left = []
    extra_right = []
    
    if stats.battery:
        status = "⚡" if stats.battery.is_charging else ("🔌" if stats.battery.is_plugged else "🔋")
        extra_left = [
            f"Level:  [{format_bar(stats.battery.percent, bar_width)}] {stats.battery.percent:5.0f}%",
            f"Status: {status} {'Charging' if stats.battery.is_charging else ('Plugged' if stats.battery.is_plugged else 'Battery')}",
        ]
        if stats.battery.time_left_mins and not stats.battery.is_plugged:
            h, m = divmod(stats.battery.time_left_mins, 60)
            extra_left.append(f"Time:   {h}h {m}m remaining")
    
    if stats.gpu:
        extra_right = [
            f"Name:   {stats.gpu.name[:col_width-12]}",
            f"Vendor: {stats.gpu.vendor}",
        ]
        if stats.gpu.vram_mb:
            extra_right.append(f"VRAM:   {stats.gpu.vram_mb} MB")
    
    if extra_left or extra_right:
        bat_box = draw_box("Battery", extra_left, col_width) if extra_left else [" " * col_width] * 5
        gpu_box = draw_box("GPU", extra_right, col_width) if extra_right else [" " * col_width] * 5
        
        for i in range(max(len(bat_box), len(gpu_box))):
            left = bat_box[i] if i < len(bat_box) else " " * col_width
            right = gpu_box[i] if i < len(gpu_box) else " " * col_width
            lines.append(f"  {left}  {right}")
    
    return "\n".join(lines)


def run_dashboard(refresh_rate: float = 1.0):
    """
    Run the live dashboard.
    
    Args:
        refresh_rate: Refresh interval in seconds
    """
    from nikhil_tools.system_monitor import get_system_stats
    
    # Track network speed
    prev_bytes_recv = 0
    prev_bytes_sent = 0
    prev_time = time.time()
    
    print(HIDE_CURSOR, end="")
    
    try:
        while True:
            # Get stats
            stats = get_system_stats()
            
            # Calculate network speed
            current_time = time.time()
            time_delta = current_time - prev_time
            
            if stats.network and time_delta > 0:
                bytes_recv_delta = stats.network.bytes_recv - prev_bytes_recv
                bytes_sent_delta = stats.network.bytes_sent - prev_bytes_sent
                
                dl_speed = (bytes_recv_delta * 8) / (time_delta * 1_000_000) if prev_bytes_recv > 0 else 0
                ul_speed = (bytes_sent_delta * 8) / (time_delta * 1_000_000) if prev_bytes_sent > 0 else 0
                
                prev_bytes_recv = stats.network.bytes_recv
                prev_bytes_sent = stats.network.bytes_sent
            else:
                dl_speed = ul_speed = 0
            
            prev_time = current_time
            
            # Get terminal size
            width, height = get_terminal_size()
            width = max(80, min(width, 120))
            
            # Render
            output = render_dashboard(stats, (dl_speed, ul_speed), width)
            
            # Clear and print
            print(CURSOR_HOME + CLEAR_SCREEN, end="")
            print(output)
            
            time.sleep(refresh_rate)
            
    except KeyboardInterrupt:
        pass
    finally:
        print(SHOW_CURSOR, end="")
        print(CLEAR_SCREEN + CURSOR_HOME, end="")
        print(f"\n{RED}on{WHITE}words{RESET} · Dashboard closed\n")


def print_brand() -> None:
    """Print the OnWords brand header."""
    print(f"{RED}on{WHITE}words{RESET} · Live Dashboard\n")


def main() -> None:
    """CLI entry point for live dashboard."""
    import sys
    
    refresh = 1.0
    
    # Parse simple args
    args = sys.argv[1:]
    if "-h" in args or "--help" in args:
        print_brand()
        print(f"Usage: nikhil-dashboard [OPTIONS]\n")
        print(f"Options:")
        print(f"  -r, --refresh SECONDS  Refresh rate (default: 1.0)")
        print(f"  -h, --help             Show this help")
        return
    
    for i, arg in enumerate(args):
        if arg in ["-r", "--refresh"] and i + 1 < len(args):
            try:
                refresh = float(args[i + 1])
            except ValueError:
                pass
    
    run_dashboard(refresh_rate=refresh)


if __name__ == "__main__":
    main()



