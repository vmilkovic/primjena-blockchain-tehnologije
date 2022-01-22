import json
from web3 import Web3

# link na infura servis – navedeni servis koristimo kao pristupnu točku prema ethereum mreži
infura_url = 'https://rinkeby.infura.io/v3/2c2b5a1b21ba4fe98ff06ee6662b6f52'
web3 = Web3(Web3.HTTPProvider(infura_url))
print(web3.isConnected())  # provjera postojanja linka na infura-u
print(web3.eth.blockNumber)  # dohvat broja zadnjeg bloka

account = ''  # unesite adresu iz metamaska
private_key = ''  # metamask private key
balance = web3.eth.getBalance(account)
print(web3.fromWei(balance, "ether"))  # ispisuje stanje računa

# ABI - opis sučelja
abi_json = """[
	{
		"constant": false,
		"inputs": [
			{
				"name": "newMessage",
				"type": "string"
			}
		],
		"name": "setMessage",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "message2",
		"outputs": [
			{
				"name": "",
				"type": "string"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "newMessage",
				"type": "string"
			}
		],
		"name": "setMessage2",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "message",
		"outputs": [
			{
				"name": "",
				"type": "string"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "vrati",
		"outputs": [
			{
				"name": "",
				"type": "string"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "constructor"
	}
]"""
abi = json.loads(abi_json)

address = '0xd8E753B9EfC6f4221F52d0148F4a7C824640134e'  # adresa ugovora
contract = web3.eth.contract(address=address, abi=abi)

nonce = web3.eth.getTransactionCount(account)
transaction = contract.functions.setMessage('Vedran').buildTransaction({
    'gas': 2000000,
    'gasPrice': web3.toWei('10', 'gwei'),
    'from': account,
    'nonce': nonce
})
signed_txn = web3.eth.account.signTransaction(
    transaction, private_key=private_key)
web3.eth.sendRawTransaction(signed_txn.rawTransaction)

transaction2 = contract.functions.setMessage2('Milković').buildTransaction({
    'gas': 2000000,
    'gasPrice': web3.toWei('15', 'gwei'),
    'from': account,
    'nonce': nonce
})
signed_txn2 = web3.eth.account.signTransaction(
    transaction2, private_key=private_key)
web3.eth.sendRawTransaction(signed_txn2.rawTransaction)

print(contract.functions.message().call())
print(contract.functions.message2().call())
print(contract.functions.vrati().call())
