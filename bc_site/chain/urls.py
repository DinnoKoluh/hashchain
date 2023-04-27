from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from . import views
from .forms import LogInForm

urlpatterns = [
    path('', views.base, name='base'),
    path('blockchain', views.blockchain, name='blockchain'),
    path('create_account', views.create_account, name='create_account'),
    path('login', auth_views.LoginView.as_view(template_name='login.html', authentication_form=LogInForm), name='login'),
    path('account_base', views.account_base, name='account_base'),
    path('logout', views.logout_view, name='logout'),
    path('transactions', views.transactions, name='transactions'),
]