import socket
import threading

# Server settings
SERVER_IP = '127.0.0.1'  # Change if running on different machines
SERVER_PORT = 12345

def receive_messages(client_socket):
    """Receive messages from the server."""
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"\n{message}\n> ", end="")
        except:
            break  # Exit on error

# Create client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

# Start receiving messages in a separate thread
threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

print(f"Connected to TCP Chat Server at {SERVER_IP}:{SERVER_PORT}")

while True:
    message = input("> ")

    if message.lower() == 'exit':
        print("Leaving chat...")
        break

    # Send message to the server
    client_socket.sendall(message.encode())

client_socket.close()
