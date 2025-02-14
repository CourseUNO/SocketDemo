import socket


def send_util_exit():
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 12345  # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            message = input("Please input two numbers: ")
            if message == "exit":
                break
            s.sendall(f'add {message}'.encode())
            data = s.recv(1024)
            print(f"Received: {data.decode()}")


if __name__ == '__main__':
    send_util_exit()
