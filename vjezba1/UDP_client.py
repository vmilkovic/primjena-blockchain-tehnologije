import socket

HOST = '127.0.0.1'
PORT = 6444

poruka = input("unesi: ")
poruka = poruka.encode()

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.sendto(poruka, (HOST, PORT))
    data = s.recv(1024)
    print('Received from server ', data)
