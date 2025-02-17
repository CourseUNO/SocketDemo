import socket
import threading

# Server settings
SERVER_IP = '127.0.0.1'  # Change to the actual server IP if needed
SERVER_PORT = 12345

# Create UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send an initial message to join the chat
client_socket.sendto("New client joined!".encode(), (SERVER_IP, SERVER_PORT))


def receive_messages():
    """Thread to receive messages from the server."""
    while True:
        try:
            data, _ = client_socket.recvfrom(1024)
            print(f"\n[Chat] {data.decode()}\n> ", end="")
        except:
            break


# Start receiving messages in a separate thread
threading.Thread(target=receive_messages, daemon=True).start()

print(f"Connected to UDP Chat Server at {SERVER_IP}:{SERVER_PORT}")

while True:
    message = input("> ")

    if message.lower() == 'exit':
        print("Leaving chat...")
        break

    # Send message to the server
    client_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

client_socket.close()
