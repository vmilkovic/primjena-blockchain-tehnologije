import socket
import threading

TCP_to_UDP_message = ""
UDP_to_TCP_message = ""
send_to_TCP_client = False


def TCP_server():
    global TCP_to_UDP_message, UDP_to_TCP_message, send_to_TCP_client
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", 5000))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by TCP', addr)
            data = conn.recv(1024)
            data = data.decode()

            if data:
                TCP_to_UDP_message = data

            while True:
                if UDP_to_TCP_message and send_to_TCP_client:
                    UDP_to_TCP_message = "#" + UDP_to_TCP_message + "#"
                    print("Before send UDP message to TCP client",
                          UDP_to_TCP_message)
                    conn.sendall(UDP_to_TCP_message.encode())
                    UDP_to_TCP_message = ""
                    send_to_TCP_client = False
                    break


def UDP_client():
    global TCP_to_UDP_message
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        while True:
            if TCP_to_UDP_message:
                s.sendto(TCP_to_UDP_message.encode(), ("localhost", 6000))


def UDP_server():
    global TCP_to_UDP_message, UDP_to_TCP_message, send_to_TCP_client
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(("localhost", 6000))

        data, address = s.recvfrom(1024)
        data = data.decode()

        if data and not send_to_TCP_client:
            print("Message from UDP server", data)
            UDP_to_TCP_message = "#" + data + "#"
            send_to_TCP_client = True

        while True:
            if TCP_to_UDP_message:
                TCP_to_UDP_message = "#" + TCP_to_UDP_message + "#"
                print("Before send TCP message to UDP server", TCP_to_UDP_message)
                s.sendto(TCP_to_UDP_message.encode(), ("localhost", 7000))
                TCP_to_UDP_message = ""


t1 = threading.Thread(target=TCP_server)
t2 = threading.Thread(target=UDP_server)
t3 = threading.Thread(target=UDP_client)

t1.start()
t2.start()
t3.start()
