import socket


def send_once_client():
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 12345  # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        message = input("Enter message to echo: ")
        s.sendall(message.encode())
        data = s.recv(1024)
        print(f"Received: {data.decode()}")


def send_twice_client():
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 12345  # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        for i in range(2):
            message = input("Enter message to echo: ")
            s.sendall(message.encode())
            data = s.recv(1024)
            print(f"Received: {data.decode()}")


def send_util_exit():
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 12345  # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            message = input("Enter message to echo: ")
            if message == "exit":
                break
            s.sendall(message.encode())
            data = s.recv(1024)
            print(f"Received: {data.decode()}")


if __name__ == '__main__':
    # send_once_client()
    # send_twice_client()
    send_util_exit()
