import socket
import threading

# Server settings
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 12345  # Port to listen on

# Store active clients
clients = {}


def broadcast_message(message, sender_socket):
    """Send a message to all clients except the sender."""
    for client_socket in clients.values():
        if client_socket != sender_socket:
            try:
                client_socket.sendall(message.encode())
            except:
                pass  # Ignore errors (client may have disconnected)


def handle_client(client_socket, client_address):
    """Handle incoming messages from a client."""
    print(f"New connection from {client_address}")

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break  # Client disconnected

            # Prepend message with client address
            formatted_message = f"[{client_address}] {message}"
            print(formatted_message)  # Print on server side

            # Broadcast to all clients
            broadcast_message(formatted_message, client_socket)
        except:
            break  # Handle disconnection

    # Remove client from list and close connection
    print(f"Client {client_address} disconnected")
    del clients[client_address]
    client_socket.close()


# Create server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)  # Allow up to 5 pending connections

print(f"TCP Chat Server started on {HOST}:{PORT}")

while True:
    client_socket, client_address = server_socket.accept()
    clients[client_address] = client_socket
    threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()
