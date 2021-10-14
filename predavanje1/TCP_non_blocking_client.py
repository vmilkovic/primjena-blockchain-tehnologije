import socket
import selectors
import types
import socket
import sys

sel = selectors.DefaultSelector()

HOST = '127.0.0.1'
PORT = 5050

messages = [b'Message 1 from client.', b'Message 2 from client.']

broj_veza = 10
brojac = broj_veza


def start_connections(host, port, num_conns):
    global brojac
    limit = 55425
    server_addr = (host, port)
    for i in range(0, num_conns):
        connid = i + 1
        print('starting connection', connid, 'to', server_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        # event_read vraća 1, event_write vraća 2, a ovako zajedno vraćaju 3 (ili na binarnoj razini)
        dataVAR = types.SimpleNamespace(connid=connid, msg_total=sum(
            len(m) for m in messages), recv_total=0, messages=list(messages), outb=b'')
        sel.register(sock, events, data=dataVAR)

    while True:
        limit -= 1
        if not brojac == 0:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    pass
                else:
                    service_connection(key, mask)
            if limit == 0:
                print('Dosegnut limit')
                break
        else:
            break


def service_connection(key, mask):
    global brojac
    sock = key.fileobj
    dataSC = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            print('received', repr(recv_data),
                  'from connection', dataSC.connid)
            dataSC.recv_total += len(recv_data)
        if not recv_data or dataSC.recv_total == dataSC.msg_total:
            print('closing connection', dataSC.connid)
            sel.unregister(sock)
            sock.close()
            brojac -= 1
    if mask & selectors.EVENT_WRITE:
        if not dataSC.outb and dataSC.messages:
            dataSC.outb = dataSC.messages.pop(0)
        if dataSC.outb:
            print('sending', repr(dataSC.outb), 'to connection', dataSC.connid)
            sent = sock.send(dataSC.outb)  # Should be ready to write
            dataSC.outb = dataSC.outb[sent:]


start_connections(HOST, PORT, broj_veza)
