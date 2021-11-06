import rpyc

genesis_block=["aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"\
               ,"00000:PRVI:BLOK:0","00000:PR:VI:0","00000:BL:OK:0","0"]

#lista sa spremljenim blokchainom
#svaki blok je string u obliku [broj_bloka#hash_bloka#transakcije_i_hash_prošlog_bloka]
blokovi=["0#945b382a5a7a29bd44780fe975c6d996d4ec9e13285dad60cc1151d0044e48f6"+'#'.join(genesis_block)]

mempool=["00001:Marko:Ivan:456","00002:Marko:Ivan:22","00003:Marko:Ivan:764","00004:Marko:Ivan:12"  \
         ,"00005:Marko:Ivan:357","00006:Marko:Ivan:562","00007:Marko:Ivan:11","00008:Marko:Ivan:94" \
         ,"00009:Marko:Ivan:911","00010:Marko:Ivan:733","00011:Marko:Ivan:879","00012:Marko:Ivan:854" \
         ,"00013:Marko:Ivan:220","00014:Marko:Ivan:2","00015:Marko:Ivan:354","00016:Marko:Ivan:213" \
         ,"00017:Marko:Ivan:238","00018:Marko:Ivan:87","00019:Marko:Ivan:34","00020:Marko:Ivan:564"]

counter=21

#pomoćna funkcija - popunjava brojač s vodećim nulama do ukupno 5 znakova
def expand(broj):
    for i in range(5,len(broj),-1):
        broj="0"+broj
    return broj    

class MyService(rpyc.Service):
    def on_connect(self, conn):
        pass

    def on_disconnect(self, conn):
        global blokovi
        print(blokovi)

    def exposed_chain_get(self):
        global blokovi
        return blokovi
    
    def exposed_chain_add(self,br_bloka,hash_bloka,blok):
        global blokovi
        blokovi.append(str(br_bloka)+"#"+hash_bloka+'#'+'#'.join(blok))

    def exposed_get_mem(self):
        global mempool
        return mempool

    def exposed_mem_remove(self,ID):
        global mempool
        for tx in mempool:
            if ID==tx[:5]:
                mempool.remove(tx)
    def exposed_mem_add(self,From,To,Amount):
        global mempool
        global counter
        tr=expand(str(counter))+":"+From+":"+To+":"+str(Amount)
        mempool.append(tr)
        counter+=1
        

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(MyService, port=35222)
    t.start()
