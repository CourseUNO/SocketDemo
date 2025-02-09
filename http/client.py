import socket


def send_http_request(ost, port=80, path="/"):
    """
    Send an HTTP GET request using raw sockets.

    Args:
        host (str): Target host (e.g., "example.com")
        port (int): Target port (default: 80)
        path (str): Request path (default: "/")

    Returns:
        str: Server response
    """
    # Create TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server
        client_socket.connect((host, port))

        # Craft HTTP GET request
        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            "Connection: close\r\n"  # Ask server to close connection after response
            "\r\n"
        )

        # Send request
        # in Python, strings are Unicode by default, but when you need to store them
        # or send them over a network, you have to encode them into bytes.
        # The encode() method does exactly that.
        client_socket.send(request.encode()) # Default: UTF-8

        # Receive response
        response = b""
        while True:
            chunk = client_socket.recv(4096)  # Receive up to 4KB at a time
            if not chunk:
                break
            response += chunk

    finally:
        client_socket.close()

    return response.decode()


if __name__ == "__main__":
    # Example usage
    host = "example.com"
    print(f"Sending request to {host}...\n")

    try:
        response = send_http_request(host)
        print(response)
    except Exception as e:
        print(f"Error: {e}")
