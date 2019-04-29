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
for i in range(bn):
	block = w3.eth.getBlock(i)
	f.write("# Block : \t" + str(i))
	f.write('\ndifficulty: ' + str(block.difficulty))
	f.write("\nsize : \t\t" + str(block.size))
	f.write('\ntimestamp : ' +  str(block.timestamp))
	f.write('\n# tx : \t\t'+ str(len(block.transactions)) + '\n\n')
	
	tsize += block.size
	ttx += len(block.transactions)

	if i == 1:
		ttime = block.timestamp
	if i == (bn-1):
		print('enter last block')
		ttime = block.timestamp - ttime

f.write('total size : ' + str(tsize) + '\ntotal #tx : ' + str(ttx) + '\ntotal time : ' + str(ttime))

kbps = (tsize / ttime * 8) / 1000
tps = ttx / ttime

f.write('\nkbps : ' + str(kbps) + '\ntps : ' + str(tps)+'\n\n')



f.close()

