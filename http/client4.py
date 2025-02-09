import asyncio


async def async_http_post(host, port, path, data, headers=None):
    """
    Sends an HTTP POST request asynchronously and parses the response.

    :param host: The target server hostname (e.g., 'httpbin.org')
    :param port: The port number (typically 80 for HTTP)
    :param path: The resource path (e.g., '/post')
    :param data: The POST body as a string.
    :param headers: Optional dictionary of additional headers.
    """
    # Set default headers if not provided.
    if headers is None:
        headers = {}
    headers.setdefault("Host", host)
    headers.setdefault("Content-Length", str(len(data.encode())))
    headers.setdefault("Content-Type", "application/x-www-form-urlencoded")
    headers.setdefault("Connection", "close")

    # Construct the HTTP request (note the CRLF line endings).
    request_line = f"POST {path} HTTP/1.1\r\n"
    header_lines = "".join(f"{k}: {v}\r\n" for k, v in headers.items())
    http_request = request_line + header_lines + "\r\n" + data

    # Open an asynchronous connection to the server.
    reader, writer = await asyncio.open_connection(host, port)
    writer.write(http_request.encode())
    await writer.drain()

    # --- Parse the response headers ---
    # Read data until we have encountered the header-body separator: '\r\n\r\n'
    header_bytes = b""
    while b"\r\n\r\n" not in header_bytes:
        chunk = await reader.read(1024)
        if not chunk:
            break  # Connection closed before complete headers received.
        header_bytes += chunk

    # Split the headers from the rest of the data.
    header_section, sep, remainder = header_bytes.partition(b"\r\n\r\n")
    header_text = header_section.decode()
    print("Received Headers:")
    print(header_text)
    print("-" * 40)

    # --- Parse the response body ---
    # Try to extract the Content-Length from the headers.
    content_length = None
    for line in header_text.split("\r\n"):
        if line.lower().startswith("content-length:"):
            try:
                content_length = int(line.split(":", 1)[1].strip())
            except ValueError:
                pass
            break

    body = remainder  # This is the initial part of the body (if any) already read.

    # If a content length is provided, read until we have all the data.
    if content_length is not None:
        while len(body) < content_length:
            chunk = await reader.read(1024)
            if not chunk:
                break
            body += chunk
    else:
        # Otherwise, read until EOF.
        more = await reader.read(1024)
        while more:
            body += more
            more = await reader.read(1024)

    # Close the connection.
    writer.close()
    await writer.wait_closed()

    # Decode and print the response body.
    body_text = body.decode(errors='replace')
    print("Received Body:")
    print(body_text)


async def main():
    host = "httpbin.org"
    port = 80
    path = "/post"
    # Data formatted as application/x-www-form-urlencoded.
    data = "field1=value1&field2=value2"
    await async_http_post(host, port, path, data)


if __name__ == '__main__':
    asyncio.run(main())
