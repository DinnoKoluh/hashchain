from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm, TxForm, BlockForm
from django.contrib import messages
from .models import Block, Account, Tx
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django import forms
from .key_generation import *
from django.conf import settings
import os
import time
import asyncio
import urllib.request
from threading import Timer

def base(request):
     """
     Where the homepage/base site will be located.
     """
     return render(request, 'base.html')

def transactions(request):
     """
     Where the transactions are going to be created site.
     """
     error = False
     form = TxForm()
     try:
          if request.method == 'POST':
               form = TxForm(request.POST, request.FILES)
          if form.is_valid():
               tx = form.save(commit=False) # type is the TX model
               given_to_address = form.cleaned_data['to_address']
               # checking if the given address is in the database   
               if not(Account.objects.filter(address=given_to_address).exists()):
                    raise Exception("The given address does not exist")
               else: 
                    current_user = request.user.account # getting the current custom user model
                    tx.from_address = current_user.address # setting my_address of the tx 
                    # do any additional processing of the form data here
                    private_key = load_secret_key(request.FILES['file'].read()) # read as bytes object and load as private key object
                    tx.public_key = get_public_key_as_bytes(private_key)
                    tx.is_tx_owner_valid(private_key) # validate account
                    current_user.increase_pending_amount(tx.amount + tx.get_fee())
                    current_user.save()
                    tx.save()
                    tx.sign_tx(private_key)
                    messages.success(request, "Transaction successfully signed")
                    messages.success(request, "Transaction successfully submitted!")
                    return redirect('transactions')
          else:
               form = TxForm()
     except Exception as e:
          error = str(e)
     context = {
          'form': form,
          'accounts': Account.objects.all(),
          'fee': 0.01, #Tx.objects.all()[0].fee, could be a problem with genesis block
          'error': error,
          }
     return render(request, 'transactions.html', context)

def blockchain(request):
     """
     Where the blockchain visualization site will be located.
     """
     blocks = None
     form = BlockForm()
     error = False
     try:
          blocks = Block.objects.all()
          if request.method == 'POST':
               form = BlockForm(request.POST)
               if len(Tx.objects.filter(executed=False)) == 0:
                    raise Exception("Cannot mine empty block. Wait for Tx's.")
               if form.is_valid():
                    block = form.save(commit=False)
                    # check if tx's are valid before mining block
                    for tx in Tx.objects.filter(executed=False):
                         tx.is_tx_valid()
                    block.miner_address = request.user.account.address # look at the case when more accounts mine a block at the same time
                    block.save()
                    block.add_txs()
                    block.execute_txs()
                    request.user.save() # saving user because of gotten block reward
                    block.save()
                    messages.success(request, "Block successfully mined!")
                    return redirect('blockchain') 
          else:
               form = BlockForm()
     except Exception as e:
          error = str(e)

     context = {
          "blocks": blocks,
          "form": form,
          "blocks_in_row": 4,
          "txs_in_row": 3,
          "pending_tx_in_row": 5,
          "full_txs": Tx.objects.filter(executed=False),
          "total_reward": estimate_reward(),
          "error": error,
          }
     return render(request, 'blockchain.html', context)

def create_account(request):
     """
     Where the account creation site will be located.
     """
     key_path = "#"
     if request.method == 'POST' and "register_btn" in request.POST:
          reg_form = SignUpForm(request.POST)
          if reg_form.is_valid():
               key_pair = generate_keys()
               account_user = reg_form.save(commit=False)
               account_user.address = generate_address(key_pair)
               account_user.save()
               key_path = os.path.join(settings.BASE_DIR, 'static', 'key', account_user.address)
               save_key(key_pair, key_path) # saving key in a temporary file
               messages.success(request, "Successfully created account!")
               genesis(account_user)
               t = Timer(10, delete_key, args=(key_path, ))
               t.start()
               return render(request, 'create_account.html', {'form': SignUpForm(), 'key_path': str("/static/key/") + str(account_user.address)})
          else:
               return redirect('create_account')
     else:
         reg_form = SignUpForm()
     return render(request, 'create_account.html', {'form': reg_form, 'key_path': key_path})

def delete_key(key_path):
     """
     Delete key file after is has been downloaded.
     """
     os.remove(key_path)
     print("Key successfully deleted")

@login_required # decorator
def logout_view(request):
    """
    Simple view for logging out.
    """
    logout(request)
    return redirect('base')

def estimate_reward():
     """
     Return total reward of mining a block.
     """
     try:
          total_reward = Block.objects.all()[0].reward # could be an issue when mining genesis block
          for tx in Tx.objects.filter(executed=False):
               total_reward = total_reward + tx.get_fee()
          return total_reward
     except:
          return None

def genesis(user):
     blocks = Block.objects.exists()
     print(blocks)
     if not Block.objects.exists():
          print("GENERATING GENESIS BLOCK")
          block = Block()
          block.miner_address = user.address
          user.balance = 100
          user.save()
          block.save()