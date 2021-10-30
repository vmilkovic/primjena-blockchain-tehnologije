import socket 
import time
import threading
import random

HOST = '127.0.0.1' # The server's hostname or IP address 
PORT = 63455 # The port used by the server

server_addr = (HOST,PORT)
messages = [b'Message 1 from client.', b'Message 2 from client.',b'Message 3 from client.',b'KRAJ']

def spoji(tid):
        print('contacting', server_addr)
        sock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        time.sleep(random.randint(1,2))       
        print('sending', messages[0], 'to connection', server_addr, ' from thread: ', tid)
        sock.sendto(messages[0],(HOST,PORT))
        time.sleep(random.randint(1,2))
        print('sending', messages[1], 'to connection', server_addr, ' from thread: ', tid)
        sock.sendto(messages[1],(HOST,PORT))
        time.sleep(random.randint(1,2))
        print('sending', messages[2], 'to connection', server_addr, ' from thread: ', tid)
        sock.sendto(messages[2],(HOST,PORT))
        time.sleep(random.randint(1,2))
        print('sending', messages[3], 'to connection', server_addr, ' from thread: ', tid)
        sock.sendto(messages[3],(HOST,PORT))

        while True:
                recv_data = sock.recv(1024)  # Shouldbereadyto read
                if recv_data:
                        print('received', repr(recv_data), 'to thread ', tid)
                if recv_data[len(recv_data)-4:]==b'KRAJ':
                        print('Završi thread',tid)
                        break

brojac=0
tlista=[]
while brojac < 3:
        tlista.append(threading.Thread(target=spoji, args=(brojac,)))
        tlista[len(tlista)-1].start()
        brojac+=1
