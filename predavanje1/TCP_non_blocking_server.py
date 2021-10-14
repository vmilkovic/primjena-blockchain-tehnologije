import socket
from time import sleep
import selectors
import types

HOST = '127.0.0.1'
PORT = 5050

sel = selectors.DefaultSelector()


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print('accept_wrapper')
    print('accepted connetion from', addr)
    # conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    print('service_connection_ulaz')
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
            print('service_connection_primanje')
            print(data.outb)
        else:
            print('service_connection_prekid')
            print('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print('service_connection_slanje')
            print('echoing', repr(data.outb), 'to', data.addr)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print('listening on', (HOST, PORT))
    # s.setblocking(False)
    sel.register(s, selectors.EVENT_READ, data=None)

    while True:
        print('loop1')
        events = sel.select(timeout=None)
        for key, mask in events:
            print('loop2')
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
