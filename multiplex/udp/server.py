import socket

# Server settings
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 12345       # Port to listen on

# Create UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

# Store client addresses
clients = set()

print(f"UDP Chat Server started on {HOST}:{PORT}")

while True:
    # Receive message from any client
    data, client_address = server_socket.recvfrom(1024)
    message = f'{client_address} says: {data.decode()}'

    # Add new clients
    if client_address not in clients:
        clients.add(client_address)
        print(f"New client joined: {client_address}")

    # Broadcast message to all clients
    print(f"Broadcasting: {message} from {client_address}")
    for client in clients:
        if client != client_address:  # Don't send message back to sender
            server_socket.sendto(message.encode(), client)
