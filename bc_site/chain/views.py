from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib import messages
from .models import BlockStruct
from django.contrib.auth import logout

def base(request):
     """
     Where the homepage/base site will be located.
     """
     return render(request, 'base.html')

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
        print("inside1")
        if form.is_valid():
          print("inside2")
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

def logout_view(request):
    logout(request)
    return redirect('base')
