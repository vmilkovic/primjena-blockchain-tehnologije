import socket  #uvoz modula socket

HOST = '127.0.0.1'    # varijabla s pridruženom IP adresom (localhost) 
PORT = 63455	      # varijabla s pridruženim mrežnim portom

listeners = []
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    while True:
        data,addr = s.recvfrom(1024)
        if not data:
            break
        if addr not in listeners:
            listeners.append(addr)
            print("new client added from %s on port %i" % (addr[0],addr[1]))
        for l in listeners:
            try:
                s.sendto(data, l)
            except Exception as e:
                print(e)
            listeners.remove(l)
