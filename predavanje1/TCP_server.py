import socket  # uvoz modula socket
from time import sleep

HOST = '127.0.0.1'  # varijabla s pridruženom IP adresom (localhost)
PORT = 4000  # varijabla s pridruženim mrežnim portom

# TCP echo server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            print("Server1", data)
            if not data:
                break
            conn.sendall(data)
            print("Server2", data)
