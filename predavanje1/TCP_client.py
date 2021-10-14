import socket  # uvoz modula socket
from time import sleep

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 4000  # The port used by the server

# TCP echo client
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    s.sendall(b'Drugi red')
    sleep(4)
    s.sendall(b'Treci red (nakon cekanja)')
    # sleep(1)
    data = s.recv(1024)
    print('Received', data)
    # sleep(10)
    #s.sendall(b'4 red')
    # data = s.recv(1024)
    # print('Received', data)
