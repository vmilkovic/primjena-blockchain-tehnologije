import socket  # uvoz modula socket
# from datetime import datetime
from time import sleep

HOST = '127.0.0.1'  # varijabla s pridruženom IP adresom (localhost)
PORT = 5000  # varijabla s pridruženim mrežnim portom

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    while True:
        data, address = s.recvfrom(1024)
        print(address)
        print(data)
        print(data.decode())
        sleep(6)
        s.sendto(data, address)
        s.sendto(b'Auto', address)

        # vrijeme=datetime.now()
        # print(vrijeme)
        #s.sendto(b'Auto'+str(vrijeme).encode(), address)
