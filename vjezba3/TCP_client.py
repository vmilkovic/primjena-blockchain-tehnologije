import socket 
import time
import threading
import random

HOST = '127.0.0.1' # The server's hostname or IP address 
PORT = 22244 # The port used by the server

server_addr = (HOST,PORT)
messages = [b'Message 1 from client.', b'Message 2 from client.',b'Message 3 from client.',b'KRAJ']

def spoji(tid):
    print('starting connection to', server_addr)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    time.sleep(tid)
    sock.connect_ex(server_addr)
    print('Thread', tid, 'otvorio:', sock.getsockname())
    time.sleep(random.randint(1, 2))
    print('sending', messages[0], 'to connection',
          server_addr, ' fromthread: ', tid)
    sock.send(messages[0])
    time.sleep(random.randint(1, 2))
    print('sending', messages[1], 'to connection',
          server_addr, ' fromthread: ', tid)
    sock.send(messages[1])
    time.sleep(random.randint(1, 2))
    print('sending', messages[2], 'to connection',
          server_addr, ' fromthread: ', tid)
    sock.send(messages[2])
    time.sleep(random.randint(1, 2))
    print('sending', messages[3], 'to connection',
          server_addr, ' fromthread: ', tid)
    sock.send(messages[3])
    while True:
        recv_data = sock.recv(1024)  # Shouldbereadytoread
        if recv_data:
            print('received', repr(recv_data), 'to thread', tid)
        if recv_data[len(recv_data)-4:] == b'KRAJ':
            print('Završi thread', tid)
            break


brojac = 1
tlista = []
while brojac < 3:
    tlista.append(threading.Thread(target=spoji, args=(brojac,)))
    tlista[len(tlista)-1].start()
    brojac += 1
