import socket
import struct
import time
import os

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
    # IP header is typically 20 bytes (without options)
    ip_header = data[:20]
    iph = struct.unpack('!BBHHHBBH4s4s', ip_header)
    ttl = iph[5]  # TTL is the 6th field in the IP header

    # ICMP header starts after IP header (20 bytes)
    icmp_header = data[20:28]  # ICMP header is 8 bytes
    icmph = struct.unpack('!BBHHh', icmp_header)
    icmp_type = icmph[0]
    icmp_code = icmph[1]
    icmp_id = icmph[3]
    icmp_seq = icmph[4]

    return ttl, icmp_type, icmp_code, icmp_id, icmp_seq


def ping(host, count=4, timeout=1):
    """Ping a host using ICMP and parse reply details."""
    try:
        dest_addr = socket.gethostbyname(host)
        print(f"Pinging {host} [{dest_addr}] with {len(b'Hello, ICMP!')} bytes of data:")

        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock.settimeout(timeout)

        identifier = os.getpid() & 0xFFFF  # Unique ID for this process

        for seq in range(count):
            packet = create_icmp_packet(identifier, seq)
            start_time = time.time()

            sock.sendto(packet, (dest_addr, 0))
            try:
                data, addr = sock.recvfrom(1024)
                end_time = time.time()
                rtt = (end_time - start_time) * 1000  # Round-trip time in ms

                # Parse the reply
                ttl, icmp_type, icmp_code, icmp_id, icmp_seq = parse_icmp_reply(data)

                # Display detailed response
                print(f"Reply from {addr[0]}: seq={icmp_seq} time={rtt:.2f}ms TTL={ttl} "
                      f"Type={icmp_type} Code={icmp_code} ID={icmp_id}")
            except socket.timeout:
                print(f"Request timed out for seq={seq}")
            time.sleep(1)  # Wait between pings

        sock.close()
    except socket.gaierror:
        print("Error: Hostname could not be resolved.")
    except PermissionError:
        print("Error: Run this script with administrative/root privileges.")


if __name__ == "__main__":
    ping("8.8.8.8")  # Example: Ping Google's DNS server