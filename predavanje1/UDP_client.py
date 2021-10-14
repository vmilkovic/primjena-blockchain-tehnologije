import socket  # socket module
from time import sleep

HOST = '127.0.0.1'  # The sever's hostname or IP address
PORT = 5000  # The port used by the server

poruka = input("unesi: ")
poruka = poruka.encode()

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    # s.sendto(b'Hello, world', (HOST, PORT))
    s.sendto(poruka, (HOST, PORT))
    # sleep(2)
    data = s.recv(1024)
    print('Received', data)
    data = s.recv(1024)
    print('Received', data)
