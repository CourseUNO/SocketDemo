import socket
import json

# Target API Server and Port (Change as needed)
HOST = "jsonplaceholder.typicode.com"  # Public test API
PORT = 80  # HTTP uses port 80


# Function to send HTTP requests via raw socket
def send_http_request(method, path, body=None):
    """Send an HTTP request using a raw socket."""

    # Create a socket connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))

        # Construct HTTP request headers
        headers = [
            f"{method} {path} HTTP/1.1",
            f"Host: {HOST}",
            "User-Agent: Python Socket Test",
            "Connection: close"  # Close connection after request
        ]

        # Add body if necessary (for POST and PUT)
        if body:
            body_json = json.dumps(body)
            headers.append("Content-Type: application/json")
            headers.append(f"Content-Length: {len(body_json)}")
            request = "\r\n".join(headers) + "\r\n\r\n" + body_json
        else:
            request = "\r\n".join(headers) + "\r\n\r\n"

        # Send the request
        sock.sendall(request.encode())

        # Receive and print the response
        response = b""
        while True:
            chunk = sock.recv(4096)  # Receive data in chunks
            if not chunk:
                break
            response += chunk

        print(f"\n=== {method} Response ===")
        print(response.decode())


def test():
    # Test API Endpoints
    get_path = "/posts/1"  # Retrieve a post
    post_path = "/posts"  # Create a post
    put_path = "/posts/1"  # Update a post
    delete_path = "/posts/1"  # Delete a post

    # Data for POST and PUT requests
    sample_data = {
        "title": "Python Socket Test",
        "body": "This is a test message sent via raw socket.",
        "userId": 1
    }

    # Perform HTTP Requests
    send_http_request("GET", get_path)  # GET request
    # send_http_request("POST", post_path, sample_data)  # POST request
    # send_http_request("PUT", put_path, sample_data)  # PUT request
    # send_http_request("DELETE", delete_path)  # DELETE request


if __name__ == '__main__':
    test()
