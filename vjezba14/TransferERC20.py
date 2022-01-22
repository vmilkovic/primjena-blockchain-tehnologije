from web3 import Web3
import json

# Fill in your infura API key here
infura_url = "https://rinkeby.infura.io/v3/2c2b5a1b21ba4fe98ff06ee6662b6f52"
web3 = Web3(Web3.HTTPProvider(infura_url))

adr_novcanika, priv_kljuc, adr_ugovora, ime_tokena, abi = '', '', '', '', ''

# U ovoj datoteci ne treba ništa dirati u source kodu osim funkcionalnosti
# slanja pri kraju ove datoteke


try:
    dat = open('adresa.txt', 'r')
    adr_novcanika = dat.readline()
    adr_novcanika = adr_novcanika[:42]
    priv_kljuc = dat.readline()
    priv_kljuc = priv_kljuc[:64]
    dat.close()
    dat = open('token.txt', 'r')
    adr_ugovora = dat.readline()
    adr_ugovora = adr_ugovora[:len(adr_ugovora)-1]
    ime_tokena = dat.readline()
    ime_tokena = ime_tokena[:len(ime_tokena)-1]
    abi_str = dat.read()
    abi = json.loads(abi_str)
    dat.close()
except:
    print('Datoteka s adresom ili ugovorom ne postoji!')


def unesi_adresu():
    global adr_novcanika
    global priv_kljuc
    adr_novcanika = str(
        input('Unesi adresu novčanika (q za izlaz iz programa): '))
    if adr_novcanika == 'q':
        return 'q'
    priv_kljuc = str(input('Unesi priv. kljuc (q za izlaz iz programa): '))
    if priv_kljuc == 'q':
        return 'q'
    if len(adr_novcanika) == 42 and len(priv_kljuc) == 64:
        dat = open('adresa.txt', 'w')
        dat.write(adr_novcanika+'\n')
        dat.write(priv_kljuc)
        dat.close()


def dodaj_token():
    global adr_ugovora
    global abi
    global ime_tokena
    adr_ugovora = str(
        input('Unesi adresu ugovora s tokenom (q za izlaz iz programa): '))
    if adr_ugovora == 'q':
        return 'q'
    # abi = str(input('Unesi abi ugovora (q za izlaz iz programa): '))
    print('Unesi abi ugovora (nakon što ga zalijepite, stisnite ENTER, te nakon toga CTRL+D): ')
    while True:
        if abi == 'q':
            break
        try:
            line = input()
        except EOFError:
            break
        abi += line
    if abi == 'q':
        return 'q'
    ime_tokena = str(input('Unesi ime tokena: '))
    if len(adr_ugovora) == 42 and len(ime_tokena) > 0 and len(abi) > 0:
        dat = open('token.txt', 'w')
        dat.write(adr_ugovora+'\n'+ime_tokena+'\n'+str(abi))
        dat.close()


while len(adr_novcanika) < 42:
    if (unesi_adresu() == 'q'):
        break

while True:
    if adr_novcanika == 'q' or priv_kljuc == 'q':
        break
    broj = int(input('''
    1-Prikaži adresu i stanje novčanika
    2-Napravi transakciju tokena
    3-Dodaj token
    4-Promijeni adresu novčanika
    5-Izlaz
    Unesi odabir: '''))

    if broj == 1:
        odabir = int(input('''
        1-Adresa ovog novčanika
        2-Unos druge adrese
        Unesi odabir: '''))
        if odabir == 1:
            addr = adr_novcanika
        if odabir == 2:
            addr = str(input('Unesi adresu za provjeru: '))
        balance = web3.eth.getBalance(addr)
        print(addr + ' --> ' + str(web3.fromWei(balance, "ether")) + ' ETH')
        contract = web3.eth.contract(address=adr_ugovora, abi=abi)
        iznos_tokena = contract.functions.balanceOf(addr).call()
        print(ime_tokena+': '+str(iznos_tokena))
    if broj == 2:
        contract = web3.eth.contract(address=adr_ugovora, abi=abi)
        iznos_tokena = contract.functions.balanceOf(adr_novcanika).call()
        print(ime_tokena+': '+str(iznos_tokena))
        adr_odrediste = str(
            input('Unesi adresu primatelja (q za izlaz iz programa): '))
        if adr_odrediste == 'q':
            break
        iznos = int(input('Unesi iznos za transfer (0 za prekid): '))
        if iznos > iznos_tokena:
            print('Nedovoljan iznos na računu!')
            iznos = 0
        if len(adr_odrediste) == 42 and iznos != 0 and len(priv_kljuc) == 64:
            ###################################################
            ### OVDJE IMPLEMENTIRAJTE FUNKCIONALNOST SLANJA ###
            ###################################################
            nonce = web3.eth.getTransactionCount(adr_novcanika)
            transaction = contract.functions.transfer(adr_odrediste, iznos).buildTransaction({
                'gas': 2000000,
                'gasPrice': web3.toWei('10', 'gwei'),
                'from': adr_novcanika,
                'nonce': nonce
            })
            signed_txn = web3.eth.adr_novcanika.signTransaction(
                transaction, private_key=priv_kljuc)
            web3.eth.sendRawTransaction(signed_txn.rawTransaction)
            print('Poslano!')
    if broj == 3:
        if (dodaj_token() == 'q'):
            break
    if broj == 4:
        if (unesi_adresu() == 'q'):
            break
    if broj == 5:
        break
