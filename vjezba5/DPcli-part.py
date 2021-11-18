import rpyc
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

#############
## KLIJENT ##
#############

def generiraj_kljuceve():
    key = RSA.generate(2048)
    #stvaranje i spremanje privatnog ključa u datoteku
    file_out = open("private_key.pem", "wb")
    file_out.write(key.export_key())
    file_out.close()
    #stvaranje i spremanje javnog ključa u datoteku
    file_out = open("public_key.pem", "wb")
    file_out.write(key.publickey().export_key())
    file_out.close()
    return True

flag = True
try:
    #klijent iz prethodno stvorenih datoteka učitava svoj javni i privatni ključ
    prKey = RSA.import_key(open('private_key.pem').read())
    puKey = RSA.import_key(open('public_key.pem').read())
except FileNotFoundError:
    #ukoliko datoteke s ključevima nisu pronađene, ide se u stvaranje novih
    print("Nije pronađena adresa pridružena klijentu!")
    odabir = input("Generirati novu adresu?[D/N]: ")
    odabir = odabir.lower() 
    if odabir == 'd':
        if generiraj_kljuceve():
            print("Stvaranje ključeva uspjelo")
            prKey = RSA.import_key(open('private_key.pem').read())
            puKey = RSA.import_key(open('public_key.pem').read())
    else:
        print('Prekid programa!')
        flag=False    

if flag:
    c = rpyc.connect("127.0.0.1", 25555)
    #nakon povezivanja sa serverom, ide se u petlju korisničnog sučelja
    while True:
        opcija = int(input(
        """ 1-Pošaljite transakciju na odabranu adresu
        2-Provjerite stanje svoje adrese
        3-Provjerite stanje tuđe adrese
        4-Prijavi svoju adresu na mrežu
        5-Odustani
        Odabir[1-5]: """))

        if opcija == 1:
            ###############################################
            #implementirati unos odredišne adrese i iznosa#
            #-> korisnika se pita da unese ta 2 podatka   #
            ###############################################
            adresa_primatelja = input('Unesite adresu primatelja: ')
            iznos = input('Unesite iznos transakcije: ')

            #message sadrži string s informacijama o transakciji u obliku:
            #adresa_pošiljatelja#adresa_primatelja#iznos
            #znak # je graničnik između pojedinih vrijednosti
            adresa_posiljatelja = str(puKey.n)

            ##################################################################
            #sastaviti string koji će se poslati serveru prema gornjem opisu #
            #spremiti ga u varijablu message                                 #
            ##################################################################
            message = '#'.join([adresa_primatelja, adresa_posiljatelja, iznos])
            #hakirani sustav
            #message = '#'.join([adresa_primatelja, adresa_posiljatelja, iznos])
            
            #prije izrade signature-a moramo regularan string pretvoriti u byte string
            message = message.encode()

            #izrađujemo hash kod poruke
            h = SHA256.new(message)

            #hash kod kriptiramo privatnim ključem klijenta i tako dobijemo signature.
            #server može dekriptirati signature pomoću javnog ključa klijenta i tako dobiti hash kod iz njega
            #server može odrediti javni ključ klijenta na temelju njegove adrese
            signature = pkcs1_15.new(prKey).sign(h)
            
            print(c.root.transakcija(message,signature))
            #gornja linija je slanje transakcije sa dig. potpisom dok je donja bez potpisa
            ##print(c.root.transakcija(message))
        elif opcija == 2:
            print('Adresa: ')
            print(str(puKey.n))
            print('Stanje: ')
            #šaljemo adresu klijenta
            #adresa se iz javnog ključa uzima pozivom atributa n
            #adresa se vraća kao integer pa ga treba pretvoriti u string
            print(c.root.provjeri_adresu(str(puKey.n)))
        elif opcija == 3:
            add = str(input('Unesi adresu za provjeru: '))
            print('Stanje: ')
            print(c.root.provjeri_adresu(add))
        elif opcija == 4:
            print(c.root.registriraj_adresu(str(puKey.n)))
        else:
            break

