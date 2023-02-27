from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def base(request):
     return render(request, 'base.html')

def blockchain(request):
     return render(request, 'blockchain.html')
