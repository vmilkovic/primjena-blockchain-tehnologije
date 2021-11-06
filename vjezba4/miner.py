import rpyc
import hashlib
import random
import time

popis=[]
br_blokova=0
br_hasheva=0

c = rpyc.connect('localhost', 35222)

mempool=c.root.get_mem()
chain=c.root.chain_get()

print("Mining started")
ts_p = time.time()

#dvostruka petlja:
#glavna u svakoj iteraciji stvori jedan blok
#unutarnja radi permutacije transakcija,prethodnog hasha i nonce-a kako bi dobila
#ispravan hash novog bloka
while True:
    ts_pocetak_stvranja_bloka = time.time()

    while True:
        nonce=random.randint(0,99999)
        blokovi=list(chain).copy()

        #u popis se dodaju elementi potencijalnog novog bloka
        popis.append(blokovi[len(blokovi)-1][2:67])
        tri_stavke=random.sample(mempool, 3)
        popis.extend(tri_stavke)
        popis.append(str(nonce))
        #novi blok se iz liste "popis" pretvara u string
        string=''.join(popis)

        #računa se hash tog bloka (spremljenog u varijablu string)
        encoded=string.encode()
        result=hashlib.sha256(encoded)
        hash_bloka=result.hexdigest()

        br_hasheva+=1

        if hash_bloka[0:4]=='0000':
            blok=popis.copy()
            print("Pronađen hash: ", hash_bloka)
            print(f"Trajanje stvaranja: {time.time()-ts_pocetak_stvranja_bloka:0.2f} sekundi")
            print("Broj hasheva: ", br_hasheva)
            br_hasheva=0
            br_blokova+=1
            #Dodajemo blok u postojeći blockchain
            c.root.chain_add(br_blokova,hash_bloka,blok)
            #Transakcije koje su uključene u blok uklanjamo iz mempool-a
            c.root.mem_remove(blok[1][0:5])
            c.root.mem_remove(blok[2][0:5])
            c.root.mem_remove(blok[3][0:5])
            popis.clear()
            break

        popis.clear()

    if br_blokova==7:
        c.close()
        break
    
ts_k = time.time()

#ukupno trajanje Mininga
print(f"Proteklo: {ts_k-ts_p:0.2f} sekundi")



