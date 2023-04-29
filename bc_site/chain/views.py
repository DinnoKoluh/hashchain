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
sys.path.append('C:\\Users\\pc\\Desktop\\MyProjects\\my_blockchain')
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
     if request.method == 'POST':
        form = TxForm(request.POST)
        if form.is_valid():
            tx = form.save(commit=False) # type is the TX model
            given_to_address = form.cleaned_data['to_address']

            # checking if the given address is in the database   
            if not(Account.objects.filter(address=given_to_address).exists()):
               raise forms.ValidationError("The given address does not exist")

            current_user = request.user.account # getting the current custom user model
            tx.from_address = current_user.address # setting my_address of the tx 
            # print(tx.my_address)
            # do any additional processing of the form data here
            # print(AccountModel.objects.all()[0]) # getting all the associated data
            tx.save()
            return redirect('transactions')
     else:
          form = TxForm()
     return render(request, 'transactions.html', {'form': form})

def blockchain(request):
     """
     Where the blockchain visualization site will be located.
     """
     blocks = Block.objects.all()
     txs = Tx.objects.all()
     # block.add_txs()
     if request.method == 'POST':
        form = BlockForm(request.POST)
        if form.is_valid():
          block = form.save(commit=False)
          block.save()
          block.add_txs()
          block.save()
          request.user.account.increase_balance(block.reward)
          request.user.save()
          return redirect('blockchain')
     else:
         form = BlockForm()

     context = {
          "blocks": blocks,
          "form": form,
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
          return redirect('login')
     else:
         form = SignUpForm()
     return render(request, 'create_account.html', {'form': form})

def account_base(request):
     """
     Where the account site will be located.
     """

     context = {
            "username":"dinnoK",
            }
     return render(request, 'account_base.html', context)

@login_required # decorator
def logout_view(request):
    """
    Simple view for logging out.
    """
    logout(request)
    return redirect('base')
