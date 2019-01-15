import os
import time
import random
from web3 import Web3, HTTPProvider
from solc import compile_source

#Connect--------------------------------------
rpc_url="http://localhost:8541"
w3 = Web3(HTTPProvider(rpc_url))

addr= w3.toChecksumAddress('2f5585e4f2505e225678483a19a2294c94f64f08')
pw = '1234'
w3.personal.unlockAccount(addr,pw,0)
balance = w3.fromWei(w3.eth.getBalance(addr), 'wei')

print('Connection success')


#Contract create-----------------------------------------
pwd = os.path.dirname(os.path.abspath(__file__))

print('asdf')

f = open(pwd + '/contract/Auction.sol')
contract_source_code = f.read()
f.close()

#Compile source code
compiled_sol = compile_source(contract_source_code, import_remappings=['=','-'])
contract_interface = compiled_sol["<stdin>:Auction"]

#Deploy
contract = w3.eth.contract(abi= contract_interface['abi'],bytecode = contract_interface['bin'],bytecode_runtime=contract_interface['bin-runtime'])
tx_hash = contract.deploy(transaction={'from':w3.eth.accounts[0]})

#Pull contract address
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
# delete waitForTransactionReceipt
contract_address = tx_receipt['contractAddress']

#Use for contract
global auction
auction = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi = contract_interface['abi'],
)

print("contract address", contract_address)
print("Creating first contract success")


#addRequest_buy---------------------------------------------
sender = addr
def buy():
	power = int("100000")
	fee = int("100000")
	tx_hash = auction.functions.addRequest_buy(power).transact({'from':sender, 'value':fee, 'gas':3000000})
	#tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
	print("Reqeust for buyer success")

#addRequest_sell---------------------------------------------
def sell():
	power = int("100000")
	fee = int("100000")
	tx_hash = auction.functions.addRequest_sell(power,fee).transact({'from':sender,'gas':3000000})
	#tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
	print('Request for seller success')


while(True):
	rand = random.randint(1,2)
	if rand ==1:
		buy()
	else:
		sell()

print ('python file execute success')


                                        
