import socket
import struct
import time
import os
import re

# ICMP Echo Request type and code
ICMP_ECHO_REQUEST = 8
ICMP_CODE = 0


def checksum(data):
    """Calculate the checksum for the ICMP packet."""
    checksum = 0
    count = 0
    data += b'\x00' if len(data) % 2 else b''  # Pad if odd length
    while count < len(data):
        temp = (data[count + 1] << 8) + data[count]
        checksum += temp
        count += 2
    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum += (checksum >> 16)
    return ~checksum & 0xffff


def create_icmp_packet(identifier, sequence):
    """Create an ICMP Echo Request packet."""
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, ICMP_CODE, 0, identifier, sequence)
    data = b'Hello, ICMP!'  # Payload
    my_checksum = checksum(header + data)
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, ICMP_CODE, my_checksum, identifier, sequence)
    return header + data


def parse_icmp_reply(data):
    """Parse the IP and ICMP headers from the reply packet."""
    ip_header = data[:20]
    iph = struct.unpack('!BBHHHBBH4s4s', ip_header)
    ttl = iph[5]

    icmp_header = data[20:28]
    icmph = struct.unpack('!BBHHh', icmp_header)
    icmp_type = icmph[0]
    icmp_code = icmph[1]
    icmp_id = icmph[3]
    icmp_seq = icmph[4]

    return ttl, icmp_type, icmp_code, icmp_id, icmp_seq


def is_valid_ip(host):
    """Check if the input is a valid IPv4 address."""
    ip_pattern = re.compile(
        r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
    return ip_pattern.match(host) is not None


def ping(host, ttl=64, count=4, timeout=1):
    """Ping a host with a custom TTL using the default source IP."""
    try:
        dest_addr = host if is_valid_ip(host) else socket.gethostbyname(host)
        print(f"Pinging {dest_addr} with {len(b'Hello, ICMP!')} bytes of data (TTL={ttl}):")

        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)  # Set custom TTL
        sock.settimeout(timeout)

        identifier = os.getpid() & 0xFFFF

        for seq in range(count):
            packet = create_icmp_packet(identifier, seq)
            try:
                start_time = time.time()
                sock.sendto(packet, (dest_addr, 0))
                data, addr = sock.recvfrom(1024)
                end_time = time.time()
                rtt = (end_time - start_time) * 1000

                ttl_reply, icmp_type, icmp_code, icmp_id, icmp_seq = parse_icmp_reply(data)

                if icmp_type == 0:  # Echo Reply
                    print(f"Reply from {addr[0]}: seq={icmp_seq} time={rtt:.2f}ms TTL={ttl_reply}")
                elif icmp_type == 11:  # Time Exceeded (TTL expired)
                    print(f"TTL Expired from {addr[0]}: seq={seq} time={rtt:.2f}ms")
                else:
                    print(f"Non-Echo Reply from {addr[0]}: seq={seq} Type={icmp_type} Code={icmp_code}")
            except socket.timeout:
                print(f"Request timed out for seq={seq}")
            time.sleep(1)

        sock.close()
    except socket.gaierror:
        print("Error: Hostname could not be resolved.")
    except PermissionError:
        print("Error: Run this script with administrative/root privileges.")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    print("Test: Pinging 8.8.8.8 with TTL=2")
    ping("8.8.8.8", ttl=5)