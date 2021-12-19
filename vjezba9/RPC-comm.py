from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import json

# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_user, rpc_password = "user", "password"

rpc_conn = AuthServiceProxy(
    "http://%s:%s@127.0.0.1:18370/wallet/Milkovic" % (rpc_user, rpc_password))

last_transaction = rpc_conn.listunspent()[0]
transaction_id = last_transaction['txid']
transaction = rpc_conn.gettransaction(transaction_id)
transaction_hex = transaction['hex']
decoded_transaction_hex = rpc_conn.decoderawtransaction(transaction_hex)
return_data = decoded_transaction_hex['vout'][1]['scriptPubKey']['asm']
hex_data = return_data.replace('OP_RETURN ', '')
decoded_data = bytes.fromhex(hex_data).decode('utf-8')
print(decoded_data)

name = input('Unesite vaše ime: ')
hex_name = name.encode('utf-8').hex()
transactions = rpc_conn.listunspent()
for transaction in transactions:
    if transaction['amount'] > 0.01:
        transaction_txid = transaction['txid']
        transaction_vout = transaction['vout']
        address = [{'txid': transaction_txid,
                    'vout': transaction_vout}]
        data = [{'data': hex_name}]
        new_transaction_hex = rpc_conn.createrawtransaction(address, data)
        rpc_conn.walletpassphrase("1234", 3600)
        funded_raw_transaction = rpc_conn.fundrawtransaction(
            new_transaction_hex)
        sign_raw_transaction = rpc_conn.signrawtransactionwithwallet(
            funded_raw_transaction['hex'])
        send_raw_transaction = rpc_conn.sendrawtransaction(
            sign_raw_transaction['hex'])
        print(send_raw_transaction)
