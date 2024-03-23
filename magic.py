# Python script to transfer MATIC with pros balance and static gas

# chain info
chainId = 80001
rpc_url = 'https://polygon-mumbai-bor.publicnode.com'

# address info
sender_pkey = 'XXX PRIVKEY'
sender_addr = 'XXX PUBKEY'
recipient_addr = 'XXX WALLET'

# extra
amount2pros = 0.01
gasPrice = 15
gasLimit = 21000

# import libraries
from decimal import *
from web3 import Web3
from pprint import pprint

# check connecting web3
web3 = Web3(Web3.HTTPProvider(rpc_url))
if  web3.is_connected() != True:
    print('ERROR: failed to connect', rpc_url)
    exit(1)

# set gas fee
gas_fee = web3.from_wei(Decimal(gasLimit * gasPrice), 'ether')
print('gas fee:', gas_fee)

# get balance
balance = web3.eth.get_balance(sender_addr)
balance = web3.from_wei(balance, 'ether')
print('balance:', balance)

# set amount to sent
amount = Decimal(amount2pros) * (balance - gas_fee)

# get nonce number
nonce = web3.eth.get_transaction_count(sender_addr)

# build transaction
tx = {
    'chainId': chainId,
    'nonce': nonce,
    'to': recipient_addr,
    'value': web3.to_wei(amount, 'ether'),
    'gas': gasLimit,
    'gasPrice': gasPrice
}
pprint({"Transaction:": tx})

# publish transaction
signed_tx = web3.eth.account.sign_transaction(tx, sender_pkey)
tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
print(f'Published: {web3.to_hex(tx_hash)}')