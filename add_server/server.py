import socket


def run_server():
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 12345  # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")

        err = 'we only support "add n1 n2"'.encode()
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)  # Receive up to 1024 bytes
                    if not data:
                        break
                    arr = data.decode().split(' ')
                    print(f"Echoed: {data.decode()}")
                    if len(arr) != 3:
                        conn.sendall(err)
                        continue
                    add, n1, n2 = arr
                    if add != "add":
                        conn.sendall(err)
                    try:
                        n3 = int(n1) + int(n2)
                        conn.sendall(f'sum is {n3}'.encode())
                    except ValueError:
                        conn.sendall(err)


if __name__ == '__main__':
    run_server()
