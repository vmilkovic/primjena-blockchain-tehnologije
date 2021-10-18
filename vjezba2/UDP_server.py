import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind(("localhost", 7000))
    while True:
        data, address = s.recvfrom(1024)
        print(data.decode())
        s.sendto(data, ("localhost", 6000))
