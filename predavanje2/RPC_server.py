import rpyc
import random


class MyService(rpyc.Service):
    def on_connect(self, conn):
        print("Početak")

    def on_disconnect(self, conn):
        print("Završetak")

    def vrati_random(self):
        return random.randint(1, 10)

    def exposed_vrati_izracun(sef, var):
        return 55 + var

    exposed_kontrolna_vrijednost = 43


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(MyService, port=25555)
    t.start()
    # input()
