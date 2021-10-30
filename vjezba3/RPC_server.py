import rpyc

class RPCService(rpyc.Service):
    server_vlasnik = 'Vedran'
    conn_count = 0

    def on_connect(self, conn):
        print("Start")

    def on_disconnect(self, conn):
        print("End")

    def exposed_vlasnik(self):
        self.conn_count = self.conn_count + 1
        return self.server_vlasnik

    def exposed_promet(self):
        self.conn_count = self.conn_count + 1
        return self.conn_count


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(RPCService, port=25555)
    t.start()
    input()
