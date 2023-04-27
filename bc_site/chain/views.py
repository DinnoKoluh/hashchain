from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm, TxForm
from django.contrib import messages
from .models import BlockStruct, AccountModel
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

def base(request):
     """
     Where the homepage/base site will be located.
     """
     if request.method == 'POST':
        form = TxForm(request.POST)
        if form.is_valid():
            tx = form.save(commit=False) # type is the TX model
            given_to_address = form.cleaned_data['to_address']

            # checking if the given address is in the database   
            if AccountModel.objects.filter(address=given_to_address).exists():
               print("Given right address")

            current_user = request.user.accountmodel # getting the current custom user model
            tx.my_address = current_user.address # setting my_address of the tx 
            # print(tx.my_address)
            # do any additional processing of the form data here
            print(AccountModel.objects.all()[0])
            tx.save()
            return redirect('base')
     else:
          form = TxForm()
     return render(request, 'base.html', {'form': form})

def blockchain(request):
     """
     Where the blockchain visualization site will be located.
     """
     blocks = BlockStruct.objects.all()
     context = {
          "blocks": blocks,
          }
     return render(request, 'blockchain.html', context)

def create_account(request):
     """
     Where the account creation site will be located.
     """
     if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
          print("inside")
          form.save()
          
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
