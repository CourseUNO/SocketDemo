import socket


def run_server():
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 12345  # Port to listen on (non-privileged ports are > 1023)

    # 1. family (Address Family)
    # Defines the type of network addresses the socket can use:
    #
    # socket.AF_INET → IPv4 (default)
    # socket.AF_INET6 → IPv6
    # socket.AF_UNIX → Unix domain sockets (for inter-process communication on the same system)

    # 2. type (Socket Type)
    # Determines how data is transmitted:
    #
    # socket.SOCK_STREAM → TCP (connection-oriented, reliable)
    # socket.SOCK_DGRAM → UDP (connectionless, fast but unreliable)
    # socket.SOCK_RAW → Raw socket (used for low-level network access, such as ICMP)

    # 3. proto (Protocol Number)
    # Specifies the protocol to be used (usually set to 0 for default).
    # For example:
    # socket.IPPROTO_TCP → TCP
    # socket.IPPROTO_UDP → UDP
    # socket.IPPROTO_ICMP → ICMP (used for ping operations)

    # 4. fileno (File Descriptor)
    # Used to create a socket object from an existing file descriptor.
    # Normally, this is set to None, and Python creates a new socket.
    # If you pass a valid file descriptor, the socket object wraps it instead.

    # with statement: python context manager
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)  # Receive up to 1024 bytes
                    if not data:
                        break
                    conn.sendall(data)  # Send back the received data
                    print(f"Echoed: {data.decode()}")


if __name__ == '__main__':
    run_server()
