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

#--------------------------COMMENT 
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
	#Case1
	#module_dir = os.path.dirname(__file__)
	#f = os.path.join(module_dir, 'Auction.sol')

	#Case2
	#f = open('./Auction.sol', 'r')

	#Case 3
	pwd = os.path.dirname(__file__)
	#f = open(pwd + '/Auction.sol')
	f = open(pwd + '/pqueue.sol')

	contract_source_code = f.read()
	f.close()

	rpc_url="http://localhost:8541"
	w3 = Web3(HTTPProvider(rpc_url))
	w3.personal.unlockAccount(w3.eth.accounts[0],"1234",0)
	print('success')

	#compiled_sol = compile_source(contract_source_code, import_remapping=['=','-'])
	compiled_sol = compile_source(contract_source_code)
	#contract_interface = compiled_sol["<stdin>:Auction"]
	contract_interface = compiled_sol["<stdin>:queue"]

	contract = w3.eth.contract(abi= contract_interface['abi'],bytecode = contract_interface['bin'],bytecode_runtime=contract_interface['bin-runtime'])

	tx_hash = contract.deploy(transaction={'from':w3.eth.accounts[0]})

	print("tx_hash : ", tx_hash)

	time.sleep(10) #Wait for mining

	tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
	contract_address = tx_receipt['contractAddress']
	
	print ("contract_address", contract_address)
	return render(request, 'blog/post_list.html')
