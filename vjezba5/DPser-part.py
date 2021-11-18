import rpyc
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

#############
## SERVER  ##
#############

#dictionary 'popis' s adresama i stanjima uz njih
#Primjer dvije adrese (u bitno skraćenom obliku zbog preglednosti) ...
#... kojima je pridruženo stanje 6.0 odnosno 4.0:
#{'242263147508167995681': 6.0, '761501431346415241697': 4.0}
popis={}

class MyService(rpyc.Service):
    def on_connect(self, conn):
        pass
    def on_disconnect(self, conn):
        pass

    #provjerava da li u rječniku popis postoji adresa
    def exposed_provjeri_adresu(self,adresa):
        if adresa not in popis:
            return "Adresa ne postoji"
        else:
            return popis[adresa]

    #u rječnik dodaje adresu koju je dojavio klijent i postavlja joj stanje u 5.0
    #svaka nova adresa dobije 5.00 tokena uz sebe
    def exposed_registriraj_adresu(self,adresa):
        if adresa not in popis:
            popis[adresa]=5.00
            print(popis)
            return "Adresa registrirana"
        else:
            return "Adresa već postoji"

    #exposed_transakcija je funkcija koju klijent poziva ukoliko želi transakciju sa svoje adrese na neku drugu
    #message je byte string u formatu:  b'adresa_pošiljatelja#adresa_primatelja#iznos'
    #signature je hash kod kodiran s privatnim ključem klijenta. hash kod je ...
    #...napravljen na strani klijenta na temelju sadržaja varijable message

    def exposed_transakcija(self,message,signature):
    #def exposed_transakcija(self,message):
        h = SHA256.new(message) #radimo hash kod na strani servera - hash se radi na temelju ...
        #... primljene poruke message

        message=message.decode() #od primljenog byte stringa radimo regularan string
        message_list = message.split("#") #string cjepkamo u listu na temelju graničnika #

        #na temelju adrese klijenta koja se sada nalazi u message_list[0], sastavljamo ...
        #...javni ključ klijenta kako bi pomoću njega dekodirali signature i izvukli hash
        puKey=RSA.construct((int(message_list[0]),65537),True) #sastavljanje javnog ključa klijenta na temelju adrese klijenta
        #javni ključ nam je potreban za dekodiranje signaturea -> dekodiranjem iz signature-a dobijemo ...
        #... hash kod koji je klijent izračunao prilikom slanja svoje poruke
        
        try:
            #uspoređujemo hash koji smo stvorili na serveru (h) sa hashom primljenim unutar signature-a.
            #pri tom moramo priložiti public key klijenta za dekodiranje njegovog signature-a.
            pkcs1_15.new(puKey).verify(h, signature)
        except (ValueError, TypeError):
            return "Digitalni potpis nije ispravan"

        #ukoliko je provjera potpisa prošla pozitivno, ide se na provjeru postojanja adresa i promjenu iznosa uz njih
        adrPos=message_list[0]
        adrPri=message_list[1]
        if adrPos not in popis:
            return "Adresa pošiljatelja ne postoji"
        elif adrPri not in popis:
            return "Adresa primatelja ne postoji"
        else:
            if float(message_list[2]) < 0:
                return "Nisu dozvoljene transakcije s negativnim iznosima"

            if popis[adrPos]-float(message_list[2]) < 0:
                return "Pošiljatelja nema dovoljno srestava za izvršavanje transakcije"

            #pošiljatelju se skida iznos, a primatelju dodaje
            popis[adrPos]=popis[adrPos]-float(message_list[2])
            popis[adrPri]=popis[adrPri]+float(message_list[2])
            return "Transakcija uspješna!"

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(MyService, port=25555)
    t.start()

