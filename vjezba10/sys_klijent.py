from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_user, rpc_password = "user", "password"

# odradi_trans je funkcija koja dobiva parametre potrebne da se stvori i pošalje nova transakcija pomoću
# metoda createrawtransaction, fundrawtransaction, signrawtransactionwithwallet i sendrawtransaction
# navedena funkcija je potrebna kako bi se odradila 5. radnja (Pošalji transakciju)

# string,int,string,float


def odradi_trans(txid, vout, adresa, izn):
    # pass zamijeniti sa željenim programskim kodom (poslužite se primjerom na 19. slajdu iz 5. predavanja)
    wallet = [{'txid': txid,
               'vout': vout}]
    data = [{adresa: izn}]
    new_transaction_hex = rpc_conn.createrawtransaction(
        wallet, data)
    funded_raw_transaction = rpc_conn.fundrawtransaction(
        new_transaction_hex)
    sign_raw_transaction = rpc_conn.signrawtransactionwithwallet(
        funded_raw_transaction['hex'])
    return rpc_conn.sendrawtransaction(
        sign_raw_transaction['hex'])


# ovu funkciju koristiti ćemo za upis stringa na blockchain
# u odnosu na prethodnu funkciju razlika je samo u izgledu metode createrawtransaction
def upisi_podatak(txid, vout, tekst):
    # prevorba običnog teksta u heksadecimalni oblik
    hexstr = tekst.encode('utf-8').hex()
    address = [{'txid': txid,
                'vout': vout}]
    data = [{'data': hexstr}]
    new_transaction_hex = rpc_conn.createrawtransaction(
        address, data)
    funded_raw_transaction = rpc_conn.fundrawtransaction(
        new_transaction_hex)
    sign_raw_transaction = rpc_conn.signrawtransactionwithwallet(
        funded_raw_transaction['hex'])
    return rpc_conn.sendrawtransaction(
        sign_raw_transaction['hex'])


while True:
    rpc_conn = AuthServiceProxy(
        "http://%s:%s@127.0.0.1:18370/wallet/Milkovic" % (rpc_user, rpc_password))

    izbor = int(input('''Odaberite radnju:
            1 - Otključaj novčanik
            2 - Zaključaj novčanik
            3 - Prikaži adrese i stanja
            4 - Stvori novu adresu
            5 - Pošalji transakciju
            6 - Upiši string u bchain
            7 - Dohvati string s bchaina
            8 - Izađi iz aplikacije
            Odabir[1-8]: '''))

    if izbor == 1:
        lozinka = input("Unesi lozinku: ")
        sekunde = int(input("Broj sekundi za otključavanje: "))
        rpc_conn.walletpassphrase(lozinka, sekunde)
        print('Wallet otključan na', str(sekunde), 'sekundi')

    elif izbor == 2:
        rpc_conn.walletlock()
        print('Wallet zaključan!')

    elif izbor == 3:
        popis = rpc_conn.listunspent()
        for i in popis:
            print('*'*40)
            print('Adresa: ', i['address'])
            print('Iznos: ', i['amount'])
        print('*'*40)

    elif izbor == 4:
        new_address = rpc_conn.getnewaddress()
        print('Nova adresa:', new_address)

    elif izbor == 5:
        print('Nova transakcija!!')
        ad = input('Unesi odredišnu adresu(bez navodnika): ')
        iz = float(input('Unesi iznos za transakciju: '))
        popis = rpc_conn.listunspent()
        for i in popis:
            if i['amount'] > 0.001:  # provjera da li ima sredstava za plaćanje naknade
                transaction_txid = i['txid']
                transaction_vout = i['vout']
                id = odradi_trans(transaction_txid, transaction_vout, ad, iz)
                print("Upis uspješan, ID: ", id)
                break

    elif izbor == 6:
        tekst = input('Unesi tekst za upis: ')
        popis = rpc_conn.listunspent()
        print(popis)
        for i in popis:
            if i['amount'] > 0.001:  # provjera da li ima sredstava za plaćanje naknade
                transaction_txid = i['txid']
                transaction_vout = i['vout']
                id = upisi_podatak(transaction_txid, transaction_vout, tekst)
                print("Upis uspješan, ID: ", id)
                break

    elif izbor == 7:
        txid = input('Unesi txid podatka za dohvat: ')
        transakcija = rpc_conn.gettransaction(txid)
        heks = transakcija['hex']
        transakcija2 = rpc_conn.decoderawtransaction(heks)
        heks = transakcija2['vout'][0]['scriptPubKey']['asm']
        heks_string = heks[10:]
        tekst = bytes.fromhex(heks_string).decode('utf-8')
        print('Dohvaćeni tekst: ', tekst)

    elif izbor == 8:
        break

    del rpc_conn
