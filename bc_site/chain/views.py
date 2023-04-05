from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.

def base(request):
     """
     Where the homepage/base site will be located.
     """
     return render(request, 'base.html')

def blockchain(request):
     """
     Where the blockchain visualization site will be located.
     """
     return render(request, 'blockchain.html')

def create_account(request):
     """
     Where the account creation site will be located.
     """
     if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log in the user
            login(request, user)
            # Redirect to a success page
            return redirect('success')
     else:
          form = UserCreationForm()
     return render(request, 'create_account.html', {'form': form})
