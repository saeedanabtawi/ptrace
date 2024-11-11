# Python Traceroute Implementation

A pure Python implementation of the traceroute network diagnostic tool that works on both Windows and Unix-like systems.

## Description

This tool traces the route that packets take to reach a network host by sending ICMP Echo Request packets with increasing Time To Live (TTL) values. It shows:
- The route taken by packets across an IP network
- The time taken for each hop
- The hostname and IP address of each intermediate router

## Features

- Cross-platform support (Windows and Unix-like systems)
- Pure Python implementation
- Hostname resolution for each hop
- Configurable maximum hops and timeout
- Windows-specific optimization using ICMP.DLL

## Prerequisites

- Python 3.7 or higher
- Administrator/root privileges (for Unix-like systems)
- Windows: No special privileges required
- Linux/Mac: Root privileges required

## Installation

1. Clone the repository: 

## Troubleshooting

### Windows
- Ensure Python is allowed through Windows Firewall
- Try running Command Prompt as Administrator
- Verify ICMP traffic isn't blocked by your firewall/antivirus

### Unix-like Systems
- Must be run with sudo/root privileges
- Check if ICMP traffic is allowed through system firewall
- Verify raw socket permissions

## How It Works

1. Creates ICMP Echo Request packets
2. Sends packets with incrementing TTL values
3. Listens for ICMP Time Exceeded or Echo Reply responses
4. Displays the IP address and hostname of responding routers
5. Measures round-trip time for each hop

## Technical Details

- Uses raw sockets on Unix-like systems
- Uses ICMP.DLL through ctypes on Windows
- Implements proper ICMP checksum calculation
- Handles both IPv4 address and hostname resolution

## Limitations

- Requires elevated privileges on Unix-like systems
- Some routers may not respond to ICMP packets
- Network security devices might block ICMP traffic
- Does not support IPv6 (currently IPv4 only)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by the original traceroute utility
- Thanks to the Python community for socket programming resources