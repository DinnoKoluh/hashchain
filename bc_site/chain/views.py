from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm, TxForm, BlockForm
from django.contrib import messages
from .models import Block, Account, Tx
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django import forms
import sys
import traceback
sys.path.append('C:\\Users\\pc\\Desktop\\MyProjects\\my_blockchain\\vanilla_classes')
import Net

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
               form = TxForm(request.POST)
          if form.is_valid():
               tx = form.save(commit=False) # type is the TX model
               given_to_address = form.cleaned_data['to_address']
               # checking if the given address is in the database   
               if not(Account.objects.filter(address=given_to_address).exists()):
                    raise Exception("The given address does not exist")
               else: 
                    current_user = request.user.account # getting the current custom user model
                    tx.from_address = current_user.address # setting my_address of the tx 
                    current_user.increase_pending_amount(tx.amount + tx.get_fee())
                    # do any additional processing of the form data here
                    tx.save()
                    current_user.save()
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
     blocks = Block.objects.all()
     if request.method == 'POST':
        form = BlockForm(request.POST)
        if len(Tx.objects.filter(executed=False)) == 0:
            raise forms.ValidationError("Cannot mine empty block. Wait for Tx's.")
        if form.is_valid():
          block = form.save(commit=False)
          block.miner_address = request.user.account.address # look at the case when more accounts mine a block at the same time
          block.save()
          block.add_txs()
          #request.user.account.increase_balance(block.reward)
          block.execute_txs()
          request.user.save()
          block.save()
          messages.success(request, "Block successfully mined!")
          return redirect('blockchain') 
     else:
         form = BlockForm()

     context = {
          "blocks": blocks,
          "form": form,
          "blocks_in_row": 4,
          "txs_in_row": 3,
          "pending_tx_in_row": 5,
          "full_txs": Tx.objects.filter(executed=False),
          "total_reward": estimate_reward(),
          }
     return render(request, 'blockchain.html', context)

def create_account(request):
     """
     Where the account creation site will be located.
     """
     if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
          account_user = form.save(commit=False)
          acc = Net.Account() # temporary create acc here to extract the address, needs to fixed later
          account_user.address = acc.address
          account_user.save()
          messages.success(request, "Successfully created account!")
          return redirect('create_account')
     else:
         form = SignUpForm()
     return render(request, 'create_account.html', {'form': form})

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
     total_reward = Block.objects.all()[0].reward # could be an issue when mining genesis block
     for tx in Tx.objects.filter(executed=False):
          total_reward = total_reward + tx.get_fee()
     return total_reward
