import socket
import threading
import time

host='localhost'
port=22244

def veza(co,ad,tr):
    with co:
        print('Thread',tr,' - Connected by', addr)
        while True:
            data = co.recv(1024)
            print("Primio thread",tr,data)
            co.sendall(data)
            print("Poslao thread",tr,data)
            if data[len(data)-4:]==b'KRAJ':
                print('Završi thread',tr)
                break
            # time.sleep(4)
tlista=[]
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    while True:
        conn, addr=s.accept()
        print('acceptedconnectionfrom', addr)
        tlista.append(threading.Thread(target=veza, args=(conn,addr,len(tlista)+1,)))
        tlista[len(tlista)-1].start()
