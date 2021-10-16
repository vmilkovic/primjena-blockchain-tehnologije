import socket

HOST = '127.0.0.1'
PORT = 6444

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    while True:
        data, address = s.recvfrom(1024)
        print(data.decode())
        s.sendto(data, address)
