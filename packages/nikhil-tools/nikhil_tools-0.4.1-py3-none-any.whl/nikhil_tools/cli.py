"""Main CLI entry point for nikhil-tools."""

from __future__ import annotations

import sys

# Brand colors
RED = "\033[31m"
WHITE = "\033[37m"
CYAN = "\033[36m"
GREEN = "\033[32m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"


def print_banner():
    """Print the OnWords banner."""
    print(f"""
{RED}  ██████╗ ███╗   ██╗{WHITE}██╗    ██╗ ██████╗ ██████╗ ██████╗ ███████╗{RESET}
{RED} ██╔═══██╗████╗  ██║{WHITE}██║    ██║██╔═══██╗██╔══██╗██╔══██╗██╔════╝{RESET}
{RED} ██║   ██║██╔██╗ ██║{WHITE}██║ █╗ ██║██║   ██║██████╔╝██║  ██║███████╗{RESET}
{RED} ██║   ██║██║╚██╗██║{WHITE}██║███╗██║██║   ██║██╔══██╗██║  ██║╚════██║{RESET}
{RED} ╚██████╔╝██║ ╚████║{WHITE}╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝███████║{RESET}
{RED}  ╚═════╝ ╚═╝  ╚═══╝{WHITE} ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝{RESET}
""")


def print_help():
    """Print help information."""
    from nikhil_tools import __version__
    
    print_banner()
    print(f"{DIM}Version:{RESET} {__version__}")
    print(f"{DIM}Python toolkit for network scanning & system monitoring{RESET}\n")
    
    print(f"{BOLD}Available Commands:{RESET}\n")
    
    commands = [
        ("nikhil-sysmon", "System monitor - CPU, RAM, Disk, GPU, Battery stats"),
        ("nikhil-dashboard", "Live dashboard - Real-time system stats with auto-refresh"),
        ("nikhil-speed", "Speed test - Test internet download/upload speed"),
        ("nikhil-wifi", "WiFi scanner - Scan nearby wireless networks"),
        ("nikhil-ip", "IP scanner - Discover devices on local network"),
        ("nikhil-ble", "BLE scanner - Find Bluetooth Low Energy devices"),
        ("nikhil", "Show this help message"),
    ]
    
    for cmd, desc in commands:
        print(f"  {GREEN}{cmd:<16}{RESET} {desc}")
    
    print(f"\n{BOLD}Python Usage:{RESET}\n")
    print(f"  {CYAN}import nikhil_tools{RESET}")
    print(f"  {CYAN}stats = nikhil_tools.get_system_stats(){RESET}")
    print(f"  {CYAN}networks = nikhil_tools.scan_wifi(){RESET}")
    print(f"  {CYAN}devices = nikhil_tools.scan_network(){RESET}")
    print(f"  {CYAN}ble = nikhil_tools.scan_devices_sync(){RESET}")
    
    print(f"\n{BOLD}Platform Support:{RESET}\n")
    print(f"  {GREEN}✓{RESET} macOS    {GREEN}✓{RESET} Windows    {GREEN}✓{RESET} Linux")
    
    print(f"\n{DIM}PyPI:{RESET} https://pypi.org/project/nikhil-tools/")
    print(f"{DIM}Install:{RESET} pip install nikhil-tools\n")


def main():
    """Main CLI entry point."""
    args = sys.argv[1:]
    
    if not args or args[0] in ["-h", "--help", "help", "list", "-l", "--list"]:
        print_help()
    elif args[0] in ["sysmon", "system", "sys"]:
        from nikhil_tools.system_monitor import main as sysmon_main
        sysmon_main()
    elif args[0] in ["dashboard", "dash", "live"]:
        from nikhil_tools.dashboard import main as dashboard_main
        dashboard_main()
    elif args[0] in ["speed", "speedtest", "test"]:
        from nikhil_tools.speed_test import main as speed_main
        speed_main()
    elif args[0] in ["wifi", "wireless"]:
        from nikhil_tools.wifi_scanner import main as wifi_main
        wifi_main()
    elif args[0] in ["ip", "network", "net"]:
        from nikhil_tools.ip_scanner import main as ip_main
        ip_main()
    elif args[0] in ["ble", "bluetooth", "bt"]:
        from nikhil_tools.ble_scanner import main as ble_main
        ble_main()
    elif args[0] in ["-v", "--version", "version"]:
        from nikhil_tools import __version__
        print(f"{RED}on{WHITE}words{RESET} nikhil-tools v{__version__}")
    else:
        print(f"{RED}Unknown command:{RESET} {args[0]}")
        print(f"{DIM}Run 'nikhil --help' for available commands{RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()

