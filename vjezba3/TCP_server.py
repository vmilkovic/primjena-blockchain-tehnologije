import socket  #uvoz modula socket
import threading

HOST = '127.0.0.1'    # varijabla s pridruženom IP adresom (localhost) 
PORT = 22244	      # varijabla s pridruženim mrežnim portom

threads = []

def veza(co, ad, tr):
    print('Thread', tr, ' - Connected by', ad)
    with co:
        while True:
            data = co.recv(1024)
            co.sendall(data)
            if data[len(data)-4:] == b'KRAJ':
                break

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        threads.append(threading.Thread(
            target=veza, args=(conn, addr, len(threads)+1)))
        threads[len(threads)-1].start()
