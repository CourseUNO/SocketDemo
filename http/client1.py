import socket


def send_http_request(host, port=80, path="/"):
    """
    Send an HTTP GET request and return parsed response components.

    Returns:
        dict: Dictionary containing:
            - status_code (int)
            - headers (dict)
            - body (str)
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    response = b""

    try:
        client_socket.connect((host, port))
        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            "Connection: close\r\n\r\n"
        )
        client_socket.send(request.encode())

        while True:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            response += chunk
    finally:
        client_socket.close()

    # The headers and body are separated by a blank line, which is \r\n\r\n.
    # Split headers and body
    header_end = response.find(b"\r\n\r\n")
    if header_end == -1:
        raise ValueError("Invalid response: No header/body separation")

    headers_part, body_part = response[:header_end], response[header_end + 4:]

    # Parse status line
    # Each header line is separated by \r\n.
    # The first line is the status line, then the rest are headers.
    # For each header line, split on the first colon to separate the key and value.
    headers_lines = headers_part.split(b"\r\n")
    status_line = headers_lines[0].decode()
    protocol, status_code, *reason = status_line.split()

    # Parse headers
    headers = {}
    for line in headers_lines[1:]:
        if not line:
            continue
        try:
            key, value = line.split(b":", 1)
            headers[key.decode().strip()] = value.decode().strip()
        except ValueError:
            continue  # Skip invalid headers

    # Decode body (simplified - should check Content-Encoding)
    charset = 'utf-8'
    if 'Content-Type' in headers:
        content_type = headers['Content-Type'].lower()
        if 'charset=' in content_type:
            charset = content_type.split('charset=')[-1].split(';')[0].strip()

    try:
        body = body_part.decode(charset)
    except UnicodeDecodeError:
        body = body_part.decode('utf-8', errors='replace')

    return {
        'status_code': int(status_code),
        'headers': headers,
        'body': body
    }


if __name__ == "__main__":
    try:
        result = send_http_request("example.com")
        print(f"Status Code: {result['status_code']}\n")
        print("Headers:")
        for key, value in result['headers'].items():
            print(f"  {key}: {value}")
        print("\nBody:")
        print(result['body'][:500] + "...")  # Show first 500 characters
    except Exception as e:
        print(f"Error: {e}")
