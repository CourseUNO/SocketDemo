import socket
from urllib.parse import urlparse


class SimpleHTTPClient:
    def __init__(self):
        self.cookies = {}

    def parse_cookies(self, cookie_headers):
        """Parse Set-Cookie headers into the cookies dictionary"""
        for header in cookie_headers:
            # Get the first part before ';' (actual cookie)
            cookie_part = header.split(';', 1)[0].strip()
            if '=' in cookie_part:
                name, value = cookie_part.split('=', 1)
                self.cookies[name] = value

    def send_request(self, url, method='GET'):
        """Send HTTP request with cookie handling"""
        parsed = urlparse(url)
        host = parsed.hostname
        port = parsed.port or 80
        path = parsed.path or '/'

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))

            # Build headers
            headers = [
                f"{method} {path} HTTP/1.1",
                f"Host: {host}",
                "Connection: close"
            ]

            # Add cookies if available
            if self.cookies:
                cookie_str = '; '.join([f"{k}={v}" for k, v in self.cookies.items()])
                headers.append(f"Cookie: {cookie_str}")

            # Add final headers
            request = '\r\n'.join(headers) + '\r\n\r\n'
            s.send(request.encode())

            # Receive response
            response = b''
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response += chunk

        # Split headers and body
        header_end = response.find(b'\r\n\r\n')
        headers_part = response[:header_end]
        body = response[header_end + 4:]

        # Parse headers
        headers = headers_part.decode().split('\r\n')
        status_line = headers[0]
        status_code = int(status_line.split()[1])

        # Extract cookies from response headers
        # . Each Set-Cookie header can have key=value
        cookie_headers = [h.split(': ', 1)[1]
                          for h in headers
                          if h.lower().startswith('set-cookie:')]
        self.parse_cookies(cookie_headers)

        # Decode body
        try:
            body = body.decode('utf-8')
        except UnicodeDecodeError:
            body = body.decode('latin-1')

        return {
            'status': status_line,
            'status_code': status_code,
            'headers': headers[1:],
            'body': body,
            'cookies': self.cookies.copy()
        }


if __name__ == "__main__":
    client = SimpleHTTPClient()

    # First request (no cookies)
    print("First request to example.com:")
    response = client.send_request('http://example.com')
    print(f"Status: {response['status_code']}")
    print(f"Cookies received: {response['cookies']}\n")

    # Second request (with cookies if any)
    print("Second request to example.com:")
    response = client.send_request('http://example.com')
    print(f"Status: {response['status_code']}")
    print(f"Cookies sent: {response['cookies']}")
