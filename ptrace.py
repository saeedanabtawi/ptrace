import socket
import struct
import time
import sys
from dataclasses import dataclass
from typing import Optional, Tuple

@dataclass  # This decorator automatically adds generated special methods like __init__ and __repr__ to the class
class ICMPPacket:
    id: int
    timestamp: float
    
    def create(self) -> bytes:
        """Create an ICMP echo request packet with checksum"""
        # Header is type (8), code (8), checksum (16), id (16), sequence (16)
        header = struct.pack('bbHHh', 8, 0, 0, self.id, 1)
        data = struct.pack('d', self.timestamp)
        
        # Calculate checksum
        checksum = self._calculate_checksum(header + data)
        
        # Reconstruct header with calculated checksum
        header = struct.pack('bbHHh', 8, 0, checksum, self.id, 1)
        return header + data
        
    def _calculate_checksum(self, packet: bytes) -> int:
        """Calculate ICMP packet checksum"""
        checksum = 0
        for i in range(0, len(packet), 2):
            if i + 1 < len(packet):
                checksum += packet[i] + (packet[i+1] << 8)
            else:
                checksum += packet[i]
        checksum = (checksum >> 16) + (checksum & 0xffff)
        return ~checksum & 0xffff

class ICMPSocket:
    def __init__(self, timeout: float = 2):
        self.sock = self._create_socket()
        self.sock.settimeout(timeout)  # Add timeout to prevent hanging
        
    def _create_socket(self) -> socket.socket:
        """Create a raw socket for ICMP"""
        try:
            icmp = socket.getprotobyname('icmp')
            return socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        except PermissionError:
            print("Error: This program requires root/admin privileges")
            sys.exit(1)
            
    def set_ttl(self, ttl: int) -> None:
        """Set Time To Live value"""
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
        
    def send_packet(self, packet: bytes, dest: str) -> None:
        """Send ICMP packet to destination"""
        self.sock.sendto(packet, (dest, 0))
        
    def receive(self) -> Tuple[bytes, Tuple]:
        """Receive ICMP response"""
        return self.sock.recvfrom(1024)
        
    def close(self) -> None:
        """Close the socket"""
        self.sock.close()

class Traceroute:
    def __init__(self, destination: str, max_hops: int = 30, timeout: float = 2):
        self.destination = destination
        self.max_hops = max_hops
        self.timeout = timeout
        
    def resolve_destination(self) -> Optional[str]:
        """Resolve hostname to IP address"""
        try:
            return socket.gethostbyname(self.destination)
        except socket.gaierror:
            print(f"Could not resolve hostname: {self.destination}")
            return None
            
    def get_hostname(self, ip: str) -> str:
        """Resolve IP to hostname"""
        try:
            return socket.gethostbyaddr(ip)[0]
        except socket.herror:
            return ip
            
    def run(self) -> None:
        """Execute traceroute"""
        dest_addr = self.resolve_destination()
        if not dest_addr:
            return
            
        print(f"traceroute to {self.destination} ({dest_addr}), {self.max_hops} hops max")
        
        for ttl in range(1, self.max_hops + 1):
            sock = ICMPSocket(timeout=self.timeout)
            sock.set_ttl(ttl)
            
            packet = ICMPPacket(id=ttl, timestamp=time.time()).create()
            sock.send_packet(packet, dest_addr)
            start_time = time.time()
            
            try:
                data, addr = sock.receive()
                end_time = time.time()
                
                addr = addr[0]
                host = self.get_hostname(addr)
                
                print(f"{ttl:2d}  {host} ({addr})  {(end_time - start_time)*1000:.3f} ms")
                
                if addr == dest_addr:
                    break
                    
            except socket.timeout:
                print(f"{ttl:2d}  * * *")
                
            finally:
                sock.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: sudo python3 ptrace.py <destination>")
        sys.exit(1)
        
    tracer = Traceroute(sys.argv[1])
    tracer.run()
