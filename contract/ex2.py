import os
import time
import random
from web3 import Web3, HTTPProvider
from solc import compile_source

#Connect--------------------------------------
rpc_url="http://localhost:8541"
w3 = Web3(HTTPProvider(rpc_url))

addr= w3.toChecksumAddress('c6d9b140af75f7087dc32b29cd50940f264012e0')
pw = '1234'
w3.personal.unlockAccount(addr,pw,0)
balance = w3.fromWei(w3.eth.getBalance(addr), 'wei')

print('Connection success')



bn = w3.eth.blockNumber

f = open("information.txt",'w')

tsize=0
ttx=0
ttime=0
#f.write('size =[')
for i in range(bn):
	block = w3.eth.getBlock(i)
#	f.write('\'' + str(block.size) + '\', ')
	f.write(str(block.size) + ' ')
#f.write(']\n')
f.write('\n')

#f.write('timestamp =[')
for i in range(bn):
	block = w3.eth.getBlock(i)
	f.write(str(block.timestamp) + ' ')
#f.write(']')
f.write('\n')
#f.write('[')
for i in range(bn):
	block = w3.eth.getBlock(i)
#	f.write('\'' + str(len(block.transactions)) + '\',')
	f.write(str(len(block.transactions)) + ' ')
#f.write(']')
f.write('\n')

f.close()
