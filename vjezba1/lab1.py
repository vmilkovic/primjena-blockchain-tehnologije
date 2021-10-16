import socket
import threading

HOST = ''  # ostaviti prazno kako bi primali poruke s bilo kojeg sučelja
PORT = 55444  # sve aplikacije čekaju poruke na ovom portu

IME = input("Vaše ime: ")

poruka = ""


def primi(HOST_IN, PORT_IN):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # složiti osluškujući port
        s.bind((HOST_IN, PORT_IN))
        # složiti petlju koja neprestano prima podatke i ispisuje ih
        while True:
            data, address = s.recvfrom(1024)
            print(data.decode())
            odgovor = ""
            while not odgovor:
                odgovor = input("Odgovor: ").encode()
                if odgovor:
                    s.sendto(odgovor, address)


def salji(IME):
    global HOST, poruka
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # složiti petlju koja vas traži IP odredišta i Poruku
        # zatim šalje vaše ime i poruku na unesenu IP adresu i port 55444
        while not HOST or not poruka:
            if not HOST:
                HOST = input("IP adresa: ")
            if not poruka:
                poruka = input("Poruka: ")

            if not HOST or not poruka:
                continue

            data = (IME + ": " + poruka).encode()
            s.sendto(data, (HOST, PORT))
            poruka = ""
            odgovor = s.recv(1024)
            print('Odgovor je:', odgovor.decode())


# funkcije primi i šalji pokrećemo kao 2 neovisna threada kako si ne bi međusobno smetale (blokirale) izvođenje
t1 = threading.Thread(target=primi, args=(HOST, PORT,))
t2 = threading.Thread(target=salji, args=(IME,))
t1.start()
t2.start()
