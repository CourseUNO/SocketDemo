import socket


def send_request(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        message = "GET ME THE PAGE"
        s.sendall(message.encode())
        data = s.recv(1024)
        print(f"Received: {data.decode()}")


if __name__ == '__main__':
    send_request("google.com", 80)  # https 443
