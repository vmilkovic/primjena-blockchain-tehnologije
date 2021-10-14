import socket
import threading
import time

HOST = 'localhost'
PORT = 6000

tlista = []


def veza(co, ad, tr):
    with co:
        print('Thread', tr, ' - Connected by', addr)
        while True:
            data = co.recv(1024)
            print("Primio thread", tr, data)
            co.sendall(data)
            print("Poslao thread", tr, data)
            if data[len(data)-4:] == b'KRAJ':
                print('Završi thread', tr)
                break
            time.sleep(3)


while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        print('accepted connection from', addr)
        tlista.append(threading.Thread(
            target=veza, args=(conn, addr, len(tlista)+1)))
        tlista[len(tlista)-1].start()
