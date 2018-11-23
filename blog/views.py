from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.contrib.auth.decorators import login_required

#---------------------------------MAIN PAGE
def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts':posts})


#---------------------------------POST PAGE
from django.shortcuts import render, get_object_or_404
def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post':post})

from .forms import PostForm
from django.shortcuts import redirect
@login_required
def post_new(request):
	form = PostForm()
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
#			post.publiched_date = timezone.now()
			post.save()
			return post_list(request)
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form':form})

@login_required
def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
#			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form':form})

@login_required
def post_draft_list(request):
	posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
	return render(request, 'blog/post_draft_list.html', {'posts':posts})

@login_required
def post_publish(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.publish()
	return redirect('post_detail', pk=pk)

def publish(self):
	self.published_date = timezone.now()
	self.save()

def post_remove(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.delete()
	return redirect('post_list')

#---------------------------------COMMENT 
from .forms import CommentForm
from .models import Comment
def add_comment_to_post(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post =post
			comment.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = CommentForm()
	return render(request, 'blog/add_comment_to_post.html', {'form':form})

@login_required
def comment_approve(request,pk):
	comment = get_object_or_404(Comment, pk=pk)
	comment.approve()
	return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
	comment = get_object_or_404(Comment, pk=pk)
	comment.delete()
	return redirect('post_detail', pk=comment.post.pk)


from django.contrib.auth.models import User
from .forms import UserForm
def signup(request):
	if request.method == "POST":
		form = UserForm(request.POST)
		if form.is_valid():
			new_user = User.objects.create_user(**form.cleaned_data)
			return post_list(request)
			#login(request, new_user)
			#return redirect('post_list')
	else:
		form = UserForm()
	return render(request, 'blog/signup.html', {'form':form})

#--------------------------------blockchain
import os
import time
from web3 import Web3, HTTPProvider
from solc import compile_source
def blockchain_start(request):
	global sender, contractAddress, balance, power, chprice, exprice, qSizeSell, qSizeBuy
	if request.method == "POST":
		if "_login" in request.POST:
			sender, balance, power = ethereum_login(request)
		elif "_create" in request.POST:
			contractAddress = contract_create(request)
		elif "_at" in request.POST:
			contractAddress = contract_ready(request)
		elif "_seller" in request.POST:
			balance, chprice = contract_sell(request)
		elif "_buyer" in request.POST:
			balance, exprice = contract_buy(request)
		elif "_queueTop_sell" in request.POST:
			chprice = cheapest(request)
		elif "_queueTop_buy" in request.POST:
			exprice = expensive(request)
		elif "_matching" in request.POST:
			chprice ,exprice, qSizeSell, qSizeBuy = matching(request)
	
	if 'sender' not in globals():
		sender = ""
	if 'contractAddress' not in globals():
		contractAddress = ""
	if 'balance' not in globals():
		balance = ""
	if 'power' not in globals():
		power = ""
	if 'chprice' not in globals():
		chprice = ""
	if 'exprice' not in globals():
		exprice = ""
	if 'qSizeSell' not in globals():
		qSizeSell = ""
	if 'qSizeBuy' not in globals():
		qSizeBuy = ""

	return render(request, 'blog/blockchain_start.html', {'contract_address': contractAddress, 'balance':balance, 'powerAmount':power, 'cheapest_price':chprice, 'expensive_price':exprice, 'queueSize_sell':qSizeSell, 'queueSize_buy':qSizeBuy})


def ethereum_login(request):
	print("login section")

	#Connect blockchain
	global w3
	rpc_url="http://localhost:8541"
	w3 = Web3(HTTPProvider(rpc_url))

	#account information
	addr = w3.toChecksumAddress(request.POST.get("_address"))
	pw = request.POST.get("_password")
	w3.personal.unlockAccount(addr, pw,0)
#TODO; login fail

	print('Connection success')

	balance = w3.fromWei(w3.eth.getBalance(addr), 'wei')
	if 'auction' not in globals():
		power = 0
	else:
		power = auction.functions.havePowerAmount(addr).call()

	return addr, balance, power



#Use only manager
def contract_create(request):
	print("contract section")

	if 'w3' not in globals():
		ethereum_login(request)

	#Read contract source file
	pwd = os.path.dirname(__file__)
	f = open(pwd + '/../contract/Auction.sol')
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
	contract_address = tx_receipt['contractAddress']

	#Save addr for various user
	#save address
	f = open(pwd + '/../contract/address','w')
	f.write(contract_address)
	f.close()
	#save abi (TODO; implement read abi.json function)
	f = open(pwd + '/../contract/abi.json','w')
	f.write(str(contract_interface['abi']))
	f.close()

	#Use for contract
	global auction
	auction = w3.eth.contract(
		address=tx_receipt.contractAddress,
		abi = contract_interface['abi'],
	)
	#Check
	print('Cheapest Price: {}'.format(auction.functions.queueTop_sell().call()))

	print ("contract_address", contract_address)
	return contract_address

def contract_ready(request):
	print ('ready section')
	
	if 'w3' not in globals():
		ethereum_login(request)

	if 'auction' not in globals():
		print ('auction not in globals section')
		#Find contract addreess	
		pwd = os.path.dirname(__file__)
		f = open(pwd + '/../contract/address','r')
		contractAddress = f.read()
		f.close()

		#Find abi (TODO; can't find ABI file parsing, so read .sol & compile again)
		#f = open(pwd + '/../contract/abi.json','r')
		#aabi = f.read(); f.close()
		f = open(pwd + '/../contract/Auction.sol','r')
		contract_source_code = f.read()
		f.close()
		compiled_sol = compile_source(contract_source_code,import_remappings=['=','-'])
		contract_interface = compiled_sol["<stdin>:Auction"]
		abi = contract_interface['abi']

		#Connect Deployed contract
		global auction
		auction = w3.eth.contract(
			address = contractAddress,
			abi = abi,
		)

	#Check
	print('Cheapest Price: {}'.format(auction.functions.queueTop_sell().call()))

	return auction.address


def contract_sell(request):
	print("sell section")
	if 'auction' not in globals():
		contract_ready(request)
	
	power = int(request.POST.get('_sellerPower'))
	fee = int(request.POST.get('_sellerFee'))

	tx_hash = auction.functions.addRequest_sell(power, fee).transact({'from':sender,'gas':3000000})
	tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
	print('tx_receipt answer')
	
	bal = w3.fromWei(w3.eth.getBalance(sender), 'wei')
	cheap = auction.functions.queueTop_sell().call()
	return bal, cheap

def contract_buy(request):
	print("buy section")
	if 'auction' not in globals():
		contract_ready(request)
	power = int(request.POST.get('_buyerPower'))
	fee = int(request.POST.get('_buyerFee'))
	tx_hash = auction.functions.addRequest_buy(power).transact({'from':sender,'value':fee,'gas':3000000})
	tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
	print('tx_receipt answer')

	bal = w3.fromWei(w3.eth.getBalance(sender), 'wei')
	expen = auction.functions.queueTop_buy().call()
	return bal, expen

#TODO; Delete later or use only manager
def cheapest(request):
	print("cheapest section")
	if 'auction' not in globals():
		contract_ready(request)
	
	#Check cheapest price
	cheapest = float(auction.functions.queueTop_sell().call())
	return cheapest

#TODO; Delete later or use only manager
def expensive(request):
	print("expensive section")
	if 'auction' not in globals():
		contract_ready(request)

	#Check most expensive price
	expensive = float(auction.functions.queueTop_buy().call())
	return expensive

def matching(request):
	print("matching section")
	if 'auction' not in globals():
		contract_ready(request)
	tx_hash = auction.functions.matching().transact({'from':sender, 'gas':3000000})
	tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
	
	cheap_price = cheapest(request)
	expen_price = expensive(request)

	qSizeSell = auction.functions.queueSize_sell().call()
	qSizeBuy = auction.functions.queueSize_buy().call()

	return cheap_price, expen_price, qSizeSell, qSizeBuy
