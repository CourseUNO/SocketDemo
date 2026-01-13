

###
#   Hailey Gillespie
#   Project 1 - CSCI3550
###


import os
import socket
import sys

receiver = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('ICMP'))
sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host = socket.gethostbyname(socket.gethostname())
receiver.bind((host, 33434))
receiver.setsockopt(socket.IPPROTO_IP, socket.SOCK_RAW, 1)
receiver.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

host = 'google.com'
server_address = socket.gethostbyname(host)
print(f"tracing to {server_address}")

try:
    # set to arbitrary max of 10 hops
    for ttl in range(1, 11):
        sender.setsockopt(socket.SOL_SOCKET, socket.IP_TTL, ttl)
        sent = sender.sendto(b"", (server_address, 33434))
        data, addr = receiver.recvfrom(512)
        print(f"received {len(data)} bytes from {addr[0]}")
except:
    print("exception")
finally:
    print('closing socket')
    sender.close()
    receiver.close()