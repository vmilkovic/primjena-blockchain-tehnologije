import socket

HOST = '127.0.0.1'
PORT = 63444

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print("Before send ->", data)
                conn.sendall(data)
                print(" After send ->", data)

    odgovor = input("Nastaviti izvođenje?[D/N]; ")
    if(odgovor == "N"):
        break
