import socket

HOST = "example.com"  # Replace with actual server
PORT = 80

# Step 1: Create a socket and connect to the server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# Step 2: Send an HTTP request without cookies (initial request)
http_request = (
    "GET / HTTP/1.1\r\n"
    f"Host: {HOST}\r\n"
    "User-Agent: Python-Socket\r\n"
    "Connection: close\r\n\r\n"
)
sock.sendall(http_request.encode())

# Step 3: Receive and process the response
response = sock.recv(4096).decode(errors="ignore")
sock.close()

# Extract 'Set-Cookie' from response headers
cookies = []
for line in response.split("\r\n"):
    if line.startswith("Set-Cookie:"):
        cookie = line.split(":", 1)[1].strip().split(";")[0]
        cookies.append(cookie)

print("Cookies received:", cookies)

# Step 4: Send another request including the received cookies
if cookies:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    cookie_header = "; ".join(cookies)
    http_request_with_cookies = (
        "GET / HTTP/1.1\r\n"
        f"Host: {HOST}\r\n"
        "User-Agent: Python-Socket\r\n"
        f"Cookie: {cookie_header}\r\n"
        "Connection: close\r\n\r\n"
    )

    sock.sendall(http_request_with_cookies.encode())

    # Receive and display the response with cookies sent
    response_with_cookies = sock.recv(4096).decode(errors="ignore")
    sock.close()

    print("\nServer Response After Sending Cookies:\n", response_with_cookies)